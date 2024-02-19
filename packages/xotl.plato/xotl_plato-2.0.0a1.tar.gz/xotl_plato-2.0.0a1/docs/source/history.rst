===========
 Changelog
===========

Series 2.x
==========

Unreleased.  Release 2.0.0
--------------------------

- Add support for Python 3.12.

  We're currently testing in our CI the following versions: 3.8, 3.11, and
  3.12.

  We don't expect our code to fail in Python 3.9, or 3.10; but it's not
  actually tested in those versions.


Series 1.x
==========

2023-03-02.  Release 1.0.1
--------------------------

- Avoid AttributeError in `xotl.plato.types.ObjectType`:class: when being
  sub-classed.


2022-09-07.  Release 1.0.0
--------------------------

This release includes the code as it was used in several other projects before
extracting to this distribution.

Some application-specific code was removed and it was updated to be compatible
Python 3.8+.  We also added many extensions to the type-system and vastly
improved the module `xotl.plato.schema`:mod:.
