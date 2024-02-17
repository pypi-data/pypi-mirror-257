import numpy as np

from . import const
from . import nds


def _ctype_map(ctype):
    return {
        'online': 'raw',
        'raw': 'raw',
        'reduced': 'raw',
        's-trend': 'sec',
        'm-trend': 'min',
    }.get(ctype, 'raw')


class DataBuffer(object):
    """data storage

    The data attribute here is actually a dict of sub-data arrays all
    with the same meta-data.  For trend data the keys should be
    ['mean', 'min', 'max'], and for full they would just be ['raw'].

    """

    __slots__ = [
        '__weakref__',
        'channel', 'ctype', 'sample_rate',
        'trend', 'unit',
        'data', 'size', 'gps_start', 'tarray',
        'max_samples', 'lookback',
        'last_append_len',
    ]

    def __init__(self, buf):
        """initialize with NDS-like Buffer object"""
        self.channel, self.ctype, mod = nds.parse_nds_channel(buf.channel)
        self.trend = _ctype_map(self.ctype)
        # HACK: fix m-trend sample rate.  The rate returned from NDS
        # is not accurate, seemingly subject to round-off error:
        # https://git.ligo.org/nds/nds2-distributed-server/issues/1
        # hopefully this should be fixed.  but in general we are
        # subject to round-off accumulation error in here as well (see
        # self.tlen())
        if self.trend == 'min':
            self.sample_rate = 1.0/60.0
        else:
            self.sample_rate = buf.channel.sample_rate
        self.unit = buf.channel.Units()
        self.data = {}
        self.data[mod] = buf.data
        self.gps_start = buf.gps_seconds + buf.gps_nanoseconds*1e-9
        self.update_tarray()
        #self.max_samples = int(const.DATA_LOOKBACK_LIMIT_BYTES / buf.channel.DataTypeSize())
        self.max_samples = int(const.TREND_MAX_SECONDS[self.trend] * self.sample_rate)
        self.lookback = 2
        self.last_append_len = 0

    def __repr__(self):
        return "<DataBuffer {} {}, {} Hz, [{}, {})>".format(
            self.channel, self.trend, self.sample_rate, self.gps_start, self.gps_end)

    def __len__(self):
        # FIXME: this is a hack way of doing this, and probably
        # doesn't perform well
        return list(self.data.values())[0].size

    def __getitem__(self, mod):
        return self.data[mod]

    def __contains__(self, mod):
        return mod in self.data

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    @property
    def is_trend(self):
        return self.trend in ['sec', 'min']

    @property
    def step(self):
        return 1./self.sample_rate

    @property
    def tlen(self):
        """time length of buffer in seconds"""
        # FIXME: this, and consequently gps_end is subject to
        # round-off accumulation error.  Should have better way to
        # calculate time array and gps_end time.
        return len(self) * self.step

    def update_tarray(self):
        # FIXME: see self.tlen()
        self.tarray = np.arange(len(self)) * self.step + self.gps_start

    @property
    def gps_end(self):
        return self.gps_start + self.tlen

    @property
    def range(self):
        return self.gps_start, self.gps_end

    @property
    def span(self):
        return self.gps_end - self.gps_start

    def extend(self, buf):
        """extend buffer to right"""
        assert buf.channel == self.channel
        assert buf.sample_rate == self.sample_rate, "extend buffer sample rate {} does not match {}".format(buf.sample_rate, self.sample_rate)
        assert buf.gps_start <= self.gps_end, "extend buffer start {} is greater than end {}".format(buf.gps_start, self.gps_end)
        if buf.gps_end <= self.gps_end:
            return
        ind = np.searchsorted(buf.tarray, self.gps_end)
        for mod, data in self.data.items():
            self.data[mod] = np.append(data, buf.data[mod][ind:])
        self.update_tarray()

    def extendleft(self, buf):
        """extend buffer to left"""
        assert buf.channel == self.channel
        assert buf.sample_rate == self.sample_rate, "extendleft buffer sample rate {} does not match {}".format(buf.sample_rate, self.sample_rate)
        assert buf.gps_end >= self.gps_start, "extendleft buffer end {} is less than start {}".format(buf.gps_end, self.gps_start)
        if buf.gps_start >= self.gps_start:
            return
        ind = np.searchsorted(buf.tarray, self.gps_start)
        for mod, data in self.data.items():
            self.data[mod] = np.append(buf.data[mod][:ind], data)
        self.gps_start = buf.gps_start
        self.update_tarray()

    def append(self, buf):
        """append data to the right, keeping overall time span"""
        assert buf.channel == self.channel
        assert buf.sample_rate == self.sample_rate, "append buffer sample rate {} does not match {}".format(buf.sample_rate, self.sample_rate)
        assert buf.gps_start == self.gps_end, "append buffer start {} does not equal end {}".format(buf.gps_start, self.gps_end)
        lbs = min(int(self.lookback * self.sample_rate), self.max_samples)
        for mod, data in self.data.items():
            self.data[mod] = np.append(data, buf.data[mod])[-lbs:]
        self.gps_start = max(
            self.gps_start,
            buf.gps_end - lbs*self.step,
        )
        self.update_tarray()
        self.last_append_len = min(len(buf), len(self)) + 1

    def last_append(self):
        """Return (t, y) data of last append"""
        if 'raw' in self.data.keys():
            mod = 'raw'
        else:
            mod = 'mean'
        t = self.tarray[-self.last_append_len:]
        y = self.data[mod][-self.last_append_len:]
        return (t, y)


class DataBufferDict(object):
    """

    Takes NDS-like Buffer list at initialization and organizes the
    included data into a dictionary of DataBuffer objects keyd by
    channel.  various trend channels are kept together in the same
    DataBuffer.

    """
    __slots__ = [
        '__weakref__',
        'buffers', 'gps_start', 'gps_end',
    ]

    def __init__(self, nds_buffers):
        self.buffers = {}
        # buffer lists should have unique channel,ctype,mod combos
        for buf in nds_buffers:
            db = DataBuffer(buf)
            chan = db.channel
            if chan in self.buffers:
                for m, d in db.data.items():
                    self.buffers[chan].data[m] = d
            else:
                self.buffers[chan] = db

    def __repr__(self):
        return "<DataBufferDict {}>".format(
            list(self.buffers.values()))

    def __getitem__(self, channel):
        return self.buffers[channel]

    def __delitem__(self, channel):
        del self.buffers[channel]

    def __contains__(self, channel):
        return channel in self.buffers

    def items(self):
        return self.buffers.items()

    def values(self):
        return self.buffers.values()

    @property
    def is_trend(self):
        return list(self.buffers.values())[0] in ['s-trend', 'm-trend']

    @property
    def range(self):
        # FIXME: pulling the span from a random channel is not good,
        # since there's no real guarantee that the channels all share
        # the same span.
        return list(self.buffers.values())[0].range

    def extendleft(self, bufs):
        for chan, buf in bufs.items():
            if chan in self.buffers:
                self.buffers[chan].extendleft(buf)
            else:
                self.buffers[chan] = buf

    def extend(self, bufs):
        for chan, buf in bufs.items():
            if chan in self.buffers:
                self.buffers[chan].extend(buf)
            else:
                self.buffers[chan] = buf

    def append(self, bufs):
        for chan, buf in bufs.items():
            self.buffers[chan].append(buf)

    def set_lookback(self, lookback):
        for buf in self.values():
            buf.lookback = lookback
