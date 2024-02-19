==============
rst-multi-refs
==============

.. note:: This is experimental package.

reStructuredText's custom roles and role builder kit for package registries of any languages.

Installation
============

.. code:: console

   pip install rst-multi-refs

Usage
=====

Command line test
-----------------

.. code:: console

   $ echo ':npm:`react`' | python -m rst_multi_refs
   <document source="<stdin>">
       <paragraph>
           <reference refuri="https://www.npmjs.com/package/react">
               react

With Sphinx
-----------

.. code:: python

   extensions = [
       "rst_multi_refs.sphinx",
   ]

.. code:: rst

   This uses :npm:`react`.

Set up for local development
============================

Pre-requirements
----------------

* `Rye <https://rye-up.com/>`_
* `pre-commit <https://pre-commit.com/>`_
* Git

Set up
------

.. code:: console

   git clone https://github.com/attakei/rst-multi-refs.git
   cd /path/to/rst-multi-refs
   rye run setup
