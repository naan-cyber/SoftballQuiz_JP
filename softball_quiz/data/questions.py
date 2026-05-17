from __future__ import annotations

from collections import Counter

from softball_quiz.data.battery_questions import CATCHER_QUESTIONS, PITCHER_QUESTIONS
from softball_quiz.data.infield_questions import INFIELD_QUESTIONS
from softball_quiz.data.outfield_questions import OUTFIELD_QUESTIONS
from softball_quiz.data.runner_questions import RUNNER_QUESTIONS
from softball_quiz.models import (
    DefensivePosition,
    POSITION_ORDER,
    RUNNER_ROLE_ORDER,
    QuizQuestion,
    RunnerRole,
)


QUESTIONS: tuple[QuizQuestion, ...] = (
    *PITCHER_QUESTIONS,
    *CATCHER_QUESTIONS,
    *INFIELD_QUESTIONS,
    *OUTFIELD_QUESTIONS,
    *RUNNER_QUESTIONS,
)


def questions_for_position(position: DefensivePosition | None) -> tuple[QuizQuestion, ...]:
    if position is None:
        return QUESTIONS
    return tuple(question for question in QUESTIONS if question.scenario.position == position)


def questions_for_runner_role(role: RunnerRole | None) -> tuple[QuizQuestion, ...]:
    if role is None:
        return QUESTIONS
    return tuple(question for question in QUESTIONS if question.scenario.runner_role == role)


def question_counts_by_position() -> dict[DefensivePosition, int]:
    counts = Counter(question.scenario.position for question in QUESTIONS)
    return {position: counts[position] for position in POSITION_ORDER}


def question_counts_by_runner_role() -> dict[RunnerRole, int]:
    counts = Counter(question.scenario.runner_role for question in QUESTIONS)
    return {role: counts[role] for role in RUNNER_ROLE_ORDER}
