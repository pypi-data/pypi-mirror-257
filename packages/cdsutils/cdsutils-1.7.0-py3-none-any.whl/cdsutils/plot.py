import numpy as np
from matplotlib import pyplot as plt


class BodePlot:
    """bode ploting object

    """
    def __init__(self, fig=None, title=None):
        """initialize with figure

        """
        self.fig = fig or plt.figure()

        self.ax_mag = self.fig.add_subplot(211)
        # self.ax_mag.axhline(1, color='k', linestyle='dashed')
        self.ax_mag.grid(True)
        self.ax_mag.set_ylabel('magnitude')

        self.ax_phase = self.fig.add_subplot(212)
        self.ax_phase.grid(True)
        self.ax_phase.set_ylim(-190, 190)
        self.ax_phase.set_yticks([-180, -90, 0, 90, 180])
        self.ax_phase.set_ylabel('phase [deg]')
        self.ax_phase.set_xlabel('frequency [Hz]')

        if title:
            self.fig.suptitle(title)

    def plot(self, freq, fr, label, **kwargs):
        """add frequency response to plot"""
        self.ax_mag.loglog(freq, np.abs(fr), label=label, **kwargs)
        self.ax_phase.semilogx(freq, np.angle(fr, deg=True), **kwargs)

    def legend(self):
        """add legend"""
        self.ax_mag.legend()

    def save(self, path):
        """save bode plot to file"""
        self.fig.savefig(path)

    def show(self):
        """show interactive plot"""
        plt.show()
