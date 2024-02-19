from docutils.parsers.rst import roles


def test_configure_default(monkeypatch):
    from rst_multi_refs.core import configure

    _role_registry = {}
    monkeypatch.setattr(roles, "_role_registry", _role_registry)
    configure()
    assert "npm" in _role_registry
