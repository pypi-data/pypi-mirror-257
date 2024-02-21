import os


def split_channel(channel):
    """Split channel into <IFO>:<SYS> and everything else."""
    if channel[0] == ':':
        channel = channel[1:]
    return channel.split('-', 1)


def split_channel_ifo(channel):
    """Split channel into <IFO>: and everything else.

    Names are split as follows:

      <IFO>:<NAME> -> <IFO>, <NAME>
      :<NAME>      ->  None, <NAME>
      <NAME>       ->  None, <NAME>

    """
    if channel[0] == ':':
        return None, channel[1:]
    elif ':' in channel:
        return channel.split(':', 1)
    return None, channel


def normalize_channel(channel):
    """Normalize channel names

    For a list of channels, return a list of channels with each
    channel fully normalized with the appropriate local IFO.  See
    `split_channel_ifo` for how channel names are parsed.  Channel
    names that specify the IFO explicitly will not be modified.

    """
    ifo, chan = split_channel_ifo(channel)
    if ifo is None:
        ifo = os.getenv('IFO', '')
    return f'{ifo}:{chan}'


def normalize_channels(channels):
    """Normalize channel names

    For a list of channels, return a list of channels with each
    channel fully normalized with the appropriate local IFO.  See
    `split_channel_ifo` for how channel names are parsed.

    """
    return list(map(normalize_channel, channels))
