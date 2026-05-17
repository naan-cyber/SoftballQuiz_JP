from __future__ import annotations

import random
from dataclasses import dataclass

from softball_quiz.models import AnswerOption, QuizQuestion


@dataclass(frozen=True)
class AnswerRecord:
    question_id: str
    selected_option_id: str
    is_correct: bool


class QuizEngine:
    def __init__(
        self,
        questions: tuple[QuizQuestion, ...],
        *,
        shuffle: bool = True,
        rng: random.Random | None = None,
    ) -> None:
        if not questions:
            raise ValueError("QuizEngine requires at least one question.")
        self._source_questions = questions
        self._rng = rng or random.Random()
        self._shuffle = shuffle
        self._questions: list[QuizQuestion] = []
        self._index = 0
        self._score = 0
        self._selected_option_id: str | None = None
        self._records: list[AnswerRecord] = []
        self.reset()

    @property
    def total(self) -> int:
        return len(self._questions)

    @property
    def current_number(self) -> int:
        return min(self._index + 1, self.total)

    @property
    def current_question(self) -> QuizQuestion:
        return self._questions[self._index]

    @property
    def score(self) -> int:
        return self._score

    @property
    def selected_option_id(self) -> str | None:
        return self._selected_option_id

    @property
    def answered(self) -> bool:
        return self._selected_option_id is not None

    @property
    def is_finished(self) -> bool:
        return self._index >= self.total - 1 and self.answered

    @property
    def progress(self) -> float:
        completed = self._index + (1 if self.answered else 0)
        return completed / self.total

    @property
    def records(self) -> tuple[AnswerRecord, ...]:
        return tuple(self._records)

    def reset(self) -> None:
        self._questions = list(self._source_questions)
        if self._shuffle:
            self._rng.shuffle(self._questions)
        self._index = 0
        self._score = 0
        self._selected_option_id = None
        self._records = []

    def select_answer(self, option_id: str) -> bool:
        if self.answered:
            return self.selected_option.is_correct

        option = self._find_option(option_id)
        self._selected_option_id = option.id
        if option.is_correct:
            self._score += 1
        self._records.append(
            AnswerRecord(
                question_id=self.current_question.id,
                selected_option_id=option.id,
                is_correct=option.is_correct,
            )
        )
        return option.is_correct

    def move_next(self) -> bool:
        if not self.answered:
            return False
        if self._index >= self.total - 1:
            return False
        self._index += 1
        self._selected_option_id = None
        return True

    @property
    def selected_option(self) -> AnswerOption:
        if self._selected_option_id is None:
            raise ValueError("No answer selected.")
        return self._find_option(self._selected_option_id)

    def _find_option(self, option_id: str) -> AnswerOption:
        for option in self.current_question.options:
            if option.id == option_id:
                return option
        raise ValueError(f"Unknown option id: {option_id}")
