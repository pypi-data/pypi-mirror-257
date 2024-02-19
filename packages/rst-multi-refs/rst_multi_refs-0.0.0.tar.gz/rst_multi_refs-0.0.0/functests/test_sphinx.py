"""Test cases as Sphinx extension."""
import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="default")
def test_work_on_sphinx(app: SphinxTestApp):
    """Simple test that it passed for sphinx-build."""
    app.build()
    index_html = app.outdir / "index.html"
    assert index_html.exists()
    assert "https://www.npmjs.com/package/react" in index_html.read_text()
