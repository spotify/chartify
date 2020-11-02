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

COLORS_CONFIG = '''\
? !!python/tuple
- 0
- 100
- 80
: Foo
? !!python/tuple
- 25
- 20
- 20
: Bar
? !!python/tuple
- 25
- 230
- 140
: Baz
'''

EXPECTED_COLORS = {
    'style.color_palette_categorical': 'My Palette',
    'style.color_palette_sequential': 'Midnight Orange Sequential',
    'style.color_palette_diverging': 'Midnight Orange Diverging',
    'style.color_palette_accent': 'My Palette',
    'style.color_palette_accent_default_color': 'light grey',
}


def test_colors_config(monkeypatch, tmpdir):
    f = tmpdir.join('colors_config.yaml')
    f.write(COLORS_CONFIG)

    # XXX (dano): CHARTIFY_CONFIG_DIR must end with /
    monkeypatch.setenv('CHARTIFY_CONFIG_DIR', os.path.join(str(tmpdir), ''))

    # reload modules to reload configuration
    import chartify._core.options
    import chartify._core.colors
    import chartify._core.style
    importlib.reload(chartify._core.options)
    importlib.reload(chartify._core.colors)

    import chartify._core.colour as colour
    assert colour.COLOR_NAME_TO_RGB['foo'] == (0, 100, 80)
    assert colour.COLOR_NAME_TO_RGB['bar'] == (25, 20, 20)
    assert colour.COLOR_NAME_TO_RGB['baz'] == (25, 230, 140)
