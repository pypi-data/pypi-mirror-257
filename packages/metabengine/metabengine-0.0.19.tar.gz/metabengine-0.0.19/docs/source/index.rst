.. metabengine documentation master file.

Welcome to metabengine!
=======================

`metabengine`_ is a fundamental package for mass spectrometry data processing with Python, 
with the emphasis on metabolomics data.

*metabengine* enables:

Untargeted feature extraction
    Accurate and comprehensive feature detection in LC-MS/MS data, with accurate annotation of isotopes, charge states,
    adducts, and in-source fragments.
    Read more about :doc:`/feature_detection`.

Compound annotation and analog search
    Ultra-fast annotation of MS/MS spectra with high confidence, suppoted by entropy similarity.
    Read more about :doc:`/annotation`.

Data visualization
    Visualize the data in a variety of ways and generate publication-quality graphs, including chromatograms, 
    single spectrum, MS/MS matching plots, and molecular networks.
    Read more about :doc:`/visualization`.
   
Tools for data analysis
    A variety of tools for data analysis, including data normalization, missing value imputation, and statistical analysis.
    Read more about :doc:`/data_analysis`.

.. _metabengine: https://github.com/Waddlessss/metabengine



Get Started
-----------

Start your journey with *metabengine* by learning about the following topics:

* **installation**: 
  :doc:`/installation`

* **Quick Start**:
  :doc:`/quick_start`


.. note::

   This project is under active development.



metabengine Functions
---------------------

Learn more about the functions in BAGO.

* **Functions to manipulate MS data**:
  :doc:`/MSdata-obj` |


Useful Links
------------

* **metabengine on GitHub**:
   `metabengine source code and more details <https://github.com/Waddlessss/metabengine>`_

* **metabengine on PyPI**:
   `metabengine Python package <https://pypi.org/project/metabengine/>`_


.. toctree::
   :maxdepth: 1

   self
   installation


.. toctree::
   :maxdepth: 1
   :caption: Get Started

   backgrounds
   getting-started-with-ipynb


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: metabengine Functions

   MSdata-obj
