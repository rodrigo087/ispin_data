==============
iSpin Data
==============

.. image:: https://travis-ci.org/lead-ratings/gender-guesser.svg?branch=master
    :target: https://github.com/rodrigo087/ispin_data


This package provides access to iSpin data for a specified turbine ID.  Its use is pretty straightforward::

    >>> import ispin_data.api as ispin
    >>> iSpin = ispin.Data()
    >>> df = iSpin.request_data(34)
    3634
    >>> df = iSpin.request_data(6)
    113

The explanation each columns of the returned DataFrame can be consulted in the XXXXXXXX.txt file

For now, the function will only provide the area of a circle given by the specified turbine ID


Licenses
========

Nabla Wind Hub.


Changelog
=========

0.1.0 (2021-08-24)
******************

* First release of the package

