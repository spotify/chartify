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
"""Examples"""

from functools import wraps as _wraps
from inspect import getsource as _getsource
import numpy as np
import pandas as pd

from chartify import _core

import chartify

_OUTPUT_FORMAT = 'png'


def _clean_source(source):
    source = source.split('"""')[2].replace("\t", "")
    # Replace the output variable wth its value
    source = source.replace("_OUTPUT_FORMAT", "'{}'".format(_OUTPUT_FORMAT))
    return source


def _print_source(f):
    """Print code after the function docstring up until the first
    set of triple quotes"""

    @_wraps(f)
    def wrapper(*args, **kwargs):
        source = _getsource(f)
        print(_clean_source(source))
        return f(*args, **kwargs)

    return wrapper


@_print_source
def plot_line():
    """
    Line example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    # Sum price grouped by date
    price_by_date = (
        data.groupby('date')['total_price'].sum()
        .reset_index()  # Move 'date' from index to column
        )
    print(price_by_date.head())
    """Print break"""
    _line_example_1(price_by_date)
    price_by_date_and_country = _line_example_2_data(data)
    _line_example_2_chart(price_by_date_and_country)


@_print_source
def _line_example_1(price_by_date):
    """# Line with datetime x axis"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.set_title("Line charts")
    ch.set_subtitle("Plot two numeric values connected by an ordered line.")
    ch.plot.line(
        # Data must be sorted by x column
        data_frame=price_by_date.sort_values('date'),
        x_column='date',
        y_column='total_price')
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _line_example_2_data(data):
    """# Line grouped by color"""
    price_by_date_and_country = (
        data.groupby(['date', 'fruit'])['total_price'].sum()
        .reset_index()  # Move 'date' and 'country' from index to column
        )
    print(price_by_date_and_country.head())
    """Print break"""
    return price_by_date_and_country


@_print_source
def _line_example_2_chart(price_by_date_and_country):
    """# Line grouped by color"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.set_title("Line charts - Grouped by color")
    ch.plot.line(
        # Data must be sorted by x column
        data_frame=price_by_date_and_country.sort_values('date'),
        x_column='date',
        y_column='total_price',
        color_column='fruit')
    ch.show(_OUTPUT_FORMAT)


plot_line.__doc__ = _core.plot.PlotNumericXY.line.__doc__


@_print_source
def chart_blank():
    """
    """
    import chartify

    # Blank charts tell you how to fill in the labels
    ch = chartify.Chart()
    ch.show(_OUTPUT_FORMAT)

@_print_source
def plot_scatter():
    """Scatter example
    """
    import numpy as np
    import pandas as pd
    import chartify

    # Generate example data
    data = chartify.examples.example_data()
    """Print break"""
    _scatter_example_1(data)
    _scatter_example_2(data)
    _scatter_example_3(data)


@_print_source
def _scatter_example_1(data):
    """# Basic Scatter"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.plot.scatter(
        data_frame=data,
        x_column='date',
        y_column='unit_price')
    ch.set_title("Scatterplot")
    ch.set_subtitle("Plot two numeric values.")
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _scatter_example_2(data):
    """# Scatter with size"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.plot.scatter(
        data_frame=data,
        x_column='date',
        y_column='unit_price',
        size_column='quantity')
    ch.set_title("Scatterplot")
    ch.set_subtitle(
        "Optional 'size_column' argument for changing scatter size.")
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _scatter_example_3(data):
    """# Scatter with size and color"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.plot.scatter(
        data_frame=data,
        x_column='date',
        y_column='unit_price',
        size_column='quantity',
        color_column='fruit')
    ch.set_title("Scatterplot")
    ch.set_subtitle("Optional 'color_column' argument for grouping by color.")
    ch.show(_OUTPUT_FORMAT)


plot_scatter.__doc__ = _core.plot.PlotNumericXY.scatter.__doc__


@_print_source
def plot_scatter_categorical():
    """Scatter example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()
    high_low = (data.groupby(['fruit'])['unit_price']
                .agg(['max', 'min'])
                .reset_index())
    print(high_low.head())
    """Print break"""
    _scatter_categorical_example(high_low)


@_print_source
def _scatter_categorical_example(high_low):
    """Scatter categorical example"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True,
                        y_axis_type='categorical')
    ch.set_title("Scatter plot with categorical y-axis")
    ch.plot.scatter(
        data_frame=high_low,
        categorical_columns='fruit',
        numeric_column='max',
        marker='circle',
    )
    ch.plot.scatter(
        data_frame=high_low,
        categorical_columns='fruit',
        numeric_column='min',
        marker='square',
    )
    ch.show(_OUTPUT_FORMAT)

plot_scatter_categorical.__doc__ = _core.plot.PlotMixedTypeXY.scatter.__doc__


