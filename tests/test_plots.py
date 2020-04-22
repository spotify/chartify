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
"""Tests for `chartify` package plotting functions."""

import pytest
import chartify
import pandas as pd
import numpy as np
import bokeh


def chart_data(chart_object, series_name):
    """Retrieve data from chart object based on series name.

    Note: if there's only one series the name is None.

    Returns:
        Dictionary populated with data from the chart.
    """
    cannonical_series_name = (
        chart_object.plot._cannonical_series_name(series_name))
    return chart_object.figure.select(cannonical_series_name)[0].data


def chart_color_mapper(chart_object):
    return chart_object.figure.select(
        bokeh.models.mappers.CategoricalColorMapper)[0]


class TestHeatmap:
    def setup(self):
        self.data = pd.DataFrame({
            'category1': ['a', 'a', 'b', 'b'],
            'category2': [1, 2, 1, 2],
            'values': [1., 2., 3., 4.]
        })

    def test_heatmap(self):
        """Area plot tests"""
        ch = chartify.Chart(
            x_axis_type='categorical', y_axis_type='categorical')
        ch.plot.heatmap(
            self.data,
            x_column='category1',
            y_column='category2',
            color_column='values')
        assert (np.array_equal(
            chart_data(ch, '')['category1'], ['a', 'a', 'b', 'b']))
        assert (np.array_equal(
            chart_data(ch, '')['category2'], ['1', '2', '1', '2']))
        assert (np.array_equal(chart_data(ch, '')['values'], [1., 2., 3., 4.]))


class TestLine:
    def setup(self):
        self.data = pd.DataFrame({
            'category1': ['a', 'b', 'a', 'b', 'a', 'b'],
            'number1': [1, 1, 2, 2, 3, 3],
            'number2': [5, 4, 10, -3, 0, -10],
            'datetimes': [
                '2017-01-01', '2017-01-01', '2017-01-02', '2017-01-02',
                '2017-01-03', '2017-01-03'
            ],
        })

    def test_single_numeric_line(self):
        """Single line test"""
        single_line = self.data[self.data['category1'] == 'a']
        ch = chartify.Chart()
        ch.plot.line(single_line, x_column='number1', y_column='number2')
        assert (np.array_equal(chart_data(ch, '')['number1'], [1., 2., 3.]))
        assert (np.array_equal(chart_data(ch, '')['number2'], [5, 10, 0]))

    def test_multi_numeric_line(self):
        """Single line test"""
        ch = chartify.Chart()
        ch.plot.line(
            self.data,
            x_column='number1',
            y_column='number2',
            color_column='category1')
        assert (np.array_equal(chart_data(ch, 'a')['number1'], [1., 2., 3.]))
        assert (np.array_equal(chart_data(ch, 'a')['number2'], [5, 10, 0]))
        assert (np.array_equal(chart_data(ch, 'b')['number1'], [1., 2., 3.]))
        assert (np.array_equal(chart_data(ch, 'b')['number2'], [4, -3, -10]))

    def test_single_datetime_line(self):
        """Single line test"""
        data = pd.DataFrame({
            'number': [1, 10, -10, 0],
            'datetimes':
            ['2017-01-01', '2017-01-02', '2017-01-03', '2017-01-04'],
        })
        ch = chartify.Chart(x_axis_type='datetime')
        ch.plot.line(data, x_column='datetimes', y_column='number')
        assert (np.array_equal(
            chart_data(ch, '')['datetimes'],
            pd.date_range('2017-01-01', '2017-01-04')))
        assert (np.array_equal(chart_data(ch, '')['number'], [1, 10, -10, 0]))


