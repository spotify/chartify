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
Module for logic related to chart axes.

"""

import pandas as pd
import bokeh
from bokeh.models.tickers import FixedTicker
from math import pi


class BaseAxes:
    """Base class for axes."""

    def __init__(self, chart):
        self._chart = chart
        self._initialize_defaults()

    @classmethod
    def _get_axis_class(cls, x_axis_type, y_axis_type):
        if x_axis_type == 'categorical' and y_axis_type == 'categorical':
            return CategoricalXYAxes
        elif x_axis_type == 'categorical':
            return NumericalYAxis
        elif y_axis_type == 'categorical':
            return NumericalXAxis
        elif x_axis_type == 'datetime':
            return DatetimeXNumericalYAxes
        return NumericalXYAxes

    @property
    def _vertical(self):
        if self._chart._x_axis_type == 'density':
            return False
        elif isinstance(self, (NumericalYAxis,
                               NumericalXYAxes,
                               DatetimeXNumericalYAxes)):
            return True
        else:
            return False

    def _initialize_defaults(self):
        xaxis_label = """ch.axes.set_xaxis_label('label (units)')"""
        yaxis_label = """ch.axes.set_yaxis_label('label (units)')"""
        if self._chart._blank_labels:
            xaxis_label = ''
            yaxis_label = ''
        self.set_xaxis_label(xaxis_label)
        self.set_yaxis_label(yaxis_label)

    @staticmethod
    def _convert_major_orientation_labels(orientation):
        """Map the user inputted orientation values to the values expected by
        bokeh for major labels."""
        if orientation == 'vertical':
            orientation = pi / 180 * 90
        elif orientation == 'diagonal':
            orientation = pi / 180 * 45
        elif orientation != 'horizontal':
            raise ValueError(
                'Orientation must be `horizontal`, `vertical`, or `diagonal`.')
        return orientation

    def _convert_subgroup_orientation_labels(self, orientation):
        """Map the user inputted orientation values to the values expected by
        bokeh for group labels."""

        if self._vertical:
            horizontal_value = 'parallel'
            vertical_value = pi / 180 * 90
        else:
            horizontal_value = 'normal'
            vertical_value = 'parallel'

        if orientation == 'horizontal':
            orientation = horizontal_value
        elif orientation == 'vertical':
            orientation = vertical_value
        elif orientation == 'diagonal':
            orientation = pi / 180 * 45
        else:
            raise ValueError(
                'Orientation must be `horizontal`, `vertical`, or `diagonal`.')
        return orientation

    @property
    def xaxis_label(self):
        """Return x-axis label.

        Returns:
            x-axis label text
        """
        return self._chart.figure.xaxis[0].axis_label

    def set_xaxis_label(self, label):
        """Set x-axis label text.

        Args:
            label (string): the text for the x-axis label

        Returns:
            Current chart object
        """
        self._chart.figure.xaxis.axis_label = label
        return self._chart

    @property
    def yaxis_label(self):
        """Return y-axis label.

        Returns:
            y-axis label text
        """
        return self._chart.figure.yaxis.axis_label

    def set_yaxis_label(self, label):
        """Set y-axis label text.

        Args:
            label (string): the text for the y-axis label

        Returns:
            Current chart object
        """
        self._chart.figure.yaxis.axis_label = label
        return self._chart

    def hide_xaxis(self):
        """Hide the tick labels, ticks, and axis lines of the x-axis.

        The x-axis label will remain visible, but can be
        removed with .axes.set_xaxis_label("")

        """
        # self._chart.figure.xaxis.visible = False

        self._chart.figure.xaxis.axis_line_alpha = 0
        self._chart.figure.xaxis.major_tick_line_color = None
        self._chart.figure.xaxis.minor_tick_line_color = None
        self._chart.figure.xaxis.major_label_text_color = None

        return self._chart

    def hide_yaxis(self):
        """Hide the tick labels, ticks, and axis lines of the y-axis.

        The y-axis label will remain visible, but can be
        removed with .axes.set_yaxis_label("")
        """
        self._chart.figure.yaxis.axis_line_alpha = 0
        self._chart.figure.yaxis.major_tick_line_color = None
        self._chart.figure.yaxis.minor_tick_line_color = None
        self._chart.figure.yaxis.major_label_text_color = None

        return self._chart

    def set_xaxis_tick_orientation(self, orientation='horizontal'):
        """Change the orientation or the x axis tick labels.

        Args:
            orientation (str or list of str):
                str: 'horizontal', 'vertical', or 'diagonal'
                list of str: different orientation values corresponding to each
                level of the grouping. Example: ['horizontal', 'vertical']
        """

        if not isinstance(orientation, list):
            orientation = [orientation] * 3

        level_1 = orientation[0]
        level_2 = orientation[1] if len(orientation) > 1 else 'horizontal'
        level_3 = orientation[2] if len(orientation) > 2 else level_2

        level_1 = self._convert_major_orientation_labels(level_1)
        level_2 = self._convert_subgroup_orientation_labels(level_2)
        level_3 = self._convert_subgroup_orientation_labels(level_3)

        self._chart.figure.xaxis.major_label_orientation = level_1

        xaxis = self._chart.figure.xaxis[0]
        has_subgroup_label = getattr(xaxis, 'subgroup_label_orientation', None)
        if has_subgroup_label is not None:
            self._chart.figure.xaxis.subgroup_label_orientation = level_2

        has_group_label = getattr(xaxis, 'group_label_orientation', None)
        if has_group_label is not None:
            self._chart.figure.xaxis.group_label_orientation = level_3
        return self._chart


class NumericalXMixin:
    def set_xaxis_range(self, start=None, end=None):
        """Set x-axis range.

        Args:
            start (numeric, optional): the start of the x-axis range
            end (numeric, optional): the end of the x-axis range

        Returns:
            Current chart object
        """
        self._chart.figure.x_range.end = end
        self._chart.figure.x_range.start = start
        return self._chart

    def set_xaxis_tick_values(self, values):
        """Set x-axis tick values.

        Args:
            values (list or DatetimeIndex): Values for the axis ticks.

        Returns:
            Current chart object
        """
        self._chart.figure.xaxis.ticker = FixedTicker(ticks=values)
        return self._chart

    def set_xaxis_tick_format(self, num_format):
        """Set x-axis tick label number format.

        Args:
            num_format (string): the number format for the x-axis tick labels

        Examples:
            Decimal precision
            >>> ch.set_xaxis_tick_format('0.0')
            Label format: 1000 -> 1000.0

            Percentage
            >>> ch.set_xaxis_tick_format("0%")
            Label format: 0.9748 -> 97%
            0.974878234 ‘0.000%’    97.488%

            Currency:
            >>> ch.set_xaxis_tick_format('$0,0.00')
            Label format: 1000.234 -> $1,000.23

            Auto formatting:
            >>> ch.set_xaxis_tick_format('0 a')
            Label format: 10000 -> 10 K

            Additional documentation: http://numbrojs.com/old-format.html

        Returns:
            Current chart object
        """
        self._chart.figure.xaxis[0].formatter = (
            bokeh.models.NumeralTickFormatter(format=num_format)
            )
        return self._chart


class NumericalYMixin:
    def set_yaxis_range(self, start=None, end=None):
        """Set y-axis range.

        Args:
            start (numeric, optional): the start of the y-axis range
            end (numeric, optional): the end of the y-axis range

        Returns:
            Current chart object
        """
        self._chart.figure.y_range.end = end
        self._chart.figure.y_range.start = start
        return self._chart

    def set_yaxis_tick_values(self, values):
        """Set y-axis tick values.

        Args:
            values (list): Values for the axis ticks.

        Returns:
            Current chart object
        """
        self._chart.figure.yaxis.ticker = FixedTicker(ticks=values)
        return self._chart

    def set_yaxis_tick_format(self, num_format):
        """Set y-axis tick label number format.

        Args:
            num_format (string): the number format for the y-axis tick labels

        Examples:
            Decimal precision
            >>> ch.set_yaxis_tick_format('0.0')
            Label format: 1000 -> 1000.0

            Percentage
            >>> ch.set_yaxis_tick_format("0%")
            Label format: 0.9748 -> 97%
            0.974878234 ‘0.000%’    97.488%

            Currency:
            >>> ch.set_yaxis_tick_format('$0,0.00')
            Label format: 1000.234 -> $1,000.23

            Auto formatting:
            >>> ch.set_xaxis_tick_format('0a')
            Label format: 10000 -> 10 K

            Additional documentation: http://numbrojs.com/old-format.html

        Returns:
            Current chart object
        """
        self._chart.figure.yaxis[
            0].formatter = bokeh.models.NumeralTickFormatter(format=num_format)
        return self._chart


class CategoricalXMixin:
    @property
    def xaxis_factors(self):
        """Return the categorical factors of the x axis.

        Can be a list or Pandas Index or MultiIndex.

        See additional usage notes in .set_xaxis_factors docstring."""
        return self._chart.figure.x_range.factors

    def set_xaxis_factors(self, factors):
        """Set the categorical factors of the x axis.

        Note:
            Advanced feature for custom sorting of factors:
            - Retrieve the factor values with .xaxis_factors
            - Reorder as necessary
            - Set the custom order with .set_xaxis_factors()

            Easier and recommended approach to reordering factors is to set the
            `categorical_order_by` and `categorical_order_ascending` parameters
            of the plotting function.

        Args:
            factors: Sequence of factors.
            Can be a list or Pandas Index or MultiIndex.
        """
        self._chart.figure.x_range.factors = factors
        return self._chart

    def hide_xaxis(self):
        super(NumericalYAxis, self).hide_xaxis()
        try:
            self._chart.figure.xaxis.subgroup_text_color = None
            self._chart.figure.xaxis.group_text_color = None
        except:
            pass
        return self._chart

    hide_xaxis.__doc__ = BaseAxes.hide_xaxis.__doc__


class CategoricalYMixin:
    @property
    def yaxis_factors(self):
        """Return the categorical factors of the y axis.

        Can be a list or Pandas Index or MultiIndex.

        See additional usage notes in .set_yaxis_factors docstring."""
        return self._chart.figure.y_range.factors

    def set_yaxis_factors(self, factors):
        """Set the categorical factors of the y axis.

        Note:
            Advanced feature for custom sorting of factors:
            - Retrieve the factor values with .yaxis_factors
            - Reorder as necessary
            - Set the custom order with .set_yaxis_factors()

            Easier and recommended approach to reordering factors is to set the
            `categorical_order_by` and `categorical_order_ascending` parameters
            of the plotting function.

        Args:
            factors: Sequence of factors.
            Can be a list or Pandas Index or MultiIndex.
        """
        self._chart.figure.y_range.factors = factors
        return self._chart

    def hide_yaxis(self):
        super(NumericalXAxis, self).hide_yaxis()
        try:
            self._chart.figure.yaxis.subgroup_text_color = None
            self._chart.figure.yaxis.group_text_color = None
        except:
            pass
        return self._chart

    def set_yaxis_tick_orientation(self, orientation='horizontal'):
        """Change the orientation or the y axis tick labels.

        Args:
            orientation (str or list of str):
                str: 'horizontal', 'vertical', or 'diagonal'
                list of str: different orientation values corresponding to each
                level of the grouping. Example: ['horizontal', 'vertical']
        """

        if not isinstance(orientation, list):
            orientation = [orientation] * 3

        level_1 = orientation[0]
        level_2 = orientation[1] if len(orientation) > 1 else 'horizontal'
        level_3 = orientation[2] if len(orientation) > 2 else level_2

        level_1 = self._convert_major_orientation_labels(level_1)
        level_2 = self._convert_subgroup_orientation_labels(level_2)
        level_3 = self._convert_subgroup_orientation_labels(level_3)

        self._chart.figure.yaxis.major_label_orientation = level_1
        self._chart.figure.yaxis.subgroup_label_orientation = level_2
        self._chart.figure.yaxis.group_label_orientation = level_3
        return self._chart

    hide_yaxis.__doc__ = BaseAxes.hide_yaxis.__doc__


class DatetimeXMixin:
    @staticmethod
    def _convert_timestamp_list_to_epoch_ms(ts_list):
        return list(
            map(
                lambda x: (
                    (pd.to_datetime(x) - pd.Timestamp("1970-01-01"))
                    // pd.Timedelta('1ms')),
                ts_list))

    @staticmethod
    def _convert_timestamp_to_epoch_ms(timestamp):
        return (pd.to_datetime(timestamp) -
                pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')

    def set_xaxis_range(self, start=None, end=None):
        """Set x-axis range.

        Args:
            start (str, pd.Timestamp, optional): the start of the x-axis range.
            end (str, pd.Timestamp, optional): the end of the x-axis range.

        Returns:
            Current chart object
        """
        if start:
            start = self._convert_timestamp_to_epoch_ms(start)
        if end:
            end = self._convert_timestamp_to_epoch_ms(end)
        self._chart.figure.x_range.end = end
        self._chart.figure.x_range.start = start
        return self._chart

    def set_xaxis_tick_values(self, values):
        """Set x-axis tick values.

        Args:
            values (list or DatetimeIndex): Values for the axis ticks.

        Note:
            Values should be a DatetimeIndex or list of
            pandas._libs.tslib.Timestamp objects.
            We suggest using pd.date_range to generate this list.

            e.g. for a range of month start dates in 2018:
            pd.date_range('2018-01-01', '2019-01-01', freq='MS')

        Returns:
            Current chart object
        """
        values = self._convert_timestamp_list_to_epoch_ms(values)
        self._chart.figure.xaxis.ticker = FixedTicker(ticks=values)
        return self._chart

    def set_xaxis_tick_format(self, date_format):
        """Set x-axis tick label date format.

        Args:
            date_format (string): the date format
            for the x-axis tick labels.

        Examples:
            Daily precision
            >>> ch.set_xaxis_tick_format('%Y-%m-%d')
            Label format: YYYY-MM-DD

            Monthly precision
            >>> ch.set_xaxis_tick_format("%Y-%m")
            Label format: YYYY-MM

            Yearly precision
            >>> ch.set_xaxis_tick_format("%Y")
            Label format: YYYY

            Second Precision
            >>> ch.set_xaxis_tick_format("%Y-%m-%d %H:%M:%S")
            Label format: YYYY-MM-DD HH:MM:SS

            Day of week and day of month
            >>> ch.set_xaxis_tick_format("%a%d")
            Label format: Wed07

            Month and year
            >>> ch.set_xaxis_tick_format("%b%y")
            Label format: Jan17

        See bokeh.models.DatetimeTickFormatter documentation
        for more formatting options.

        Returns:
            Current chart object
        """
        self._chart.figure.xaxis[
            0].formatter = bokeh.models.DatetimeTickFormatter(
                milliseconds=[date_format],
                seconds=[date_format],
                minsec=[date_format],
                minutes=[date_format],
                hourmin=[date_format],
                hours=[date_format],
                days=[date_format],
                months=[date_format],
                years=[date_format])
        return self._chart


class NumericalXAxis(BaseAxes, NumericalXMixin, CategoricalYMixin):
    """Axis class for numerical X and categorical Y axes"""

    def __init__(self, chart):
        super(NumericalXAxis, self).__init__(chart)
        self._chart.style._apply_settings('categorical_yaxis')


class NumericalYAxis(BaseAxes, CategoricalXMixin, NumericalYMixin):
    """Axis class for numerical Y and categorical X axes"""

    def __init__(self, chart):
        super(NumericalYAxis, self).__init__(chart)
        self._chart.style._apply_settings('categorical_xaxis')


class NumericalXYAxes(BaseAxes, NumericalXMixin, NumericalYMixin):
    """Axis class for numerical X and Y axes."""


class DatetimeXNumericalYAxes(BaseAxes, DatetimeXMixin, NumericalYMixin):
    """Axis class for datetime X and numerical Y axes."""


class CategoricalXYAxes(BaseAxes, CategoricalXMixin, CategoricalYMixin):
    """Axis class for categorical X and Y axes."""

    def __init__(self, chart):
        super(CategoricalXYAxes, self).__init__(chart)
        self._chart.style._apply_settings('categorical_xyaxis')
