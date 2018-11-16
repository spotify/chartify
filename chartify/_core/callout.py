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
Module for chart callouts.

"""

import bokeh
from chartify._core import colors
from chartify._core.axes import DatetimeXNumericalYAxes


class Callout:
    """Class for adding callouts to the chart."""

    def __init__(self, chart):
        self._chart = chart

    def line(self,
             location,
             orientation='width',
             line_color='black',
             line_dash='solid',
             line_width=2,
             line_alpha=1.0):
        """Add line callout to the chart.

        Args:
            location (numeric):
            orientation (str, optional): (default: 'width')
                - 'width'
                - 'height'
            line_color (str, optional): Color name or hex value.
                See chartify.color_palettes.show() for available color names.
            line_dash (str, optional): Dash style for the line. One of:
                - 'solid'
                - 'dashed'
                - 'dotted'
                - 'dotdash'
                - 'dashdot'
            line_width (int, optional): Width of the line
            line_alpha (float, optional): Alpha of the line. Between 0 and 1.

        Returns:
            Current chart object
        """
        # Convert datetime values to epoch if datetime axis.
        if isinstance(self._chart.axes,
                      DatetimeXNumericalYAxes) and orientation == 'height':
            location = self._chart.axes._convert_timestamp_to_epoch_ms(location)
        line_color = colors.Color(line_color).get_hex_l()
        location_units = 'data'
        span = bokeh.models.Span(
            location=location,
            dimension=orientation,
            line_color=line_color,
            line_dash=line_dash,
            line_width=line_width,
            location_units=location_units,
            line_alpha=line_alpha)
        self._chart.figure.add_layout(span)
        return self._chart

    def line_segment(self,
                     x_start,
                     y_start,
                     x_end,
                     y_end,
                     line_color='black',
                     line_dash='solid',
                     line_width=2,
                     line_alpha=1.0):
        """Add line segment callout to the chart.

        Args:
            x_start (numeric)
            y_start (numeric)
            x_end (numeric)
            y_end (numeric)
            line_color (str): Color name or hex value.
                See chartify.color_palettes.show() for available color names.
            line_dash (str, optional): Dash style for the line. One of:
                - 'solid'
                - 'dashed'
                - 'dotted'
                - 'dotdash'
                - 'dashdot'
            line_width (int, optional): Width of the line
            line_alpha (float, optional): Alpha of the line. Between 0 and 1.

        Returns:
            Current chart object
        """
        # Convert datetime values to epoch if datetime axis.
        if isinstance(self._chart.axes, DatetimeXNumericalYAxes):
            x_start = self._chart.axes._convert_timestamp_to_epoch_ms(x_start)
            x_end = self._chart.axes._convert_timestamp_to_epoch_ms(x_end)
        line_color = colors.Color(line_color).get_hex_l()
        segment = bokeh.models.Arrow(
            x_start=x_start,
            y_start=y_start,
            x_end=x_end,
            y_end=y_end,
            end=None,
            start=None,
            line_color=line_color,
            line_width=line_width,
            line_dash=line_dash,
            line_alpha=line_alpha)

        self._chart.figure.add_layout(segment)
        return self._chart

    def box(self,
            top=None,
            bottom=None,
            left=None,
            right=None,
            alpha=.2,
            color='red'):
        """Add box callout to the chart.

        Args:
            top (numeric, optional): Top edge of the box.
            bottom (numeric, optional): Bottom edge of the box.
            left (numeric, optional): Left edge of the box.
            right (numeric, optional): Right edge of the box.
            alpha (float, optional): 0.2
            color (str): Color name or hex value.
                See chartify.color_palettes.show() for available color names.

        Note:
            The box will extend to the edge if the corresponding position
            argument is omitted.

        Returns:
            Current chart object
        """
        # Convert datetime values to epoch if datetime axis.
        if isinstance(self._chart.axes, DatetimeXNumericalYAxes):
            if left is not None:
                left = self._chart.axes._convert_timestamp_to_epoch_ms(left)
            if right is not None:
                right = self._chart.axes._convert_timestamp_to_epoch_ms(right)
        color = colors.Color(color).get_hex_l()
        box = bokeh.models.BoxAnnotation(
            top=top,
            bottom=bottom,
            left=left,
            right=right,
            fill_alpha=alpha,
            fill_color=color)
        self._chart.figure.add_layout(box)
        return self._chart

    def text(self,
             text,
             x,
             y,
             text_color='black',
             text_align='left',
             font_size='1em',
             angle=0):
        """Add text callout to the chart.

        Note:
            Use `\n` within text for newlines.
        Args:
            x (numeric): x location of the text.
            y (numeric, optional): y location of the text.
            text_color (str): Color name or hex value.
                See chartify.color_palettes.show() for available color names.
            text_align (str: 'left', 'right', 'center'): Text alignment.
            font_size (str): Font size.
            angle (int, 0 to 360): Angle in degrees from horizontal. Default: 0

        Returns:
            Current chart object
        """
        # Convert datetime values to epoch if datetime axis.
        if isinstance(self._chart.axes, DatetimeXNumericalYAxes):
            x = self._chart.axes._convert_timestamp_to_epoch_ms(x)
        text_color = colors.Color(text_color).get_hex_l()
        source = bokeh.models.ColumnDataSource({
            'text': [text],
            'x': [x],
            'y': [y]
        })
        text_font = self._chart.style._get_settings('text_callout_and_plot')[
            'font']
        self._chart.figure.text(
            x='x',
            y='y',
            text='text',
            text_color=text_color,
            text_align=text_align,
            angle=angle,
            angle_units='deg',
            text_font=text_font,
            source=source,
            text_font_size=font_size)
        return self._chart
