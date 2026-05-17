from __future__ import annotations

from collections.abc import Sequence

from softball_quiz.models import (
    AnswerOption,
    DefensivePosition,
    Difficulty,
    QuizQuestion,
    RunnerRole,
    RunnerState,
    Scenario,
)

OptionSpec = tuple[str, bool, str]


def make_question(
    *,
    question_id: str,
    outs: int,
    runners: RunnerState,
    ball: str,
    note: str,
    options: Sequence[OptionSpec],
    point: str,
    position: DefensivePosition | None = None,
    runner_role: RunnerRole | None = None,
    prompt: str = "あなたがまずやることは？",
    difficulty: Difficulty = Difficulty.BASIC,
) -> QuizQuestion:
    if (position is None) == (runner_role is None):
        raise ValueError("Set exactly one of position or runner_role.")

    option_ids = ("a", "b", "c", "d")
    return QuizQuestion(
        id=question_id,
        scenario=Scenario(
            outs=outs,
            runners=runners,
            batted_ball=ball,
            fielding_note=note,
            position=position,
            runner_role=runner_role,
            difficulty=difficulty,
        ),
        prompt=prompt,
        options=tuple(
            AnswerOption(id=option_id, text=text, is_correct=is_correct, feedback=feedback)
            for option_id, (text, is_correct, feedback) in zip(option_ids, options)
        ),
        principle=point,
    )
