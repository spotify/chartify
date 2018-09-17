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
import numpy as np


class TestLegend:
    def test_set_legend_location(self):
        data = chartify.examples.example_data()
        ch = chartify.Chart(x_axis_type='datetime')
        ch.plot.scatter(
            data_frame=data,
            x_column='date',
            y_column='unit_price',
            size_column='quantity',
            color_column='fruit')
        ch.set_legend_location('top_right')
        assert (ch.figure.legend[0].location == 'top_right')
        assert (ch.figure.legend[0].orientation == 'horizontal')
        ch.set_legend_location('top_left', 'vertical')
        assert (ch.figure.legend[0].location == 'top_left')
        assert (ch.figure.legend[0].orientation == 'vertical')
        ch.set_legend_location('outside_bottom')
        ch = chartify.Chart(x_axis_type='datetime')
        ch.plot.scatter(
            data_frame=data,
            x_column='date',
            y_column='unit_price',
            size_column='quantity',
            color_column='fruit')
        ch.set_legend_location(None)
        assert (ch.figure.legend[0].visible is False)


class TestChart:
    def test_data(self):
        data = chartify.examples.example_data()
        data = data.sort_values(['date', 'fruit'])
        color_order = data['fruit'].unique()
        ch = chartify.Chart(x_axis_type='datetime')
        ch.plot.scatter(
            data_frame=data,
            x_column='date',
            y_column='unit_price',
            size_column='quantity',
            color_column='fruit',
            color_order=color_order)
        assert (np.array_equal(
            list(filter(lambda x: x['fruit'][0] == color_order[0],
                        ch.data))[0]['unit_price'],
            data[data['fruit'] == color_order[0]]['unit_price'].values))