class TestScatter:
    def setup(self):
        self.data = pd.DataFrame({
            'category1': ['a', 'b', 'a', 'b', 'a', 'b'],
            'number1': [1, 1, 2, 2, 3, 3],
            'number2': [5, 4, 10, -3, 0, -10],
            'datetimes': [
                '2017-01-01', '2017-01-01', '2017-01-02', '2017-01-02',
                '2017-01-03', '2017-01-03'
            ],
        })

    def test_single_numeric_scatter(self):
        """Single line test"""
        single_scatter = self.data[self.data['category1'] == 'a']
        ch = chartify.Chart()
        ch.plot.line(single_scatter, x_column='number1', y_column='number2')
        assert (np.array_equal(chart_data(ch, '')['number1'], [1., 2., 3.]))
        assert (np.array_equal(chart_data(ch, '')['number2'], [5, 10, 0]))

    def test_multi_numeric_scatter(self):
        """Single line test"""
        ch = chartify.Chart()
        ch.plot.scatter(
            self.data,
            x_column='number1',
            y_column='number2',
            color_column='category1')
        assert (np.array_equal(chart_data(ch, 'a')['number1'], [1., 2., 3.]))
        assert (np.array_equal(chart_data(ch, 'a')['number2'], [5, 10, 0]))
        assert (np.array_equal(chart_data(ch, 'b')['number1'], [1., 2., 3.]))
        assert (np.array_equal(chart_data(ch, 'b')['number2'], [4, -3, -10]))

    def test_single_datetime_scatter(self):
        """Single line test"""
        data = pd.DataFrame({
            'number': [1, 10, -10, 0],
            'datetimes':
            ['2017-01-01', '2017-01-02', '2017-01-03', '2017-01-04'],
        })
        ch = chartify.Chart(x_axis_type='datetime')
        ch.plot.scatter(data, x_column='datetimes', y_column='number')
        assert (np.array_equal(
            chart_data(ch, '')['datetimes'],
            pd.date_range('2017-01-01', '2017-01-04')))
        assert (np.array_equal(chart_data(ch, '')['number'], [1, 10, -10, 0]))


class TestText:
    def setup(self):
        self.data = pd.DataFrame({
            'text': ['a', 'b', 'a', 'b', 'a', 'b'],
            'number1': [1, 1, 2, 2, 3, 3],
            'number2': [5, 4, 10, -3, 0, -10],
            'datetimes': [
                '2017-01-01', '2017-01-01', '2017-01-02', '2017-01-02',
                '2017-01-03', '2017-01-03'
            ],
        })

    def test_single_numeric_text(self):
        """Single line test"""
        single_text = self.data[self.data['text'] == 'a']
        ch = chartify.Chart()
        ch.plot.text(
            single_text,
            x_column='number1',
            y_column='number2',
            text_column='text')
        assert (np.array_equal(chart_data(ch, '')['number1'], [1., 2., 3.]))
        assert (np.array_equal(chart_data(ch, '')['number2'], [5, 10, 0]))
        assert (np.array_equal(chart_data(ch, '')['text'], ['a', 'a', 'a']))

    def test_multi_numeric_text(self):
        """Single line test"""
        ch = chartify.Chart()
        ch.plot.text(
            self.data,
            x_column='number1',
            y_column='number2',
            text_column='text',
            color_column='text')
        assert (np.array_equal(chart_data(ch, 'a')['number1'], [1., 2., 3.]))
        assert (np.array_equal(chart_data(ch, 'a')['number2'], [5, 10, 0]))
        assert (np.array_equal(chart_data(ch, 'a')['text'], ['a', 'a', 'a']))
        assert (np.array_equal(chart_data(ch, 'b')['number1'], [1., 2., 3.]))
        assert (np.array_equal(chart_data(ch, 'b')['number2'], [4, -3, -10]))
        assert (np.array_equal(chart_data(ch, 'b')['text'], ['b', 'b', 'b']))

    def test_single_datetime_text(self):
        """Single line test"""
        data = pd.DataFrame({
            'number': [1, 10, -10, 0],
            'datetimes':
            ['2017-01-01', '2017-01-02', '2017-01-03', '2017-01-04'],
            'text': ['a', 'b', 'a', 'b'],
        })
        ch = chartify.Chart(x_axis_type='datetime')
        ch.plot.text(
            data, x_column='datetimes', y_column='number', text_column='text')
        assert (np.array_equal(
            chart_data(ch, '')['datetimes'],
            pd.date_range('2017-01-01', '2017-01-04')))
        assert (np.array_equal(chart_data(ch, '')['number'], [1, 10, -10, 0]))
        assert (np.array_equal(
            chart_data(ch, '')['text'], ['a', 'b', 'a', 'b']))


