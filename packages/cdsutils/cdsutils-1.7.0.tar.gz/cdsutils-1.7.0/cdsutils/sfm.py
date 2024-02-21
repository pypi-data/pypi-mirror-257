import os
import argparse
import operator
import functools

import numpy as np
from scipy import signal
from matplotlib import pyplot as plt

import foton
from gpstime import GPSTimeParseAction
from ezca import SFMask, Ezca
import ezca.const as ezca_const

from ._util import split_channel_ifo

#############################################

IFO = os.getenv('IFO')

USERAPPS = os.getenv(
    'USERAPPS_DIR',
    '/opt/rtcds/userapps/release',
)

#############################################


def foton_find_filter(filter_name, path=None):
    """retrieve the foton filter for the specified SFM channel

    Finds the corresponding filter file in USERAPPS/*/filterfiles,
    loads the files with foton, and extracts the appropriate filter
    bank.

    """
    ifo, rest = split_channel_ifo(filter_name)
    if not ifo:
        ifo = IFO.lower()
    subsys, fname = rest.split('-', 1)
    instance, rest = fname.split('_', 1)
    filterfile = f'{ifo}{subsys}{instance}'.upper() + '.txt'
    if not path:
        path = os.path.join(
            USERAPPS,
            subsys.lower(),
            ifo.lower(),
            'filterfiles',
            filterfile,
        )
    if not os.path.exists(path):
        raise FileNotFoundError(f"filter file not found: {path}")
    ff = foton.FilterFile(path)

    if fname in ff:
        return ff[fname]
    topname = subsys + "_" + fname
    if topname in ff:
        return ff[topname]
    raise KeyError(f"Could not find filter module {fname} or {topname}")




def sfm_retrieve_state(filter_name, gps=None, ezca=None):
    """Retrieve the state of a filter module

    If a GPS time is not provided, the current state will be retrieved
    via EPICS.  If a time is provided, NDS will be used to retrieve
    the state from that time.  A list of all active buttons for the
    filter will be returned.

    """
    if gps in ['now', None]:
        if not ezca:
            ezca = Ezca()
        ligo_filter = ezca.LIGOFilter(filter_name)
        #buttons = ligo_filter.get_current_switch_mask().buttons
        buttons = ligo_filter.get_current_swstat_mask().buttons
    else:
        from . import nds
        gps = int(gps)
        #channels = [filter_name+'_SW{}S'.format(i) for i in (1, 2)]
        #bufs = nds.fetch(channels, gps, gps+1)
        #state = [int(buf.data[0]) for buf in bufs]
        #mask = SFMask.from_sw(*state)
        channels = [filter_name+'_SWSTAT']
        bufs = nds.fetch(channels, gps, gps+1)
        mask = SFMask.from_swstat(int(bufs[0].data[0]))
        buttons = [button for button in ezca_const.BUTTONS_ORDERED if button in mask]
    return buttons


class FilterState:
    """Individual SFM filter object

    """
    def __init__(self, ff, engaged=False):
        self.__ff = ff
        self.__engaged = engaged

    @property
    def index(self):
        """Filter index (1-indexed)"""
        return int(self.ff.index + 1)

    @property
    def slot(self):
        """Filter slot name ("FM?")"""
        return "FM{}".format(self.index)

    @property
    def name(self):
        """Filter given name"""
        return self.ff.name

    @property
    def ff(self):
        """Foton filter object for filter"""
        return self.__ff

    @property
    def engaged(self):
        """True if filter engaged"""
        return self.__engaged

    def freqresp(self, freq):
        """Filter frequency response at specified frequencies"""
        num, den, gain = self.ff.get_rpoly()
        w, fr = signal.freqs(
            gain*np.array(num),
            np.array(den),
            worN=2*np.pi*freq,
        )
        return fr


