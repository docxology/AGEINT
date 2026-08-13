"""One injectable source of "now" for every generated artifact.

Ten report modules previously called ``datetime.now(timezone.utc)`` directly, so
every regeneration wrote a fresh ``generated_at`` and any date-relative figure
recomputed against the wall clock. Two consequences, both observed on this repo:

* Committed reports rot on their own. Between 2026-08-03 and 2026-08-12
  ``output/reports/source_refresh_due.md`` moved ``Current 445 -> 431`` and
  ``Due soon 27 -> 41`` with no source change, because anchors aged past their
  refresh thresholds. The figure that renders that data changed too
  (``302267 -> 301875`` bytes) — content drift, not renderer nondeterminism.
* Because *every* rebuild differs, the freshness checks that compare a fresh
  build against the committed tree cannot separate real drift from clock noise,
  which is why those gates report drift on every run.

Routing all of it through here makes a generated artifact a pure function of
(source, build instant), so pinning the instant makes a rebuild byte-comparable.

``SOURCE_DATE_EPOCH`` is the cross-ecosystem reproducible-builds convention
(https://reproducible-builds.org/docs/source-date-epoch/) rather than a
project-specific variable, so the same pin works for other tooling. When it is
unset the clock is the real one, so interactive builds are unchanged.
"""

from __future__ import annotations

import os
from datetime import date, datetime, timezone

SOURCE_DATE_EPOCH_ENV = "SOURCE_DATE_EPOCH"


def build_datetime() -> datetime:
    """Return the build instant as an aware UTC datetime.

    Reads ``SOURCE_DATE_EPOCH`` (seconds since the Unix epoch) when set to a
    non-empty value, otherwise the current time.

    A malformed value raises rather than falling back to the wall clock: the
    caller asked for a reproducible build and silently giving them a
    non-reproducible one would defeat the point, and the reproducible-builds
    specification requires erroring out.
    """
    raw = os.environ.get(SOURCE_DATE_EPOCH_ENV)
    if raw is None or not raw.strip():
        return datetime.now(timezone.utc)

    text = raw.strip()
    try:
        epoch = int(text)
    except ValueError as exc:
        raise ValueError(
            f"{SOURCE_DATE_EPOCH_ENV} must be an integer number of seconds "
            f"since the Unix epoch; got {raw!r}"
        ) from exc
    if epoch < 0:
        raise ValueError(
            f"{SOURCE_DATE_EPOCH_ENV} must not be negative; got {epoch}"
        )
    return datetime.fromtimestamp(epoch, tz=timezone.utc)


def build_timestamp() -> str:
    """Return the build instant as a second-precision ISO-8601 string."""
    return build_datetime().isoformat(timespec="seconds")


def build_date() -> date:
    """Return the build instant's UTC date, for date-relative report fields."""
    return build_datetime().date()
