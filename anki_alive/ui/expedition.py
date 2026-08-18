from __future__ import annotations

from datetime import date
from html import escape

from anki_alive.expedition.model import (
    Expedition,
    ExpeditionCheckpoint,
    ExpeditionStatus,
    checkpoint_targets,
)
from anki_alive.expedition.viewmodel import ExpeditionView, build_expedition_view


def _bool_attr(value: bool) -> str:
    return "true" if value else "false"


def _format_study_date(value: date) -> str:
    return value.strftime("%d %b %Y")


def _checkpoint_nodes(view: ExpeditionView) -> str:
    nodes = []
    for checkpoint in view.checkpoints:
        label = (
            f"Checkpoint {checkpoint.ordinal}: "
            f"{checkpoint.target_progress} reviews, {checkpoint.state}"
        )
        completion_class = " aa-expedition-node--completion" if checkpoint.is_completion else ""
        nodes.append(
            (
                '<span class="aa-expedition-node'
                f' aa-expedition-node--{checkpoint.state}{completion_class}" '
                f'style="--aa-node-position:{checkpoint.position_percent:.3f}%;" '
                f'data-status="{escape(checkpoint.state)}" '
                f'data-status-label="{escape(label)}" '
                f'aria-label="{escape(label)}">'
                '<span class="aa-expedition-node__dot" aria-hidden="true"></span>'
                f'<span class="aa-expedition-node__value">{checkpoint.target_progress}</span>'
                "</span>"
            )
        )
    return "".join(nodes)


def render_expedition_track(view: ExpeditionView, *, compact: bool = False) -> str:
    compact_class = " aa-expedition-track--compact" if compact else ""
    next_text = (
        "Route closed"
        if view.closed_before_target
        else "Route complete"
        if view.reviews_to_next_checkpoint is None
        else f"{view.reviews_to_next_checkpoint} to next checkpoint"
    )
    return f"""
    <div class="aa-expedition-track{compact_class}"
         role="progressbar"
         aria-valuemin="0"
         aria-valuemax="{view.target_reviews}"
         aria-valuenow="{view.completed_reviews}"
         aria-label="Expedition progress: {view.completed_reviews} of {view.target_reviews} reviews">
      <div class="aa-expedition-track__rail" aria-hidden="true">
        <span class="aa-expedition-track__fill"
              style="--aa-progress:{view.progress_percent:.3f}%;"></span>
        <span class="aa-expedition-position"
              style="--aa-progress:{view.progress_percent:.3f}%;"></span>
        {_checkpoint_nodes(view)}
      </div>
      <div class="aa-expedition-track__meta">
        <span class="aa-type-metric">{view.completed_reviews} / {view.target_reviews}</span>
        <span class="aa-type-caption">{escape(next_text)}</span>
      </div>
    </div>
    """


def _preview_expedition(target_reviews: int) -> ExpeditionView:
    from datetime import datetime, timezone
    from uuid import UUID

    expedition = Expedition(
        expedition_id=UUID(int=0),
        profile_key="preview",
        local_study_date=datetime.now(timezone.utc).date(),
        status=ExpeditionStatus.PLANNED,
        created_at=datetime.now(timezone.utc),
        target_reviews=target_reviews,
    )
    checkpoints = tuple(
        ExpeditionCheckpoint(
            checkpoint_id=UUID(int=index),
            expedition_id=expedition.expedition_id,
            ordinal=index,
            target_progress=target,
        )
        for index, target in enumerate(checkpoint_targets(target_reviews), start=1)
    )
    return build_expedition_view(expedition, checkpoints)


