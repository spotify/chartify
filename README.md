Chartify
========

![Status](https://img.shields.io/badge/Status-Beta-blue.svg)
![Latest release](https://img.shields.io/badge/Release-5.0.0-blue.svg "Latest release: 5.0.0")
![python](https://img.shields.io/badge/Python-3.9-blue.svg "Python 3.9")
![python](https://img.shields.io/badge/Python-3.10-blue.svg "Python 3.10")
![python](https://img.shields.io/badge/Python-3.11-blue.svg "Python 3.11")
![CI](https://github.com/spotify/chartify/workflows/Tox/badge.svg "Tox")

Chartify is a Python library that makes it easy for data scientists to create charts.

Why use Chartify?
-----------------

- Consistent input data format: Spend less time transforming data to get your charts to work. All plotting functions use a consistent tidy input data format.
- Smart default styles: Create pretty charts with very little customization required.
- Simple API: We've attempted to make the API as intuitive and easy to learn as possible.
- Flexibility: Chartify is built on top of [Bokeh](http://bokeh.pydata.org/en/latest/), so if you do need more control you can always fall back on Bokeh's API.

Examples
--------

![](https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify1.png)
![](https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify2.png)
![](https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify3.png)
![](https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify4.png)
![](https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify5.png)
![](https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify6.png)

[See this notebook for more examples!](</examples/Examples.ipynb>).

Installation
------------

1. Chartify can be installed via pip:

`pip3 install chartify`

2. Install chromedriver requirement (Optional. Needed for PNG output):
    - Install google chrome.
    - Download the appropriate version of chromedriver for your OS [here](https://sites.google.com/chromium.org/driver/).
    - Copy the executable file to a directory within your PATH.
	- View directorys in your PATH variable: `echo $PATH`
	- Copy chromedriver to the appropriate directory, e.g.: `cp chromedriver /usr/local/bin`

Getting started
---------------

This [tutorial notebook](https://github.com/spotify/chartify/blob/master/examples/Chartify%20Tutorial.ipynb) is the best place to get started with a guided tour of the core concepts of Chartify.

From there, check out the [example notebook](https://github.com/spotify/chartify/blob/master/examples/Examples.ipynb) for a list of all the available plots.

Docs
---------------

Documentation available on [chartify.readthedocs.io](https://chartify.readthedocs.io/en/latest/).

Getting support
---------------

Use the [chartify tag on StackOverflow](https://stackoverflow.com/questions/tagged/chartify).

Code of Conduct
---------------

This project adheres to the [Open Code of Conduct](https://github.com/spotify/code-of-conduct/blob/master/code-of-conduct.md). By participating, you are expected to honor this code.

Contributing
------------

[See the contributing docs](https://github.com/spotify/chartify/blob/master/CONTRIBUTING.rst).
