import pytest


def test_sphinx_gallery_example_header():
    """
    We have copied EXAMPLE_HEADER and modified it to include meta keywords.
    This test monitors that the version we have copied is still the same as
    the EXAMPLE_HEADER in sphinx-gallery. If sphinx-gallery changes its
    EXAMPLE_HEADER, this test will start to fail. In that case, please update
    the monkey-patching of EXAMPLE_HEADER in conf.py.
    """
    gen_rst = pytest.importorskip('sphinx_gallery.gen_rst')

    EXAMPLE_HEADER = """
.. DO NOT EDIT.
.. THIS FILE WAS AUTOMATICALLY GENERATED BY SPHINX-GALLERY.
.. TO MAKE CHANGES, EDIT THE SOURCE PYTHON FILE:
.. "{0}"
.. LINE NUMBERS ARE GIVEN BELOW.

.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        :ref:`Go to the end <sphx_glr_download_{1}>`
        to download the full example code{2}

.. rst-class:: sphx-glr-example-title

.. _sphx_glr_{1}:

"""
    assert gen_rst.EXAMPLE_HEADER == EXAMPLE_HEADER
