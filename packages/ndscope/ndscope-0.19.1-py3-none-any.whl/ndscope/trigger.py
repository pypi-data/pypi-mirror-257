import numpy as np

from qtpy import QtCore
from qtpy.QtCore import Signal
import pyqtgraph as pg

from .const import COLOR_MODE, LABEL_ALPHA


class Trigger(QtCore.QObject):
    __slots__ = [
        'channel', 'line', 'invert', 'single',
    ]

    level_changed_signal = Signal('PyQt_PyObject')

    def __init__(self):
        super().__init__()
        self.channel = None
        self.plot = None
        self.line = pg.InfiniteLine(
            angle=0,
            movable=True,
            pen= {
                'style': QtCore.Qt.DotLine,
                'width': 3,
            },
            label='trigger level',
            labelOpts={
                'position': 0,
                'anchors': [(0, 0.5), (0, 0.5)],
                'fill': (0, 0, 0, LABEL_ALPHA),
            },
        )
        self.line.sigPositionChanged.connect(self._update_level_from_line)
        self.invert = False
        self.single = False
        self._level = self.line.value()

    def set_font(self, font):
        """set text label font label"""
        self.line.label.textItem.setFont(font)

    def set_color_mode(self, mode):
        """set color mode"""
        fg = COLOR_MODE[mode]['fg']
        bg = COLOR_MODE[mode]['bg']
        fill_color = bg.color()
        fill_color.setAlpha(LABEL_ALPHA)
        self.line.label.fill.setColor(fill_color)
        self.line.label.setColor(fg)
        self.line.pen.setColor(fg)

    def set_color(self, color):
        """set the trigger line pen color"""
        self.line.pen.setColor(color)

    @property
    def active(self):
        """True if trigger is active"""
        return self.channel is not None

    def _set_level(self, level):
        self._level = level
        self.line.label.setText(f'trigger level\n{level:g}')

    def _update_level_from_line(self, line):
        pos = line.value()
        level = self.plot.y_pos_to_val(pos)
        self._set_level(level)
        self.level_changed_signal.emit(level)

    def set_level(self, value):
        """set the trigger level"""
        if not self.plot:
            return
        self._set_level(value)
        # update the line
        pos = self.plot.y_val_to_pos(value)
        if pos is None:
            self.line.setVisible(False)
        else:
            self.line.setValue(pos)
            self.line.setVisible(True)

    @property
    def level(self):
        """trigger level"""
        return self._level

    def redraw(self):
        """redraw the trigger level line

        Use when plot Y axis scale changes.

        """
        self.set_level(self.level)

    def set_single(self, value):
        """set single shot mode"""
        self.single = value

    def set_invert(self, value):
        """set trigger invert mode"""
        self.invert = value

    def check(self, data):
        """Check for trigger in last_append of DataBufferDict

        Returns trigger time or None

        """
        if self.channel is None:
            return

        t, y = data[self.channel].last_append()

        level = self.level
        yp = np.roll(y, 1)
        yp[0] = y[0]
        if self.invert:
            tind = np.where((yp >= level) & (y < level))[0]
        else:
            tind = np.where((yp <= level) & (y > level))[0]

        if not np.any(tind):
            return None

        tti = tind.min()
        ttime = t[tti]
        return ttime
