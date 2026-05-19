from __future__ import annotations

from collections import Counter

from softball_quiz.data.battery_questions import CATCHER_QUESTIONS, PITCHER_QUESTIONS
from softball_quiz.data.defense_extra_questions import DEFENSE_EXTRA_QUESTIONS
from softball_quiz.data.infield_questions import INFIELD_QUESTIONS
from softball_quiz.data.outfield_questions import OUTFIELD_QUESTIONS
from softball_quiz.data.rule_questions import RULE_QUESTIONS
from softball_quiz.data.runner_questions import RUNNER_QUESTIONS
from softball_quiz.models import (
    DefensivePosition,
    POSITION_ORDER,
    RULE_TOPIC_ORDER,
    RUNNER_ROLE_ORDER,
    QuizQuestion,
    RuleTopic,
    RunnerRole,
)


QUESTIONS: tuple[QuizQuestion, ...] = (
    *PITCHER_QUESTIONS,
    *CATCHER_QUESTIONS,
    *INFIELD_QUESTIONS,
    *OUTFIELD_QUESTIONS,
    *DEFENSE_EXTRA_QUESTIONS,
    *RUNNER_QUESTIONS,
    *RULE_QUESTIONS,
)


def questions_for_position(position: DefensivePosition | None) -> tuple[QuizQuestion, ...]:
    if position is None:
        return QUESTIONS
    return tuple(question for question in QUESTIONS if question.scenario.position == position)


def questions_for_runner_role(role: RunnerRole | None) -> tuple[QuizQuestion, ...]:
    if role is None:
        return QUESTIONS
    return tuple(question for question in QUESTIONS if question.scenario.runner_role == role)


def questions_for_rule_topic(topic: RuleTopic | None) -> tuple[QuizQuestion, ...]:
    if topic is None:
        return QUESTIONS
    return tuple(question for question in QUESTIONS if question.scenario.rule_topic == topic)


def question_counts_by_position() -> dict[DefensivePosition, int]:
    counts = Counter(question.scenario.position for question in QUESTIONS)
    return {position: counts[position] for position in POSITION_ORDER}


def question_counts_by_runner_role() -> dict[RunnerRole, int]:
    counts = Counter(question.scenario.runner_role for question in QUESTIONS)
    return {role: counts[role] for role in RUNNER_ROLE_ORDER}


def question_counts_by_rule_topic() -> dict[RuleTopic, int]:
    counts = Counter(question.scenario.rule_topic for question in QUESTIONS)
    return {topic: counts[topic] for topic in RULE_TOPIC_ORDER}
