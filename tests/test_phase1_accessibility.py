from datetime import date
from pathlib import Path

from anki_alive.ui.expedition import render_today


def test_today_core_actions_keep_native_keyboard_semantics() -> None:
    html = render_today(
        study_date=date(2026, 8, 19),
        context_name="Test deck",
        due_reviews=6,
        proposed_target=6,
        expedition=None,
        focus_mode=False,
        reduced_motion=False,
    )

    assert 'type="button"' in html
    assert "Begin Expedition" in html
    assert "Focus mode · Off" in html
    assert 'aria-pressed="false"' in html
    assert 'tabindex="-1"' not in html


def test_focus_mode_and_reduced_motion_are_explicit_in_today_projection() -> None:
    html = render_today(
        study_date=date(2026, 8, 19),
        context_name="Test deck",
        due_reviews=6,
        proposed_target=6,
        expedition=None,
        focus_mode=True,
        reduced_motion=True,
    )

    assert 'data-focus-mode="true"' in html
    assert 'data-reduced-motion="true"' in html
    assert "Focus mode · On" in html
    assert 'aria-pressed="true"' in html


def test_phase1_css_keeps_focus_visible_and_motion_optional() -> None:
    root = Path(__file__).parents[1]
    foundation = (root / "anki_alive" / "ui" / "foundation.css").read_text(
        encoding="utf-8"
    )
    expedition = (root / "anki_alive" / "ui" / "expedition.css").read_text(
        encoding="utf-8"
    )

    assert ":focus-visible" in foundation
    assert 'data-focus-mode="true"' in foundation
    assert 'data-reduced-motion="true"' in foundation
    assert "prefers-reduced-motion: reduce" in foundation
    assert "animation-iteration-count: 1" in foundation
    assert '.aa-review-strip[data-focus-mode="true"]' in expedition
    assert '.anki-alive[data-reduced-motion="true"].aa-today' in expedition
    assert "animation: none" in expedition
