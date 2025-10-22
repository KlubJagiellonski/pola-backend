import pytest

from pola.company.factories import CompanyFactory
from pola.company.views import _find_best_company_id, _is_value_set


def test_is_value_set_basic_cases():
    # None and empty/whitespace-only strings are not set
    assert _is_value_set(None) is False
    assert _is_value_set("") is False
    assert _is_value_set("   ") is False

    # Non-empty strings are set
    assert _is_value_set("x") is True

    # Non-string, non-None values are considered set
    assert _is_value_set(0) is True
    assert _is_value_set(False) is True
    assert _is_value_set(0.0) is True


@pytest.mark.django_db
def test_find_best_company_id_picks_highest_score():
    # Very few fields set (override factory defaults to empty where applicable)
    c1 = CompanyFactory(name="", official_name="", common_name="", description="")

    # Default factory has several string fields set
    c2 = CompanyFactory()

    # Many fields set to maximize score
    c3 = CompanyFactory(
        address="Some address",
        plCapital=100,
        plCapital_notes="note",
        plRnD=100,
        plRnD_notes="note",
        plWorkers=100,
        plWorkers_notes="note",
        plNotGlobEnt=100,
        plNotGlobEnt_notes="note",
        plRegistered=100,
        plRegistered_notes="note",
        description="desc",
        # verified and is_friend default to False which still count as set
    )

    companies = {c1.id: c1, c2.id: c2, c3.id: c3, -1: None}
    best = _find_best_company_id(companies)
    assert best == c3.id


@pytest.mark.django_db
def test_find_best_company_id_tie_returns_first_inserted():
    # Two companies with similar default-filled fields (tie)
    a = CompanyFactory()
    b = CompanyFactory()
    companies = {a.id: a, b.id: b}
    best = _find_best_company_id(companies)
    assert best == a.id


def test_find_best_company_id_empty_or_none_only():
    assert _find_best_company_id({}) is None
    assert _find_best_company_id({1: None, 2: None}) is None
