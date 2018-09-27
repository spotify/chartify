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
import chartify


class TestColor:
    def test_color(self):
        color = chartify._core.colors.Color('red')
        assert (color.hex == '#f00')


class TestColorPalettes:
    def test_getitem(self):
        palette = chartify.color_palettes['Category20']
        assert (isinstance(palette, chartify._core.colors.ColorPalette))
        assert (palette.name == 'Category20')

    def test_create_palette(self):
        chartify.color_palettes.create_palette(['white', 'black', '#fff000'],
                                               'sequential',
                                               'New')
        new_palette = chartify.color_palettes['New']
        assert new_palette.to_hex_list() == ['#ffffff', '#000000', '#fff000']