class StandardFilterModule:
    """Standard Filter Module (SFM) interface

    This is a high-level interface to the SFM, able to retrieve the
    filters via the foton filter file, and the state of the module via
    EPICS or NDS.

    """
    def __init__(self, name, gps=None, ezca=None, path=None):
        """Initialize with the full base channel name of the filter, e.g.

          [[IFO]:]ISI-HAM3_BLND_X_CPS_CUR

        If an Ezca object is supplied it will be used to retrieve the
        current state of the filter module. If path is given, the path
        will be used as the location of the filter file.

        """
        self.name = name
        self.ffm = foton_find_filter(name, path=path)
        buttons = sfm_retrieve_state(name, gps=gps, ezca=ezca)
        engaged = list(map(lambda b: int(b[2:]), filter(lambda b: b[:2] == 'FM', buttons)))
        self.fs = [FilterState(f, i+1 in engaged) for i, f in enumerate(self.ffm)]

    def __repr__(self):
        return "<StandardFilterModule '{}' {}>".format(
            self.name,
            list(self.filters(engaged=True)),
        )

    def __getitem__(self, name):
        """get individual filter by index or name

        Accepts either integer or string number, or 'FM?' string.
        Indicies are 1-indexed.

        """
        try:
            i = int(name)
        except ValueError:
            # assume name is string 'FM?' or '?'
            i = int(name[-1])
            if i == 0:
                i = 10
        assert i in range(1, 11)
        return self.fs[i-1]

    def filters(self, engaged=False):
        """iterator over filters in the bank

        If `engaged` is True then only the engaged filters will be
        returned.

        """
        if engaged:
            def en(ff):
                return ff.engaged
        else:
            def en(ff):
                return True
        return filter(en, [self[i] for i in range(1, 11)])

    __iter__ = filters

    def freqresp(self, freq):
        """full module frequency response at the specified frequencies

        Convolves the response of all engaged filters.

        """
        return functools.reduce(
            operator.mul,
            [f.freqresp(freq) for f in self.filters(engaged=True)],
            np.ones_like(freq),
        )

    def plot(self, freq, fig=None):
        """bode plot state of filter module state

        All "engaged" filters will be convolved and the total
        frequency response will be included.  Returns the figure
        object.

        """
        frs = {ff.name: ff.freqresp(freq) for ff in self}

        if not fig:
            fig = plt.figure()

        fig.suptitle(f"{self.name} (solid lines: engaged filters)")
        ax_mag = fig.add_subplot(211)
        ax_mag.grid(True)
        ax_mag.set_ylabel('magnitude [dB]')
        ax_phase = fig.add_subplot(212)
        ax_phase.grid(True)
        ax_phase.set_ylim(-190, 190)
        ax_phase.set_yticks([-180, -90, 0, 90, 180])
        ax_phase.set_ylabel('phase [deg]')
        ax_phase.set_xlabel('frequency [Hz]')

        def bode(freq, fr, **kwargs):
            mag = 20 * np.log10(np.abs(fr))
            ang = np.angle(fr) * 180/np.pi
            line, = ax_mag.semilogx(freq, mag, **kwargs)
            ax_phase.semilogx(freq, ang, **kwargs)
            return line

        fr_total = self.freqresp(freq)
        linet = bode(freq, fr_total, label='Total', color='black', linestyle='-', linewidth=5, alpha=0.7)
        ax_mag.add_artist(ax_mag.legend(handles=[linet]))

        lines = []
        for ff in self:
            label = f'{ff.slot}: {ff.name}'
            fr = frs[ff.name]
            if ff.engaged:
                style = '-'
                linewidth = 3
            else:
                style = '--'
                linewidth = 2
            lines.append(bode(freq, fr, label=label, linestyle=style, linewidth=linewidth, alpha=0.7))

        ax_mag.legend(handles=lines, ncol=5, loc='upper center', bbox_to_anchor=(0.5, 1.2))

        return fig


#############################################


def cmd_decode(args):
    if len(args.SW) == 1:
        sw = args.SW[0]
        try:
            SWSTAT = int(sw)
        except ValueError:
            SWSTAT = int(Ezca().read(sw))
        buttons = SFMask.from_swstat(SWSTAT)
    elif len(args.SW) == 2:
        try:
            SW1 = int(args.SW[0])
            SW2 = int(args.SW[1])
        except ValueError:
            raise SystemExit("SW values must be integers")
        buttons = SFMask.from_sw(SW1, SW2).buttons
    else:
        raise SystemExit("Improper number of arguments.")

    for button in ezca_const.BUTTONS_ORDERED:
        if button in buttons:
            print(button)


def cmd_encode(args):
    BUTTONS = [b.upper() for b in args.BUTTONS]
    try:
        mask = SFMask.for_buttons_engaged(*BUTTONS, engaged=args.engaged)
    except Exception as e:
        raise SystemExit("Error: "+str(e))
    print('SW1: {:d}'.format(mask.SW1))
    print('SW2: {:d}'.format(mask.SW2))
    print('SWSTAT: {:d}'.format(mask.SWSTAT))


def cmd_show(args):
    fms = StandardFilterModule(args.FILTER, gps=args.time)
    freq = np.logspace(-3, 3, 1000)
    fig = fms.plot(freq)
    plt.show(fig)


summary = "decode/encode filter module switch values"


def main():
    parser = argparse.ArgumentParser(
        description=summary,
    )
    subparsers = parser.add_subparsers()
    parser_decode = subparsers.add_parser(
        'decode',
        help="decode SFM state",
    )
    parser_decode.set_defaults(func=cmd_decode)
    parser_decode.add_argument(
        'SW', metavar='FILTER/SW', nargs='+',
        help="filter name (for EPICS state retrieval), integer SWSTAT value, or integer SW1/2 values"
    )
    parser_encode = subparsers.add_parser(
        'encode', prefix_chars='-+',
        help="encode SFM state",
    )
    parser_encode.set_defaults(func=cmd_encode)
    parser_encode.add_argument(
        '+engaged', '+e', action='store_false',
        help="don't include engaged button bits"
    )
    parser_encode.add_argument(
        'BUTTONS', nargs='+',
        help="button name list"
    )
    parser_show = subparsers.add_parser(
        'show', aliases=['plot', 'bode'], prefix_chars='-+',
        help="bode plot of SFM state",
    )
    parser_show.set_defaults(func=cmd_show)
    parser_show.add_argument(
        'FILTER',
        help="filter name"
    )
    parser_show_time = parser_show.add_mutually_exclusive_group()
    parser_show_time.set_defaults(time='now')
    parser_show_time.add_argument(
        '--time', '-t', action=GPSTimeParseAction, dest='time',
        help="time to fetch filter state"
    )
    parser_show_time.add_argument(
        '+epics', '+e', action='store_const', dest='time', const=None,
        help="don't fetch current state via EPICS"
    )
    args = parser.parse_args()
    args.func(args)