class CategoricalTextTest:
    def test_float_labels(self):
        label_test = pd.DataFrame(
            {'value': [.20, .40, .05, .6, .2, .8],
             'bucket': [1, 2, 3, 1, 2, 3],
             'platform': ['android', 'android', 'android', 'ios', 'ios', 'ios'],
             'value2': [1.0, 2.0, 3, 6., 8., 10.]})
        ch = chartify.Chart(x_axis_type='categorical')
        ch.plot.text(label_test, ['bucket', 'platform'], 'value', 'value')
        assert (np.array_equal(
            ch.data[0]['text_column'].values,
            ['0.8', '0.05', '0.6', '0.2', '0.4', '0.2']))


class TestAreaPlot:
    """Area plot tests.

    - Single series zero-baseline
    - Multi series zero-baseline unstacked
    - Multi series zero-baseline stacked
    - Single series interval
    - Multi series interval
    """

    def setup(self):
        self.data = pd.DataFrame({
            'category': ['a', 'a', 'b', 'b'],
            'upper': [20, 30, 2, 3],
            'lower': [10, 20, 1, 2],
            'x': [1, 2, 1, 2]
        })

        self.data_missing = pd.DataFrame({
            'category': ['a', 'a', 'b', 'b', 'a', 'c'],
            'upper': [20, 30, 2, 3, 40, 4],
            'lower': [10, 20, 1, 2, 25, 6],
            'x': [1, 2, 1, 2, 3, 3]
        })

    def test_single_series_zero_baseline(self):
        """Area plot tests"""
        test_data = self.data.loc[lambda x: x['category'] == 'a']
        ch = chartify.Chart()
        ch.plot.area(test_data, 'x', 'upper')
        assert (np.array_equal(chart_data(ch, None)['x'], [1, 2, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, None)['upper'], [20., 30., 0., 0.]))

    def test_multi_series_zero_baseline_unstacked(self):
        """Area plot tests"""
        test_data = self.data
        ch = chartify.Chart()
        ch.plot.area(test_data, 'x', 'upper', color_column='category')
        assert (np.array_equal(chart_data(ch, 'a')['x'], [1, 2, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, 'a')['upper'], [20., 30., 0., 0.]))

        assert (np.array_equal(chart_data(ch, 'b')['x'], [1, 2, 2, 1]))
        assert (np.array_equal(chart_data(ch, 'b')['upper'], [2., 3., 0., 0.]))

    def test_multi_series_zero_baseline_stacked(self):
        """Area plot tests"""
        test_data = self.data
        ch = chartify.Chart()
        ch.plot.area(
            test_data, 'x', 'upper', color_column='category', stacked=True)
        assert (np.array_equal(chart_data(ch, 'a')['x'], [1, 2, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, 'a')['upper'], [20., 30., 0., 0.]))

        assert (np.array_equal(chart_data(ch, 'b')['x'], [1, 2, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, 'b')['upper'], [22., 33., 30., 20.]))

    def test_single_series_interval(self):
        """Area plot tests"""
        test_data = self.data.loc[lambda x: x['category'] == 'a']
        ch = chartify.Chart()
        ch.plot.area(test_data, 'x', y_column='upper', second_y_column='lower')
        assert (np.array_equal(chart_data(ch, None)['x'], [1, 2, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, None)['upper'], [20., 30., 20., 10.]))

    def test_multi_series_interval(self):
        """Area plot tests"""
        test_data = self.data
        ch = chartify.Chart()
        ch.plot.area(
            test_data,
            'x',
            y_column='upper',
            second_y_column='lower',
            color_column='category')
        assert (np.array_equal(chart_data(ch, 'a')['x'], [1, 2, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, 'a')['upper'], [20., 30., 20., 10.]))

        assert (np.array_equal(chart_data(ch, 'b')['x'], [1, 2, 2, 1]))
        assert (np.array_equal(chart_data(ch, 'b')['upper'], [2, 3, 2, 1]))

    def test_multi_series_zero_baseline_unstacked_missing(self):
        """Area plot tests"""
        test_data = self.data_missing
        ch = chartify.Chart()
        ch.plot.area(test_data, 'x', 'upper', color_column='category')
        assert (np.array_equal(chart_data(ch, 'a')['x'], [1, 2, 3, 3, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, 'a')['upper'], [20., 30., 40.,  0.,  0.,  0.]))

        assert (np.array_equal(chart_data(ch, 'c')['x'], [1, 2, 3, 3, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, 'c')['upper'], [0., 0., 4., 0., 0., 0.]))

    def test_multi_series_zero_baseline_stacked_missing(self):
        """Area plot tests"""
        test_data = self.data_missing
        ch = chartify.Chart()
        ch.plot.area(
            test_data, 'x', 'upper', color_column='category', stacked=True)
        assert (np.array_equal(chart_data(ch, 'a')['x'], [1, 2, 3, 3, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, 'a')['upper'], [20., 30., 40.,  0.,  0.,  0.]))

        assert (np.array_equal(chart_data(ch, 'c')['x'], [1, 2, 3, 3, 2, 1]))
        assert (np.array_equal(
            chart_data(ch, 'c')['upper'], [22., 33., 44., 40., 33., 22.]))


