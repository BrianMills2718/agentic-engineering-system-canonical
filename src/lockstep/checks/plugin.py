"""pytest plugin that registers the `req` marker linking a test to an OpenSpec scenario.

Implements: lockstep-projection/the-pytest-plugin-ships-as-a-pytest11-entry-point

Requirement text (generated):
    lockstep-projection/the-pytest-plugin-ships-as-a-pytest11-entry-point: Installing Lockstep SHALL
        register the `req` marker with pytest through a `pytest11` entry point
        (`lockstep.checks.plugin`), and registering it SHALL stay compatible with a project that
        also declares `req` in its own pytest configuration.
"""


def pytest_configure(config: object) -> None:
    """Register the `req` marker so pytest does not warn about it.

    Args:
        config: The pytest config object.
    """
    config.addinivalue_line(  # type: ignore[attr-defined]
        "markers", 'req(id, existing=False): the OpenSpec scenario this test verifies, as "<capability>/<scenario-slug>"; '
        "existing=True when the behavior already existed before the scenario was written"
    )