@_print_source
def plot_text():
    """
    Text example
    """
    import chartify

    data = chartify.examples.example_data()

    # Manipulate the data
    price_and_quantity_by_country = (
        data.groupby('country')[['total_price', 'quantity']].sum()
        .reset_index())
    print(price_and_quantity_by_country.head())
    """Print break"""
    _text_example_1(price_and_quantity_by_country)


@_print_source
def _text_example_1(price_and_quantity_by_country):
    """Plot text with scatter"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True)
    ch.plot.scatter(
        data_frame=price_and_quantity_by_country,
        x_column='total_price',
        y_column='quantity',
        color_column='country')
    ch.style.color_palette.reset_palette_order()
    ch.plot.text(
        data_frame=price_and_quantity_by_country,
        x_column='total_price',
        y_column='quantity',
        text_column='country',
        color_column='country',
        x_offset=1,
        y_offset=-1,
        font_size='10pt')
    ch.set_title("Text")
    ch.set_subtitle("Labels for specific observations.")
    ch.show(_OUTPUT_FORMAT)


plot_text.__doc__ = _core.plot.PlotNumericXY.text.__doc__


@_print_source
def plot_area():
    """
    Area example
    """
    import pandas as pd
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    total_quantity_by_month_and_fruit = (data.groupby(
        [data['date'] + pd.offsets.MonthBegin(-1), 'fruit'])['quantity'].sum()
        .reset_index().rename(columns={'date': 'month'})
        .sort_values('month'))
    print(total_quantity_by_month_and_fruit.head())
    """Print break"""
    _area_example_1(total_quantity_by_month_and_fruit)
    _area_example_2(total_quantity_by_month_and_fruit)
    _plot_shaded_interval(data)


@_print_source
def plot_hexbin():
    """
    Hexbin example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    ch = chartify.Chart(blank_labels=True,
                        x_axis_type='density',
                        y_axis_type='density')
    ch.set_title("Hexbin")
    ch.plot.hexbin(data_frame=data,
                   x_values_column='unit_price',
                   y_values_column='quantity',
                   size=.2,
                   orientation='pointytop')
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _area_example_1(total_quantity_by_month_and_fruit):
    """# Stacked area"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.set_title("Stacked area")
    ch.set_subtitle("Represent changes in distribution.")
    ch.plot.area(
        data_frame=total_quantity_by_month_and_fruit,
        x_column='month',
        y_column='quantity',
        color_column='fruit',
        stacked=True)
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _area_example_2(total_quantity_by_month_and_fruit):
    """# Unstacked area chart"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.set_title("Unstacked area")
    ch.set_subtitle("Show overlapping values. Automatically adjusts opacity.")
    ch.plot.area(
        data_frame=total_quantity_by_month_and_fruit,
        x_column='month',
        y_column='quantity',
        color_column='fruit',
        stacked=False)
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _plot_shaded_interval(data):
    """
    Shaded interval example
    """

    # Sum price grouped by date
    price_by_date = (data.groupby(['date'])['total_price'].agg(
        ['mean', 'std', 'count'])
        .loc['2017-12-01':].assign(
            lower_ci=lambda x: x['mean'] - 1.96 * x['std'] / x['count']**.5,
            upper_ci=lambda x: x['mean'] + 1.96 * x['std'] / x['count']**.5)
        .reset_index())
    print(price_by_date.head())
    """Print break"""
    _shaded_interval_example_1(price_by_date)


@_print_source
def _shaded_interval_example_1(price_by_date):
    """# Line with datetime x axis"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.set_title("Area with second_y_column")
    ch.set_subtitle(
        "Use alone or combined with line graphs to represent confidence."
    )
    ch.plot.area(
        data_frame=price_by_date,
        x_column='date',
        y_column='lower_ci',
        second_y_column='upper_ci')
    # Reset to ensure same color of line & shaded interval
    ch.style.color_palette.reset_palette_order()
    ch.plot.line(
        data_frame=price_by_date,
        x_column='date',
        y_column='mean')
    ch.show(_OUTPUT_FORMAT)


plot_area.__doc__ = _core.plot.PlotNumericXY.area.__doc__


@_print_source
def plot_bar():
    """
    Bar example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    quantity_by_fruit = (data.groupby('fruit')['quantity'].sum().reset_index())

    print(quantity_by_fruit.head())
    """Print break"""
    _bar_example_1(quantity_by_fruit)
    _bar_example_2(quantity_by_fruit)
    _bar_example_3(quantity_by_fruit)
    _bar_example_4(quantity_by_fruit)


