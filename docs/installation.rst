Installation
============

Installing pywwt with conda
---------------------------

.. warning:: This does not work yet as there has not been a stable release
             of pywwt on conda.

If you use the `Anaconda Distribution <https://www.anaconda.com/download/#macos>`_
(or `Miniconda <https://conda.io/miniconda.html>`_), you can install the latest
release of pywwt using::

    conda install -c wwt pywwt

This will automatically install pywwt, its dependencies, and will enable the
Jupyter extension.

Installing pywwt with pip
-------------------------

You can also install the latest release of pywwt using `pip
<http://pip.pypa.io>`_::

    pip install pywwt

If you want to use the Jupyter widget, you will need to also enable the
extension using::

    jupyter nbextension enable --py --sys-prefix pywwt

If you want to use the Qt widget, you will need to install
`PyQt <https://riverbankcomputing.com/software/pyqt/intro>`_ or
`PySide <https://wiki.qt.io/PySide>`_ separately.

Dependencies
------------

If you install pywwt using pip or conda, any required dependencies will get
installed automatically (with the exception of PyQt/PySide if using pip). These
dependencies are as follows:

* `Python <http://www.python.org>`_ 2.7, or 3.5 or later
* `NumPy <http://www.numpy.org>`_ 1.9 or later
* `Matplotlib <http://matplotlib.org>`_ 1.5 or later
* `Astropy <http://www.astropy.org>`_ 1.0 or later
* `Requests <http://docs.python-requests.org/en/latest/>`_
* `Beautiful Soup 4 <http://www.crummy.com/software/BeautifulSoup>`_
* `Dateutil <http://labix.org/python-dateutil>`_
* `lxml <http://lxml.de>`_
* `ipywidgets <http://ipywidgets.readthedocs.io>`_ 7.0.0 or later
* `ipyevents <https://github.com/mwcraig/ipyevents>`_
* `traitlets <http://traitlets.readthedocs.io>`_

In addition, if you want to use the Qt widget, you will need:

* `PySide <https://wiki.qt.io/PySide>`__ or `PyQt
  <https://riverbankcomputing.com/software/pyqt/intro>`__ (both PyQt4 and PyQt5 are supported)
* `QtPy <https://pypi.python.org/pypi/QtPy/>`__ 1.2 or higher

Installing the developer version
--------------------------------

If you want to use the very latest developer version version, you can clone
this repository and install the package manually (note that this requires `npm
<https://www.npmjs.com>`_ to be installed)::

    git clone https://github.com/WorldWideTelescope/pywwt.git
    cd pywwt
    pip install -e .

If you want to use the Jupyter widget, you will also need to run::

    jupyter nbextension install --py --symlink --sys-prefix pywwt
    jupyter nbextension enable --py --sys-prefix pywwt

If you use conda, you can alternatively install a recent developer version
using::

    conda install -c conda-forge -c wwt/label/dev pywwt

This will install a version built in the last 24 hours so may not strictly be
the absolute latest version in some cases.
