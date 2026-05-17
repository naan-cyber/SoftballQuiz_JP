from __future__ import annotations

from collections import Counter

from softball_quiz.data.battery_questions import CATCHER_QUESTIONS, PITCHER_QUESTIONS
from softball_quiz.data.infield_questions import INFIELD_QUESTIONS
from softball_quiz.data.outfield_questions import OUTFIELD_QUESTIONS
from softball_quiz.models import DefensivePosition, POSITION_ORDER, QuizQuestion


QUESTIONS: tuple[QuizQuestion, ...] = (
    *PITCHER_QUESTIONS,
    *CATCHER_QUESTIONS,
    *INFIELD_QUESTIONS,
    *OUTFIELD_QUESTIONS,
)


def questions_for_position(position: DefensivePosition | None) -> tuple[QuizQuestion, ...]:
    if position is None:
        return QUESTIONS
    return tuple(question for question in QUESTIONS if question.scenario.position == position)


def question_counts_by_position() -> dict[DefensivePosition, int]:
    counts = Counter(question.scenario.position for question in QUESTIONS)
    return {position: counts[position] for position in POSITION_ORDER}
