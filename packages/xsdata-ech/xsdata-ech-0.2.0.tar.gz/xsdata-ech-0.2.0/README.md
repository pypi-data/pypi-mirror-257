eCH xsdata dataclasses
======================

Provides [xsdata](https://xsdata.readthedocs.io) dataclasses for swiss
e-government standards defined by [eCH](https://ech.ch).


! JSON deserialization might return wrong classes, if they have the same structure.

Tests
-----

Run the tests

    pip install .[test]
    tox

Releasing
---------

Bump version

    pip install .[dev]
    bump2version {major|minor|patch}

Update definitions
------------------

Generate files

    pip install .[dev]
    xsdata generate xxx.xsd

Then move the files and fix the imports.