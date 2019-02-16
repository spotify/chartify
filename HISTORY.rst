=======
History
=======

2.4.0 (YYYY-MM-DD)

Improvements:

* Added chromedriver-installer requirement to remove
  the manual installation process of chromedriver.
* Added README links to launch tutorial and example notebooks with Binder.

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
