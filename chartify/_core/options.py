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
from collections import OrderedDict
import os
from pathlib import Path
import yaml


class ChartifyOptions:
    def __init__(self):

        try:
            options_path = os.environ['CHARTIFY_CONFIG_DIR']
        except KeyError:
            home_path = str(Path.home())
            options_path = home_path + '/.chartify/'
        self._options = OrderedDict({
            'style.color_palette_categorical':
            OptionValue('Category20'),
            'style.color_palette_sequential':
            OptionValue('Blues'),
            'style.color_palette_diverging':
            OptionValue('RdBu'),
            'style.color_palette_accent':
            OptionValue('Category20'),
            'style.color_palette_accent_default_color':
            OptionValue('grey'),
            'chart.blank_labels':
            OptionValue(False),
            'config.logos_path':
            OptionValue(options_path + 'logos/'),
            'config.options':
            OptionValue(options_path + 'options_config.yaml'),
            'config.style_settings':
            OptionValue(options_path + 'style_settings_config.yaml'),
            'config.colors':
            OptionValue(options_path + 'colors_config.yaml'),
            'config.color_palettes':
            OptionValue(options_path + 'color_palettes_config.yaml')
        })

        config_filename = self.get_option('config.options')
        try:
            self._from_yaml(config_filename)
        except FileNotFoundError:
            pass

    def get_option(self, option_name):
        """Return the value of the given option"""
        return self._options[option_name].value

    def set_option(self, option_name, option_value):
        """Set the default value of the specified option.

        Available options:
            'style.color_palette_categorical': (str)
                Color palette for categorical palette types.

            'style.color_palette_sequential': (str)
                Color palette for sequential palette types.

            'style.color_palette_diverging': (str)
                Color palette for diverging palette types.

            'style.color_palette_accent': (str)
                Color palette for assigning color to specific values.

            'style.color_palette_accent_default_color': (str)
                Default color of values in the 'color_column' that
                    are not accented.
                Default: 'light grey'

            'chart.blank_labels': boolean
                If False, chartify.Chart objects populate the default
                    chart labels with helper text.
                Default: False
        """
        self._options[option_name].value = option_value

    @staticmethod
    def _get_value(option_value):
        if isinstance(option_value, OptionValue):
            return option_value.value
        else:
            return option_value

    def _to_yaml(self, filename):
        """Write the options to a yaml file"""
        with open(filename, 'w') as outfile:
            yaml.dump(self._options, outfile, default_flow_style=False)

    def _from_yaml(self, filename):
        """Load options from a yaml file.

        Overwrites any options that are specified in the yaml file.
        """
        yaml_options = yaml.load(open(filename))
        self._options.update(yaml_options)


class OptionValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '%s' % self.value


options = ChartifyOptions()
