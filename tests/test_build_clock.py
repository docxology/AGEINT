"""Tests for the injectable build clock behind every generated artifact."""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest

from build_clock import (
    SOURCE_DATE_EPOCH_ENV,
    build_date,
    build_datetime,
    build_timestamp,
)

# A fixed instant on AGEINT's v0.1 release date (2026-06-17), so a failure
# message points at a recognisable moment rather than an arbitrary number. The
# pair is asserted literally in both directions below, which is what caught an
# earlier mismatched constant here.
PINNED_EPOCH = 1781699696
PINNED_ISO = "2026-06-17T12:34:56+00:00"


def test_unset_epoch_uses_the_real_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(SOURCE_DATE_EPOCH_ENV, raising=False)
    before = datetime.now(timezone.utc)
    observed = build_datetime()
    after = datetime.now(timezone.utc)

    assert before <= observed <= after
    assert observed.tzinfo is timezone.utc


def test_pinned_epoch_is_honoured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(SOURCE_DATE_EPOCH_ENV, str(PINNED_EPOCH))
    assert build_datetime() == datetime.fromtimestamp(PINNED_EPOCH, tz=timezone.utc)


def test_pinned_epoch_makes_repeated_reads_identical(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The whole point: two builds of the same source must agree on "now".
    monkeypatch.setenv(SOURCE_DATE_EPOCH_ENV, str(PINNED_EPOCH))
    assert build_timestamp() == build_timestamp()
    assert build_date() == build_date()


def test_surrounding_whitespace_is_tolerated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(SOURCE_DATE_EPOCH_ENV, f"  {PINNED_EPOCH}  ")
    assert build_datetime() == datetime.fromtimestamp(PINNED_EPOCH, tz=timezone.utc)


@pytest.mark.parametrize("blank", ["", "   ", "\t"])
def test_blank_epoch_falls_back_to_the_real_clock(
    monkeypatch: pytest.MonkeyPatch, blank: str
) -> None:
    # An exported-but-empty variable is a common shell accident and must not be
    # read as "epoch 0" (1970), which would silently backdate every report.
    monkeypatch.setenv(SOURCE_DATE_EPOCH_ENV, blank)
    assert build_datetime().year >= 2026


@pytest.mark.parametrize("bad", ["not-a-number", "2026-06-17", "12.5", "1e9"])
def test_malformed_epoch_raises_rather_than_silently_drifting(
    monkeypatch: pytest.MonkeyPatch, bad: str
) -> None:
    monkeypatch.setenv(SOURCE_DATE_EPOCH_ENV, bad)
    with pytest.raises(ValueError, match=SOURCE_DATE_EPOCH_ENV):
        build_datetime()


def test_negative_epoch_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(SOURCE_DATE_EPOCH_ENV, "-1")
    with pytest.raises(ValueError, match="must not be negative"):
        build_datetime()


def test_timestamp_is_second_precision_iso(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(SOURCE_DATE_EPOCH_ENV, str(PINNED_EPOCH))
    stamp = build_timestamp()

    assert stamp == PINNED_ISO
    assert stamp.endswith("+00:00")
    assert "." not in stamp  # no microseconds, so reports stay diff-stable


def test_build_date_is_the_utc_date_of_the_instant(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(SOURCE_DATE_EPOCH_ENV, str(PINNED_EPOCH))
    observed = build_date()

    assert isinstance(observed, date)
    assert observed == datetime.fromtimestamp(PINNED_EPOCH, tz=timezone.utc).date()