@_print_source
def _bar_example_1(quantity_by_fruit):
    """# Plot the data ordered by the numerical axis"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Vertical bar plot")
    ch.set_subtitle("Automatically sorts by value counts.")
    ch.plot.bar(
        data_frame=quantity_by_fruit,
        categorical_columns='fruit',
        numeric_column='quantity')
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _bar_example_2(quantity_by_fruit):
    """# Plot the data ordered by the categorical axis labels"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Vertical bar plot - Label sort")
    ch.set_subtitle("Set `categorical_order_by` to sort by labels")
    ch.plot.bar(
        data_frame=quantity_by_fruit,
        categorical_columns='fruit',
        numeric_column='quantity',
        categorical_order_by='labels',
        categorical_order_ascending=True)
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _bar_example_3(quantity_by_fruit):
    """# Plot the data with color grouping"""
    ch = chartify.Chart(blank_labels=True, y_axis_type='categorical')
    ch.set_title("Horizontal bar plot")
    ch.set_subtitle("Horizontal with color grouping")
    ch.plot.bar(
        data_frame=quantity_by_fruit,
        categorical_columns='fruit',
        numeric_column='quantity',
        color_column='fruit')
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _bar_example_4(quantity_by_fruit):
    """# Plot the data with labels"""
    ch = chartify.Chart(x_axis_type='categorical', blank_labels=True)
    ch.set_title("Vertical bar plot with labels")
    ch.set_subtitle("Hidden y-axis")
    ch.plot.bar(
        data_frame=quantity_by_fruit,
        categorical_columns='fruit',
        numeric_column='quantity',
        color_column='fruit')
    ch.style.color_palette.reset_palette_order()
    ch.plot.text(
        data_frame=quantity_by_fruit,
        categorical_columns='fruit',
        numeric_column='quantity',
        text_column='quantity',
        color_column='fruit')
    # Adjust the axis range to prevent clipping of the text labels.
    ch.axes.set_yaxis_range(0, 1200)
    ch.axes.hide_yaxis()
    ch.show(_OUTPUT_FORMAT)


plot_bar.__doc__ = _core.plot.PlotMixedTypeXY.bar.__doc__


@_print_source
def plot_interval():
    """
    Interval example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()
    """Print Break"""
    avg_price_with_interval = _interval_example_data(data)
    _interval_example(avg_price_with_interval)
    _interval_example2(avg_price_with_interval)


@_print_source
def _interval_example_data(data):
    """Docstring"""
    avg_price_with_interval = (data.groupby('fruit')['total_price'].agg(
        ['mean', 'std', 'count'])
        .assign(
            lower_ci=lambda x: x['mean'] - 1.96 * x['std'] / x['count']**.5,
            upper_ci=lambda x: x['mean'] + 1.96 * x['std'] / x['count']**.5)
        .reset_index())
    """Print break"""
    return avg_price_with_interval


@_print_source
def _interval_example(avg_price_with_interval):
    """# Plot the data ordered by the numerical axis"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Interval plots")
    ch.set_subtitle(
        "Represent variation. Optional `middle_column` to mark a middle point."
    )
    ch.plot.interval(
        data_frame=avg_price_with_interval,
        categorical_columns='fruit',
        lower_bound_column='lower_ci',
        upper_bound_column='upper_ci',
        middle_column='mean')
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _interval_example2(avg_price_with_interval):
    """# Plot the data ordered by the numerical axis"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Combined interval plot & bar plot")
    ch.plot.bar(
        data_frame=avg_price_with_interval,
        categorical_columns='fruit',
        numeric_column='mean')
    ch.plot.interval(
        data_frame=avg_price_with_interval,
        categorical_columns='fruit',
        lower_bound_column='lower_ci',
        upper_bound_column='upper_ci')
    ch.show(_OUTPUT_FORMAT)


plot_interval.__doc__ = _core.plot.PlotMixedTypeXY.interval.__doc__


@_print_source
def plot_bar_grouped():
    """
    Grouped bar example.

    ch.plot.bar() docstring:
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    quantity_by_fruit_and_country = (data.groupby(
        ['fruit', 'country'])['quantity'].sum().reset_index())
    print(quantity_by_fruit_and_country.head())
    """Print break"""
    _bar_grouped_example_1(quantity_by_fruit_and_country)
    _bar_grouped_example_2(quantity_by_fruit_and_country)
    _bar_grouped_example_3(quantity_by_fruit_and_country)
    _bar_grouped_example_4(quantity_by_fruit_and_country)