class TestBarLollipopParallel:
    """Tests for bar, lollipop, and parallel plots"""

    def setup(self):
        self.data = pd.DataFrame({
            'category1': ['a', 'b', 'a', 'b', 'a'],
            'category2': [1, 1, 2, 2, 3],
            'color': ['c', 'd', 'e', 'f', 'g'],
            'number': [5, 4, 10, -3, 0],
        })
        self.plot_methods = ['bar', 'lollipop', 'parallel']

    def test_vertical(self):
        """Vertical test"""
        sliced_data = self.data[self.data['category1'] == 'a']
        for method_name in self.plot_methods:
            ch = chartify.Chart(x_axis_type='categorical')
            plot_method = getattr(ch.plot, method_name)
            plot_method(
                sliced_data,
                categorical_columns='category2',
                numeric_column='number')
            assert (np.array_equal(
                chart_data(ch, '')['factors'], ['2', '1', '3']))
            assert (np.array_equal(chart_data(ch, '')['number'], [10, 5, 0]))

    def test_horizontal(self):
        """Horizontal test"""
        sliced_data = self.data[self.data['category1'] == 'a']
        for method_name in self.plot_methods:
            ch = chartify.Chart(y_axis_type='categorical')
            plot_method = getattr(ch.plot, method_name)
            plot_method(
                sliced_data,
                categorical_columns='category2',
                numeric_column='number')
            assert (np.array_equal(
                chart_data(ch, '')['factors'], ['2', '1', '3']))
            assert (np.array_equal(chart_data(ch, '')['number'], [10, 5, 0]))

    def test_grouping_error(self):
        for method_name in self.plot_methods:
            ch = chartify.Chart(x_axis_type='categorical')
            plot_method = getattr(ch.plot, method_name)
            with pytest.raises(ValueError):
                plot_method(
                    self.data,
                    categorical_columns='category2',
                    numeric_column='number')

    def test_grouped_categorical(self):
        """Grouped test"""
        for method_name in self.plot_methods:
            ch = chartify.Chart(x_axis_type='categorical')
            plot_method = getattr(ch.plot, method_name)

            plot_method(
                self.data,
                categorical_columns=['category1', 'category2'],
                numeric_column='number')
            assert (np.array_equal(
                chart_data(ch, '')['number'], [10, 5, 0, 4, -3]))
            multi_index = pd.MultiIndex(
                levels=[['a', 'b'], ['1', '2', '3']],
                codes=[[0, 0, 0, 1, 1], [1, 0, 2, 0, 1]],
                names=['category1', 'category2'])
            assert (np.array_equal(chart_data(ch, '')['factors'], multi_index))

            ch = chartify.Chart(x_axis_type='categorical')
            plot_method = getattr(ch.plot, method_name)
            plot_method(
                self.data,
                categorical_columns=['category2', 'category1'],
                numeric_column='number')
            assert (np.array_equal(
                chart_data(ch, '')['number'], [5, 4, 10, -3, 0]))
            multi_index = pd.MultiIndex(
                levels=[['1', '2', '3'], ['a', 'b']],
                codes=[[0, 0, 1, 1, 2], [0, 1, 0, 1, 0]],
                names=['category2', 'category1'])
            assert (np.array_equal(chart_data(ch, '')['factors'], multi_index))

    def test_bar_color_column(self):
        sliced_data = self.data[self.data['category1'] == 'a']
        ch = chartify.Chart(x_axis_type='categorical')
        ch.plot.bar(
            sliced_data,
            categorical_columns='category2',
            numeric_column='number',
            color_column='category2')
        assert (np.array_equal(
            chart_color_mapper(ch).factors, ['1', '2', '3']))
        assert (np.array_equal(
            chart_color_mapper(ch).palette, ['#1f77b4', '#ff7f0e', '#2ca02c']))

    def test_lollipop_color_column(self):
        sliced_data = self.data[self.data['category1'] == 'a']
        ch = chartify.Chart(x_axis_type='categorical')
        ch.plot.lollipop(
            sliced_data,
            categorical_columns='category2',
            numeric_column='number',
            color_column='category2')
        assert (np.array_equal(
            chart_color_mapper(ch).factors, ['1', '2', '3']))
        assert (np.array_equal(
            chart_color_mapper(ch).palette, ['#1f77b4', '#ff7f0e', '#2ca02c']))

    def test_bar_parallel_color_column(self):
        ch = chartify.Chart(x_axis_type='categorical')
        ch.plot.parallel(
            self.data,
            categorical_columns='category1',
            numeric_column='number',
            color_column='category2')
        assert (np.array_equal(chart_data(ch, '')['factors'], ['a', 'b']))
        assert (np.array_equal(chart_data(ch, '')['1'], [5, 4]))
        assert (np.array_equal(chart_data(ch, '')['2'], [10, -3]))
        assert (np.array_equal(chart_data(ch, '')['3'], [0, 0]))

    def test_bar_color(self):
        ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
        ch.plot.bar(
            data_frame=self.data,
            categorical_columns=['category1', 'category2'],
            numeric_column='number',
            color_column='color')
        assert np.array_equal(
            ch.data[0]['color_column'], ['e', 'c', 'g', 'd', 'f'])