def render_today(
    *,
    study_date: date,
    context_name: str,
    due_reviews: int,
    proposed_target: int | None,
    expedition: Expedition | None,
    checkpoints: tuple[ExpeditionCheckpoint, ...] = (),
    completed_summary: Expedition | None = None,
    completed_checkpoints: tuple[ExpeditionCheckpoint, ...] = (),
    focus_mode: bool,
    reduced_motion: bool,
) -> str:
    context_label = escape(context_name or "Current study context")
    date_label = escape(_format_study_date(study_date))
    focus_label = "On" if focus_mode else "Off"

    if completed_summary is not None:
        summary_view = build_expedition_view(completed_summary, completed_checkpoints)
        if summary_view.closed_before_target:
            completion_heading = "The available route is complete."
            completion_copy = (
                f"{summary_view.completed_reviews} reviews completed. "
                f"The planned target stayed {summary_view.target_reviews}; "
                "Anki had no eligible reviews left in this study context."
            )
        else:
            completion_heading = "The route is complete."
            completion_copy = (
                f"{summary_view.target_reviews} reviews completed across "
                f"{summary_view.total_checkpoints} checkpoints. "
                "The finish line stays finished."
            )
        expedition_content = f"""
          <p class="aa-type-ritual">EXPEDITION COMPLETE</p>
          <h2 class="aa-type-h2">{completion_heading}</h2>
          <p class="aa-type-body aa-copy-muted">{completion_copy}</p>
          {render_expedition_track(summary_view)}
          <div class="aa-action-row">
            <button class="aa-button aa-button--primary"
                    type="button"
                    onclick="return pycmd('anki-alive:expedition:done')">
              Done
            </button>
            <button class="aa-button aa-button--secondary"
                    type="button"
                    onclick="return pycmd('anki-alive:expedition:continue')">
              Continue reviewing
            </button>
          </div>
        """
        panel_class = " aa-expedition-panel--complete"
    elif expedition is not None:
        view = build_expedition_view(expedition, checkpoints)
        if expedition.status is ExpeditionStatus.PLANNED:
            heading = "Expedition ready"
            action = "Begin Expedition"
        else:
            heading = "Expedition in progress"
            action = "Resume Expedition"
        expedition_content = f"""
          <p class="aa-type-label aa-feature-label">Expedition</p>
          <h2 class="aa-type-h2">{heading}</h2>
          <p class="aa-type-body aa-copy-muted">
            A bounded route through your real Anki reviews. Every honest grade advances one step.
          </p>
          {render_expedition_track(view)}
          <div class="aa-action-row">
            <button class="aa-button aa-button--primary"
                    type="button"
                    onclick="return pycmd('anki-alive:expedition:resume')">
              {action}
            </button>
            <button class="aa-button aa-button--quiet"
                    type="button"
                    onclick="return pycmd('anki-alive:expedition:end')">
              End Expedition
            </button>
          </div>
        """
        panel_class = ""
    elif proposed_target is not None and proposed_target > 0:
        preview = _preview_expedition(proposed_target)
        expedition_content = f"""
          <p class="aa-type-label aa-feature-label">Expedition</p>
          <h2 class="aa-type-h2">A clear finish line</h2>
          <p class="aa-type-body aa-copy-muted">
            Begin a route of {proposed_target} reviews. Your Anki queue and scheduler stay unchanged.
          </p>
          {render_expedition_track(preview)}
          <div class="aa-action-row">
            <button class="aa-button aa-button--primary"
                    type="button"
                    onclick="return pycmd('anki-alive:expedition:begin')">
              Begin Expedition
            </button>
          </div>
        """
        panel_class = ""
    else:
        expedition_content = """
          <p class="aa-type-label aa-feature-label">Expedition</p>
          <h2 class="aa-type-h2">No route needed right now</h2>
          <p class="aa-type-body aa-copy-muted">
            There are no review actions due in this study context. Normal Anki controls remain available.
          </p>
        """
        panel_class = ""

    due_copy = "review due" if due_reviews == 1 else "reviews due"
    return f"""
    <section id="anki-alive-today"
             class="anki-alive aa-today"
             data-focus-mode="{_bool_attr(focus_mode)}"
             data-reduced-motion="{_bool_attr(reduced_motion)}"
             aria-labelledby="aa-today-title">
      <header class="aa-today__header">
        <div>
          <p class="aa-type-label aa-today__date">{date_label}</p>
          <h1 id="aa-today-title" class="aa-type-h1">Today</h1>
          <p class="aa-type-body aa-copy-muted">{context_label}</p>
        </div>
        <button class="aa-button aa-button--quiet aa-focus-toggle"
                type="button"
                aria-pressed="{_bool_attr(focus_mode)}"
                onclick="return pycmd('anki-alive:focus:toggle')">
          Focus mode · {focus_label}
        </button>
      </header>

      <div class="aa-today__primary">
        <section class="aa-memory-core" aria-labelledby="aa-memory-core-title">
          <div class="aa-memory-core__instrument" aria-hidden="true" data-ambient="true">
            <span class="aa-memory-core__ring aa-memory-core__ring--outer"></span>
            <span class="aa-memory-core__ring aa-memory-core__ring--inner"></span>
            <span class="aa-memory-core__center"></span>
          </div>
          <div class="aa-memory-core__copy">
            <p class="aa-type-label aa-feature-label">Memory core</p>
            <h2 id="aa-memory-core-title" class="aa-type-h2">Review queue</h2>
            <div class="aa-memory-core__metric">
              <span class="aa-type-metric-large">{due_reviews}</span>
              <span class="aa-type-body aa-copy-muted">{due_copy}</span>
            </div>
            <p class="aa-type-caption">
              This reflects your current Anki queue without judging memory quality.
            </p>
          </div>
        </section>

        <section class="aa-expedition-panel{panel_class}" aria-label="Expedition">
          {expedition_content}
        </section>
      </div>

      <section class="aa-signals" aria-labelledby="aa-signals-title">
        <div class="aa-section-heading">
          <h2 id="aa-signals-title" class="aa-type-h3">Today’s signals</h2>
          <span class="aa-type-caption">Quiet by default</span>
        </div>
        <div class="aa-empty-signal">
          <span class="aa-empty-signal__mark" aria-hidden="true"></span>
          <div>
            <p class="aa-type-body-strong">No additional signals right now.</p>
            <p class="aa-type-caption">
              The interface stays quiet until something meaningful changes.
            </p>
          </div>
        </div>
      </section>
    </section>
    """


