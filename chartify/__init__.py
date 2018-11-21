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
"""Top-level package for chartify."""
from chartify._core.chart import Chart
from chartify._core.colors import color_palettes
from chartify._core.options import options
from chartify import examples

__author__ = """Chris Halpert"""
__email__ = 'chalpert@spotify.com'
__version__ = '2.3.5'

_IPYTHON_INSTANCE = False


def set_display_settings():
    """Enable notebook output settings if running in a jupyter notebook"""
    from IPython.core.getipython import get_ipython
    from ipykernel.zmqshell import ZMQInteractiveShell
    from bokeh.io import output_notebook
    from bokeh.resources import Resources

    ipython_instance = get_ipython()
    if ipython_instance is not None:
        if isinstance(ipython_instance, ZMQInteractiveShell):
            _IPYTHON_INSTANCE = True
            # Inline resources uses bokeh.js from the local version.
            # This enables offline usage.
            output_notebook(Resources('inline'))


set_display_settings()
del set_display_settings