@_print_source
def _bar_grouped_example_1(quantity_by_fruit_and_country):
    """Docstring"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Grouped bar chart")
    ch.set_subtitle(
        "Pass a list to group by multiple factors. Color grouped by 'fruit'")
    ch.plot.bar(
        data_frame=quantity_by_fruit_and_country,
        categorical_columns=['fruit', 'country'],
        numeric_column='quantity',
        color_column='fruit')
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _bar_grouped_example_2(quantity_by_fruit_and_country):
    """Docstring"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Grouped bar chart - Color groupings")
    ch.set_subtitle(
        "Change color independent of the axis factors. Color grouped by 'country'"
    )
    ch.plot.bar(
        data_frame=quantity_by_fruit_and_country,
        categorical_columns=['fruit', 'country'],
        numeric_column='quantity',
        color_column='country')
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _bar_grouped_example_3(quantity_by_fruit_and_country):
    """Docstring"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Grouped bar chart - Group hierarchy order")
    ch.set_subtitle(
        "Change chage order of 'categorical_column' list to switch grouping hierarchy."
    )
    ch.plot.bar(
        data_frame=quantity_by_fruit_and_country,
        categorical_columns=['country', 'fruit'],
        numeric_column='quantity',
        color_column='country')
    ch.axes.set_xaxis_tick_orientation('vertical')
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _bar_grouped_example_4(quantity_by_fruit_and_country):
    """Docstring"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Grouped bar chart - Factor order")
    ch.set_subtitle("Change categorical order with 'categorical_order_by'.")
    ch.plot.bar(
        data_frame=quantity_by_fruit_and_country,
        categorical_columns=['country', 'fruit'],
        numeric_column='quantity',
        color_column='country',
        categorical_order_by='labels',
        categorical_order_ascending=True)
    ch.axes.set_xaxis_tick_orientation('vertical')
    ch.show(_OUTPUT_FORMAT)


plot_bar_grouped.__doc__ += _core.plot.PlotMixedTypeXY.bar.__doc__


@_print_source
def plot_bar_stacked():
    """
    Bar example
    """
    import numpy as np
    import pandas as pd
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    quantity_by_fruit_and_country = (data.groupby(
        ['fruit', 'country'])['quantity'].sum().reset_index())
    print(quantity_by_fruit_and_country.head())
    """Print Break"""
    _bar_stacked_example_1(quantity_by_fruit_and_country)
    _bar_stacked_example_2(quantity_by_fruit_and_country)
    country_order = _bar_stacked_example_3(quantity_by_fruit_and_country)
    _bar_stacked_example_4(quantity_by_fruit_and_country, country_order)


@_print_source
def _bar_stacked_example_1(quantity_by_fruit_and_country):
    """Docstring"""
    # Plot the data
    (chartify.Chart(blank_labels=True,
                    x_axis_type='categorical')
     .set_title("Stacked bar chart")
     .set_subtitle("Stack columns by a categorical factor.")
     .plot.bar_stacked(
         data_frame=quantity_by_fruit_and_country,
         categorical_columns=['fruit'],
         numeric_column='quantity',
         stack_column='country',
         normalize=False)
     .show(_OUTPUT_FORMAT))


@_print_source
def _bar_stacked_example_2(quantity_by_fruit_and_country):
    """Docstring"""
    (chartify.Chart(blank_labels=True, x_axis_type='categorical')
     .set_title("Grouped bar chart - Normalized")
     .set_subtitle("Set the 'normalize' parameter for 100% bars.")
     .plot.bar_stacked(
         data_frame=quantity_by_fruit_and_country,
         categorical_columns=['fruit'],
         numeric_column='quantity',
         stack_column='country',
         normalize=True)
     .show(_OUTPUT_FORMAT))


@_print_source
def _bar_stacked_example_3(quantity_by_fruit_and_country):
    """Docstring"""
    # Get the ordered list of quanity by country to order the stacks.
    country_order = (
        quantity_by_fruit_and_country.groupby('country')['quantity'].sum()
        .sort_values(ascending=False).index)
    (chartify.Chart(blank_labels=True, x_axis_type='categorical')
     .set_title("Grouped bar chart - Ordered stack")
     .set_subtitle("Change the order of the stack with `stack_order`.")
     .plot.bar_stacked(
         data_frame=quantity_by_fruit_and_country,
         categorical_columns=['fruit'],
         numeric_column='quantity',
         stack_column='country',
         normalize=True,
         stack_order=country_order)
     .show(_OUTPUT_FORMAT))
    """Print break"""
    return country_order


@_print_source
def _bar_stacked_example_4(quantity_by_fruit_and_country, country_order):
    """Docstring"""
    # Add a column for labels.
    # Note: Null labels will not be added to the chart.
    quantity_by_fruit_and_country['label'] = np.where(
        quantity_by_fruit_and_country['country'].isin(['US', 'CA']),
        quantity_by_fruit_and_country['quantity'],
        None)

    (chartify.Chart(blank_labels=True, x_axis_type='categorical')
     .set_title("Stacked bar with labels")
     .set_subtitle("")
     .plot.bar_stacked(
         data_frame=quantity_by_fruit_and_country,
         categorical_columns=['fruit'],
         numeric_column='quantity',
         stack_column='country',
         normalize=True,
         stack_order=country_order)
     .plot.text_stacked(
         data_frame=quantity_by_fruit_and_country,
         categorical_columns=['fruit'],
         numeric_column='quantity',
         stack_column='country',
         text_column='label',
         normalize=True,
         stack_order=country_order,
         # Set the text color otherwise it will take
         # The next color in the color palette.
         text_color='white'
         )
     .show(_OUTPUT_FORMAT))


