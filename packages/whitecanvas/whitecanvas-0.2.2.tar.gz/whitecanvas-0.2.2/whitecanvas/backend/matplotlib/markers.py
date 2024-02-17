from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import matplotlib.markers as mmarkers
import matplotlib.transforms as mtransforms
import numpy as np
from matplotlib.collections import PathCollection
from numpy.typing import NDArray

from whitecanvas.backend.matplotlib._base import MplMouseEventsMixin
from whitecanvas.protocols import MarkersProtocol, check_protocol
from whitecanvas.types import Hatch, LineStyle, Symbol
from whitecanvas.utils.normalize import as_color_array
from whitecanvas.utils.type_check import is_real_number

if TYPE_CHECKING:
    from whitecanvas.backend.matplotlib.canvas import Canvas


def _get_path(symbol: Symbol):
    marker_obj = mmarkers.MarkerStyle(symbol.value)
    return marker_obj.get_path().transformed(marker_obj.get_transform())


@check_protocol(MarkersProtocol)
class Markers(PathCollection, MplMouseEventsMixin):
    def __init__(self, xdata, ydata):
        offsets = np.stack([xdata, ydata], axis=1)
        self._symbol = Symbol.CIRCLE
        super().__init__(
            (_get_path(self._symbol),),
            sizes=[6] * len(offsets),
            offsets=offsets,
            picker=True,
        )
        self.set_transform(mtransforms.IdentityTransform())
        self._edge_styles = [LineStyle.SOLID] * len(offsets)
        MplMouseEventsMixin.__init__(self)

    ##### XYDataProtocol #####
    def _plt_get_data(self):
        offsets = self.get_offsets()
        return offsets[:, 0], offsets[:, 1]

    def _plt_set_data(self, xdata, ydata):
        data = np.stack([xdata, ydata], axis=1)
        self.set_offsets(data)

    ##### HasSymbol protocol #####

    def _plt_get_symbol(self) -> Symbol:
        return self._symbol

    def _plt_set_symbol(self, symbol: Symbol):
        path = _get_path(symbol)
        self.set_paths([path] * len(self.get_offsets()))
        self._symbol = symbol

    def _plt_get_symbol_size(self) -> NDArray[np.floating]:
        return np.sqrt(self.get_sizes())

    def _plt_set_symbol_size(self, size: float | NDArray[np.floating]):
        if is_real_number(size):
            size = np.full(len(self.get_offsets()), size)
        self.set_sizes(size**2)

    ##### HasFaces protocol #####
    def _plt_get_face_color(self) -> NDArray[np.float32]:
        return self.get_facecolor()

    def _plt_set_face_color(self, color: NDArray[np.float32]):
        color = as_color_array(color, len(self.get_offsets()))
        self.set_facecolor(color)

    def _plt_get_face_hatch(self) -> Hatch:
        return [Hatch(self.get_hatch() or "")] * len(self.get_offsets())

    def _plt_set_face_hatch(self, pattern: Hatch | list[Hatch]):
        if not isinstance(pattern, Hatch):
            if len(set(pattern)) > 1:
                warnings.warn(
                    "matplotlib markers do not support multiple hatch patterns.",
                    UserWarning,
                    stacklevel=2,
                )
            pattern = pattern[0]
        if pattern is Hatch.SOLID:
            ptn = None
        else:
            ptn = pattern.value
        self.set_hatch(ptn)

    ##### HasEdges protocol #####

    def _plt_get_edge_color(self) -> NDArray[np.float32]:
        return self.get_edgecolor()

    def _plt_set_edge_color(self, color: NDArray[np.float32]):
        color = as_color_array(color, len(self.get_offsets()))
        self.set_edgecolor(color)

    def _plt_get_edge_style(self) -> list[LineStyle]:
        return self._edge_styles

    def _plt_set_edge_style(self, style: LineStyle | list[LineStyle]):
        if isinstance(style, LineStyle):
            styles = [style.value] * len(self.get_offsets())
        else:
            styles = [s.value for s in style]
        self.set_linestyle(styles)
        self._edge_styles = styles

    def _plt_get_edge_width(self) -> NDArray[np.floating]:
        return self.get_linewidth()

    def _plt_set_edge_width(self, width: float | NDArray[np.floating]):
        if is_real_number(width):
            width = np.full(len(self.get_offsets()), width)
        self.set_linewidth(width)

    def post_add(self, canvas: Canvas):
        MplMouseEventsMixin.post_add(self, canvas)
        self.set_offset_transform(canvas._axes.transData)
