Chartify
========

|status|release|python|CI|
|---|----|----|----|
|<img src="https://img.shields.io/badge/Status-Beta-blue.svg" />|<img src="https://img.shields.io/badge/Release-3.0.0-blue.svg" />|<img src="https://img.shields.io/badge/Python-3.6-blue.svg" />|<img src="https://github.com/spotify/chartify/workflows/Tox/badge.svg" />|<img src="https://github.com/spotify/chartify/actions" />

<img width="100" align="right" src="https://user-images.githubusercontent.com/94545831/196786770-b10bd085-9b56-4575-8925-d90ee72bbcc2.png" />

<br>

![Github Repo Size](https://img.shields.io/github/repo-size/spotify/chartify?style=for-the-badge&color=aqua)

Chartify is a Python library that makes it easy for data scientists to create charts.


Why use Chartify?
-----------------

- **Consistent input data format:** Spend less time transforming data to get your charts to work. All plotting functions use a consistent tidy input data format.
- **Smart default styles:** Create pretty charts with very little customization required.
- **Simple API:** We've attempted to make the API as intuitive and easy to learn as possible.
- **Flexibility:** Chartify is built on top of [Bokeh](https://docs.bokeh.org/en/latest/) so if you do need more control you can always fall back on Bokeh's API.

<br>

<details>
<summary><h2> Examples </h2></summary>


<img  width="500" src="https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify1.png" />
<img  width="500" src="https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify2.png" />
<img  width="500" src="https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify3.png" />
<img  width="500" src="https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify4.png" />
<img  width="500" src="https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify5.png" />
<img  width="500" src="https://raw.githubusercontent.com/spotify/chartify/master/docs/_static/chartify6.png" />

[See this notebook for more examples!](https://github.com/spotify/chartify/blob/master/examples/Examples.ipynb)

</details><br>

Installation
------------

1. Chartify can be installed via pip:

``pip3 install chartify``

2. Install chromedriver requirement (Optional. Needed for PNG output):
    - Install google chrome.
    - Download the appropriate version of chromedriver for your OS [here](https://sites.google.com/chromium.org/driver/)
    - Copy the executable file to a directory within your PATH.
	- View directorys in your PATH variable: ``echo $PATH``
	- Copy chromedriver to the appropriate directory, e.g.: ``cp chromedriver /usr/local/bin``

Getting started
---------------

This [tutorial notebook](https://github.com/spotify/chartify/blob/master/examples/Chartify%20Tutorial.ipynb) is the best place to get started with a guided tour of the core concepts of Chartify.

From there, check out the [example notebook](https://github.com/spotify/chartify/blob/master/examples/Examples.ipynb) for a list of all the available plots.


Getting support
---------------

Join #chartify on [SLACK](https://slackin.spotify.com/) &nbsp; **AND** &nbsp; Use the [chartify tag on StackOverflow](https://stackoverflow.com/questions/tagged/chartify)

Resources
---------------

- Data Visualization with [Chartify](https://www.section.io/engineering-education/data-viz-chartify/)

<br>

[Documentation](https://chartify.readthedocs.io/en/latest/) &nbsp;  **AND**   [Code of Conduct](https://github.com/spotify/code-of-conduct/blob/master/code-of-conduct.md) &nbsp; **AND**    [Contributing Guidelines](https://github.com/spotify/chartify/blob/master/CONTRIBUTING.rst)