plot_bar_stacked.__doc__ = _core.plot.PlotMixedTypeXY.bar_stacked.__doc__


@_print_source
def plot_lollipop():
    """
    Lollipop example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    quantity_by_fruit_and_country = (data.groupby(
        ['fruit', 'country'])['quantity'].sum().reset_index())
    print(quantity_by_fruit_and_country.head())
    """Print break"""
    _lollipop_example_1(quantity_by_fruit_and_country)


@_print_source
def _lollipop_example_1(quantity_by_fruit_and_country):
    """Docstring"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, y_axis_type='categorical')
    ch.set_title("Lollipop chart")
    ch.set_subtitle("Same options as bar plot")
    ch.plot.lollipop(
        data_frame=quantity_by_fruit_and_country,
        categorical_columns=['country', 'fruit'],
        numeric_column='quantity',
        color_column='country')
    ch.show(_OUTPUT_FORMAT)


plot_lollipop.__doc__ = _core.plot.PlotMixedTypeXY.lollipop.__doc__


@_print_source
def plot_parallel():
    """
    Parallel coordinate plot example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    total_quantity_by_fruit_and_country = (data.groupby(
        ['fruit', 'country'])['quantity'].sum().reset_index())
    print(total_quantity_by_fruit_and_country.head())
    """Print break"""
    _parallel_example_1(total_quantity_by_fruit_and_country)


@_print_source
def _parallel_example_1(total_quantity_by_fruit_and_country):
    """# Parallel with datetime x axis"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Parallel coordinate charts")
    ch.set_subtitle("")
    ch.plot.parallel(
        data_frame=total_quantity_by_fruit_and_country,
        categorical_columns='fruit',
        numeric_column='quantity',
        color_column='country')
    ch.show(_OUTPUT_FORMAT)


plot_parallel.__doc__ = _core.plot.PlotMixedTypeXY.parallel.__doc__


@_print_source
def plot_histogram():
    """
    Histogram example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    print(data.head())
    """Print break"""
    _histogram_example(data)
    _histogram_example2(data)


@_print_source
def _histogram_example(data):
    """# Histogram"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, y_axis_type='density')
    ch.set_title("Histogram")
    ch.set_subtitle("")
    ch.plot.histogram(
        data_frame=data,
        values_column='unit_price',
        bins=50)
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _histogram_example2(data):
    """# Horizontal histogram"""
    ch = chartify.Chart(blank_labels=True, x_axis_type='density')
    ch.set_title("Horizontal histogram with grouping")
    ch.set_subtitle("")
    ch.plot.histogram(
        data_frame=data,
        values_column='unit_price',
        color_column='fruit')
    ch.show(_OUTPUT_FORMAT)


plot_histogram.__doc__ = _core.plot.PlotNumericDensityXY.histogram.__doc__


@_print_source
def plot_kde():
    """
    KDE example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    print(data.head())
    """Print break"""
    _kde_example(data)
    _kde_example2(data)


@_print_source
def _kde_example(data):
    """# Parallel with datetime x axis"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, y_axis_type='density')
    ch.set_title("KDE plot")
    ch.plot.kde(
        data_frame=data,
        values_column='unit_price',
        color_column='fruit')
    ch.show(_OUTPUT_FORMAT)


@_print_source
def _kde_example2(data):
    """# Parallel with datetime x axis"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True, y_axis_type='density')
    ch.set_title("KDE plot + Histogram")
    ch.plot.kde(
        data_frame=data,
        values_column='unit_price',
        color_column='fruit')
    ch.style.color_palette.reset_palette_order()
    ch.plot.histogram(
        data_frame=data,
        values_column='unit_price',
        color_column='fruit',
        method='density')
    ch.show(_OUTPUT_FORMAT)


plot_histogram.__doc__ = _core.plot.PlotNumericDensityXY.kde.__doc__


@_print_source
def plot_heatmap():
    """
    Bar example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    average_price_by_fruit_and_country = (data.groupby(
        ['fruit', 'country'])['total_price'].mean().reset_index())
    """Print break"""
    _heatmap_example_1(average_price_by_fruit_and_country)


