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

COLOR_PALETTES_CONFIG = '''\
- - - '#5ff550'
    - '#fae62d'
    - '#f037a5'
  - categorical
  - Foo Bar
- - - '#ffc864'
    - '#ffcdd2'
    - '#eb1e32'
  - categorical
  - Baz Quux
'''

EXPECTED_COLOR_PALETTES = {
    'foo bar': ['#5ff550', '#fae62d', '#f037a5'],
    'baz quux': ['#ffc864', '#ffcdd2', '#eb1e32'],
}


def test_color_palettes_config(monkeypatch, tmpdir):
    f = tmpdir.join('color_palettes_config.yaml')
    f.write(COLOR_PALETTES_CONFIG)

    # XXX (dano): CHARTIFY_CONFIG_DIR must end with /
    monkeypatch.setenv('CHARTIFY_CONFIG_DIR', os.path.join(str(tmpdir), ''))

    # reload modules to reload configuration
    import chartify._core.options
    import chartify._core.colors
    importlib.reload(chartify._core.options)
    importlib.reload(chartify._core.colors)

    # Check that the expected palettes are loaded
    color_palettes = chartify._core.colors.color_palettes
    for name, palette in EXPECTED_COLOR_PALETTES.items():
        assert color_palettes[name].to_hex_list() == palette
