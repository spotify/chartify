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
import pandas as pd


class TestBaseAxes:
    def test_vertical(self):
        ch = chartify.Chart()
        assert (ch.axes._vertical)
        ch = chartify.Chart(x_axis_type='categorical')
        assert (ch.axes._vertical)
        ch = chartify.Chart(y_axis_type='categorical')
        assert (not ch.axes._vertical)
        ch = chartify.Chart(y_axis_type='density')
        assert (ch.axes._vertical)
        ch = chartify.Chart(x_axis_type='density')
        assert (not ch.axes._vertical)
        ch = chartify.Chart(x_axis_type='datetime')
        assert (ch.axes._vertical)

    def test_numeric_set_xaxis_range(self):
        ch = chartify.Chart()
        start, end = 0, 10
        ch.axes.set_xaxis_range(start, end)
        assert (ch.figure.x_range.end == end)
        assert (ch.figure.x_range.start == start)

    def test_datetime_set_xaxis_range(self):
        ch = chartify.Chart(x_axis_type='datetime')
        ch.axes.set_xaxis_range(
            pd.to_datetime('2018-01-01'), pd.to_datetime('2018-02-01'))
        assert (ch.figure.x_range.end == 1517443200000)
        assert (ch.figure.x_range.start == 1514764800000)
