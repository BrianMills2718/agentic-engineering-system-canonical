import pytest

from people_finder import find_people


def test_returns_current_employees_only():
    handles = {p["handle"] for p in find_people("Northwind Robotics")}
    assert handles == {"@ada_builds", "@lin_ships", "@noor_ml"}  # lower-case employer included
    assert "@kai_former" not in handles  # former employee excluded


def test_empty_company_is_rejected():
    with pytest.raises(ValueError):
        find_people("  ")
