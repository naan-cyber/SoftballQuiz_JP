from __future__ import annotations

from collections.abc import Sequence

from softball_quiz.models import (
    AnswerOption,
    DefensivePosition,
    Difficulty,
    QuizQuestion,
    RuleTopic,
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
    rule_topic: RuleTopic | None = None,
    prompt: str = "あなたがまずやることは？",
    difficulty: Difficulty = Difficulty.BASIC,
) -> QuizQuestion:
    actor_count = sum(actor is not None for actor in (position, runner_role, rule_topic))
    if actor_count != 1:
        raise ValueError("Set exactly one of position, runner_role, or rule_topic.")

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
            rule_topic=rule_topic,
            difficulty=difficulty,
        ),
        prompt=prompt,
        options=tuple(
            AnswerOption(id=option_id, text=text, is_correct=is_correct, feedback=feedback)
            for option_id, (text, is_correct, feedback) in zip(option_ids, options)
        ),
        principle=point,
    )