def render_review_strip(
    expedition: Expedition,
    checkpoints: tuple[ExpeditionCheckpoint, ...],
    *,
    focus_mode: bool,
    reduced_motion: bool,
) -> str:
    view = build_expedition_view(expedition, checkpoints)
    next_text = (
        "Final segment"
        if view.reviews_to_next_checkpoint is None
        else f"Next · {view.reviews_to_next_checkpoint}"
    )
    return f"""
    <aside id="anki-alive-review-strip"
           class="anki-alive aa-review-strip"
           data-focus-mode="{_bool_attr(focus_mode)}"
           data-reduced-motion="{_bool_attr(reduced_motion)}"
           aria-label="Expedition progress">
      <div class="aa-review-strip__row">
        <span class="aa-type-label aa-review-strip__name">Expedition</span>
        <span id="aa-review-progress-value" class="aa-type-metric">
          {view.completed_reviews} / {view.target_reviews}
        </span>
        <span id="aa-review-progress-next" class="aa-type-caption">{escape(next_text)}</span>
      </div>
      <div class="aa-review-strip__rail"
           role="progressbar"
           aria-valuemin="0"
           aria-valuemax="{view.target_reviews}"
           aria-valuenow="{view.completed_reviews}">
        <span id="aa-review-progress-fill"
              class="aa-review-strip__fill"
              style="--aa-progress-ratio:{view.progress_percent / 100.0:.6f};"></span>
      </div>
      <div id="aa-review-progress-notice"
           class="aa-review-strip__notice aa-type-caption"
           aria-live="polite"></div>
    </aside>
    """
