# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2018 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Module for chart plots.

"""

import bokeh
import pandas as pd
import numpy as np
from chartify._core.colors import Color, color_palettes
from chartify._core.axes import NumericalYMixin, NumericalXMixin

from scipy.stats.kde import gaussian_kde


class BasePlot:
    """Base for all plot classes."""

    def __init__(self, chart):
        self._chart = chart

    @staticmethod
    def _axis_format_precision(max_value, min_value):
        difference = abs(max_value - min_value)
        precision = abs(int(np.floor(np.log10(difference)))) + 1
        zeros = ''.join(['0']*precision)
        return "0,0.[{}]".format(zeros)

    @classmethod
    def _get_plot_class(cls, x_axis_type, y_axis_type):
        if x_axis_type == 'categorical' and y_axis_type == 'categorical':
            return PlotCategoricalXY
        elif x_axis_type not in ('categorical',
                                 'density') and y_axis_type not in (
                                     'categorical', 'density'):
            return PlotNumericXY
        elif x_axis_type == 'density' and y_axis_type == 'density':
            return PlotDensityXY
        elif x_axis_type == 'datetime' and y_axis_type == 'density':
            raise NotImplementedError(
                "Plot for this axis type combination not yet implemented.")
        elif x_axis_type == 'density' or y_axis_type == 'density':
            return PlotNumericDensityXY
        else:
            return PlotMixedTypeXY

    def _get_color_and_order(self,
                             data_frame,
                             color_column,
                             color_order,
                             categorical_columns=None):
        """
        Returns:
            colors: List of hex colors or factor_cmap.
            color_order: List of values for each color.
        """
        if color_column is None:
            colors = [self._chart.style.color_palette.next_color()]
            color_order = [None]
        else:
            # Determine color order or verify integrity of specified order.
            if color_order is None:
                color_order = sorted(data_frame[color_column].unique())
            else:
                # Check that all color factors are present in the color order.
                if not set(data_frame[color_column].unique()).issubset(
                        set(color_order)):
                    raise ValueError("""Color order must include
                                     all unique factors of variable `%s`.""" %
                                     color_column)

            next_colors = self._chart.style.color_palette.next_colors(
                color_order)
            if categorical_columns is None:  # Numeric data
                colors = next_colors
            else:
                # Color column must be in the categorical_columns
                try:
                    color_index = categorical_columns.index(color_column)
                except ValueError:
                    raise ValueError(
                        '''`color_column` must be present
                         in the `categorical_columns`'''
                    )
                color_order = [str(factor) for factor in color_order]
                colors = bokeh.transform.factor_cmap(
                    'factors',
                    palette=next_colors,
                    factors=color_order,
                    start=color_index,
                    end=color_index + 1,
                )
        return colors, color_order

    @staticmethod
    def _cannonical_series_name(series_name):
        if series_name is None:
            series_name = ''
        return 'Series:{}'.format(series_name)

    @staticmethod
    def _named_column_data_source(data_frame, series_name):
        """Ensure consistent naming of column data sources."""
        cannonical_series_name = BasePlot._cannonical_series_name(series_name)
        return bokeh.models.ColumnDataSource(
            data_frame, name=cannonical_series_name)

    def _cast_datetime_axis(self, data_frame, column):
        if self._chart._x_axis_type == 'datetime':
            if data_frame[column].dtype != 'datetime64[ns]':
                return data_frame.astype({column: 'datetime64[ns]'})
        return data_frame

    def __getattr__(self, item):
        """Override attribute error
        """
        raise AttributeError("""Plot `{}` not avaiable for the given Chart.
            Try changing the Chart parameters x_axis_type and y_axis_type.
            """.format(item))

    def _set_numeric_axis_default_format(self, data_frame,
                                         x_column=None, y_column=None):
        """Set numeric axis range based on the input data.
        """

        if isinstance(self._chart.axes, NumericalXMixin):
            # Warn user if they try to plot date data on a non-datetime axis.
            if data_frame[x_column].dtype == 'datetime64[ns]':
                raise ValueError("""Set chartify.Chart(x_axis_type='datetime')
                when plotting datetime data.""")
            # Warn user if they try to plot date data that hasn't been cast
            # to the proper dtype.
            elif data_frame[x_column].dtype == 'O':
                raise ValueError("""Attempting to plot `{}` on a numeric
                    axis. Ensure that chartify.Chart x_axis_type and y_axis_type
                    are set properly, or cast your input data appropriately.
                    """.format(x_column))

        if isinstance(self._chart.axes, NumericalXMixin):
            max_x_value = data_frame[x_column].max()
            min_x_value = data_frame[x_column].min()
            max_x_value, min_x_value = max(max_x_value, 0), min(min_x_value, 0)
            self._chart.axes.set_xaxis_tick_format(
                self._axis_format_precision(max_x_value,
                                            min_x_value)
                )

        if isinstance(self._chart.axes, NumericalYMixin):
            max_y_value = data_frame[y_column].max()
            min_y_value = data_frame[y_column].min()
            max_y_value, min_y_value = max(max_y_value, 0), min(min_y_value, 0)
            self._chart.axes.set_yaxis_tick_format(
                self._axis_format_precision(max_y_value,
                                            min_y_value)
                )


class PlotCategoricalXY(BasePlot):
    """Plot functions for categorical x & y axes:

    Methods:
        - heatmap
    """

    def heatmap(self,
                data_frame,
                x_column,
                y_column,
                color_column,
                text_column=None,
                color_palette='RdBu',
                reverse_color_order=False,
                text_color='white',
                text_format='{:,.2f}',
                color_value_min=None,
                color_value_max=None,
                color_value_range=100):
        """Heatmap.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            x_column (str): Column name to plot on the x axis.
            y_column (str): Column name to plot on the y axis.
            color_column (str): Column name of numerical type to plot on
                the color dimension.
            text_column (str or None): Column name of the text labels.
            color_palette (str, chartify.ColorPalette): Color palette to
                apply to the heatmap.
                See chartify.color_palettes.show() for available color palettes.
            reverse_color_order (bool): Reverse order of the color palette.
            text_color (str): Color name or hex value.
                See chartify.color_palettes.show() for available color names.
            text_format: Python string formatting to apply to the text labels.
            color_value_min (float): Minimum value for the color palette.
                If None, will default to the min value of the
                color_column dimension.
            color_value_max (float): Maximum value for the color palette.
                If None, will default to the max value of the
                color_column dimension.
            color_value_range (int): The size of the range of colors in
                the color palette.
                A larger color range will result in greater variation
                among the cell colors.
            """
        # Cast all categorical columns to strings
        # Plotting functions will break with non-str types.
        type_map = {column: str for column in [x_column, y_column]}
        self._chart.figure.x_range.factors = data_frame[x_column].astype(
            str).unique()
        self._chart.figure.y_range.factors = data_frame[y_column].astype(
            str).unique()

        cast_data = data_frame[[x_column, y_column,
                                color_column]].astype(type_map)

        source = self._named_column_data_source(cast_data, series_name=None)
        if text_color:
            text_color = Color(text_color).get_hex_l()
        if isinstance(color_palette, str):
            color_palette = color_palettes[color_palette]
        if reverse_color_order:
            color_palette = color_palette[::-1]
        color_palette = color_palette.expand_palette(color_value_range)
        color_palette = [c.get_hex_l() for c in color_palette.colors]

        # If not specified set the min and max value based on the data.
        if not color_value_min:
            color_value_min = data_frame[color_column].min()
        if not color_value_max:
            color_value_max = data_frame[color_column].max()
        mapper = bokeh.models.LinearColorMapper(
            palette=color_palette, low=color_value_min, high=color_value_max)
        self._chart.figure.rect(
            source=source,
            x=x_column,
            y=y_column,
            fill_color={
                'field': color_column,
                'transform': mapper
            },
            width=1,
            height=1,
            dilate=True,
            line_alpha=0)

        if text_column:
            text_font = self._chart.style._get_settings(
                'text_callout_and_plot')['font']
            formatted_text = data_frame[text_column].map(text_format.format)
            source.add(formatted_text, 'formatted_text')
            self._chart.figure.text(
                text='formatted_text',
                x=x_column,
                y=y_column,
                source=source,
                text_align='center',
                text_baseline='middle',
                text_color=text_color,
                text_font=text_font)
        return self._chart


class PlotNumericXY(BasePlot):
    """Plot functions for numeric x & y axes:

    Methods:
        - line
        - scatter
        - text
        - area
    """

    def line(self,
             data_frame,
             x_column,
             y_column,
             color_column=None,
             color_order=None,
             line_dash='solid',
             line_width=4,
             alpha=1.0):
        """Line Chart.

        Note:
            This method will not automatically sort the x-axis.
            Try sorting the axis if the line graph looks strange.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            x_column (str): Column name to plot on the x axis.
            y_column (str): Column name to plot on the y axis.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific sorting of the colors.
            line_dash (str, optional): Dash style for the line. One of:
                - 'solid'
                - 'dashed'
                - 'dotted'
                - 'dotdash'
                - 'dashdot'
            line_width (int, optional): Width of the line
            alpha (float): Alpha value.
        """
        settings = self._chart.style._get_settings('line_plot')
        line_cap = settings['line_cap']
        line_join = settings['line_join']

        colors, color_values = self._get_color_and_order(
            data_frame, color_column, color_order)

        self._set_numeric_axis_default_format(data_frame, x_column, y_column)

        for color_value, color in zip(color_values, colors):

            if color_column is None:  # Single line
                sliced_data = data_frame
            else:
                sliced_data = data_frame[data_frame[color_column] ==
                                         color_value]
            # Filter to only relevant columns.
            sliced_data = (
                sliced_data[
                    [col for col in sliced_data.columns
                        if col in (
                            x_column, y_column, color_column)]])

            cast_data = self._cast_datetime_axis(sliced_data, x_column)

            source = self._named_column_data_source(
                cast_data, series_name=color_value)

            color_value = str(
                color_value) if color_value is not None else color_value

            self._chart.figure.line(
                x=x_column,
                y=y_column,
                source=source,
                line_width=line_width,
                color=color,
                line_join=line_join,
                line_cap=line_cap,
                legend=color_value,
                line_dash=line_dash,
                alpha=alpha)

        # Set legend defaults if there are multiple series.
        if color_column is not None:
            self._chart.style._apply_settings('legend')

        return self._chart

    def scatter(self,
                data_frame,
                x_column,
                y_column,
                size_column=None,
                color_column=None,
                color_order=None,
                alpha=1.0,
                marker='circle'):
        """Scatter plot.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            x_column (str): Column name to plot on the x axis.
            y_column (str): Column name to plot on the y axis.
            size_column (str, optional): Column name of numerical values
                to plot on the size dimension.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific sorting of the colors.
            alpha (float): Alpha value.
            marker (str): marker type. Valid types:
                'asterisk', 'circle', 'circle_cross', 'circle_x', 'cross',
                'diamond', 'diamond_cross', 'hex', 'inverted_triangle',
                'square', 'square_x', 'square_cross', 'triangle',
                'x', '*', '+', 'o', 'ox', 'o+'
        """
        if size_column is None:
            size_column = 6

        colors, color_values = self._get_color_and_order(
            data_frame, color_column, color_order)

        self._set_numeric_axis_default_format(data_frame, x_column, y_column)

        for color_value, color in zip(color_values, colors):

            if color_column is None:  # Single series
                sliced_data = data_frame
            else:
                sliced_data = data_frame[data_frame[color_column] ==
                                         color_value]
            # Filter to only relevant columns.
            sliced_data = (
                sliced_data[
                    [col for col in sliced_data.columns
                        if col in (
                            x_column, y_column, size_column, color_column)]])
            cast_data = self._cast_datetime_axis(sliced_data, x_column)

            source = self._named_column_data_source(
                cast_data, series_name=color_value)

            color_value = str(
                color_value) if color_value is not None else color_value

            self._chart.figure.scatter(
                x=x_column,
                y=y_column,
                size=size_column,
                source=source,
                fill_color=color,
                legend=color_value,
                marker=marker,
                line_color=color,
                alpha=alpha)

        # Set legend defaults if there are multiple series.
        if color_column is not None:
            self._chart.style._apply_settings('legend')

        return self._chart

    def text(self,
             data_frame,
             x_column,
             y_column,
             text_column,
             color_column=None,
             color_order=None,
             font_size='1em',
             x_offset=0,
             y_offset=0,
             angle=0,
             text_color=None):
        """Text plot.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            x_column (str): Column name to plot on the x axis.
            y_column (str): Column name to plot on the y axis.
            text_column (str): Column name to plot as text labels.
            color_column (str, optional): Column name to group by on the
                color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific sorting of the colors.
            font_size (str, optional): Size of text.
            x_offset (int, optional): # of pixels for horizontal text offset.
                Can be negative. Default: 0.
            y_offset (int, optional): # of pixels for vertical text offset.
                Can be negative. Default: 0.
            angle (int): Degrees from horizontal for text rotation.
            text_color (str): Color name or hex value.
                See chartify.color_palettes.show() for available color names.
                If omitted, will default to the next color in the
                current color palette.
        """
        text_font = self._chart.style._get_settings('text_callout_and_plot')[
            'font']
        if text_color:
            text_color = Color(text_color).get_hex_l()
            colors, color_values = [text_color], [None]
        else:
            colors, color_values = self._get_color_and_order(
                data_frame, color_column, color_order)

        self._set_numeric_axis_default_format(data_frame, x_column, y_column)

        for color_value, color in zip(color_values, colors):

            if color_column is None:  # Single series
                sliced_data = data_frame
            else:
                sliced_data = data_frame[data_frame[color_column] ==
                                         color_value]
            # Filter to only relevant columns.
            sliced_data = (
                sliced_data[
                    [col for col in sliced_data.columns
                        if col in (
                            x_column, y_column, text_column, color_column)]])
            cast_data = self._cast_datetime_axis(sliced_data, x_column)

            source = self._named_column_data_source(
                cast_data, series_name=color_value)

            self._chart.figure.text(
                text=text_column,
                x=x_column,
                y=y_column,
                text_font_size=font_size,
                source=source,
                text_color=color,
                y_offset=y_offset,
                x_offset=x_offset,
                angle=angle,
                angle_units='deg',
                text_font=text_font)
        return self._chart

    def area(self,
             data_frame,
             x_column,
             y_column,
             second_y_column=None,
             color_column=None,
             color_order=None,
             stacked=False):
        """Area plot.

        Note:
            - When a single y_column is passed: Shade area between the
                y_values and zero.
            - Use `stacked` argument for stacked areas.
            - When both y_column and second_y_column are passed:
                Shade area between the two y_columns.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            x_column (str): Column name to plot on the x axis.
            y_column (str): Column name to plot on the y axis.
            second_y_column (str, optional): Column name to plot on
                the y axis.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific sorting of the colors.
            stacked (bool, optional): Stacked the areas.
                Only applicable with a single y_column.
                Default: False.
        """
        # Vertical option only applies to density plots
        vertical = self._chart.axes._vertical

        alpha = 0.2
        colors, color_values = self._get_color_and_order(
            data_frame, color_column, color_order)

        self._set_numeric_axis_default_format(data_frame, x_column, y_column)

        if color_column is not None:
            data_frame = (
                data_frame.set_index([x_column, color_column]).reindex(
                    index=pd.MultiIndex.from_product(
                        [data_frame[x_column].unique(),
                         data_frame[color_column].unique()],
                        names=[x_column, color_column]))
                .reset_index(drop=False)
                .fillna(0))

        if second_y_column is None and color_column is not None:
            last_y = np.zeros(data_frame.groupby(color_column).size().iloc[0])

        for color_value, color in zip(color_values, colors):
            if color_column is None:
                data = data_frame

                if second_y_column is None:
                    alpha = .8
                    y_data = np.hstack((data[y_column],
                                        np.zeros(len(data[y_column]))))
                else:
                    y_data = pd.concat(
                        [data[y_column], data[second_y_column][::-1]])

            else:

                data = data_frame[data_frame[color_column] == color_value]

                if second_y_column is None:
                    y_data = np.hstack((data[y_column].reset_index(drop=True),
                                        last_y[::-1]))

                    if stacked:
                        alpha = .8
                        next_y = last_y + data[y_column].reset_index(drop=True)
                        y_data = np.hstack((next_y, last_y[::-1]))
                        last_y = next_y
                        # Reverse order of vertical legends to ensure
                        # that the order is consistent with the stack order.
                        self._chart._reverse_vertical_legend = True
                else:
                    y_data = pd.concat(
                        [data[y_column], data[second_y_column][::-1]])

            x_data = pd.concat([data[x_column], data[x_column][::-1]])

            sliced_data = pd.DataFrame({x_column: x_data, y_column: y_data})
            cast_data = self._cast_datetime_axis(sliced_data, x_column)
            source = self._named_column_data_source(
                cast_data, series_name=color_value)

            color_value = str(
                color_value) if color_value is not None else color_value

            if vertical:
                self._chart.figure.patch(
                    x=x_column,
                    y=y_column,
                    alpha=alpha,
                    source=source,
                    legend=color_value,
                    color=color)
            else:
                self._chart.figure.patch(
                    x=y_column,
                    y=x_column,
                    alpha=alpha,
                    source=source,
                    legend=color_value,
                    color=color)

        # Set legend defaults if there are multiple series.
        if color_column is not None:
            self._chart.style._apply_settings('legend')

        return self._chart


class PlotNumericDensityXY(BasePlot):
    """Plot functions for single density:

    Methods:
        - histogram
        - kde
    """

    # def __dir__(self):
    #     """Hide inherited plotting methods"""
    #     inherited_public_methods = [
    #         attr for attr in dir(PlotNumericXY)
    #         if callable(getattr(PlotNumericXY, attr))
    #         and not attr.startswith("_")
    #     ]
    #     return sorted((set(dir(self.__class__)) | set(self.__dict__.keys())) -
    #                   set(inherited_public_methods))

    def histogram(self,
                  data_frame,
                  values_column,
                  color_column=None,
                  color_order=None,
                  method='count',
                  bins='auto'):
        """Histogram.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            values_column (str): Column of numeric values.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific sorting of the colors.
            method (str, optional):
            - 'count': Result will contain the number of samples at each bin.
            - 'density': Result is the value of the probability density
                function at each bin.
                The PDF is normalized so that the integral over the range is 1.
            - 'mass': Result is the value of the probability mass
                function at each bin.
                The PMF is normalized so that the value is equivalent to
                the sample count at each bin divided by the total count.
            bins (int or sequence of scalars or str, optional):
                If bins is an int, it defines the number of equal-width
                bins in the given range.
                If bins is a sequence, it defines the bin edges,
                including the rightmost edge, allowing for non-uniform
                bin widths. See numpy.histogram documentation for more details.
            - ‘auto’:
                Maximum of the ‘sturges’ and ‘fd’ estimators.
                Provides good all around performance.
            - ‘fd’ (Freedman Diaconis Estimator)
                Robust (resilient to outliers) estimator that takes into
                account data variability and data size.
            - ‘doane’
                An improved version of Sturges’ estimator that works
                better with non-normal datasets.
            - ‘scott’
                Less robust estimator that that takes into account data
                variability and data size.
            - ‘rice’
                Estimator does not take variability into account, only
                data size. Commonly overestimates number of bins required.
            - ‘sturges’
                R’s default method, only accounts for data size.
                Only optimal for gaussian data and underestimates number
                of bins for large non-gaussian datasets.
            - ‘sqrt’
                Square root (of data size) estimator, used by Excel and
                other programs for its speed and simplicity.
        """
        vertical = self._chart.axes._vertical

        colors, color_values = self._get_color_and_order(
            data_frame, color_column, color_order)

        for color_value, color in zip(color_values, colors):

            if color_column is None:  # Single line
                sliced_data = data_frame[[values_column]]
            else:
                sliced_data = data_frame[data_frame[color_column] ==
                                         color_value][[values_column]]

            density = True if method == 'density' else False
            hist, edges = np.histogram(sliced_data, density=density, bins=bins)

            if method == 'mass':
                hist = hist * 1.0 / hist.sum()

            histogram_data = pd.DataFrame({
                'values': hist,
                'min_edge': edges[:-1],
                'max_edge': edges[1:]
            })

            source = self._named_column_data_source(
                histogram_data, series_name=color_value)

            color_value = str(
                color_value) if color_value is not None else color_value

            if vertical:
                self._chart.figure.quad(
                    top='values',
                    bottom=0,
                    left='min_edge',
                    right='max_edge',
                    source=source,
                    fill_color=color,
                    line_color=color,
                    alpha=.3,
                    legend=color_value)
            else:
                self._chart.figure.quad(
                    top='max_edge',
                    bottom='min_edge',
                    left=0,
                    right='values',
                    source=source,
                    fill_color=color,
                    line_color=color,
                    alpha=.3,
                    legend=color_value)

        # Set legend defaults if there are multiple series.
        if color_column is not None:
            self._chart.style._apply_settings('legend')

        return self._chart

    def kde(self,
            data_frame,
            values_column,
            color_column=None,
            color_order=None):
        """Kernel Density Estimate Plot.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            values_column (str): Column of numeric values.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific sorting of the colors.
        """
        # Vertical is unused since the logic is handled
        # by the area chart
        # vertical = self._chart.axes._vertical

        if color_column is not None:
            color_values = sorted(data_frame[color_column].unique())
        else:
            color_values = [None]

        data = pd.DataFrame()
        for color_value in color_values:
            if color_column is None:  # Single line
                sliced_data = data_frame
            else:
                sliced_data = data_frame[data_frame[color_column] ==
                                         color_value]
            values = sliced_data[values_column]

            kde = gaussian_kde(values)
            index = np.linspace(values.min(), values.max(), 300)
            kde_pdf = kde.evaluate(index)
            data = pd.concat(
                [
                    data,
                    pd.DataFrame({
                        'x': index,
                        'y': kde_pdf,
                        'color': color_value
                    })
                ],
                axis=0)

        color_column = 'color' if color_column is not None else None

        PlotNumericXY.area(
            self,
            data,
            'x',
            'y',
            color_column=color_column,
            color_order=color_values,
            stacked=False)

        return self._chart


class PlotDensityXY(BasePlot):
    """Plot functions for denxity X & Y:

    Methods:
        - hexbin
    """

    def hexbin(self,
               data_frame,
               x_values_column,
               y_values_column,
               size,
               color_palette='Blues',
               reverse_color_order=False,
               orientation='pointytop',
               color_value_range=10
               ):
        """Hexbin.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            x_values_column (str): Column of numeric values to bin into tiles.
            y_values_column (str): Column of numeric values to bin into tiles.
            size (float): Bin size for the tiles.
            color_palette (str, chartify.ColorPalette): Color palette to
                apply to the tiles.
                See chartify.color_palettes.show() for available color palettes.
            reverse_color_order (bool): Reverse order of the color palette.
            orientation (str): "pointytop" or "flattop". Whether the hexagonal
                tiles should be oriented with a pointed corner on top, or a
                flat side on top.
            color_value_range (int): The size of the range of colors in
                the color palette.
                A larger color range will result in greater variation
                among the cell colors.
        """
        if isinstance(color_palette, str):
            color_palette = color_palettes[color_palette]
        if reverse_color_order:
            color_palette = color_palette[::-1]
        color_palette = color_palette.expand_palette(color_value_range)
        color_palette = [c.get_hex_l() for c in color_palette.colors]

        # Set the chart aspect ratio otherwise the hexbins won't be symmetric.
        aspect_scale = (self._chart.style.plot_width
                        / self._chart.style.plot_height)
        self._chart.figure.match_aspect = True
        self._chart.figure.aspect_scale = aspect_scale
        self._chart.figure.hexbin(
            data_frame[x_values_column],
            data_frame[y_values_column],
            size=size,
            orientation=orientation,
            aspect_scale=aspect_scale,
            palette=color_palette,
            line_color='white'
            )

        return self._chart


class PlotMixedTypeXY(BasePlot):
    """Plot functions for mixed type x & y axes:

    Methods:
        - bar
        - bar_stacked
        - lollipop
        - parallel
    """

    def _set_categorical_axis_default_factors(self, vertical, factors):
        """Reassign the categorical axis with the given factors.
        """
        if vertical:
            self._chart.figure.x_range.factors = factors
        else:
            self._chart.figure.y_range.factors = factors

    def _set_categorical_axis_default_range(self, vertical, data_frame,
                                            numeric_column):
        """Set numeric axis range based on the input data.
        """
        max_value = data_frame[numeric_column].max()
        min_value = data_frame[numeric_column].min()

        max_ge_zero = max_value >= 0
        min_ge_zero = min_value >= 0

        range_start, range_end = None, None
        if max_ge_zero and min_ge_zero:
            range_start = 0
        elif not max_ge_zero and not min_ge_zero:
            range_end = 0

        max_value = max(max_value, 0)
        min_value = min(min_value, 0)

        if vertical:
            self._chart.axes.set_yaxis_range(start=range_start, end=range_end)
            self._chart.axes.set_yaxis_tick_format(
                self._axis_format_precision(max_value, min_value))
        else:
            self._chart.axes.set_xaxis_range(start=range_start, end=range_end)
            self._chart.axes.set_xaxis_tick_format(
                self._axis_format_precision(max_value, min_value))

    @staticmethod
    def _get_bar_width(factors):
        """Get the bar width based on the number of factors"""
        n_factors = len(factors)
        if n_factors == 1:
            return .3
        elif n_factors == 2:
            return .5
        elif n_factors == 3:
            return .7
        else:
            return .9

    def _construct_source(self,
                          data_frame,
                          categorical_columns,
                          numeric_column,
                          stack_column=None,
                          normalize=False,
                          categorical_order_by=None,
                          categorical_order_ascending=False):
        """Constructs ColumnDataSource

        Returns:
            source: ColumnDataSource
            factors: list of categorical factors
            stack_values: list of stack values
        """
        # Cast categorical columns to a list.
        if not isinstance(categorical_columns, str):
            categorical_columns = [c for c in categorical_columns]
        else:
            categorical_columns = [categorical_columns]

        # Check that there's only one row per grouping
        grouping = categorical_columns[:]
        if stack_column is not None:
            grouping.append(stack_column)
        rows_per_grouping = (data_frame.groupby(grouping).size())
        max_one_row_per_grouping = all(rows_per_grouping <= 1)
        if not max_one_row_per_grouping:
            raise ValueError(
                """Each categorical grouping should have at most 1 observation.
                Group the dataframe and aggregate before passing to
                the plot function.
                """)

        # Cast stack column to strings
        # Plotting functions will break with non-str types.
        type_map = {}
        if stack_column is not None:
            type_map[stack_column] = str
        # Apply mapping within pivot so original data frame isn't modified.
        source = (
            pd.pivot_table(
                data_frame.astype(type_map),
                columns=stack_column,
                index=categorical_columns,
                values=numeric_column,
                aggfunc='sum').fillna(0)  # NA columns break the stacks
        )

        # Normalize values at the grouped levels.
        # Only relevant for stacked objects
        if normalize:
            source = source.div(source.sum(axis=1), axis=0)

        order_length = getattr(categorical_order_by, "__len__", None)
        # Sort the categories
        if categorical_order_by == 'values':
            # Recursively sort values within each level of the index.
            row_totals = source.sum(axis=1)
            row_totals.name = 'sum'
            old_index = row_totals.index
            row_totals = row_totals.reset_index()
            row_totals.columns = ['_%s' % col for col in row_totals.columns]
            row_totals.index = old_index

            heirarchical_sort_cols = categorical_columns[:]
            for i, _ in enumerate(heirarchical_sort_cols):
                row_totals['level_%s' % i] = (row_totals.groupby(
                    heirarchical_sort_cols[:i + 1])['_sum'].transform('sum'))
            row_totals = row_totals.sort_values(
                by=[
                    'level_%s' % i
                    for i, _ in enumerate(heirarchical_sort_cols)
                ],
                ascending=categorical_order_ascending)
            source = source.reindex(row_totals.index)
        elif categorical_order_by == 'labels':
            source = source.sort_index(
                0, ascending=categorical_order_ascending)
        # Manual sort
        elif order_length is not None:
            source = source.reindex(categorical_order_by, axis='index')
        else:
            raise ValueError(
                """Must be 'values', 'labels', or a list of values.""")

        # Cast all categorical columns to strings
        # Plotting functions will break with non-str types.
        if isinstance(source.index, pd.MultiIndex):
            for level in range(len(source.index.levels)):
                source.index = source.index.set_levels(
                    source.index.levels[level].astype(str), level=level)
        else:
            source.index = source.index.astype(str)

        factors = source.index
        source = source.reset_index(drop=True)
        stack_values = source.columns
        source = self._named_column_data_source(source, series_name=None)
        source.add(factors, 'factors')

        return source, factors, stack_values

    def text(self,
             data_frame,
             categorical_columns,
             numeric_column,
             text_column,
             color_column=None,
             color_order=None,
             categorical_order_by='values',
             categorical_order_ascending=False,
             font_size='1em',
             x_offset=0,
             y_offset=0,
             angle=0,
             text_color=None):
        """Text plot.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            categorical_columns (str or list): Column name to plot on
                the categorical axis.
            numeric_column (str): Column name to plot on the numerical axis.
            text_column (str): Column name to plot as text labels.
            color_column (str, optional): Column name to group by on the
                color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific color sort.
            categorical_order_by (str or array-like, optional):
                Dimension for ordering the categorical axis. Default 'values'.
                - 'values': Order categorical axis by the numerical axis
                    values. Default.
                - 'labels': Order categorical axis by the categorical labels.
                - array-like object (list, tuple, np.array): New labels
                    to conform the categorical axis to.
            categorical_order_ascending (bool, optional): Sort order of the
                categorical axis. Default False.
            font_size (str, optional): Size of text.
            x_offset (int, optional): # of pixels for horizontal text offset.
                Can be negative. Default: 0.
            y_offset (int, optional): # of pixels for vertical text offset.
                Can be negative. Default: 0.
            angle (int): Degrees from horizontal for text rotation.
            text_color (str): Color name or hex value.
                See chartify.color_palettes.show() for available color names.
                If omitted, will default to the next color in
                the current color palette.
        """
        vertical = self._chart.axes._vertical
        text_font = self._chart.style._get_settings('text_callout_and_plot')[
            'font']

        source, factors, _ = self._construct_source(
            data_frame,
            categorical_columns,
            numeric_column,
            categorical_order_by=categorical_order_by,
            categorical_order_ascending=categorical_order_ascending)

        if text_color:
            text_color = Color(text_color).get_hex_l()
            colors, color_values = [text_color], [None]
        else:
            colors, color_values = self._get_color_and_order(
                data_frame, color_column, color_order)

        self._set_categorical_axis_default_factors(vertical, factors)

        if vertical:
            text_align = 'center'
            text_baseline = 'bottom'
            x_value, y_value = 'factors', numeric_column
            y_offset = y_offset - 4
        else:
            y_value, x_value = 'factors', numeric_column
            text_align = 'left'
            text_baseline = 'middle'
            x_offset = x_offset + 10

        for color_value, color in zip(color_values, colors):

            if color_column is None:  # Single series
                sliced_data = data_frame
            else:
                sliced_data = data_frame[data_frame[color_column] ==
                                         color_value]

            # Construct a new source based on the sliced data.
            source, _, _ = self._construct_source(
                sliced_data,
                categorical_columns,
                numeric_column,
                categorical_order_by=categorical_order_by,
                categorical_order_ascending=categorical_order_ascending)
            sliced_data = (sliced_data.set_index(categorical_columns)
                           .reindex(source.data['factors']).reset_index())
            # Text column isn't in the source so it needs to be added.
            if text_column != numeric_column:
                source.add(sliced_data[text_column], name=text_column)

            self._chart.figure.text(
                text=text_column,
                x=x_value,
                y=y_value,
                text_font_size=font_size,
                source=source,
                text_color=color,
                y_offset=y_offset,
                x_offset=x_offset,
                angle=angle,
                angle_units='deg',
                text_align=text_align,
                text_baseline=text_baseline,
                text_font=text_font)

        return self._chart

    def text_stacked(self,
                     data_frame,
                     categorical_columns,
                     numeric_column,
                     stack_column,
                     text_column,
                     normalize=False,
                     stack_order=None,
                     categorical_order_by='values',
                     categorical_order_ascending=False,
                     font_size='1em',
                     x_offset=0,
                     y_offset=0,
                     angle=0,
                     text_color=None):
        """Text plot for use with stacked plots.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            categorical_columns (str or list): Column name to plot on
                the categorical axis.
            numeric_column (str): Column name to plot on the numerical axis.
            text_column (str): Column name to plot as text labels.
                Note: Null text values will be omitted from the plot.
            stack_column (str): Column name to group by on the stack dimension.
            normalize (bool, optional): Normalize numeric dimension for
                100% stacked bars. Default False.
            stack_order (list, optional): List of values within the
                'stack_column' dimension for specific stack sort.
            categorical_order_by (str or array-like, optional):
                Dimension for ordering the categorical axis. Default 'values'.
                - 'values': Order categorical axis by the numerical
                    axis values. Default.
                - 'labels': Order categorical axis by the categorical labels.
                - array-like object (list, tuple, np.array): New labels
                    to conform the categorical axis to.
            categorical_order_ascending (bool, optional): Sort order of the
                categorical axis. Default False.
            font_size (str, optional): Size of text.
            x_offset (int, optional): # of pixels for horizontal text offset.
                Can be negative. Default: 0.
            y_offset (int, optional): # of pixels for vertical text offset.
                Can be negative. Default: 0.
            angle (int): Degrees from horizontal for text rotation.
            text_color (str): Color name or hex value.
                See chartify.color_palettes.show() for available color names.
                If omitted, will default to the next color in
                the current color palette.
        """
        vertical = self._chart.axes._vertical
        text_font = self._chart.style._get_settings('text_callout_and_plot')[
            'font']

        source, factors, stack_values = self._construct_source(
            data_frame,
            categorical_columns,
            numeric_column,
            stack_column,
            normalize=normalize,
            categorical_order_by=categorical_order_by,
            categorical_order_ascending=categorical_order_ascending)

        if text_color:
            text_color = Color(text_color).get_hex_l()
            if stack_order is None:
                stack_order = sorted(data_frame[stack_column].unique())
            else:
                # If stack order is set then
                # make sure it includes all the levels.
                if not set(data_frame[stack_column].unique()).issubset(
                        set(stack_order)):
                    raise ValueError("""Color order must include
                                    all unique factors of variable `%s`.""" %
                                     stack_order)
            colors, color_values = [text_color] * len(
                data_frame[stack_column].unique()), stack_order
        else:
            colors, color_values = self._get_color_and_order(
                data_frame, stack_column, stack_order)

        self._set_categorical_axis_default_factors(vertical, factors)
        self._set_categorical_axis_default_range(vertical, data_frame,
                                                 numeric_column)

        # Set numeric axis format to percentages.
        if normalize:
            if vertical:
                self._chart.axes.set_yaxis_tick_format("0%")
            else:
                self._chart.axes.set_xaxis_tick_format("0%")

        text_baseline = 'middle'
        if vertical:
            text_align = 'center'
        else:
            text_align = 'left'
            x_offset = x_offset + 10

        cumulative_numeric_value = None

        for color_value, color in zip(color_values, colors):

            sliced_data = data_frame[(data_frame[stack_column] == color_value)]
            # Reindex to be consistent with the factors.
            type_map = {column: str for column in categorical_columns}
            sliced_data = (sliced_data.astype(type_map)
                           .set_index(categorical_columns)
                           .reindex(index=factors).reset_index())

            text_values = np.where(sliced_data[text_column].isna(), '',
                                   sliced_data[text_column])

            if cumulative_numeric_value is not None:
                cumulative_numeric_value = (
                    cumulative_numeric_value
                    + source.data[color_value]
                    * .5
                    )
            else:
                cumulative_numeric_value = source.data[color_value] * .5

            if vertical:
                x_value, y_value = factors, cumulative_numeric_value
            else:
                y_value, x_value = factors, cumulative_numeric_value

            self._chart.figure.text(
                text=text_values,
                x=x_value,
                y=y_value,
                text_font_size=font_size,
                text_color=color,
                y_offset=y_offset,
                x_offset=x_offset,
                angle=angle,
                angle_units='deg',
                text_align=text_align,
                text_baseline=text_baseline,
                text_font=text_font)

            cumulative_numeric_value = (
                cumulative_numeric_value
                + source.data[color_value]
                * .5
            )

        return self._chart

    def bar(self,
            data_frame,
            categorical_columns,
            numeric_column,
            color_column=None,
            color_order=None,
            categorical_order_by='values',
            categorical_order_ascending=False):
        """Bar chart.

        Note:
            To change the orientation set x_axis_type or y_axis_type
            argument of the Chart object.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            categorical_columns (str or list): Column name to plot on
                the categorical axis.
            numeric_column (str): Column name to plot on the numerical axis.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific color sort.
            categorical_order_by (str or array-like, optional):
                Dimension for ordering the categorical axis. Default 'values'.
                - 'values': Order categorical axis by the numerical
                    axis values. Default.
                - 'labels': Order categorical axis by the categorical labels.
                - array-like object (list, tuple, np.array): New labels
                    to conform the categorical axis to.
            categorical_order_ascending (bool, optional): Sort order of the
                categorical axis. Default False.
        """
        vertical = self._chart.axes._vertical

        source, factors, _ = self._construct_source(
            data_frame,
            categorical_columns,
            numeric_column,
            categorical_order_by=categorical_order_by,
            categorical_order_ascending=categorical_order_ascending)

        colors, _ = self._get_color_and_order(data_frame, color_column,
                                              color_order, categorical_columns)
        if color_column is None:
            colors = colors[0]

        self._set_categorical_axis_default_factors(vertical, factors)
        self._set_categorical_axis_default_range(vertical, data_frame,
                                                 numeric_column)
        bar_width = self._get_bar_width(factors)
        if vertical:
            self._chart.figure.vbar(
                x='factors',
                width=bar_width,
                top=numeric_column,
                bottom=0,
                line_color='white',
                source=source,
                fill_color=colors)
        else:
            self._chart.figure.hbar(
                y='factors',
                height=bar_width,
                right=numeric_column,
                left=0,
                line_color='white',
                source=source,
                fill_color=colors)
        return self._chart

    def interval(self,
                 data_frame,
                 categorical_columns,
                 lower_bound_column,
                 upper_bound_column,
                 middle_column=None,
                 categorical_order_by='values',
                 categorical_order_ascending=False,
                 color='black'):
        """Interval.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            categorical_columns (str or list): Column name to plot on
                the categorical axis.
            lower_bound_column (str): Column name to plot on the
                numerical axis for the lower bound.
            upper_bound_column (str): Column name to plot on the
                numerical axis for the upper bound.
            middle_column (str, optional): Column name to plot on the
                numerical axis for the middle tick.
            categorical_order_by (str or array-like, optional):
                Dimension for ordering the categorical axis. Default 'values'.
                - 'values': Order categorical axis by the numerical
                    axis values. Default.
                - 'labels': Order categorical axis by the categorical labels.
                - array-like object (list, tuple, np.array): New labels
                    to conform the categorical axis to.
            categorical_order_ascending (bool, optional): Sort order of the
                categorical axis. Default False.
            color (str): Color name or hex value.
                See chartify.color_palettes.show() for available color names.
        """
        interval_color = Color(color).get_hex_l()

        vertical = self._chart.axes._vertical

        _, factors, _ = self._construct_source(
            data_frame,
            categorical_columns,
            lower_bound_column,
            categorical_order_by=categorical_order_by,
            categorical_order_ascending=categorical_order_ascending)
        self._set_categorical_axis_default_factors(vertical, factors)

        # Set the axis precision
        max_value = max(data_frame[lower_bound_column].max(),
                        data_frame[upper_bound_column].max())
        min_value = min(data_frame[lower_bound_column].min(),
                        data_frame[upper_bound_column].min())
        max_value, min_value = max(max_value, 0), min(min_value, 0)
        if vertical:
            self._chart.axes.set_yaxis_tick_format(
                self._axis_format_precision(max_value,
                                            min_value)
                )
        else:
            self._chart.axes.set_xaxis_tick_format(
                self._axis_format_precision(max_value,
                                            min_value)
                )

        interval_settings = self._chart.style._get_settings('interval_plot')
        SPACE_BETWEEN_BARS = interval_settings['space_between_bars']
        MARGIN = interval_settings['margin']
        BAR_WIDTH = interval_settings['bar_width']
        SPACE_BETWEEN_CATEGORIES = interval_settings[
            'space_between_categories']
        INTERVAL_END_STEM_SIZE = interval_settings['interval_end_stem_size']
        INTERVAL_MIDPOINT_STEM_SIZE = interval_settings[
            'interval_midpoint_stem_size']

        def bar_edges(index, category_number):
            """Return start, midpoint, end edge coordinates"""
            bar_num = index + 1
            start = (
                bar_num * MARGIN + (bar_num - 1) * MARGIN + (bar_num - 1) *
                (BAR_WIDTH) + SPACE_BETWEEN_BARS * (bar_num - 1) +
                SPACE_BETWEEN_CATEGORIES * (category_number - 1))
            midpoint = start + BAR_WIDTH / 2.
            end = start + BAR_WIDTH
            return (start, midpoint, end)

        aggregate_columns = [lower_bound_column, upper_bound_column]
        if middle_column is not None:
            aggregate_columns.append(middle_column)
        # Categorical_columns to List
        if not isinstance(categorical_columns, str):
            categorical_columns = [c for c in categorical_columns]
        else:
            categorical_columns = [categorical_columns]
        # Cast categorical columns to str to prevent dates from breaking
        type_map = {column: str for column in categorical_columns}
        values = (data_frame.astype(type_map)
                  .groupby(categorical_columns)[aggregate_columns].sum()
                  .reindex(factors).reset_index())
        # Need to keep track of changes to categorical columns
        # To calculate spacing between values
        values['new_heirarchy'] = False
        if len(categorical_columns) > 1:
            for col in categorical_columns[:-1]:
                values['new_column'] = values[col] != values[col].shift(1)
                values['new_heirarchy'] = values[[
                    'new_heirarchy', 'new_column'
                ]].max(axis=1)
            values['category_number'] = values['new_heirarchy'].cumsum()
        else:
            values['category_number'] = 1
        for index, row in values.iterrows():
            bar_midpoint = bar_edges(index, row['category_number'])[1]
            if vertical:
                # Vertical line
                self._chart.figure.segment(
                    bar_midpoint,
                    row[lower_bound_column],
                    bar_midpoint,
                    row[upper_bound_column],
                    color=interval_color)
                # Top
                self._chart.figure.segment(
                    bar_midpoint - INTERVAL_END_STEM_SIZE,
                    row[upper_bound_column],
                    bar_midpoint + INTERVAL_END_STEM_SIZE,
                    row[upper_bound_column],
                    color=interval_color)
                # Bottom
                self._chart.figure.segment(
                    bar_midpoint - INTERVAL_END_STEM_SIZE,
                    row[lower_bound_column],
                    bar_midpoint + INTERVAL_END_STEM_SIZE,
                    row[lower_bound_column],
                    color=interval_color)
                # Middle
                if middle_column is not None:
                    self._chart.figure.segment(
                        bar_midpoint - INTERVAL_MIDPOINT_STEM_SIZE,
                        row[middle_column],
                        bar_midpoint + INTERVAL_MIDPOINT_STEM_SIZE,
                        row[middle_column],
                        color=interval_color)
            else:
                # Horizontal line
                self._chart.figure.segment(
                    row[lower_bound_column],
                    bar_midpoint,
                    row[upper_bound_column],
                    bar_midpoint,
                    color=interval_color)
                # Left
                self._chart.figure.segment(
                    row[lower_bound_column],
                    bar_midpoint - INTERVAL_END_STEM_SIZE,
                    row[lower_bound_column],
                    bar_midpoint + INTERVAL_END_STEM_SIZE,
                    color=interval_color)
                # Right
                self._chart.figure.segment(
                    row[upper_bound_column],
                    bar_midpoint - INTERVAL_END_STEM_SIZE,
                    row[upper_bound_column],
                    bar_midpoint + INTERVAL_END_STEM_SIZE,
                    color=interval_color)
                # Middle
                if middle_column is not None:
                    self._chart.figure.segment(
                        row[middle_column],
                        bar_midpoint - INTERVAL_MIDPOINT_STEM_SIZE,
                        row[middle_column],
                        bar_midpoint + INTERVAL_MIDPOINT_STEM_SIZE,
                        color=interval_color)
        return self._chart

    def bar_stacked(self,
                    data_frame,
                    categorical_columns,
                    numeric_column,
                    stack_column,
                    normalize=False,
                    stack_order=None,
                    categorical_order_by='values',
                    categorical_order_ascending=False):
        """Plot stacked bar chart.

        Note:
            - To change the orientation set x_axis_type or y_axis_type
            argument of the Chart object.
            - Stacked numeric values must be all positive or all negative.
            To plot both positive and negative values on the same chart
            call this method twice. Once for the positive values and
            once for the negative values.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            categorical_columns (str or list): Column name to plot on
                the categorical axis.
            numeric_column (str): Column name to plot on the numerical axis.
            stack_column (str): Column name to group by on the stack dimension.
            normalize (bool, optional): Normalize numeric dimension for
                100% stacked bars. Default False.
            stack_order (list, optional): List of values within the
                'stack_column' dimension for specific stack sort.
            categorical_order_by (str or array-like, optional):
                Dimension for ordering the categorical axis. Default 'values'.
                - 'values': Order categorical axis by the numerical
                    axis values. Default.
                - 'labels': Order categorical axis by the categorical labels.
                - array-like object (list, tuple, np.array): New labels
                    to conform the categorical axis to.
            categorical_order_ascending (bool, optional): Sort order
                of the categorical axis. Default False.
        """

        vertical = self._chart.axes._vertical

        source, factors, stack_values = self._construct_source(
            data_frame,
            categorical_columns,
            numeric_column,
            stack_column,
            normalize=normalize,
            categorical_order_by=categorical_order_by,
            categorical_order_ascending=categorical_order_ascending)

        colors, _ = self._get_color_and_order(data_frame, stack_column,
                                              stack_order)
        if stack_column is None:
            colors = colors[0]

        self._set_categorical_axis_default_factors(vertical, factors)
        self._set_categorical_axis_default_range(vertical, data_frame,
                                                 numeric_column)
        bar_width = self._get_bar_width(factors)
        # Set numeric axis format to percentages.
        if normalize:
            if vertical:
                self._chart.axes.set_yaxis_tick_format("0%")
            else:
                self._chart.axes.set_xaxis_tick_format("0%")

        if stack_order is not None:
            if not set(stack_values).issubset(set(stack_order)):
                raise ValueError("""Stack order must include all distinct
                                    values of the stack column `%s`
                                 """ % (stack_column))
            stack_values = stack_order

        legend = [bokeh.core.properties.value(str(x)) for x in stack_values]

        if vertical:
            self._chart.figure.vbar_stack(
                stack_values,
                x='factors',
                width=bar_width,
                line_color='white',
                source=source,
                fill_color=colors,
                legend=legend)
        else:
            self._chart.figure.hbar_stack(
                stack_values,
                y='factors',
                height=bar_width,
                line_color='white',
                source=source,
                fill_color=colors,
                legend=legend)
        self._chart.style._apply_settings('legend')
        # Reverse order of vertical legends to ensure that the order
        # is consistent with the stack order.
        self._chart._reverse_vertical_legend = True

        return self._chart

    def lollipop(self,
                 data_frame,
                 categorical_columns,
                 numeric_column,
                 color_column=None,
                 color_order=None,
                 categorical_order_by='values',
                 categorical_order_ascending=False):
        """Lollipop chart.

        Note:
            To change the orientation set x_axis_type or y_axis_type
            argument of the Chart object.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            categorical_columns (str or list): Column name to plot on
                the categorical axis.
            numeric_column (str): Column name to plot on the numerical axis.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional):
                List of values within the 'color_column' for
                    specific color sort.
            categorical_order_by (str or array-like, optional):
                Dimension for ordering the categorical axis. Default 'values'.
                - 'values': Order categorical axis by the numerical axis values.
                - 'labels': Order categorical axis by the categorical labels.
                - array-like object (list, tuple, np.array): New labels
                    to conform the categorical axis to.
            categorical_order_ascending (bool, optional):
                Sort order of the categorical axis. Default False.
        """

        vertical = self._chart.axes._vertical

        source, factors, _ = self._construct_source(
            data_frame,
            categorical_columns,
            numeric_column,
            categorical_order_by=categorical_order_by,
            categorical_order_ascending=categorical_order_ascending)

        colors, _ = self._get_color_and_order(data_frame, color_column,
                                              color_order, categorical_columns)
        if color_column is None:
            colors = colors[0]

        self._set_categorical_axis_default_factors(vertical, factors)
        self._set_categorical_axis_default_range(vertical, data_frame,
                                                 numeric_column)

        if vertical:
            self._chart.figure.segment(
                'factors',
                0,
                'factors',
                numeric_column,
                line_width=2,
                line_color=colors,
                source=source)
            self._chart.figure.circle(
                'factors',
                numeric_column,
                size=10,
                fill_color=colors,
                line_color=colors,
                line_width=3,
                source=source)
        else:
            self._chart.figure.segment(
                0,
                'factors',
                numeric_column,
                'factors',
                line_width=2,
                line_color=colors,
                source=source)
            self._chart.figure.circle(
                numeric_column,
                'factors',
                size=10,
                fill_color=colors,
                line_color=colors,
                line_width=3,
                source=source)
        return self._chart

    def parallel(self,
                 data_frame,
                 categorical_columns,
                 numeric_column,
                 color_column=None,
                 color_order=None,
                 categorical_order_by='values',
                 categorical_order_ascending=False,
                 line_dash='solid',
                 line_width=4,
                 alpha=1.0
                 ):
        """Parallel coordinate plot.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            categorical_columns (str or list): Column name to plot on
                the categorical axis.
            numeric_column (str): Column name to plot on the numerical axis.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific color sort.
            categorical_order_by (str or array-like, optional):
                Dimension for ordering the categorical axis. Default 'values'.
                - 'values': Order categorical axis by the numerical axis values.
                - 'labels': Order categorical axis by the categorical labels.
                - array-like object (list, tuple, np.array): New labels
                    to conform the categorical axis to.
            categorical_order_ascending (bool, optional):
                Sort order of the categorical axis. Default False.
            line_dash (str, optional): Dash style for the line. One of:
                - 'solid'
                - 'dashed'
                - 'dotted'
                - 'dotdash'
                - 'dashdot'
            line_width (int, optional): Width of the line
            alpha (float): Alpha value
        """
        settings = self._chart.style._get_settings('line_plot')
        line_cap = settings['line_cap']
        line_join = settings['line_join']

        vertical = self._chart.axes._vertical

        source, factors, _ = self._construct_source(
            data_frame,
            categorical_columns,
            numeric_column,
            # Each color has its own stack for parallel plots.
            # This causes each color to appear as its own column.
            stack_column=color_column,
            categorical_order_by=categorical_order_by,
            categorical_order_ascending=categorical_order_ascending)

        colors, color_values = self._get_color_and_order(
            data_frame, color_column, color_order)

        self._set_categorical_axis_default_factors(vertical, factors)
        self._set_numeric_axis_default_format(data_frame,
                                              numeric_column,
                                              numeric_column)

        for color_value, color in zip(color_values, colors):

            if color_column is None:  # Single series
                color_value = numeric_column
                legend = None
            else:
                legend = bokeh.core.properties.value(str(color_value))

            if vertical:
                x_value, y_value = 'factors', str(color_value)
            else:
                y_value, x_value = 'factors', str(color_value)

            self._chart.figure.line(
                x=x_value,
                y=y_value,
                source=source,
                line_width=line_width,
                color=color,
                line_join=line_join,
                line_cap=line_cap,
                legend=legend,
                line_dash=line_dash,
                alpha=alpha)

        # Set legend defaults if there are multiple series.
        if color_column is not None:
            self._chart.style._apply_settings('legend')

    def scatter(self,
                data_frame,
                categorical_columns,
                numeric_column,
                size_column=None,
                color_column=None,
                color_order=None,
                categorical_order_by='count',
                categorical_order_ascending=False,
                alpha=1.0,
                marker='circle'):
        """Scatter chart.

        Note:
            To change the orientation set x_axis_type or y_axis_type
            argument of the Chart object.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            categorical_columns (str or list): Column name to plot on
                the categorical axis.
            numeric_column (str): Column name to plot on the numerical axis.
            size_column (str, optional): Column name of numerical values
                to plot on the size dimension.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional):
                List of values within the 'color_column' for
                    specific color sort.
            categorical_order_by (str or array-like, optional):
                Dimension for ordering the categorical axis. Default 'count'.
                - 'count': Order categorical axis by the count of values.
                - 'labels': Order categorical axis by the categorical labels.
                - array-like object (list, tuple, np.array): New labels
                    to conform the categorical axis to.
            categorical_order_ascending (bool, optional):
                Sort order of the categorical axis. Default False.
            alpha (float): Alpha value.
            marker (str): marker type. Valid types:
                'asterisk', 'circle', 'circle_cross', 'circle_x', 'cross',
                'diamond', 'diamond_cross', 'hex', 'inverted_triangle',
                'square', 'square_x', 'square_cross', 'triangle',
                'x', '*', '+', 'o', 'ox', 'o+'
        """
        vertical = self._chart.axes._vertical

        if size_column is None:
            size_column = 15

        axis_factors = data_frame.groupby(categorical_columns).size()

        order_length = getattr(categorical_order_by, "__len__", None)
        if categorical_order_by == 'labels':
            axis_factors = axis_factors.sort_index(
                ascending=categorical_order_ascending).index
        elif categorical_order_by == 'count':
            axis_factors = axis_factors.sort_values(
                ascending=categorical_order_ascending).index
        # User-specified order.
        elif order_length is not None:
            axis_factors = categorical_order_by
        else:
            raise ValueError(
                """Must be 'count', 'labels', or a list of values.""")

        colors, color_values = self._get_color_and_order(
            data_frame, color_column, color_order)
        # Apply factors to the axis.
        self._set_categorical_axis_default_factors(vertical, axis_factors)

        for color_value, color in zip(color_values, colors):
            if color_column is None:  # Single series
                color_value = numeric_column
                legend = None
                sliced_data = data_frame
            else:
                legend = bokeh.core.properties.value(str(color_value))
                sliced_data = data_frame[data_frame[color_column] ==
                                         color_value]
            # Filter to only relevant columns.
            data_factors = sliced_data.set_index(categorical_columns).index
            sliced_data = (
                sliced_data[
                    [col for col in sliced_data.columns
                        if col in (
                            numeric_column, size_column)]])
            source = self._named_column_data_source(
                sliced_data, series_name=color_value)
            source.add(data_factors, 'factors')

            if vertical:
                x_value, y_value = 'factors', numeric_column
            else:
                y_value, x_value = 'factors', numeric_column

            self._chart.figure.scatter(
                x=x_value,
                y=y_value,
                size=size_column,
                fill_color=color,
                line_color=color,
                source=source,
                legend=legend,
                marker=marker,
                alpha=alpha
                )

        # Set legend defaults if there are multiple series.
        if color_column is not None:
            self._chart.style._apply_settings('legend')

        return self._chart