@_print_source
def _heatmap_example_1(average_price_by_fruit_and_country):
    """Docstring"""
    # Plot the data
    (chartify.Chart(
        blank_labels=True,
        x_axis_type='categorical',
        y_axis_type='categorical')
     .plot.heatmap(
        data_frame=average_price_by_fruit_and_country,
        x_column='fruit',
        y_column='country',
        color_column='total_price',
        text_column='total_price',
        text_color='white')
     .axes.set_xaxis_label('Fruit')
     .axes.set_yaxis_label('Country')
     .set_title('Heatmap')
     .set_subtitle("Plot numeric value grouped by two categorical values")
     .show(_OUTPUT_FORMAT))


plot_heatmap.__doc__ = _core.plot.PlotCategoricalXY.heatmap.__doc__


@_print_source
def style_color_palette_accent():
    """
    Color palette
    """
    import numpy as np
    import pandas as pd
    import chartify

    # Generate example data
    data = pd.DataFrame({'x': list(range(100))})
    data['y'] = data['x'] * np.random.normal(size=100)
    data['z'] = np.random.choice([2, 4, 5], size=100)
    data['country'] = np.random.choice(
        ['US', 'GB', 'CA', 'JP', 'BR'], size=100)

    # Plot the data
    ch = chartify.Chart(blank_labels=True)
    ch.style.set_color_palette('accent', accent_values=['US', 'CA'])
    ch.plot.scatter(
        data_frame=data,
        x_column='x',
        y_column='y',
        size_column='z',
        color_column='country')
    ch.set_title("Accent color palette")
    ch.set_subtitle(
        "Highlight specific color values or assign specific colors to values.")
    ch.show(_OUTPUT_FORMAT)


