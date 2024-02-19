"""CLI entrypoint for simple testing by users.

.. note:: Current implementatoin is stub to pass functests.
"""

from docutils.core import publish_cmdline

from .core import configure

configure()
publish_cmdline()
