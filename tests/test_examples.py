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
"""Tests for `chartify` package."""

import chartify
import importlib


def test_examples():
    # reload configuration
    importlib.reload(chartify)

    excluded_examples = ['chart_show']
    public_examples = [
        attr for attr in dir(chartify.examples) if
        callable(getattr(chartify.examples, attr))
        and not attr.startswith("_")
        and attr not in excluded_examples
    ]
    # Disable chart rendering
    chartify.examples._OUTPUT_FORMAT = None
    for example in public_examples:
        getattr(chartify.examples, example)()
