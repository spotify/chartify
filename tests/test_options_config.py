# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020 Spotify AB
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

import importlib
import os

OPTIONS_CONFIG = '''\
!!python/object/apply:collections.OrderedDict
- - - style.color_palette_categorical
    - !!python/object:chartify._core.options.OptionValue
      value: My Palette
  - - style.color_palette_sequential
    - !!python/object:chartify._core.options.OptionValue
      value: Midnight Orange Sequential
  - - style.color_palette_diverging
    - !!python/object:chartify._core.options.OptionValue
      value: Midnight Orange Diverging
  - - style.color_palette_accent
    - !!python/object:chartify._core.options.OptionValue
      value: My Palette
  - - style.color_palette_accent_default_color
    - !!python/object:chartify._core.options.OptionValue
      value: light grey
'''

EXPECTED_CONFIG = {
    'style.color_palette_categorical': 'My Palette',
    'style.color_palette_sequential': 'Midnight Orange Sequential',
    'style.color_palette_diverging': 'Midnight Orange Diverging',
    'style.color_palette_accent': 'My Palette',
    'style.color_palette_accent_default_color': 'light grey',
}


def test_options_config(monkeypatch, tmpdir):
    f = tmpdir.join('options_config.yaml')
    f.write(OPTIONS_CONFIG)

    # XXX (dano): CHARTIFY_CONFIG_DIR must end with /
    monkeypatch.setenv('CHARTIFY_CONFIG_DIR', os.path.join(str(tmpdir), ''))

    # reload modules to reload configuration
    import chartify._core.options
    options = importlib.reload(chartify._core.options)

    config = {key: options.options.get_option(key)
              for key in EXPECTED_CONFIG}
    assert config == EXPECTED_CONFIG
