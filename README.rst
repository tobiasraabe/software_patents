Identification of Software Patents
==================================

.. image:: https://travis-ci.com/tobiasraabe/software_patents.svg?branch=master
    :target: https://travis-ci.com/tobiasraabe/software_patents

.. image:: https://pyup.io/repos/github/tobiasraabe/software_patents/shield.svg
    :target: https://pyup.io/repos/github/tobiasraabe/software_patents/
    :alt: Updates

Introduction
------------

This project deals with the identification of software patents and combines
multiple approaches from simple algorithms to novel machine learning models to
achieve this goal.


Background
----------

The origin of this project was a Bachelor's thesis built on the algorithmic
approach of [BH2007]_. The authors wanted to estimate the number of software
patents and find out where software patents are used and what economic
indicators are correlated with having more software patents.

To classify patents into categories of software and non-software, the authors
developed a simple alogrithm based on the evaluation of a random sample of
patents. The algorithm is as follows:

..

    (("software" in specification) OR ("computer" AND "program" in
    specification))

    AND (utility patent excluding reissues)

    ANDNOT ("chip" OR "semiconductor" OR "bus" OR "circuit" OR "circuitry" in
    title)

    ANDNOT ("antigen" OR "antigenic" OR "chromatography" in specification)

Whereas title is simply identified, specification is defined as the abstract
and the description of the patent ([PATENTSVIEW]_ separates the description in
[BH2007]_ definition into description and summary).

To replicate the algorithm, the project relies on two strategies. The first
data source is `Google Patents <https://patents.google.com/>`_ where the texts
can be crawled. As this procedure is not feasible for the whole corpus of
patents, the second data source is [PATENTSVIEW]_ which provides large data
files for all patents from 1976 on.

The replication of the original algorithm succeeds in 398 of 400 cases as one
patent was retracted and in one case an indicator was overlooked which lead to
a error in the classification.

Compared to the manual classification of the authors, the algorithm performed
in the following way:

+-------------------+----------+--------------+
|                   | Relevant | Not Relevant |
+===================+==========+==============+
| **Retrieved**     |       42 |            8 |
+-------------------+----------+--------------+
| **Not Retrieved** |       12 |          337 |
+-------------------+----------+--------------+

Applying the algorithm on the whole patent corpus, we get the following
distributions of patents and software versus non-software patents.

**Absolute number of Utility Patents**

.. raw:: html

        <p align="center">
            <img src="_static/fig-patents-distribution.png"
            width="600" height="400">
        </p>

**Absolute Number of Software vs. Non-Software Patents**

.. raw:: html

        <p align="center">
            <img src="_static/fig-patents-distribution-vs.png"
            width="600" height="400">
        </p>

**Relative Number of Software vs. Non-Software Patents**

.. raw:: html

        <p align="center">
            <img src="_static/fig-patents-distribution-vs-shares.png"
            width="600" height="400">
        </p>


Installation
------------

To work on the project yourself, clone the repository on your disk with

.. code-block:: bash

    $ git clone https://github.com/tobiasraabe/software_patents

After that create an environment with ``conda`` and activate it by running

.. code-block:: bash

    $ conda env create -n sp -f environment.yml
    $ activate sp

Then, download the data. If you want to download only the files for reproducing
the analysis based on the indicators, run the following commands to download
the data and to validate the files:

.. code-block:: bash

    $ python prepare_data_for_project download --subset replication
    $ python prepare_data_for_project validate

(If you want to have the raw data or everything, use ``--subset raw`` or
``--subset all``. Note that, you need about 60GB of free space on your disk.
Furthermore, handling the raw data requires an additional step where the files
are splitted into smaller chunks, so that they can fit into the memory of your
machine. These steps require knowledge about `Dask
<https://dask.pydata.org/en/latest/>`_. You can find more on this `here
<https://github.com/tobiasraabe/software_patents/blob/master/src/documentation/
data.rst>`_.)

Then, run the following two commands to replicate the results.

.. code-block:: bash

    $ python waf.py configure distclean
    $ python waf.py build


References
----------

.. [BH2007] https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1530-9134.2007.00136.x
.. [PATENTSVIEW] http://www.patentsview.org/download/
