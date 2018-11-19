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
Module for logic related to chart styles.


"""

from itertools import cycle
import yaml

import bokeh

from chartify._core import colors
from chartify._core.options import options


class BasePalette:
    """Base class for color palettes."""

    def __init__(self, chart, palette):
        self._chart = chart
        self._set_palette_colors(palette)

    def _set_palette_colors(self, palette):

        try:
            # Palette is a string.
            # Retreive the appropriate ColorPalette object.
            if palette.lower():
                palette = colors.color_palettes[palette]
        except AttributeError:
            pass

        palette_colors = getattr(palette, 'colors', None)
        if palette_colors is not None:
            # Palette is a ColorPalette object
            self._colors = [color.get_hex_l() for color in palette_colors]
        else:
            # Palette is a list of color strings
            self._colors = [
                colors.Color(color).get_hex_l() for color in palette
            ]

    @classmethod
    def _get_palette_class(cls,
                           chart,
                           palette_type='categorical',
                           palette=None,
                           accent_values=None):
        if palette_type == 'categorical':
            if palette is None:
                palette_name = options.get_option(
                    'style.color_palette_categorical')
                palette = colors.color_palettes[palette_name]
            return CategoricalPalette(chart, palette)
        elif palette_type == 'sequential':
            if palette is None:
                palette_name = options.get_option(
                    'style.color_palette_sequential')
                palette = colors.color_palettes[palette_name]
            return OrdinalPalette(chart, palette)
        elif palette_type == 'diverging':
            if palette is None:
                palette_name = options.get_option(
                    'style.color_palette_diverging')
                palette = colors.color_palettes[palette_name]
            return OrdinalPalette(chart, palette)
        elif palette_type == 'accent':
            if palette is None:
                palette_name = options.get_option('style.color_palette_accent')
                palette = colors.color_palettes[palette_name]
            return AccentPalette(chart, palette, accent_values)
        else:
            raise ValueError(
                """Type must be one of: ('categorical', 'sequential',
                                         'diverging', 'accent').""")

    def next_colors(self, color_column_values):
        """Return a list of colors associated with each value."""
        return [self.next_color(o) for o in color_column_values]

    def next_color(self, color_column_value=None):
        """Return the next color from the color palette."""
        raise NotImplementedError


class OrderedPaletteMixin:
    """Mixin for palettes that should be applied in order."""

    def reset_palette_order(self):
        """Reset the order of the color palette."""
        self._color_cycle = cycle(self._colors)

    def next_color(self, color_column_value=None):
        """Return the next color from the color palette."""
        return next(self._color_cycle)


class CategoricalPalette(OrderedPaletteMixin, BasePalette):
    """Categorical palettes are those that have no designated order."""

    def __init__(self, chart, palette):
        super(CategoricalPalette, self).__init__(chart, palette)
        self._color_cycle = cycle(self._colors)


class OrdinalPalette(OrderedPaletteMixin, BasePalette):
    """Ordinal palettes have an order associated with the color dimension."""

    def __init__(self, chart, palette):
        super(OrdinalPalette, self).__init__(chart, palette)
        self._color_cycle = cycle(self._colors)

    def next_colors(self, color_column_values):
        """Return a list of colors associated with each value."""
        palette_colors = self._colors
        if len(color_column_values) > len(self._colors):
            palette = (colors.ColorPalette.from_hex_list(colors=self._colors)
                       .expand_palette(len(color_column_values)))
            palette_colors = [color.get_hex_l() for color in palette.colors]
        return bokeh.palettes.linear_palette(palette_colors,
                                             len(color_column_values))


class AccentPalette(BasePalette):
    """Accent Palette.

    Accent palette assigns specific colors to specific values
    within the color dimension.

    The default color is used for values that are unassigned."""

    def __init__(self, chart, palette, accent_values=None):
        super(AccentPalette, self).__init__(chart, palette)
        self._accent_color_map = None
        self.set_accent_values(accent_values)
        self.set_default_color(
            options.get_option('style.color_palette_accent_default_color'))

    def set_accent_values(self, accent_values):
        """Set values that should be accented.

        Args:
        - accent_values (list or dict): List of values that
        should be accented or dictionary of 'value': 'color' pairs.
        """
        if isinstance(accent_values, dict):
            self._accent_color_map = {
                value: colors.Color(color).get_hex_l()
                for value, color in accent_values.items()
            }
        else:
            self._accent_color_map = dict(
                list(zip(accent_values, cycle(self._colors))))
        return self._chart

    def next_color(self, color_column_value=None):
        """Return the color for the given values.

        Args:
            color_column_value: TODO
        """
        return self._accent_color_map.get(color_column_value,
                                          self._default_color)

    def set_default_color(self, color):
        """
        Set default color of values in the 'color_column'
        that are not accented."""
        color = colors.Color(color).get_hex_l()
        self._default_color = color


class Style:
    """
    Contains attributes and methods for modifying the aesthetic
    style of the chart.
    """

    def __init__(self, chart, layout):
        self._chart = chart
        self.color_palette = BasePalette._get_palette_class(self._chart)
        self._layout = layout
        self._set_width_and_height(layout)

        self.settings = {
            'legend': {
                'figure.legend.orientation': 'horizontal',
                'figure.legend.location': 'top_left',
                'figure.legend.label_text_font': 'helvetica'
            },
            'chart': {
                'figure.background_fill_color': "white",
                'figure.xgrid.grid_line_color': None,
                'figure.ygrid.grid_line_color': None,
                'figure.border_fill_color': "white",
                'figure.min_border_left': 60,
                'figure.min_border_right': 60,
                'figure.min_border_top': 40,
                'figure.min_border_bottom': 60,
                'figure.xaxis.axis_line_width': 1,
                'figure.yaxis.axis_line_width': 1,
                'figure.yaxis.axis_line_color': "#C0C0C0",
                'figure.xaxis.axis_line_color': "#C0C0C0",
                'figure.yaxis.axis_label_text_color': "#666666",
                'figure.xaxis.axis_label_text_color': "#666666",
                'figure.xaxis.major_tick_line_color': "#C0C0C0",
                'figure.xaxis.minor_tick_line_color': "#C0C0C0",
                'figure.yaxis.major_tick_line_color': "#C0C0C0",
                'figure.yaxis.minor_tick_line_color': "#C0C0C0",
                'figure.xaxis.major_label_text_color': '#898989',
                'figure.yaxis.major_label_text_color': '#898989',
                'figure.outline_line_alpha': 1,
                'figure.outline_line_color': 'white',
                'figure.xaxis.axis_label_text_font': 'helvetica',
                'figure.yaxis.axis_label_text_font': 'helvetica',
                'figure.yaxis.major_label_text_font': 'helvetica',
                'figure.xaxis.major_label_text_font': 'helvetica',
                'figure.yaxis.axis_label_text_font_style': 'bold',
                'figure.xaxis.axis_label_text_font_style': 'bold',
                'figure.yaxis.axis_label_text_font_size': "11pt",
                'figure.xaxis.axis_label_text_font_size': "11pt",
                'figure.yaxis.major_label_text_font_size': "10pt",
                'figure.xaxis.major_label_text_font_size': "10pt",
                'figure.title.text_font': 'helvetica',
                'figure.title.text_color': '#333333',
                'figure.title.text_font_size': "18pt",
                'figure.xaxis.minor_tick_out': 1,
                'figure.yaxis.minor_tick_out': 1,
                'figure.xaxis.major_tick_line_width': 1,
                'figure.yaxis.major_tick_line_width': 1,
                'figure.xaxis.major_tick_out': 4,
                'figure.yaxis.major_tick_out': 4,
                'figure.xaxis.major_tick_in': 0,
                'figure.yaxis.major_tick_in': 0,
            },
            'categorical_xaxis': {
                # Used for grouped categorical axes
                'figure.xaxis.separator_line_alpha': 0,
                'figure.xaxis.subgroup_text_font': 'helvetica',
                'figure.xaxis.group_text_font': 'helvetica',
                'figure.xaxis.subgroup_text_font_size': "11pt",
                'figure.xaxis.group_text_font_size': "11pt",
                'figure.x_range.factor_padding': .25
            },
            'categorical_yaxis': {
                # Used for grouped categorical axes
                'figure.yaxis.separator_line_alpha': 0,
                'figure.yaxis.subgroup_text_font': 'helvetica',
                'figure.yaxis.group_text_font': 'helvetica',
                'figure.y_range.factor_padding': .25,
                'figure.yaxis.subgroup_text_font_size': "11pt",
                'figure.yaxis.group_text_font_size': "11pt",
            },
            'categorical_xyaxis': {
                # Used for grouped categorical axes
                'figure.yaxis.separator_line_alpha': 0,
                'figure.yaxis.subgroup_text_font': 'helvetica',
                'figure.yaxis.group_text_font': 'helvetica',
                'figure.yaxis.subgroup_text_font_size': "11pt",
                'figure.yaxis.group_text_font_size': "11pt",
                # Used for grouped categorical axes
                'figure.xaxis.separator_line_alpha': 0,
                'figure.xaxis.subgroup_text_font': 'helvetica',
                'figure.xaxis.group_text_font': 'helvetica',
                'figure.xaxis.subgroup_text_font_size': "11pt",
                'figure.xaxis.group_text_font_size': "11pt",
            },
            'subtitle': {
                'subtitle_align': 'left',
                'subtitle_text_color': '#666666',
                'subtitle_location': 'above',
                'subtitle_text_size': '12pt',
                'subtitle_text_font': 'helvetica'
            },
            'text_callout_and_plot': {
                'font': 'helvetica',
            },
            'interval_plot': {
                'space_between_bars': .25,
                'margin': .05,
                'bar_width': .9,
                'space_between_categories': 1.15,
                # Note each stem is drawn twice
                'interval_end_stem_size': .1 / 2,
                'interval_midpoint_stem_size': .03 / 2
            },
            'line_plot': {
                'line_cap': 'round',
                'line_join': 'round',
                'line_width': 4,
                'line_dash': 'solid'
            }
        }

        config_filename = options.get_option('config.style_settings')
        try:
            self._settings_from_yaml(
                config_filename, apply_chart_settings=False)
        except FileNotFoundError:
            pass

    def _set_width_and_height(self, layout='slide_100%'):
        """Set plot width and height based on the layout"""
        self.plot_width = 960
        self.plot_height = 540
        height_multiplier, width_multiplier = 1., 1.

        if layout == 'slide_75%':
            height_multiplier = 1. * .8
            width_multiplier = .75 * .8

        elif layout == 'slide_50%':
            height_multiplier = 1.
            width_multiplier = .5

        elif layout == 'slide_25%':
            height_multiplier = .5
            width_multiplier = .5

        self.plot_height = int(self.plot_height * height_multiplier)
        self.plot_width = int(self.plot_width * width_multiplier)

    def set_color_palette(self, palette_type, palette=None,
                          accent_values=None):
        """
        Args:
            palette_type:
                - 'categorical': Use when the color dimension
                    has no meaningful order.
                - 'sequential': Use when the color dimension
                    has a sequential order.
                - 'diverging'
                - 'accent': Use to assign color to specific
                    values in the color dimension.
            palette (color palette name, ColorPalette object, or list of colors)
                See chartify.color_palettes.show() for palette & color names.
                Default: 'Spotify Palette'
            accent_values (list or dict): List of values that should be
            accented or dictionary of 'value': 'color' pairs.
                Only applies to 'accent' palette type.

        """
        self.color_palette = BasePalette._get_palette_class(
            self._chart,
            palette_type=palette_type,
            palette=palette,
            accent_values=accent_values)

        return self._chart

    def _apply_bokeh_settings(self, attributes):
        for key, value in attributes.items():
            self._apply_bokeh_setting(key, value)

    def _apply_bokeh_setting(self, attribute, value, base_obj=None):
        """Recursively apply the settings value to the given settings attribute.

        Recursion is necessary because some bokeh objects may
        have multiple child objects.
        E.g. figures can have more than one x-axis.
        """
        # If not a bokeh attribute then we don't need to apply anything.
        if 'figure' not in attribute and base_obj is None:
            return

        split_attribute = attribute.split('.')
        if base_obj is None:
            base_obj = self._chart
        if len(split_attribute) == 1:
            setattr(base_obj, attribute, value)
        else:
            for i, attr in enumerate(split_attribute):
                if i < len(split_attribute) - 1:
                    base_obj = getattr(base_obj, attr)
                if isinstance(base_obj, (list, )):
                    for obj in base_obj:
                        self._apply_bokeh_setting(
                            '.'.join(split_attribute[i + 1:]),
                            value,
                            base_obj=obj)
                    break
            else:
                setattr(base_obj, attr, value)

    def _apply_settings(self, key):
        """Apply the specified bokeh settings"""
        setting_values = self.settings[key]
        self._apply_bokeh_settings(setting_values)

    def _get_settings(self, key):
        """Return the values of the given settings key"""
        setting_values = self.settings[key]
        return setting_values

    def _settings_to_yaml(self, filename):
        """Write the chart settings dict to a yaml file"""
        with open(filename, 'w') as outfile:
            yaml.dump(self.settings, outfile, default_flow_style=False)

    def _settings_from_yaml(self, filename, apply_chart_settings=True):
        """Load the chart settings dict from a yaml file"""
        yaml_settings = yaml.safe_load(open(filename))

        self.settings.update(yaml_settings)
        # Apply the settings that have been loaded.
        if apply_chart_settings:
            self._apply_settings('chart')
