SKOS: W3C SKOS for humans
==========================


SKOS is a lightweight `W3C SKOS<https://www.w3.org/2004/02/skos/>`_
client library written in Python.

It has been designed for conveniently retrieving data from
SPARQL endpoints the Pythonic way:

    >>> from skos import SKOSEndpoint
    >>> url = "http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc"
    >>> endpoint = SKOSEndpoint(url)

Features
--------

- Search skos:concept(s) based on preferred or alternative labels.
- Extract all labels from a concept in different languages.
- Navigational traversal of the concept hierarchy: broader, narrower, related.


Installation
------------

::

    pip install skos

Dependencies:

* `sparqlwrapper <https://github.com/RDFLib/sparqlwrapper`_



Documentation
-------------

Documentation is available at `Read the Docs <https://sickle.readthedocs.org/en/latest/>`_

Development
-----------

* `SKOS @ GitHub <https://github.com/msicilia/skos>`_
