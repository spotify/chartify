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
# flake8: noqa
"""Top-level package for chartify."""
from chartify._core.chart import Chart
from chartify._core.radar_chart import RadarChart
from chartify._core.colors import color_palettes
from chartify._core.options import options
from chartify import examples

__author__ = """Chris Halpert"""
__email__ = "chalpert@spotify.com"
__version__ = "5.0.1"

_IPYTHON_INSTANCE = False


def _running_in_notebook_like_environment(ipython_instance):
    """Return True if the current IPython instance is a notebook-style
    frontend that Bokeh can render inline into.

    This includes classic/Jupyter notebooks and JupyterLab (both backed by
    ``ipykernel.zmqshell.ZMQInteractiveShell``), as well as Google Colab,
    which implements its own shell (``google.colab._shell.Shell``) that is
    *not* a subclass of ``ZMQInteractiveShell``. Relying solely on the
    ``ZMQInteractiveShell`` isinstance check causes Colab to be silently
    skipped, so ``output_notebook`` is never called and charts render an
    empty output (see issue #131).
    """
    from ipykernel.zmqshell import ZMQInteractiveShell

    if isinstance(ipython_instance, ZMQInteractiveShell):
        return True

    # Google Colab ships its own shell implementation that doesn't inherit
    # from ZMQInteractiveShell. Detect it by class name/module instead of
    # importing the (Colab-only) google.colab package directly.
    shell_class = type(ipython_instance)
    shell_module = getattr(shell_class, "__module__", "")
    if shell_module.startswith("google.colab"):
        return True

    return False


def set_display_settings():
    """Enable notebook output settings if running in a jupyter notebook"""
    global _IPYTHON_INSTANCE
    from IPython.core.getipython import get_ipython
    from bokeh.io import output_notebook
    from bokeh.resources import Resources
    from bokeh.io.state import curstate

    ipython_instance = get_ipython()
    if ipython_instance is not None:
        if _running_in_notebook_like_environment(ipython_instance):
            _IPYTHON_INSTANCE = True
            # Defer to previous call to ``output_notebook`` so that users
            # can specify their own notebook type and Bokeh resources
            if curstate().notebook_type is None:
                # Inline resources uses bokeh.js from the local version.
                # This enables offline usage.
                output_notebook(Resources("inline"), hide_banner=True)


set_display_settings()
del set_display_settings