@_print_source
def style_color_palette_custom():
    """
    Custom color palette
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    # Create a new custom palette
    chartify.color_palettes.create_palette(colors=['#ff0000', 'yellow',
                                                   'purple', 'orange'],
                                           palette_type='categorical',
                                           name='custom palette')

    ch = chartify.Chart(blank_labels=True)
    # Apply the custom palette
    ch.style.set_color_palette('categorical', 'custom palette')
    ch.plot.scatter(
        data_frame=data,
        x_column='unit_price',
        y_column='quantity',
        color_column='fruit')
    ch.set_title("Custom color palette")
    ch.show(_OUTPUT_FORMAT)

def example_data():
    """Data set used in Chartify examples.
    """
    import numpy as np
    import pandas as pd

    np.random.seed(1)
    N_SAMPLES = 1000

    example_data = pd.DataFrame()
    date_range = pd.date_range('2017-01-01', '2017-12-31')

    COUNTRIES, COUNTRY_P = ['US', 'GB', 'CA', 'JP',
                            'BR'], [.35, .17, .23, .15, .1]

    FRUIT = ['Orange', 'Apple', 'Banana', 'Grape']
    PRICE = [.5, 1., .25, 2.]
    fruit_price_map = dict(list(zip(FRUIT, PRICE)))
    day_probabilities = np.random.dirichlet(list(range(1, 366)))
    example_data['date'] = np.random.choice(
        date_range, p=day_probabilities, size=N_SAMPLES)

    COUNTRY_FRUIT_P = {
        c: np.random.dirichlet([len(FRUIT)] * len(FRUIT))
        for c in COUNTRIES
    }
    example_data['country'] = np.random.choice(
        COUNTRIES, p=COUNTRY_P, size=N_SAMPLES)

    example_data['fruit'] = example_data['country'].apply(
        lambda x: np.random.choice(FRUIT, p=COUNTRY_FRUIT_P[x]))

    example_data['unit_price'] = example_data['fruit'].map(fruit_price_map) * (
        1.0 + np.random.normal(0, .1, size=N_SAMPLES))
    example_data['quantity'] = example_data['unit_price'].apply(lambda x: max(0, np.random.poisson(max(3. - x*1.25, 0)) + 1))
    example_data['total_price'] = (example_data['unit_price']
                                   * example_data['quantity'])
    return example_data


@_print_source
def style_color_palette_categorical():
    """
    Color palette
    """
    import numpy as np
    import pandas as pd
    import chartify

    # Generate example data
    data = pd.DataFrame({'x': list(range(100))})
    data['y'] = data['x'] * np.random.normal(size=100)
    data['z'] = np.random.choice([2, 4, 5], size=100)
    data['country'] = np.random.choice(
        ['US', 'GB', 'CA', 'JP', 'BR'], size=100)

    # Plot the data
    ch = chartify.Chart(blank_labels=True)
    ch.style.set_color_palette(palette_type='categorical')
    ch.plot.scatter(
        data_frame=data,
        x_column='x',
        y_column='y',
        color_column='country')
    ch.set_title("Categorical color palette type")
    ch.set_subtitle(
        "Default palette type. Use to differentiate categorical series.")
    ch.show(_OUTPUT_FORMAT)
    """Line break"""
    _categorical_example_2(data)


@_print_source
def _categorical_example_2(data):
    """Docstring"""
    # Plot the data
    ch = chartify.Chart(blank_labels=True)
    ch.style.set_color_palette(
        palette_type='categorical',)
    ch.plot.scatter(
        data_frame=data,
        x_column='x',
        y_column='y',
        color_column='country')
    ch.set_title(
        "Pass 'palette' parameter to .set_color_palette() to change palette colors."
    )
    ch.set_subtitle("")
    ch.show(_OUTPUT_FORMAT)


@_print_source
def style_color_palette_sequential():
    """
    Color palette sequential
    """
    import numpy as np
    import pandas as pd
    import chartify

    data = pd.DataFrame({'time': pd.date_range('2015-01-01', '2018-01-01')})
    n_days = len(data)
    data['1st'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days)
    data['2nd'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days) + 200
    data['3rd'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days) + 500
    data['4th'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days) + 700
    data['5th'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days) + 800
    data['6th'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days) + 1000
    data = pd.melt(
        data,
        id_vars=['time'],
        value_vars=data.columns[1:],
        value_name='y',
        var_name=['grouping'])

    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.style.set_color_palette(palette_type='sequential')
    ch.plot.line(
        data_frame=data.sort_values('time'),
        x_column='time',
        y_column='y',
        color_column='grouping')
    ch.set_title("Sequential color palette type")
    ch.set_subtitle("Palette type for sequential ordered dimensions")
    ch.show(_OUTPUT_FORMAT)


@_print_source
def style_color_palette_diverging():
    """
    Color palette sequential
    """
    import numpy as np
    import pandas as pd
    import chartify

    data = pd.DataFrame({'time': pd.date_range('2015-01-01', '2018-01-01')})
    n_days = len(data)
    data['Very Unlikely'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days)
    data['Unlikely'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days) + 200
    data['Neutral'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days) + 500
    data['Likely'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days) + 700
    data['Very Likely'] = np.array(list(range(n_days))) + np.random.normal(
        0, 10, size=n_days) + 800
    data = pd.melt(
        data,
        id_vars=['time'],
        value_vars=data.columns[1:],
        value_name='y',
        var_name=['grouping'])

    # Plot the data

    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.style.set_color_palette(palette_type='diverging')
    color_order = [
        'Very Unlikely', 'Unlikely', 'Neutral', 'Likely', 'Very Likely'
    ]
    ch.plot.line(
        data_frame=data.sort_values('time'),
        x_column='time',
        y_column='y',
        color_column='grouping',
        color_order=color_order)  # Your data must be sorted
    ch.set_title("Diverging color palette type")
    ch.set_subtitle("Palette type for diverging ordered dimensions")
    ch.show(_OUTPUT_FORMAT)


@_print_source
def callout_line():
    """
    Line example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    # Plot the data
    (chartify.Chart(blank_labels=True)
     .plot.scatter(
        data_frame=data,
        x_column='unit_price',
        y_column='total_price')
     .callout.line(2)  # Callout horizontal line
     .callout.line(1, 'height')  # Callout vertical line
     .set_title('Line callout')
     .set_subtitle("Callout lines on either axis")
     .show(_OUTPUT_FORMAT))