class TestBarNumericSort:
    def setup(self):
        self.data = pd.DataFrame({
            'category': ['a', 'a', 'b', 'b', 'a', 'c'],
            'upper': [20, 30, 2, 3, 40, 4],
            'lower': [10, 20, 1, 2, 25, 6],
            'x': [1, 2, 1, 2, 11, 10]
        })

    def test_bar_sort(self):
        ch = chartify.Chart(x_axis_type='categorical')
        ch.plot.bar(self.data,
                    ['x', 'category'],
                    'upper',
                    categorical_order_by='labels',
                    categorical_order_ascending=True)
        assert (np.array_equal(
            chart_data(ch, '')['upper'], [20,  2, 30,  3,  4, 40]))
        assert (np.array_equal(
            chart_data(ch, '')['index'], [0, 1, 2, 3, 4, 5]))


class TestBarStacked:
    """Tests for stacked bar plots"""

    def setup(self):
        self.data = pd.DataFrame({
            'category1': ['a', 'b', 'a', 'b', 'a'],
            'category2': [1, 1, 2, 2, 3],
            'number': [5, 4, 10, -3, 0],
        })


class TestAxisFormatPrecision:

    def setup(self):
        self.tests = {
            (0, 0): "0,0.[0]",
            (0, 0.004): "0,0.[0000]",
            (0, 0.04): "0,0.[000]",
            (0, 0.4): "0,0.[00]",
            (0, 1.0): "0,0.[0]",
            (0, 3.0): "0,0.[0]",
            (0, 6.0): "0,0.[0]",
            (0, 60): "0,0.[00]",
            (0, 600): "0,0.[000]",
            (-0.4, 0.4): "0,0.[00]",
            (-4.0, 4.0): "0,0.[0]",
            (-0.2, 0): "0,0.[00]",
            (-3.2, 0): "0,0.[0]",
            (-100, 0): "0,0.[000]",
            (0, 0.32): "0,0.[00]",
            (0, 10000): "0,0.[00000]",
            (0, 0.0032): "0,0.[0000]",
        }

    def test_axis_format_precision(self):
        ch = chartify.Chart()
        for parameters, value in self.tests.items():
            assert (ch.plot._axis_format_precision(parameters[0],
                                                   parameters[1]) == value)


