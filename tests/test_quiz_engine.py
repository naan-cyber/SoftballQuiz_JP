import random
import unittest

from softball_quiz.data import (
    QUESTIONS,
    question_counts_by_position,
    question_counts_by_rule_topic,
    question_counts_by_runner_role,
    questions_for_position,
    questions_for_rule_topic,
    questions_for_runner_role,
)
from softball_quiz.models import POSITION_ORDER, RULE_TOPIC_ORDER, RUNNER_ROLE_ORDER
from softball_quiz.services import QuizEngine
from softball_quiz.ui.components import FieldDiagram
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

    def test_each_runner_role_has_questions(self) -> None:
        counts = question_counts_by_runner_role()
        for role in RUNNER_ROLE_ORDER:
            self.assertGreaterEqual(counts[role], 6, msg=role.value)

    def test_each_rule_topic_has_questions(self) -> None:
        counts = question_counts_by_rule_topic()
        for topic in RULE_TOPIC_ORDER:
            self.assertGreaterEqual(counts[topic], 5, msg=topic.value)

    def test_filter_returns_only_selected_position(self) -> None:
        for position in POSITION_ORDER:
            questions = questions_for_position(position)
            self.assertTrue(questions, msg=position.value)
            self.assertTrue(
                all(question.scenario.position == position for question in questions),
                msg=position.value,
            )

    def test_runner_filter_returns_only_selected_role(self) -> None:
        for role in RUNNER_ROLE_ORDER:
            questions = questions_for_runner_role(role)
            self.assertTrue(questions, msg=role.value)
            self.assertTrue(
                all(question.scenario.runner_role == role for question in questions),
                msg=role.value,
            )

    def test_rule_filter_returns_only_selected_topic(self) -> None:
        for topic in RULE_TOPIC_ORDER:
            questions = questions_for_rule_topic(topic)
            self.assertTrue(questions, msg=topic.value)
            self.assertTrue(
                all(question.scenario.rule_topic == topic for question in questions),
                msg=topic.value,
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

    def test_hit_locations_stay_inside_fair_lines(self) -> None:
        diagram = FieldDiagram()
        hit_words = ("ヒット", "ライト前", "レフト前", "センター前", "左中間", "右中間", "外野の間")
        hit_questions = [
            question
            for question in QUESTIONS
            if any(word in f"{question.scenario.batted_ball} {question.scenario.fielding_note}" for word in hit_words)
        ]
        self.assertTrue(hit_questions)

        for question in hit_questions:
            text = f"{question.scenario.batted_ball} {question.scenario.fielding_note}"
            if "ファウル" in text or "ラインの外" in text:
                continue
            point = diagram._location_point(text)
            self.assertIsNotNone(point, msg=question.id)
            self.assertTrue(self._is_inside_fair_lines(point), msg=(question.id, point, text))

    def test_short_foul_before_first_stops_on_first_base_line(self) -> None:
        diagram = FieldDiagram()
        point = diagram._location_point("打球が1るいより手前で、ラインの外に止まった")

        self.assertEqual((204, 212), point)
        self.assertTrue(self._is_inside_fair_lines(point))

    def test_foul_line_fair_question_stops_on_first_base_line(self) -> None:
        diagram = FieldDiagram()
        question = next(question for question in QUESTIONS if question.id == "rule-foul-line-is-fair")

        point = diagram._location_point(question.scenario.batted_ball)

        self.assertEqual((204, 212), point)
        self.assertTrue(self._is_inside_fair_lines(point))

    def test_outfield_foul_fly_lands_outside_fair_lines(self) -> None:
        diagram = FieldDiagram()
        point = diagram._location_point("外野フライがファウルラインの外に落ちた")

        self.assertEqual((328, 84), point)
        self.assertFalse(self._is_inside_fair_lines(point))

    def test_past_first_base_then_foul_lands_outside_first_base_line(self) -> None:
        diagram = FieldDiagram()
        question = next(question for question in QUESTIONS if question.id == "rule-past-base-then-foul")

        point = diagram._location_point(question.scenario.batted_ball)

        self.assertEqual((328, 84), point)
        self.assertFalse(self._is_inside_fair_lines(point))

    def test_throw_scenarios_show_possession_instead_of_destination(self) -> None:
        diagram = FieldDiagram()

        self.assertEqual(
            (92, 122),
            diagram._possession_point("ショートから1るいへボールがなげられた", None),
        )
        self.assertEqual(
            (160, 300),
            diagram._possession_point("キャッチャーが2るいへなげようとしている", None),
        )
        self.assertEqual(
            "ボール: 守る人が持つ",
            diagram.ball_summary(
                "ショートから1るいへボールがなげられた",
                "バッターランナーが1るいへ走ってくる。",
                None,
            ),
        )

    def test_first_base_near_grounder_is_drawn_near_first_base(self) -> None:
        diagram = FieldDiagram()

        self.assertEqual((212, 174), diagram._location_point("1るいの近くへゴロ"))
        self.assertEqual(
            (212, 174),
            diagram._location_point("ファースト正面の強いゴロ ショートが2るいに入った。"),
        )

    def test_ball_visual_locations_match_common_text_patterns(self) -> None:
        diagram = FieldDiagram()

        self.assertEqual((160, 166), diagram._location_point("ピッチャー前のゆるいゴロ"))
        self.assertEqual((112, 130), diagram._location_point("ショートの左へゴロ。2るいランナーが3るいへ走りそう"))
        self.assertEqual((104, 174), diagram._location_point("3るい手前の強いゴロ 満るい。本るいへなげても間に合う強さ。"))
        self.assertEqual((203, 126), diagram._location_point("ランナーが1るいと2るいの間で止まった"))
        self.assertEqual((160, 58), diagram._location_point("バッターが高いフライを打った"))
        self.assertEqual(
            (160, 300),
            diagram._possession_point("ピッチャーのボールをとったあと、1るいランナーが2るいへ走った", None),
        )

    def test_ball_path_colors_are_consistent_by_kind(self) -> None:
        diagram = FieldDiagram()

        self.assertEqual(("フライ", "まだ空中", FieldDiagram.FLY_COLOR), diagram._ball_style("フライが上がった", is_throw=False))
        self.assertEqual(("ライナー", "まだ空中", FieldDiagram.LINER_COLOR), diagram._ball_style("ライナーが飛んだ", is_throw=False))
        self.assertEqual(("ゴロ", "地面", FieldDiagram.GROUND_COLOR), diagram._ball_style("ゴロが転がった", is_throw=False))
        self.assertEqual(("返球", "ボールが向かう", FieldDiagram.THROW_COLOR), diagram._ball_style("返球", is_throw=True))

    def test_uncaught_paths_are_dashed_and_caught_paths_are_solid(self) -> None:
        diagram = FieldDiagram()
        start = (160, 255)
        end = (160, 58)

        uncaught = diagram._path_controls(start, end, FieldDiagram.FLY_COLOR, "フライ", False, solid=False)
        caught = diagram._path_controls(start, end, FieldDiagram.FLY_COLOR, "フライ", False, solid=True)

        self.assertGreater(len(uncaught), 10)
        self.assertGreater(len(caught), len(uncaught))
        self.assertTrue(diagram._is_caught_state("とられた"))
        self.assertFalse(diagram._is_caught_state("まだ空中"))

    def test_grounder_path_uses_small_connected_bounces(self) -> None:
        diagram = FieldDiagram()
        start = (160, 255)
        end = (212, 174)

        points = [
            diagram._grounder_bounce_point(start, end, index / 32)
            for index in range(33)
        ]

        self.assertEqual(start, points[0])
        self.assertAlmostEqual(end[0], points[-1][0])
        self.assertAlmostEqual(end[1], points[-1][1])
        self.assertTrue(any(0 < abs(point[0] - diagram._line_point(start, end, index / 32)[0]) < 5 for index, point in enumerate(points[1:-1], start=1)))

    def _is_inside_fair_lines(self, point: tuple[int, int] | None) -> bool:
        if point is None:
            return False
        x, y = point
        if y < 108:
            return 8 <= x <= 312
        if y > 255:
            return False
        ratio = (255 - y) / (255 - 108)
        left_line = 160 + (8 - 160) * ratio
        right_line = 160 + (312 - 160) * ratio
        return left_line <= x <= right_line


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

    def test_options_are_shuffled_without_breaking_correct_answer(self) -> None:
        engine = QuizEngine(QUESTIONS, shuffle=False, rng=random.Random(1))
        original_option_ids = [option.id for option in QUESTIONS[0].options]
        shown_option_ids = [option.id for option in engine.current_question.options]

        self.assertCountEqual(original_option_ids, shown_option_ids)
        self.assertNotEqual(original_option_ids, shown_option_ids)
        self.assertTrue(engine.select_answer(engine.current_question.correct_option.id))


class KidsTextTest(unittest.TestCase):
    def test_does_not_duplicate_force_explanation(self) -> None:
        text = kids_text("フォースアウト（ふむだけのアウト）をねらう")
        self.assertEqual("フォースアウト（ふむだけのアウト）をねらう", text)


if __name__ == "__main__":
    unittest.main()
