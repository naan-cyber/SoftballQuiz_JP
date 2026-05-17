import random
import unittest

from softball_quiz.data import QUESTIONS, question_counts_by_position, questions_for_position
from softball_quiz.models import POSITION_ORDER
from softball_quiz.services import QuizEngine
from softball_quiz.ui.kids_text import kids_text


class QuestionDataTest(unittest.TestCase):
    def test_each_question_has_exactly_one_correct_answer(self) -> None:
        for question in QUESTIONS:
            self.assertEqual(
                1,
                sum(option.is_correct for option in question.options),
                msg=question.id,
            )

    def test_question_ids_are_unique(self) -> None:
        ids = [question.id for question in QUESTIONS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_question_bank_has_enough_variation(self) -> None:
        self.assertGreaterEqual(len(QUESTIONS), 55)

    def test_each_position_has_questions(self) -> None:
        counts = question_counts_by_position()
        for position in POSITION_ORDER:
            self.assertGreaterEqual(counts[position], 6, msg=position.value)

    def test_filter_returns_only_selected_position(self) -> None:
        for position in POSITION_ORDER:
            questions = questions_for_position(position)
            self.assertTrue(questions, msg=position.value)
            self.assertTrue(
                all(question.scenario.position == position for question in questions),
                msg=position.value,
            )

    def test_cover_questions_are_anticipatory(self) -> None:
        cover_questions = [
            question
            for question in QUESTIONS
            if "cover" in question.id or "backup" in question.id
        ]
        self.assertTrue(cover_questions)

        for question in cover_questions:
            scenario_text = f"{question.scenario.batted_ball} {question.scenario.fielding_note}"
            self.assertNotIn("ボールがなげられた", scenario_text, msg=question.id)

            correct = question.correct_option
            guidance_text = f"{correct.text} {correct.feedback} {question.principle}"
            self.assertTrue(
                any(word in guidance_text for word in ("先", "見", "予想", "そなえ", "時点", "回り")),
                msg=question.id,
            )


class QuizEngineTest(unittest.TestCase):
    def test_correct_answer_increments_score_once(self) -> None:
        engine = QuizEngine(QUESTIONS, shuffle=False)
        correct = engine.current_question.correct_option

        self.assertTrue(engine.select_answer(correct.id))
        self.assertEqual(1, engine.score)

        engine.select_answer(correct.id)
        self.assertEqual(1, engine.score)

    def test_next_question_requires_answer(self) -> None:
        engine = QuizEngine(QUESTIONS, shuffle=False)

        self.assertFalse(engine.move_next())
        self.assertEqual(1, engine.current_number)

    def test_reset_clears_progress(self) -> None:
        engine = QuizEngine(QUESTIONS, shuffle=False, rng=random.Random(1))
        engine.select_answer(engine.current_question.correct_option.id)
        engine.move_next()

        engine.reset()

        self.assertEqual(0, engine.score)
        self.assertEqual(1, engine.current_number)
        self.assertIsNone(engine.selected_option_id)


class KidsTextTest(unittest.TestCase):
    def test_does_not_duplicate_force_explanation(self) -> None:
        text = kids_text("フォースアウト（ふむだけのアウト）をねらう")
        self.assertEqual("フォースアウト（ふむだけのアウト）をねらう", text)


if __name__ == "__main__":
    unittest.main()