@_print_source
def callout_text():
    """
    Line segment
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    # Plot the data
    ch = chartify.Chart(blank_labels=True)
    ch.plot.scatter(
        data_frame=data,
        x_column='unit_price',
        y_column='total_price')
    ch.callout.text("Description of what is\ngoing on in this chart!", 0, 6)
    ch.set_title("Text callout")
    ch.set_subtitle("Add narrative to your chart.")
    ch.show(_OUTPUT_FORMAT)


callout_text.__doc__ = _core.callout.Callout.text.__doc__


@_print_source
def callout_box():
    """
    Box example
    """
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    # Plot the data
    (chartify.Chart(blank_labels=True)
     .plot.scatter(
        data_frame=data,
        x_column='total_price',
        y_column='unit_price')
     .callout.box(top=1, bottom=-1, color='red')
     .callout.box(top=2, left=4, color='blue')
     .callout.box(bottom=2, right=3, color='green')
     .set_title("Shaded area callout")
     .set_subtitle("Highlight notable areas of your chart")
     .show(_OUTPUT_FORMAT))


callout_box.__doc__ = _core.callout.Callout.box.__doc__


@_print_source
def axes_axis_type():
    """
    Axis type examples
    """
    import numpy as np
    import pandas as pd
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    # Plot the data
    (chartify.Chart(blank_labels=True, x_axis_type='log')
     .plot.scatter(
        data_frame=data,
        x_column='total_price',
        y_column='quantity')
     .set_subtitle(
        "Set axis type for auto handling of categorical, datetime, linear, or log values."
    )
     .set_title("Axis Type")
     .show(_OUTPUT_FORMAT))


# axis_type.__doc__ = _core.axes.Axes.set_xaxis_type.__doc__


@_print_source
def axes_axis_tick_format():
    """
    Axis scale examples
    """
    import numpy as np
    import pandas as pd
    import chartify

    # Generate example data
    data = chartify.examples.example_data()
    data['%_sales'] = data['quantity'] / data['quantity'].sum()

    # Plot the data
    (chartify.Chart(blank_labels=True)
     .plot.scatter(
        data_frame=data,
        x_column='%_sales',
        y_column='unit_price')
     .axes.set_yaxis_tick_format("$0.00")
     .axes.set_xaxis_tick_format("0.00%")
     .set_subtitle("Format ticks on either axis to set units or precision")
     .set_title("Axis tick format").show(_OUTPUT_FORMAT))


# tick_format.__doc__ = _core.axes.Axes.format_xaxis_tick_labels.__doc__


@_print_source
def axes_axis_tick_values():
    """
    Axis scale examples
    """
    import pandas as pd
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
    ch.plot.scatter(data, 'date', 'quantity')
    ch.set_title("Axis tick values")
    ch.set_subtitle(
        "Pass a list of values or use pd.date_range for datetime axes")
    # Use pd.date_range to generate a range of dates
    # at the start of each month
    ch.axes.set_xaxis_tick_values(
        pd.date_range('2017-01-01', '2018-01-01', freq='MS'))
    ch.axes.set_yaxis_tick_values(list(range(0, 8, 2)))
    ch.show(_OUTPUT_FORMAT)


@_print_source
def chart_labels():
    """
    Chart label examples
    """
    import numpy as np
    import pandas as pd
    import chartify

    # Generate example data
    data = chartify.examples.example_data()

    apple_prices = (data[data['fruit'] == 'Apple']
                    .groupby(['quantity'])['unit_price'].mean().reset_index())
    # Plot the data with method chaining
    (chartify.Chart(blank_labels=True)
     .plot.scatter(apple_prices, 'quantity', 'unit_price')
     .set_title(
         "Quantity decreases as price increases. <--  Use title for takeaway.")
     .set_subtitle(
         "Quantity vs. Price. <-- Use subtitle for data description.")
     .axes.set_xaxis_label("Quantity per sale (Apples)")
     .axes.set_yaxis_label("Price ($)")
     .axes.set_yaxis_tick_format("$0.00")
     .show(_OUTPUT_FORMAT))


@_print_source
def chart_layouts():
    """
    Layout examples
    """
    import numpy as np
    import pandas as pd
    import chartify

    # Generate example data
    data = pd.DataFrame({'Price': list(range(100))})
    data['Demand'] = 100 + -.5 * data['Price'] + np.random.normal(size=100)

    layouts = ['slide_100%', 'slide_75%', 'slide_50%', 'slide_25%']

    def display_layout(layout):
        (chartify.Chart(
            layout=layout)  # Assign the layout when instantiating the chart.
         .plot.scatter(
            data_frame=data,
            x_column='Price',
            y_column='Demand')
         .set_title("Slide layout: '{}'".format(layout))
         .set_subtitle("Demand vs. Price.")
         .set_source_label("")
         .axes.set_xaxis_label("Demand (# Users)")
         .axes.set_yaxis_label("Price ($)")
         .show(_OUTPUT_FORMAT))

    [display_layout(layout) for layout in layouts]


@_print_source
def chart_show():
    """
    Docstring
    """
    import numpy as np
    import pandas as pd
    import chartify

    # Generate example data
    data = pd.DataFrame({'x': list(range(100))})
    data['y'] = data['x'] * np.random.normal(size=100)
    data['z'] = np.random.choice([2, 4, 5], size=100)
    data['country'] = np.random.choice(
        ['US', 'GB', 'CA', 'JP', 'BR'], size=100)

    # Plot the data
    ch = chartify.Chart(blank_labels=True)
    ch.plot.scatter(
        data_frame=data,
        x_column='x',
        y_column='y',
        size_column='z',
        color_column='country')
    ch.set_title(
        'ch.show(): Faster rendering with HTML. Recommended while drafting.')
    ch.set_subtitle('No watermark. Does not display on github.')
    ch.show('html')  # Show with HTML

    ch.set_title(
        'ch.show("png"): Return a png file for easy copying into slides')
    ch.set_subtitle('Will display on github.')
    ch.show('png')  # Show with PNG

chart_show.__doc__ = _core.chart.Chart.show.__doc__