class TestHexbin:
    def setup(self):
        n_samples = 2000
        np.random.seed(10)
        x_values = 2 + .5 * np.random.standard_normal(n_samples)
        y_values = 1 + .5 * np.random.standard_normal(n_samples)
        data = pd.DataFrame({'x': x_values, 'y': y_values})
        self.data = data

    def test_hexbin(self):
        ch = chartify.Chart(
            x_axis_type='density',
            y_axis_type='density',
            layout='slide_100%',
            )
        ch.plot.hexbin(self.data, 'x', 'y', .5, orientation='flattop')
        assert (ch.data[0]['r'].tolist() == [
            -2, -1, -2, -1, -3, -2, -1, -3, -2, -4, -3
        ])
        assert (ch.data[0]['q'].tolist() == [
            1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5
        ])
        assert (ch.data[0]['c'].tolist() == [
            13, 75, 485, 232, 126, 851, 27, 123, 64, 1, 3
        ])

        ch = chartify.Chart(
            x_axis_type='density',
            y_axis_type='density',
            layout='slide_50%',
            )
        ch.plot.hexbin(self.data, 'x', 'y', 1, orientation='flattop')
        assert (ch.data[0]['r'].tolist() == [
            -1, 0, -2, -1, 0, -3, -2, -1
        ])
        assert (ch.data[0]['q'].tolist() == [
            0, 0, 1, 1, 1, 2, 2, 2
        ])
        assert (ch.data[0]['c'].tolist() == [
            11, 3, 180, 1181, 32, 2, 391, 200
        ])


class TestHistogram:
    def setup(self):
        self.data = pd.DataFrame({
            'values': [0, 4, 8, 22, 2, 2, 10],
            'dimension': ['a', 'a', 'a', 'a', 'b', 'b', 'b']
        })

    def test_histogram(self):
        """No groupings."""
        ch = chartify.Chart(y_axis_type='density')
        ch.plot.histogram(self.data, 'values', bins=2, method='count')
        assert (np.array_equal(chart_data(ch, '')['values'], [6, 1]))
        assert (np.array_equal(chart_data(ch, '')['max_edge'], [11., 22.]))
        assert (np.array_equal(chart_data(ch, '')['min_edge'], [0., 11.]))

    def test_grouped_histogram(self):
        """Grouped histogram."""
        ch = chartify.Chart(y_axis_type='density')
        ch.plot.histogram(
            self.data,
            values_column='values',
            color_column='dimension',
            bins=2,
            method='count')
        assert (np.array_equal(chart_data(ch, 'a')['values'], [3, 1]))
        assert (np.array_equal(chart_data(ch, 'a')['max_edge'], [11., 22.]))
        assert (np.array_equal(chart_data(ch, 'a')['min_edge'], [0., 11.]))

        assert (np.array_equal(chart_data(ch, 'b')['values'], [2, 1]))
        assert (np.array_equal(chart_data(ch, 'b')['max_edge'], [6., 10.]))
        assert (np.array_equal(chart_data(ch, 'b')['min_edge'], [2., 6.]))


def test_categorical_axis_type_casting():
    """Categorical axis plotting breaks for non-str types.
    Test that type casting is performed correctly"""

    test_df = pd.DataFrame({
        'categorical_strings': ['a', 'a', 'c', 'd'],
        'categorical_integers': [1, 2, 3, 3],
        'categorical_floats': [1.1, 2.1, 3.3, 4.4],
        'numeric': [1, 2, 3, 4]
    })

    # Multi factor test
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.plot.bar(
        test_df,
        categorical_columns=['categorical_strings', 'categorical_integers'],
        numeric_column='numeric')

    # Single factor test
    ch = chartify.Chart(blank_labels=True, y_axis_type='categorical')
    ch.plot.bar(test_df, 'categorical_floats', 'numeric')

    # Stacked bar test
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.plot.bar_stacked(test_df, 'categorical_strings', 'numeric',
                        'categorical_floats')

    # Color test
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.plot.bar(
        test_df,
        categorical_columns=['categorical_strings', 'categorical_integers'],
        numeric_column='numeric',
        color_column='categorical_integers')

    # Test that original data frame dtypes are not overwritten.
    assert (test_df.dtypes['categorical_integers'] == 'int64')
    assert (test_df.dtypes['categorical_floats'] == 'float64')
