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
Module for Radar Chart
"""
from chartify._core.colors import Color
from chartify._core.chart import Chart
from chartify._core.style import Style
from chartify._core.axes import BaseAxes
from chartify._core.plot import BasePlot
from chartify._core.callout import Callout
from chartify._core.options import options
import numpy as np
import pandas as pd


class RadarChart(Chart):

    def __init__(self,
                 blank_labels=options.get_option('chart.blank_labels'),
                 layout='slide_50%'):
        """Create a Radar Chart instance.

        Note:
            Radar charts plot each vertex in counter-clockwise order starting
            from the top.

        Args:
            blank_labels (bool): When true removes the title,
                subtitle, axes, and source labels from the chart.
                Default False.
            layout (str): Change size & aspect ratio of the chart for
                fitting into slides.
                - 'slide_100%'
                - 'slide_75%'
                - 'slide_50%' (Suggested for Radar Charts)
                - 'slide_25%'
        """
        # Validate axis type input
        valid_axis_types = [
            'linear', 'log'
        ]
        self._axis_type = 'linear'
        self._x_axis_type, self._y_axis_type = self._axis_type, self._axis_type
        if self._axis_type not in valid_axis_types:
            raise ValueError('axis_type must be one of {options}'.format(
                options=valid_axis_types))
        self._blank_labels = options._get_value(blank_labels)
        self.style = Style(self, layout)
        self.figure = self._initialize_figure(self._axis_type,
                                              self._axis_type)
        self.style._apply_settings('chart')
        self.callout = Callout(self)
        self.axes = BaseAxes._get_axis_class(self._axis_type,
                                             self._axis_type)(self)
        self.plot = PlotRadar(self)
        self._source = self._add_source_to_figure()
        self._subtitle_glyph = self._add_subtitle_to_figure()
        self.figure.toolbar.logo = None  # Remove bokeh logo from toolbar.
        # Reverse the order of vertical legends. Used with stacked plot types
        # to ensure that the stack order is consistent with the legend order.
        self._reverse_vertical_legend = False
        # Logos disabled for now.
        # self.logo = Logo(self)
        # Set default for title
        title = """ch.set_title('Takeaway')"""
        if self._blank_labels:
            title = ""
        self.set_title(title)


class PlotRadar(BasePlot):

    _X_COLUMN = '__xs'
    _Y_COLUMN = '__ys'
    _THETA_COLUMN = '__theta'

    @staticmethod
    def _get_thetas(num_vars):
        thetas = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
        # rotate theta such that the first axis is at the top
        thetas += np.pi/2
        return thetas

    @staticmethod
    def _to_xy_coords(df, r, theta, center=0, offset=0.00):
        """ Returns the x and y coordinates corresponding to the magnitudes of
        each variable displayed in the radar plot
        """
        # offset from center of circle
        ys = (df[r] + offset) * np.sin(df[theta]) + center
        xs = (df[r] + offset) * np.cos(df[theta]) + center
        return pd.DataFrame({'xs': xs, 'ys': ys})

    def text(self,
             data_frame,
             radius_column,
             text_column,
             color_column=None,
             color_order=None,
             font_size='1em',
             x_offset=0,
             y_offset=0,
             angle=0,
             text_color=None,
             text_align='left'):
        """Text plot.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            radius_column (str): Column name containing radius values.
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
            text_align (str): 'left', 'right', or 'center'
        """
        text_font = self._chart.style._get_settings('text_callout_and_plot')[
            'font']
        if text_color:
            text_color = Color(text_color).get_hex_l()
            colors, color_values = [text_color], [None]
        else:
            colors, color_values = self._get_color_and_order(
                data_frame, color_column, color_order)

        self._set_numeric_axis_default_format(data_frame,
                                              radius_column,
                                              radius_column)

        for color_value, color in zip(color_values, colors):

            if color_column is None:  # Single series
                sliced_data = data_frame
            else:
                sliced_data = data_frame[
                    data_frame[color_column] == color_value]

            coord_df = sliced_data.copy()
            coord_df[self._THETA_COLUMN] = self._get_thetas(len(coord_df))
            coord_df[[self._X_COLUMN, self._Y_COLUMN]] = self._to_xy_coords(
                coord_df, radius_column, self._THETA_COLUMN)

            source = self._named_column_data_source(
                coord_df, series_name=color_value)

            self._chart.figure.text(
                text=text_column,
                x=self._X_COLUMN,
                y=self._Y_COLUMN,
                text_font_size=font_size,
                source=source,
                text_color=color,
                y_offset=y_offset,
                x_offset=x_offset,
                angle=angle,
                angle_units='deg',
                text_font=text_font,
                y_range_name=self._y_range_name,
                text_align=text_align)
        return self._chart

    def perimeter(self,
                  data_frame,
                  radius_column,
                  color_column=None,
                  color_order=None,
                  line_dash='solid',
                  line_width=4,
                  alpha=1.0):
        """Perimeter line plot.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            radius_column (str): Column name containing radius values.
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

        self._set_numeric_axis_default_format(data_frame,
                                              radius_column,
                                              radius_column)

        for color_value, color in zip(color_values, colors):

            if color_column is None:  # Single line
                sliced_data = data_frame
            else:
                sliced_data = data_frame[
                    data_frame[color_column] == color_value]

            coord_df = sliced_data[[radius_column]].copy()
            coord_df[self._THETA_COLUMN] = self._get_thetas(len(coord_df))
            coord_df[[self._X_COLUMN, self._Y_COLUMN]] = self._to_xy_coords(
                coord_df, radius_column, self._THETA_COLUMN)
            # Add endpoint
            coord_df = coord_df.append(coord_df.iloc[0])

            source = self._named_column_data_source(
                coord_df, series_name=color_value)

            color_value = str(
                color_value) if color_value is not None else color_value

            self._plot_with_legend(
                self._chart.figure.line,
                legend_label=color_value,
                x=self._X_COLUMN,
                y=self._Y_COLUMN,
                source=source,
                line_width=line_width,
                color=color,
                line_join=line_join,
                line_cap=line_cap,
                line_dash=line_dash,
                alpha=alpha,
                y_range_name=self._y_range_name
                )

        # Set legend defaults if there are multiple series.
        if color_column is not None:
            self._chart.style._apply_settings('legend')

        return self._chart

    def area(self,
             data_frame,
             radius_column,
             color_column=None,
             color_order=None,
             alpha=.2):
        """Area plot.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            radius_column (str): Column name containing radius values.
            color_column (str, optional): Column name to group by on
                the color dimension.
            color_order (list, optional): List of values within the
                'color_column' for specific sorting of the colors.
            alpha (float): Alpha value.
        """
        colors, color_values = self._get_color_and_order(
            data_frame, color_column, color_order)

        self._set_numeric_axis_default_format(data_frame,
                                              radius_column,
                                              radius_column)

        for color_value, color in zip(color_values, colors):

            if color_column is None:  # Single line
                sliced_data = data_frame
            else:
                sliced_data = data_frame[
                    data_frame[color_column] == color_value]

            coord_df = sliced_data[[radius_column]].copy()
            coord_df[self._THETA_COLUMN] = self._get_thetas(len(coord_df))
            coord_df[[self._X_COLUMN, self._Y_COLUMN]] = self._to_xy_coords(
                coord_df, radius_column, self._THETA_COLUMN)
            # Add endpoint
            coord_df = coord_df.append(coord_df.iloc[0])

            source = self._named_column_data_source(
                coord_df, series_name=color_value)

            color_value = str(
                color_value) if color_value is not None else color_value

            self._plot_with_legend(
                self._chart.figure.patch,
                legend_label=color_value,
                x=self._X_COLUMN,
                y=self._Y_COLUMN,
                source=source,
                color=color,
                line_width=0,
                alpha=alpha,
                y_range_name=self._y_range_name
                )

        # Set legend defaults if there are multiple series.
        if color_column is not None:
            self._chart.style._apply_settings('legend')

        return self._chart

    def radius(self,
               data_frame,
               radius_column,
               color_column=None,
               color_order=None,
               line_dash='solid',
               line_width=4,
               alpha=1.0):
        """Radius line plot.

        Args:
            data_frame (pandas.DataFrame): Data source for the plot.
            radius_column (str): Column name containing radius values.
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

        self._set_numeric_axis_default_format(
            data_frame, radius_column, radius_column)

        for color_value, color in zip(color_values, colors):
            if color_column is None:  # Single line
                sliced_data = data_frame
            else:
                sliced_data = data_frame[
                    data_frame[color_column] == color_value]

            coord_df = sliced_data[[radius_column]].copy()
            coord_df[self._THETA_COLUMN] = self._get_thetas(len(coord_df))
            coord_df[[self._X_COLUMN, self._Y_COLUMN]] = self._to_xy_coords(
                coord_df, radius_column, self._THETA_COLUMN)

            color_value = str(
                color_value) if color_value is not None else color_value

            for i, r in coord_df.iterrows():

                self._plot_with_legend(
                    self._chart.figure.line,
                    legend_label=color_value,
                    x=[0, r[self._X_COLUMN]],
                    y=[0, r[self._Y_COLUMN]],
                    line_width=line_width,
                    color=color,
                    line_join=line_join,
                    line_cap=line_cap,
                    line_dash=line_dash,
                    alpha=alpha,
                    y_range_name=self._y_range_name
                    )

        # Set legend defaults if there are multiple series.
        if color_column is not None:
            self._chart.style._apply_settings('legend')

        return self._chart
