from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Difficulty(str, Enum):
    BASIC = "やさしい"
    INTERMEDIATE = "ちょいむず"


class DefensivePosition(str, Enum):
    PITCHER = "pitcher"
    CATCHER = "catcher"
    FIRST_BASE = "first_base"
    SECOND_BASE = "second_base"
    THIRD_BASE = "third_base"
    SHORTSTOP = "shortstop"
    LEFT_FIELD = "left_field"
    CENTER_FIELD = "center_field"
    RIGHT_FIELD = "right_field"

    @property
    def label(self) -> str:
        return {
            DefensivePosition.PITCHER: "ピッチャー",
            DefensivePosition.CATCHER: "キャッチャー",
            DefensivePosition.FIRST_BASE: "一るい",
            DefensivePosition.SECOND_BASE: "二るい",
            DefensivePosition.THIRD_BASE: "三るい",
            DefensivePosition.SHORTSTOP: "ショート",
            DefensivePosition.LEFT_FIELD: "レフト",
            DefensivePosition.CENTER_FIELD: "センター",
            DefensivePosition.RIGHT_FIELD: "ライト",
        }[self]


POSITION_ORDER: tuple[DefensivePosition, ...] = (
    DefensivePosition.PITCHER,
    DefensivePosition.CATCHER,
    DefensivePosition.FIRST_BASE,
    DefensivePosition.SECOND_BASE,
    DefensivePosition.THIRD_BASE,
    DefensivePosition.SHORTSTOP,
    DefensivePosition.LEFT_FIELD,
    DefensivePosition.CENTER_FIELD,
    DefensivePosition.RIGHT_FIELD,
)


class RunnerRole(str, Enum):
    BATTER_RUNNER = "batter_runner"
    FIRST_RUNNER = "first_runner"
    SECOND_RUNNER = "second_runner"
    THIRD_RUNNER = "third_runner"

    @property
    def label(self) -> str:
        return {
            RunnerRole.BATTER_RUNNER: "バッターランナー",
            RunnerRole.FIRST_RUNNER: "一るいランナー",
            RunnerRole.SECOND_RUNNER: "二るいランナー",
            RunnerRole.THIRD_RUNNER: "三るいランナー",
        }[self]


RUNNER_ROLE_ORDER: tuple[RunnerRole, ...] = (
    RunnerRole.BATTER_RUNNER,
    RunnerRole.FIRST_RUNNER,
    RunnerRole.SECOND_RUNNER,
    RunnerRole.THIRD_RUNNER,
)


class RuleTopic(str, Enum):
    OUTS = "outs"
    FORCE_TAG = "force_tag"
    FAIR_FOUL = "fair_foul"
    RUNNING_RULES = "running_rules"
    GAME_FLOW = "game_flow"

    @property
    def label(self) -> str:
        return {
            RuleTopic.OUTS: "アウト",
            RuleTopic.FORCE_TAG: "フォース・タッチ",
            RuleTopic.FAIR_FOUL: "フェア・ファウル",
            RuleTopic.RUNNING_RULES: "走るルール",
            RuleTopic.GAME_FLOW: "試合の流れ",
        }[self]


RULE_TOPIC_ORDER: tuple[RuleTopic, ...] = (
    RuleTopic.OUTS,
    RuleTopic.FORCE_TAG,
    RuleTopic.FAIR_FOUL,
    RuleTopic.RUNNING_RULES,
    RuleTopic.GAME_FLOW,
)


@dataclass(frozen=True)
class RunnerState:
    first: bool = False
    second: bool = False
    third: bool = False

    @property
    def occupied_bases(self) -> tuple[str, ...]:
        bases: list[str] = []
        if self.first:
            bases.append("一るい")
        if self.second:
            bases.append("二るい")
        if self.third:
            bases.append("三るい")
        return tuple(bases)

    @property
    def label(self) -> str:
        if not self.occupied_bases:
            return "ランナーなし"
        return "・".join(self.occupied_bases)


@dataclass(frozen=True)
class Scenario:
    outs: int
    runners: RunnerState
    batted_ball: str
    fielding_note: str
    position: DefensivePosition | None = None
    runner_role: RunnerRole | None = None
    rule_topic: RuleTopic | None = None
    difficulty: Difficulty = Difficulty.BASIC

    @property
    def outs_label(self) -> str:
        return f"{self.outs}アウト"

    @property
    def actor_label(self) -> str:
        if self.position is not None:
            return self.position.label
        if self.runner_role is not None:
            return self.runner_role.label
        if self.rule_topic is not None:
            return self.rule_topic.label
        return "ぜんぶ"


@dataclass(frozen=True)
class AnswerOption:
    id: str
    text: str
    is_correct: bool
    feedback: str


@dataclass(frozen=True)
class QuizQuestion:
    id: str
    scenario: Scenario
    prompt: str
    options: tuple[AnswerOption, ...]
    principle: str

    @property
    def correct_option(self) -> AnswerOption:
        correct = [option for option in self.options if option.is_correct]
        if len(correct) != 1:
            raise ValueError(f"Question {self.id} must have exactly one correct option.")
        return correct[0]
