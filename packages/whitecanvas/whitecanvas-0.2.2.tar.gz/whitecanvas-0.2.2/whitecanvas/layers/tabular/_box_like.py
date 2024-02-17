"""Layer with a dataframe bound to it."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Generic, Sequence, TypeVar

import numpy as np
from cmap import Color

from whitecanvas import theme
from whitecanvas.backend import Backend
from whitecanvas.layers import _mixin
from whitecanvas.layers import group as _lg
from whitecanvas.layers.tabular import _jitter, _shared
from whitecanvas.layers.tabular import _plans as _p
from whitecanvas.layers.tabular._df_compat import DataFrameWrapper
from whitecanvas.types import (
    ColormapType,
    ColorType,
    Hatch,
    LineStyle,
    Orientation,
    _Void,
)
from whitecanvas.utils.type_check import is_real_number

if TYPE_CHECKING:
    from typing_extensions import Self

    from whitecanvas.canvas.dataframe._base import CatIterator

    _FE = _mixin.AbstractFaceEdgeMixin[_mixin.FaceNamespace, _mixin.EdgeNamespace]

_DF = TypeVar("_DF")
_void = _Void()


def _norm_color_hatch(
    color,
    hatch,
    df: DataFrameWrapper[_DF],
) -> tuple[_p.ColorPlan, _p.HatchPlan]:
    color_cov = _shared.ColumnOrValue(color, df)
    if color_cov.is_column:
        color_by = _p.ColorPlan.from_palette(color_cov.columns)
    elif color_cov.value is not None:
        color_by = _p.ColorPlan.from_const(Color(color_cov.value))
    else:
        color_by = _p.ColorPlan.default()
    hatch_cov = _shared.ColumnOrValue(hatch, df)
    if hatch_cov.is_column:
        hatch_by = _p.HatchPlan.new(hatch_cov.columns)
    elif hatch_cov.value is not None:
        hatch_by = _p.HatchPlan.from_const(Hatch(hatch_cov.value))
    else:
        hatch_by = _p.HatchPlan.default()
    return color_by, hatch_by


class _BoxLikeMixin:
    _source: DataFrameWrapper[_DF]

    def __init__(
        self,
        categories: list[tuple],
        splitby: tuple[str, ...],
        color_by: _p.ColorPlan,
        hatch_by: _p.HatchPlan,
    ):
        self._splitby = splitby
        self._categories = categories
        self._color_by = color_by
        self._hatch_by = hatch_by
        self._get_base().face.color = color_by.generate(self._categories, self._splitby)
        self._get_base().face.hatch = hatch_by.generate(self._categories, self._splitby)
        if not hasattr(self, "with_hover_template"):
            return
        self.with_hover_template("\n".join(f"{k}: {{{k}!r}}" for k in self._splitby))

    def _get_base(self) -> _FE:
        """Just for typing."""
        return self._base_layer

    def _normalize_by_arg(self, by, default: tuple[str, ...]) -> tuple[str, ...]:
        if by is None:
            by = default
        elif isinstance(by, str):
            if by not in self._splitby:
                raise ValueError(
                    f"Cannot color by {by!r} as the plot is not split by this column. "
                    f"Valid columns are: {self._splitby!r}."
                )
            by = (by,)
        else:
            for b in by:
                if not isinstance(b, str):
                    raise TypeError("`by` must be a str or sequence of str.")
                if b not in self._splitby:
                    raise ValueError(
                        f"Cannot color by {by!r} as the plot is not split by this "
                        f"column. Valid columns are: {self._splitby!r}."
                    )
        return by

    def update_color_palette(
        self,
        palette: ColormapType | None = None,
        *,
        alpha: float | None = None,
        cycle_by: str | Sequence[str] | None = None,
    ) -> Self:
        """
        Update the colors by a color palette.

        Parameters
        ----------
        palette : colormap type
            Color palette used to generate colors for each category. A color palette
            can be a list of colors or any types that can be converted into a
            `cmap.Colormap` object.
        alpha : float, optional
            Additional alpha value that will be applied to the palette colors.
        cycle_by : str or sequence of str, optional
            If given, colors will be cycled on this column name(s).
        """
        by = self._normalize_by_arg(cycle_by, self._color_by.by)
        color_by = _p.ColorPlan.from_palette(by, palette=palette)
        colors = color_by.generate(self._categories, self._splitby)
        color_arr = np.stack([c.rgba for c in colors], dtype=np.float32)
        if alpha is not None:
            if is_real_number(alpha) and 0 <= alpha <= 1:
                color_arr[:, 3] = alpha
            else:
                raise TypeError(
                    f"`alpha` must be a scalar value between 0 and 1, got {alpha!r}."
                )
        self._get_base().face.color = color_arr
        self._color_by = color_by
        return self

    def update_hatch_palette(
        self,
        palette: Sequence[str | Hatch],
        *,
        cycle_by: str | Sequence[str] | None = None,
    ) -> Self:
        """
        Update the hatch patterns by a list of hatch values.

        Parameters
        ----------
        palette : sequence of str or Hatch
            Hatch palette used to generate colors for each category.
        """
        by = self._normalize_by_arg(cycle_by, self._hatch_by.by)
        hatch_by = _p.HatchPlan.new(by, values=palette)
        self._get_base().face.hatch = hatch_by.generate(self._categories, self._splitby)
        self._hatch_by = hatch_by
        return self

    def update_const(
        self,
        *,
        color: ColorType | _Void = _void,
        hatch: str | Hatch | _Void = _void,
    ) -> Self:
        """
        Update the plot features to the constant values.

        Parameters
        ----------
        color : color-type, optional
            Constant colors used for the plot.
        hatch : str or Hatch, optional
            Constant hatch used for the plot.
        """
        cat = self._categories
        if color is not _void:
            color_by = _p.ColorPlan.from_const(Color(color))
            self._get_base().face.color = color_by.generate(cat, self._splitby)
            self._color_by = color_by
        if hatch is not _void:
            hatch_by = _p.HatchPlan.from_const(Hatch(hatch))
            self._get_base().face.hatch = hatch_by.generate(cat, self._splitby)
            self._hatch_by = hatch_by
        return self

    def with_edge(
        self,
        *,
        color: ColorType | None = None,
        width: float = 1.0,
        style: str | LineStyle = LineStyle.SOLID,
        alpha: float = 1.0,
    ) -> Self:
        """Add edge to the plot with given settings."""
        self._get_base().with_edge(color=color, width=width, style=style, alpha=alpha)
        return self


class DFViolinPlot(
    _shared.DataFrameLayerWrapper[_lg.ViolinPlot, _DF],
    _BoxLikeMixin,
    Generic[_DF],
):
    def __init__(
        self,
        cat: CatIterator[_DF],
        value: str,
        color: str | tuple[str, ...] | None = None,
        hatch: str | tuple[str, ...] | None = None,
        dodge: str | tuple[str, ...] | bool | None = None,
        name: str | None = None,
        orient: Orientation = Orientation.VERTICAL,
        extent: float = 0.8,
        shape: str = "both",
        backend: str | Backend | None = None,
    ):
        _splitby, dodge = _shared.norm_dodge(
            cat.df, cat.offsets, color, hatch, dodge=dodge
        )  # fmt: skip
        x, arr, categories = cat.prep_arrays(_splitby, value, dodge=dodge)
        _extent = cat.zoom_factor(dodge=dodge) * extent
        color_by, hatch_by = _norm_color_hatch(color, hatch, cat.df)
        base = _lg.ViolinPlot.from_arrays(
            x, arr, name=name, orient=orient, shape=shape, extent=_extent,
            backend=backend,
        )  # fmt: skip
        super().__init__(base, cat.df)
        _BoxLikeMixin.__init__(self, categories, _splitby, color_by, hatch_by)
        self._value = value
        self._map = cat.prep_position_map(_splitby, dodge)
        self.with_hover_template("\n".join(f"{k}: {{{k}!r}}" for k in self._splitby))

    @property
    def orient(self) -> Orientation:
        """Orientation of the violins."""
        return self._base_layer.orient

    def move(self, shift: float = 0.0) -> Self:
        """Move the layer by the given shift."""
        for layer in self._base_layer:
            _old = layer.data
            layer.set_data(edge_low=_old.y0 + shift, edge_high=_old.y1 + shift)
        if canvas := self._canvas_ref():
            canvas._autoscale_for_layer(self, pad_rel=0.025)
        return self

    def with_hover_text(self, text: str | list[str]) -> Self:
        """Set the hover tooltip text for the layer."""
        self.base.with_hover_text(text)
        return self

    def with_hover_template(self, template: str) -> Self:
        """Set the hover tooltip template for the layer."""
        extra = {}
        for i, key in enumerate(self._splitby):
            extra[key] = [row[i] for row in self._categories]
        self.base.with_hover_template(template, extra=extra)
        return self

    def with_rug(
        self,
        *,
        width: float = 1.0,
        color="black",
    ):
        from whitecanvas.layers.tabular import DFRugGroups

        _extent = self.base.extent
        jitter = _jitter.CategoricalJitter(self._splitby, self._map)
        if self.base._shape == "both":
            align = "center"
        elif self.base._shape == "left":
            align = "high"
        else:
            align = "low"
        rug = DFRugGroups.from_table(
            self._source,
            jitter,
            self._value,
            color=color,
            width=width,
            extent=_extent,
            backend=self.base._backend_name,
        ).scale_by_density(align=align)
        old_name = self.name
        return _lg.LayerTuple([self, rug], name=old_name)

    # def with_box(self):


class DFBoxPlot(
    _shared.DataFrameLayerWrapper[_lg.BoxPlot, _DF], _BoxLikeMixin, Generic[_DF]
):
    def __init__(
        self,
        cat: CatIterator[_DF],
        value: str,
        color: str | tuple[str, ...] | None = None,
        hatch: str | tuple[str, ...] | None = None,
        dodge: str | tuple[str, ...] | bool | None = None,
        name: str | None = None,
        orient: Orientation = Orientation.VERTICAL,
        extent: float = 0.8,
        capsize: float = 0.1,
        backend: str | Backend | None = None,
    ):
        _splitby, dodge = _shared.norm_dodge(
            cat.df, cat.offsets, color, hatch, dodge=dodge,
        )  # fmt: skip
        x, arr, categories = cat.prep_arrays(_splitby, value, dodge=dodge)
        _extent = cat.zoom_factor(dodge=dodge) * extent
        _capsize = cat.zoom_factor(dodge=dodge) * capsize
        color_by, hatch_by = _norm_color_hatch(color, hatch, cat.df)
        base = _lg.BoxPlot.from_arrays(
            x, arr, name=name, orient=orient, capsize=_capsize, extent=_extent,
            backend=backend,
        )  # fmt: skip
        super().__init__(base, cat.df)
        _BoxLikeMixin.__init__(self, categories, _splitby, color_by, hatch_by)

    @property
    def orient(self) -> Orientation:
        """Orientation of the violins."""
        return self._base_layer.orient

    def move(self, shift: float = 0.0) -> Self:
        """Move the layer by the given shift."""
        self._base_layer.move(shift)
        return self

    def with_hover_text(self, text: str | list[str]) -> Self:
        """Set the hover tooltip text for the layer."""
        self.base.boxes.with_hover_text(text)
        return self

    def with_hover_template(self, template: str) -> Self:
        """Set the hover tooltip template for the layer."""
        extra = {}
        for i, key in enumerate(self._splitby):
            extra[key] = [row[i] for row in self._categories]
        self.base.boxes.with_hover_template(template, extra=extra)
        return self


class _EstimatorMixin(_BoxLikeMixin):
    orient: Orientation

    def est_by_mean(self) -> Self:
        """Set estimator to mean."""

        def est_func(x):
            return np.mean(x)

        return self._update_estimate(est_func)

    def est_by_median(self) -> Self:
        """Set estimator to median."""

        def est_func(x):
            return np.median(x)

        return self._update_estimate(est_func)

    def err_by_sd(self, scale: float = 1.0, *, ddof: int = 1) -> Self:
        """Set error to standard deviation."""

        def err_func(x):
            _mean = np.mean(x)
            _sd = np.std(x, ddof=ddof) * scale
            return _mean - _sd, _mean + _sd

        return self._update_error(err_func)

    def err_by_se(self, scale: float = 1.0, *, ddof: int = 1) -> Self:
        """Set error to standard error."""

        def err_func(x):
            _mean = np.mean(x)
            _er = np.std(x, ddof=ddof) / np.sqrt(len(x)) * scale
            return _mean - _er, _mean + _er

        return self._update_error(err_func)

    def err_by_quantile(self, low: float = 0.25, high: float | None = None) -> Self:
        """Set error to quantile."""
        if low < 0 or low > 1:
            raise ValueError(f"Quantile must be between 0 and 1, got {low}")
        if high is None:
            high = 1 - low
        elif high < 0 or high > 1:
            raise ValueError(f"Quantile must be between 0 and 1, got {high}")

        def err_func(x):
            _qnt = np.quantile(x, [low, high])
            return _qnt[0], _qnt[1]

        return self._update_error(err_func)

    def _update_estimate(self, est_func: Callable[[np.ndarray], float]) -> Self:
        arrays = self._get_arrays()
        est = [est_func(arr) for arr in arrays]
        self._set_estimation_values(est)
        return self

    def _update_error(
        self,
        err_func: Callable[[np.ndarray], tuple[float, float]],
    ) -> Self:
        arrays = self._get_arrays()
        err_low = []
        err_high = []
        for arr in arrays:
            low, high = err_func(arr)
            err_low.append(low)
            err_high.append(high)
        self._set_error_values(err_low, err_high)
        return self


class DFPointPlot(
    _shared.DataFrameLayerWrapper[_lg.LabeledPlot, _DF], _EstimatorMixin, Generic[_DF]
):
    def __init__(
        self,
        cat: CatIterator[_DF],
        value: str,
        color: str | tuple[str, ...] | None = None,
        hatch: str | tuple[str, ...] | None = None,
        dodge: str | tuple[str, ...] | bool | None = None,
        name: str | None = None,
        orient: Orientation = Orientation.VERTICAL,
        capsize: float = 0.1,
        backend: str | Backend | None = None,
    ):
        _splitby, dodge = _shared.norm_dodge(
            cat.df, cat.offsets, color, hatch, dodge=dodge,
        )  # fmt: skip
        x, arr, categories = cat.prep_arrays(_splitby, value, dodge=dodge)
        _capsize = cat.zoom_factor(dodge=dodge) * capsize
        color_by, hatch_by = _norm_color_hatch(color, hatch, cat.df)
        base = _lg.LabeledPlot.from_arrays(
            x, arr, name=name, orient=orient, capsize=_capsize, backend=backend,
        )  # fmt: skip
        self._arrays = arr
        super().__init__(base, cat.df)
        _BoxLikeMixin.__init__(self, categories, _splitby, color_by, hatch_by)
        base.with_edge(color=theme.get_theme().foreground_color)
        self._orient = orient

    @property
    def orient(self) -> Orientation:
        """Orientation of the violins."""
        return self._orient

    def move(self, shift: float = 0.0) -> Self:
        """Move the layer by the given shift."""
        base = self._base_layer
        data = base.data
        if self._orient.is_vertical:
            base.set_data(data.x + shift, data.y)
        else:
            base.set_data(data.x, data.y + shift)
        return self

    def _get_arrays(self) -> list[np.ndarray]:
        return self._arrays

    def _set_estimation_values(self, est):
        if self.orient.is_vertical:
            self._base_layer.set_data(ydata=est)
        else:
            self._base_layer.set_data(xdata=est)

    def _set_error_values(self, err_low, err_high):
        mdata = self._base_layer.data
        if self.orient.is_vertical:
            self._base_layer.yerr.set_data(mdata.x, err_low, err_high)
        else:
            self._base_layer.xerr.set_data(err_low, err_high, mdata.y)

    def with_hover_text(self, text: str | list[str]) -> Self:
        """Set the hover tooltip text for the layer."""
        self.base.markers.with_hover_text(text)
        return self

    def with_hover_template(self, template: str) -> Self:
        """Set the hover tooltip template for the layer."""
        extra = {}
        for i, key in enumerate(self._splitby):
            extra[key] = [row[i] for row in self._categories]
        self.base.markers.with_hover_template(template, extra=extra)
        return self


class DFBarPlot(
    _shared.DataFrameLayerWrapper[_lg.LabeledBars, _DF], _EstimatorMixin, Generic[_DF]
):
    def __init__(
        self,
        cat: CatIterator[_DF],
        value: str,
        color: str | tuple[str, ...] | None = None,
        hatch: str | tuple[str, ...] | None = None,
        dodge: str | tuple[str, ...] | bool | None = None,
        name: str | None = None,
        orient: Orientation = Orientation.VERTICAL,
        capsize: float = 0.1,
        extent: float = 0.8,
        backend: str | Backend | None = None,
    ):
        _splitby, dodge = _shared.norm_dodge(
            cat.df, cat.offsets, color, hatch, dodge=dodge,
        )  # fmt: skip
        x, arr, categories = cat.prep_arrays(_splitby, value, dodge=dodge)
        _extent = cat.zoom_factor(dodge=dodge) * extent
        _capsize = cat.zoom_factor(dodge=dodge) * capsize
        color_by, hatch_by = _norm_color_hatch(color, hatch, cat.df)
        base = _lg.LabeledBars.from_arrays(
            x, arr, name=name, orient=orient, capsize=_capsize, extent=_extent,
            backend=backend,
        )  # fmt: skip
        self._arrays = arr
        super().__init__(base, cat.df)
        _BoxLikeMixin.__init__(self, categories, _splitby, color_by, hatch_by)
        base.with_edge(color=theme.get_theme().foreground_color)
        self._orient = orient

    @property
    def orient(self) -> Orientation:
        return self._base_layer.bars.orient

    def _get_arrays(self) -> list[np.ndarray]:
        return self._arrays

    def _set_estimation_values(self, est):
        if self.orient.is_vertical:
            self._base_layer.set_data(ydata=est)
        else:
            self._base_layer.set_data(xdata=est)

    def _set_error_values(self, err_low, err_high):
        mdata = self._base_layer.data
        if self.orient.is_vertical:
            self._base_layer.yerr.set_data(mdata.x, err_low, err_high)
        else:
            self._base_layer.xerr.set_data(err_low, err_high, mdata.y)

    def with_hover_text(self, text: str | list[str]) -> Self:
        """Set the hover tooltip text for the layer."""
        self.base.bars.with_hover_text(text)
        return self

    def with_hover_template(self, template: str) -> Self:
        """Set the hover tooltip template for the layer."""
        extra = {}
        for i, key in enumerate(self._splitby):
            extra[key] = [row[i] for row in self._categories]
        self.base.bars.with_hover_template(template, extra=extra)
        return self
