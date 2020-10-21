=======
History
=======

3.0.2 (2020-10-21)
------------------

* Support pyyaml 5.2+

3.0.1 (2020-06-02)
------------------

* Reduce dependencies by switching from Jupyter to IPython.

3.0.0 (2020-05-29)
------------------

* Updated Python to 3.6+ and Pandas to 1.0+ (Thanks @tomasaschan!)
* Updated Bokeh to 2.0+
* Removed colour dependency to fix setup errors.

2.7.0 (2019-11-27)
------------------

Bugfixes:

* Updated default yaml loader to move off of
  deprecated method (Thanks @vh920!)
* Updated legend handling to adjust for deprecated methods
  in recent versions of Bokeh (Thanks for reporting @jpkoc)
* Updated license in setup.py (Thanks for reporting @jsignell)
* Bump base Pillow dependency to avoid insecure version.
* Update MANIFEST to include missing files (Thanks @toddrme2178!)

2.6.1 (2019-08-15)
------------------

Bugfixes:

* Moved package requirements and fixed bug that occured with
  latest version of Bokeh (Thanks @emschuch & @mollymzhu!)
* Fixed bug in README while generating docs (Thanks @Bharat123rox!)

2.6.0 (2019-03-08)
------------------

Improvements:

* Allows users to plot colors on bar charts that aren't contained in the
  categorical axis.


Bugfixes:

* Fixed bug that caused float types to break when plotted with categorical
  text plots (Thanks for finding @danela!)
* Fixed broken readme links.

2.5.0 (2019-02-17)
------------------

Improvements:

* Added Radar Chart

2.4.0 (2019-02-16)
------------------

Improvements:

* Added second Y axis plotting.
* Removed Bokeh loading notification on import (Thanks @canavandl!)
* Added support for custom Bokeh resource loading (Thanks @canavandl!)
* Added example for Chart.save() method (Thanks @david30907d!)

Bugfixes:

* Updated documentation for saving and showing svgs.
* Fixed bug that broke plots with no difference between min and max
  points. (Thanks for finding @fabioconcina!)

2.3.5 (2018-11-21)
------------------

Improvements:

* Updated docstrings (Thanks @gregorybchris @ItsPugle!)
* Added SVG output options to Chart.show() and Chart.save()
  (Thanks for the suggestion @jdmendoza!)

Bugfixes:

* Fixed bug that caused source label to overlap with xaxis labels.
* Fixed bug that prevented x axis orientation changes
  with datetime axes (Thanks for finding @simonwongwong!)
* Fixed bug that caused subtitle to disappear
  with `outside_top` legend location (Thanks for finding @simonwongwong!)
* Line segment callout properties will work
  correctly. (Thanks @gregorybchris!)

2.3.4 (2018-11-13)
------------------

* Updated Bokeh version requirements to support 1.0

2.3.3 (2018-10-24)
------------------

* Removed upper bound of Pillow dependency.

2.3.2 (2018-10-18)
------------------

* Stacked bar and area order now matches default vertical legend order.
* Added method for shifting color palettes.
* Added scatter plots with a single categorical axis.
* Fixed bug with text_stacked that occurred with multiple categorical levels.

2.3.1 (2018-09-27)
------------------

* Fix scatter plot bug that can occur due to nested data types.

2.3.0 (2018-09-26)
------------------

* Added hexbin plot type.
* More control over grouped axis label orientation.
* Added alpha control to scatter, line, and parallel plots.
* Added control over marker style to scatter plot.
* Added ability to create custom color palettes.
* Changed default accent color.
* Visual tweaks to lollipop plot.
* Bar plots with a few number of series will have better widths.


2.2.0 (2018-09-17)
------------------

* First release on PyPI.
