"""pytest plugin that registers the `req` marker linking a test to an OpenSpec scenario.

Implements: lockstep-projection/the-pytest-plugin-ships-as-a-pytest11-entry-point

Requirement text (generated):
    lockstep-projection/the-pytest-plugin-ships-as-a-pytest11-entry-point: Installing Lockstep SHALL
        register the `req` marker with pytest through a `pytest11` entry point
        (`lockstep.checks.plugin`), and registering it SHALL stay compatible with a project that
        also declares `req` in its own pytest configuration.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:plugin.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-projection/the-pytest-plugin-ships-as-a-pytest11-entry-point

### Requirement: The pytest plugin ships as a pytest11 entry point

Installing Lockstep SHALL register the `req` marker with pytest through a `pytest11` entry point (`lockstep.checks.plugin`), and registering it SHALL stay compatible with a project that also declares `req` in its own pytest configuration.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: The plugin registers the req marker

- **GIVEN** Lockstep is installed
- **WHEN** pytest starts with `--strict-markers`
- **THEN** tests marked `req` run, with or without the project's own declaration

Tested by: tests/lockstep/checks/test_lockstep_check_plugin.py
[[[end]]]
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
