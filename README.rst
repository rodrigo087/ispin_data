==============
iSpin Data
==============

.. image:: https://travis-ci.org/lead-ratings/gender-guesser.svg?branch=master
    :target: https://github.com/rodrigo087/ispin_data


This package provides access to iSpin data for a specified turbine ID.  Its use is pretty straightforward::

    >>> import ispin_data.api as ispin
    
    >>> ispin.username = 'your_username'
    >>> ispin.password = 'your_password'
    
    >>> df = ispin.request_overview()
    # Returns iSpin installations
    
    >>> df = iSpin.request_data(6)
    # Returns data for installation number 6. The start and end date can also be specified




Licenses
========

Nabla Wind Hub.


Changelog
=========

0.1.0 (2021-08-24)
******************

* First release

0.2.5 (2021-08-26)
******************

* Current release
