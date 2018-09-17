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


class TestBaseAxes:

    def test_datetime_callouts(self):
        data = chartify.examples.example_data()

        # Sum price grouped by date
        price_by_date = (
            data.groupby('date')['total_price'].sum()
            .reset_index()  # Move 'date' from index to column
            )

        # Plot the data
        ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
        ch.plot.line(
            # Data must be sorted by x column
            data_frame=price_by_date.sort_values('date'),
            x_column='date',
            y_column='total_price')
        ch.callout.line('2017-08-01', orientation='height', line_width=10)
        ch.callout.line_segment('2017-08-01', 10, '2017-09-05', 20)
        ch.callout.box(10, 0, '2017-05-01', '2017-05-05')
        ch.callout.text('text', '2017-05-01', 10)
