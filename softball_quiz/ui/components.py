from __future__ import annotations

import math
from collections.abc import Callable

import flet as ft

from softball_quiz.models import (
    AnswerOption,
    DefensivePosition,
    POSITION_ORDER,
    RULE_TOPIC_ORDER,
    RUNNER_ROLE_ORDER,
    QuizQuestion,
    RuleTopic,
    RunnerRole,
    RunnerState,
)
from softball_quiz.ui import theme
from softball_quiz.ui.kids_text import kids_text


class HeaderBar:
    def render(
        self,
        *,
        current_number: int,
        total: int,
        score: int,
        progress: float,
        on_reset: Callable[[ft.Event[ft.Button]], None],
    ) -> ft.Control:
        return ft.Container(
            bgcolor=theme.PRIMARY_DARK,
            border_radius=theme.CARD_RADIUS,
            padding=ft.Padding(18, 16, 18, 16),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        theme.APP_TITLE,
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                    ft.Text(
                                        kids_text("まもる場所・走る人・アウト・ボールの動きを見て、はじめの動きをえらぶ"),
                                        size=13,
                                        color="#DCE9DF",
                                    ),
                                ],
                            ),
                            ft.Button(
                                content="はじめから",
                                icon=ft.Icons.REFRESH,
                                on_click=on_reset,
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                f"もんだい {current_number} / {total}",
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Text(
                                f"せいかい {score}",
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.W_600,
                            ),
                        ],
                    ),
                    ft.ProgressBar(
                        value=progress,
                        height=7,
                        color=theme.SECONDARY,
                        bgcolor="#346B58",
                    ),
                ],
            ),
        )


class PositionSelector:
    def render(
        self,
        *,
        selected_position: DefensivePosition | None,
        selected_runner_role: RunnerRole | None,
        selected_rule_topic: RuleTopic | None,
        position_counts: dict[DefensivePosition, int],
        runner_counts: dict[RunnerRole, int],
        rule_counts: dict[RuleTopic, int],
        on_select_all: Callable[[], None],
        on_select_position: Callable[[DefensivePosition | None], None],
        on_select_runner_role: Callable[[RunnerRole], None],
        on_select_rule_topic: Callable[[RuleTopic], None],
    ) -> ft.Control:
        all_selected = (
            selected_position is None
            and selected_runner_role is None
            and selected_rule_topic is None
        )
        all_count = sum(position_counts.values()) + sum(runner_counts.values()) + sum(rule_counts.values())
        all_buttons = [
            self._button(
                label="ぜんぶ",
                count=all_count,
                selected=all_selected,
                on_click=on_select_all,
            )
        ]
        defense_buttons: list[ft.Control] = []
        for position in POSITION_ORDER:
            defense_buttons.append(
                self._button(
                    label=position.label,
                    count=position_counts.get(position, 0),
                    selected=(
                        selected_position == position
                        and selected_runner_role is None
                        and selected_rule_topic is None
                    ),
                    on_click=lambda position=position: on_select_position(position),
                )
            )

        runner_buttons: list[ft.Control] = []
        for role in RUNNER_ROLE_ORDER:
            runner_buttons.append(
                self._button(
                    label=role.label,
                    count=runner_counts.get(role, 0),
                    selected=selected_runner_role == role and selected_rule_topic is None,
                    on_click=lambda role=role: on_select_runner_role(role),
                )
            )

        rule_buttons: list[ft.Control] = []
        for topic in RULE_TOPIC_ORDER:
            rule_buttons.append(
                self._button(
                    label=topic.label,
                    count=rule_counts.get(topic, 0),
                    selected=selected_rule_topic == topic,
                    on_click=lambda topic=topic: on_select_rule_topic(topic),
                )
            )

        return ft.Container(
            bgcolor=theme.SURFACE,
            border=ft.Border.all(1, theme.BORDER),
            border_radius=theme.CARD_RADIUS,
            padding=ft.Padding(14, 12, 14, 12),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.SPORTS_BASEBALL, size=20, color=theme.PRIMARY),
                            ft.Text(
                                kids_text("クイズのしゅるいをえらぶ"),
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=theme.TEXT,
                            ),
                        ],
                    ),
                    ft.Row(spacing=8, run_spacing=8, wrap=True, controls=all_buttons),
                    ft.Text(kids_text("まもる場所"), size=12, color=theme.TEXT_MUTED),
                    ft.Row(spacing=8, run_spacing=8, wrap=True, controls=defense_buttons),
                    ft.Text(kids_text("走る人"), size=12, color=theme.TEXT_MUTED),
                    ft.Row(spacing=8, run_spacing=8, wrap=True, controls=runner_buttons),
                    ft.Text("きほんルール", size=12, color=theme.TEXT_MUTED),
                    ft.Row(spacing=8, run_spacing=8, wrap=True, controls=rule_buttons),
                ],
            ),
        )

    def _button(
        self,
        *,
        label: str,
        count: int,
        selected: bool,
        on_click: Callable[[], None],
    ) -> ft.Control:
        return ft.Button(
            on_click=lambda _: on_click(),
            content=ft.Container(
                bgcolor="#E3F3E8" if selected else "#F7FAF7",
                border=ft.Border.all(1, theme.PRIMARY if selected else theme.BORDER),
                border_radius=theme.CARD_RADIUS,
                padding=ft.Padding(10, 8, 10, 8),
                content=ft.Row(
                    spacing=7,
                    tight=True,
                    controls=[
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE if selected else ft.Icons.CIRCLE_OUTLINED,
                            size=17,
                            color=theme.PRIMARY if selected else theme.TEXT_MUTED,
                        ),
                        ft.Text(kids_text(label), size=13, weight=ft.FontWeight.W_600, color=theme.TEXT),
                        ft.Text(f"{count}もん", size=12, color=theme.TEXT_MUTED),
                    ],
                ),
            ),
        )


class ScenarioPanel:
    def __init__(self) -> None:
        self._field = FieldDiagram()

    def render(self, question: QuizQuestion) -> ft.Control:
        scenario = question.scenario
        return ft.Container(
            bgcolor="#FFFDF6",
            border=ft.Border.all(2, theme.SECONDARY),
            border_radius=theme.CARD_RADIUS,
            padding=ft.Padding(18, 16, 18, 16),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                spacing=8,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.INFO, size=24, color=theme.SECONDARY),
                                    ft.Text(
                                        "いまのばめん",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=theme.TEXT,
                                    ),
                                ],
                            ),
                            _status_chip(scenario.difficulty.value, ft.Icons.SCHOOL, theme.WARNING),
                        ],
                    ),
                    _role_banner(self._actor_description(question), self._actor_label_icon(question)),
                    ft.Row(
                        spacing=12,
                        run_spacing=12,
                        wrap=True,
                        controls=[
                            _summary_tile(
                                self._actor_label_title(question),
                                scenario.actor_label,
                                self._actor_label_icon(question),
                                190,
                            ),
                            _summary_tile("アウト", scenario.outs_label, ft.Icons.OUTBOUND, 128),
                            _summary_tile("ランナー", scenario.runners.label, ft.Icons.DIRECTIONS_RUN, 180),
                            _summary_tile(
                                "ボールのうごき",
                                scenario.batted_ball,
                                ft.Icons.SPORTS_BASEBALL,
                                280,
                            ),
                            _summary_tile("メモ", scenario.fielding_note, ft.Icons.INFO, 340),
                        ],
                    ),
                ],
            ),
        )

    def render_field(self, question: QuizQuestion) -> ft.Control:
        scenario = question.scenario
        ball_summary = self._field.ball_summary(
            scenario.batted_ball,
            scenario.fielding_note,
            scenario.position,
        )
        controls: list[ft.Control] = [
            ft.Row(
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.SPORTS_BASEBALL, size=20, color=theme.PRIMARY),
                    ft.Text("ずでみる", size=16, weight=ft.FontWeight.BOLD, color=theme.TEXT),
                ],
            )
        ]
        if ball_summary is not None:
            controls.append(_field_note_banner(ball_summary))
        controls.append(
            self._field.render(
                scenario.runners,
                scenario.position,
                scenario.runner_role,
                scenario.rule_topic,
                scenario.batted_ball,
                scenario.fielding_note,
            )
        )

        return ft.Container(
            bgcolor=theme.SURFACE,
            border=ft.Border.all(1, theme.BORDER),
            border_radius=theme.CARD_RADIUS,
            padding=ft.Padding(14, 14, 14, 14),
            content=ft.Column(
                spacing=10,
                controls=controls,
            ),
        )

    def _actor_label_title(self, question: QuizQuestion) -> str:
        if question.scenario.position is not None:
            return "まもる場所"
        if question.scenario.runner_role is not None:
            return "走る人"
        return "きほんルール"

    def _actor_label_icon(self, question: QuizQuestion) -> ft.Icons:
        if question.scenario.position is not None:
            return ft.Icons.SHIELD
        if question.scenario.runner_role is not None:
            return ft.Icons.DIRECTIONS_RUN
        return ft.Icons.MENU_BOOK

    def _actor_description(self, question: QuizQuestion) -> str:
        scenario = question.scenario
        if scenario.position is not None:
            return f"あなたは {scenario.actor_label} として、まもりのうごきをえらびます。"
        if scenario.runner_role is not None:
            return f"あなたは {scenario.actor_label} として、走り方をえらびます。"
        if scenario.rule_topic == RuleTopic.OUTS:
            return "これはアウトのルールです。場面を見て、どうなるかをえらびます。"
        if scenario.rule_topic == RuleTopic.FORCE_TAG:
            return "これはフォース・タッチのルールです。場面を見て、どうアウトにするかをえらびます。"
        if scenario.rule_topic == RuleTopic.FAIR_FOUL:
            return "これはフェア・ファウルのルールです。ボールの場所を見て、どうなるかをえらびます。"
        if scenario.rule_topic == RuleTopic.RUNNING_RULES:
            return "これは走るルールです。ランナーやバッターがどうするかをえらびます。"
        if scenario.rule_topic == RuleTopic.GAME_FLOW:
            return "これはしあいの流れのルールです。始まり・交代・終わりで何をするかをえらびます。"
        return "これはきほんルールです。場面を見て、正しい決まりをえらびます。"


class FieldDiagram:
    def ball_summary(
        self,
        batted_ball: str,
        fielding_note: str,
        active_position: DefensivePosition | None,
    ) -> str | None:
        text = f"{batted_ball} {fielding_note}"
        if self._skip_ball_visual(text):
            return None
        if self._possession_point(text, active_position) is not None:
            kind, state = "ボール", "守る人が持つ"
        else:
            kind, state, _ = self._ball_style(
                text,
                is_throw=False,
            )
        return self._visual_label_text(kind, state)

    def render(
        self,
        runners: RunnerState,
        position: DefensivePosition | None,
        runner_role: RunnerRole | None,
        rule_topic: RuleTopic | None,
        batted_ball: str,
        fielding_note: str,
    ) -> ft.Control:
        ball_visual = self._ball_visual_controls(batted_ball, fielding_note, position)
        return ft.Container(
            height=345,
            bgcolor=theme.FIELD,
            border=ft.Border.all(1, "#C8DDC4"),
            border_radius=theme.CARD_RADIUS,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Stack(
                controls=[
                    ft.Container(
                        width=138,
                        height=138,
                        left=92,
                        top=92,
                        rotate=0.785,
                        bgcolor=theme.INFIELD,
                        opacity=0.35,
                        border_radius=4,
                    ),
                    *self._foul_line_controls(),
                    self._base(
                        "2るい",
                        runners.second,
                        self._active_runner_base(runner_role, rule_topic, RunnerRole.SECOND_RUNNER),
                        134,
                        62,
                    ),
                    self._base(
                        "3るい",
                        runners.third,
                        self._active_runner_base(runner_role, rule_topic, RunnerRole.THIRD_RUNNER),
                        48,
                        152,
                    ),
                    self._base(
                        "1るい",
                        runners.first,
                        self._active_runner_base(runner_role, rule_topic, RunnerRole.FIRST_RUNNER),
                        220,
                        152,
                    ),
                    self._base(
                        "本るい",
                        False,
                        runner_role == RunnerRole.BATTER_RUNNER,
                        134,
                        236,
                    ),
                    *self._fielders(position),
                    *ball_visual,
                ],
            ),
        )

    def _base(self, label: str, occupied: bool, active: bool, left: int, top: int) -> ft.Control:
        return ft.Container(
            left=left,
            top=top,
            width=52,
            height=38,
            bgcolor=theme.BASE_OCCUPIED if occupied or active else theme.BASE_EMPTY,
            border=ft.Border.all(
                3 if active else 2,
                theme.ERROR if active else theme.PRIMARY if occupied else "#D8CBA7",
            ),
            border_radius=6,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        ft.Icons.DIRECTIONS_RUN if active else ft.Icons.PERSON if occupied else ft.Icons.SQUARE_OUTLINED,
                        size=15,
                        color=theme.ERROR if active else theme.PRIMARY_DARK if occupied else theme.TEXT_MUTED,
                    ),
                    ft.Text(label, size=11, color=theme.TEXT),
                ],
            ),
        )

    def _active_runner_base(
        self,
        runner_role: RunnerRole | None,
        rule_topic: RuleTopic | None,
        role: RunnerRole,
    ) -> bool:
        _ = rule_topic
        return runner_role == role

    def _fielders(self, active_position: DefensivePosition | None) -> list[ft.Control]:
        spots = {
            DefensivePosition.PITCHER: ("ピッチャー", 126, 150),
            DefensivePosition.CATCHER: ("キャッチャー", 126, 286),
            DefensivePosition.FIRST_BASE: ("ファースト", 202, 184),
            DefensivePosition.SECOND_BASE: ("セカンド", 198, 106),
            DefensivePosition.THIRD_BASE: ("サード", 50, 184),
            DefensivePosition.SHORTSTOP: ("ショート", 58, 106),
            DefensivePosition.LEFT_FIELD: ("レフト", 24, 48),
            DefensivePosition.CENTER_FIELD: ("センター", 126, 28),
            DefensivePosition.RIGHT_FIELD: ("ライト", 230, 48),
        }
        return [
            self._fielder(label, active_position == position, left, top)
            for position, (label, left, top) in spots.items()
        ]

    def _fielder(self, label: str, active: bool, left: int, top: int) -> ft.Control:
        return ft.Container(
            left=left,
            top=top,
            width=68,
            height=30,
            bgcolor=theme.PRIMARY if active else "#FFFFFFAA",
            border=ft.Border.all(2 if active else 1, theme.PRIMARY_DARK if active else "#B7C8B7"),
            border_radius=6,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                label,
                size=10,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE if active else theme.TEXT_MUTED,
            ),
        )

    def _ball_visual_controls(
        self,
        batted_ball: str,
        fielding_note: str,
        active_position: DefensivePosition | None,
    ) -> list[ft.Control]:
        text = f"{batted_ball} {fielding_note}"
        if self._skip_ball_visual(text):
            return []

        possession_point = self._possession_point(text, active_position)
        if possession_point is not None:
            kind, state, color = "ボール", "守る人が持つ", theme.PRIMARY
            return [
                self._ball_marker(possession_point[0] - 10, possession_point[1] - 10, color),
                self._ball_label(kind, state, 12, 12, color),
            ]

        kind, state, color = self._ball_style(text, is_throw=False)
        start = (160, 255)
        end = self._location_point(batted_ball) or self._location_point(text) or (160, 120)

        return [
            *self._path_controls(start, end, color, kind, False),
            self._ball_marker(end[0] - 10, end[1] - 10, color),
            self._ball_label(kind, state, 12, 12, color),
        ]

    def _possession_point(
        self,
        text: str,
        active_position: DefensivePosition | None,
    ) -> tuple[int, int] | None:
        possession_words = (
            "ボールが返ってきた",
            "ボールが来る",
            "ボールがなげられた",
            "ボールをとったあと",
            "ボールを持って",
            "なげようとしている",
        )
        if not any(word in text for word in possession_words):
            return None
        if "ピッチャーのボールをとったあと" in text:
            return (160, 300)
        return self._throw_source(text) or (
            self._position_point(active_position) if active_position is not None else None
        )

    def _skip_ball_visual(self, text: str) -> bool:
        no_ball_words = (
            "プレイボール",
            "ゲームセット",
            "攻守交代",
            "打席に入る",
            "ボックスを出",
            "まだ投げる前",
            "投げる前の準備",
            "ストライクを3つ",
            "ベースから少し離れた",
            "3つ目のアウト",
            "一回の表",
        )
        if any(word in text for word in no_ball_words):
            return True

        ball_words = (
            "ゴロ",
            "フライ",
            "ライナー",
            "バント",
            "ヒット",
            "打球",
            "ボール",
            "なげ",
            "返",
            "送球",
            "キャッチ",
            "転が",
            "バウンド",
            "ファウル",
            "フェア",
        )
        return not any(word in text for word in ball_words)

    def _ball_style(self, text: str, *, is_throw: bool) -> tuple[str, str, str]:
        if is_throw:
            return "返球", "ボールが向かう", theme.ERROR

        if "フライ" in text:
            kind = "フライ"
            color = "#2F80ED"
        elif "ライナー" in text:
            kind = "ライナー"
            color = "#7B3FB2"
        elif "バント" in text:
            kind = "バント"
            color = theme.WARNING
        elif "ゴロ" in text:
            kind = "ゴロ"
            color = theme.PRIMARY_DARK
        elif "ヒット" in text:
            kind = "ヒット"
            color = theme.PRIMARY_DARK
        elif "ファウル" in text:
            kind = "ファウル"
            color = theme.WARNING
        elif "打球" in text:
            kind = "打球"
            color = theme.PRIMARY_DARK
        else:
            kind = "ボール"
            color = theme.PRIMARY

        if "ボールが返ってきた" in text or "ボールが来る" in text or "ボールがなげられた" in text:
            state = "守る人が持つ"
        elif "ピッチャーのボールをとったあと" in text:
            state = "キャッチャーが持つ"
        elif "それた" in text or "そらした" in text:
            state = "それた"
        elif "止まった" in text or "止まっている" in text:
            state = "止まった"
        elif "ぬける" in text or "ぬけそう" in text:
            state = "ぬける"
        elif "ボールを持って" in text:
            state = "守る人が持つ"
        elif (
            "キャッチした" in text
            or "キャッチされた" in text
            or "しっかりとった" in text
            or "とったあと" in text
            or "とられた" in text
        ):
            state = "とられた"
        elif (
            "とられそう" in text
            or "とられるか" in text
            or "とれそう" in text
            or "落ちそう" in text
            or "まだ分からない" in text
        ):
            state = "まだ空中"
        elif "落ちた" in text or "転が" in text or "バウンド" in text or kind in ("ゴロ", "バント", "ヒット"):
            state = "地面"
        elif kind in ("フライ", "ライナー"):
            state = "まだ空中"
        else:
            state = "位置"

        return kind, state, color

    def _throw_points(
        self,
        text: str,
        active_position: DefensivePosition | None,
    ) -> tuple[tuple[int, int], tuple[int, int]] | None:
        throw_words = ("なげ", "返", "送球", "ボールが来る", "ボールがなげられた")
        if not any(word in text for word in throw_words):
            return None

        target = self._throw_target(text)
        if target is None:
            return None

        source = self._throw_source(text)
        if source is None and active_position is not None:
            source = self._position_point(active_position)
        if source is None:
            source = (160, 255)
        if source == target:
            return None
        return source, target

    def _throw_source(self, text: str) -> tuple[int, int] | None:
        if "キャッチャーから" in text or "キャッチャーが" in text:
            return (160, 300)
        if "ピッチャーから" in text or "ピッチャーが" in text:
            return (160, 168)
        if "ショートから" in text or "ショートが" in text:
            return (92, 122)
        if "ファーストから" in text or "ファーストが" in text:
            return (250, 188)
        if "セカンドから" in text or "セカンドが" in text or "2るい手が" in text:
            return (210, 120)
        if "サードから" in text or "サードが" in text or "3るい手が" in text:
            return (74, 188)
        if "レフト" in text:
            return (58, 64)
        if "センター" in text:
            return (160, 46)
        if "ライト" in text:
            return (264, 64)
        return None

    def _throw_target(self, text: str) -> tuple[int, int] | None:
        if "本るいへ" in text or "ホームへ" in text or "本るいに" in text:
            return (160, 255)
        if "1るいへ" in text or "一るいへ" in text or "1るいに" in text:
            return (246, 170)
        if "2るいへ" in text or "二るいへ" in text or "2るいに" in text:
            return (160, 82)
        if "3るいへ" in text or "三るいへ" in text or "3るいに" in text:
            return (74, 170)
        if "キャッチャーの後ろ" in text:
            return (160, 325)
        return None

    def _location_point(self, text: str) -> tuple[int, int] | None:
        foul_point = self._foul_location_point(text)
        if foul_point is not None:
            return foul_point

        fair_hit_point = self._fair_hit_location_point(text)
        if fair_hit_point is not None:
            return fair_hit_point

        checks: tuple[tuple[tuple[str, ...], tuple[int, int]], ...] = (
            (("キャッチャーの後ろ",), (160, 325)),
            (("本るい前",), (160, 238)),
            (("キャッチャー",), (160, 300)),
            (("ピッチャー前", "ピッチャー正面", "ピッチャーへの"), (160, 166)),
            (("1るいと2るいの間",), (203, 126)),
            (("ファースト正面", "1るいの近く", "1るいの右", "1るい線", "1るい前", "ファースト"), (212, 174)),
            (("サード正面", "3るい手", "3るい線", "3るい前", "3るい横"), (104, 174)),
            (("ショートの左",), (112, 130)),
            (("ショート",), (92, 122)),
            (("左中間",), (105, 52)),
            (("右中間",), (220, 52)),
            (("レフト",), (58, 64)),
            (("センター",), (160, 46)),
            (("ライト",), (264, 64)),
            (("1・2るい間",), (212, 174)),
            (("2るい手", "2るいベース", "2るい手前"), (210, 118)),
            (("外野",), (160, 58)),
            (("内野",), (160, 140)),
            (("高いフライ",), (160, 58)),
            (("満るいでゴロ", "バッターがゴロ", "ゴロ"), (160, 140)),
        )
        for words, point in checks:
            if any(word in text for word in words):
                return point
        return None

    def _fair_hit_location_point(self, text: str) -> tuple[int, int] | None:
        fair_words = (
            "ヒット",
            "ライト前",
            "レフト前",
            "センター前",
            "左中間",
            "右中間",
            "外野の間",
            "ぬけそう",
            "ぬけた",
        )
        if not any(word in text for word in fair_words):
            return None
        if "ファウル" in text or "ラインの外" in text:
            return None

        if "左中間" in text:
            return (112, 58)
        if "右中間" in text:
            return (208, 58)
        if "レフト" in text:
            return (72, 78)
        if "ライト" in text:
            return (248, 78)
        if "センター" in text or "外野の間" in text:
            return (160, 58)
        return (160, 70)

    def _foul_location_point(self, text: str) -> tuple[int, int] | None:
        is_foul_area = (
            "ラインの外" in text
            or "ファウルラインの外" in text
            or "ファウルの場所" in text
            or "ファウルボール" in text
        )
        if not is_foul_area:
            return None

        if "1るいベースの上を通って" in text and "ラインの外へ" in text:
            return (302, 86)
        if "1るいより手前" in text and "ラインの外" in text:
            return (204, 212)
        if "1るい" in text or "ライト" in text:
            return (292, 92 if "外野" in text else 226)
        if "3るい" in text or "レフト" in text:
            return (28, 92 if "外野" in text else 226)
        if "外野" in text:
            return (328, 84)
        return (34, 226)

    def _position_point(self, position: DefensivePosition) -> tuple[int, int]:
        return {
            DefensivePosition.PITCHER: (160, 168),
            DefensivePosition.CATCHER: (160, 300),
            DefensivePosition.FIRST_BASE: (236, 184),
            DefensivePosition.SECOND_BASE: (210, 120),
            DefensivePosition.THIRD_BASE: (84, 184),
            DefensivePosition.SHORTSTOP: (92, 122),
            DefensivePosition.LEFT_FIELD: (58, 64),
            DefensivePosition.CENTER_FIELD: (160, 46),
            DefensivePosition.RIGHT_FIELD: (264, 64),
        }[position]

    def _path_controls(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: str,
        kind: str,
        is_throw: bool,
    ) -> list[ft.Control]:
        if is_throw:
            return self._straight_path_controls(start, end, color)
        if kind in ("フライ", "ライナー"):
            return self._arc_path_controls(start, end, color, high=kind == "フライ")
        if kind in ("ゴロ", "バント", "ヒット"):
            return self._rolling_path_controls(start, end, color)
        return self._straight_path_controls(start, end, color)

    def _foul_line_controls(self) -> list[ft.Control]:
        home = (160, 255)
        first_side = (312, 108)
        third_side = (8, 108)
        return [
            self._segment_between(home, first_side, "#F8FFF8", height=2, opacity=0.95),
            self._segment_between(home, third_side, "#F8FFF8", height=2, opacity=0.95),
        ]

    def _straight_path_controls(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: str,
    ) -> list[ft.Control]:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = max(24, math.hypot(dx, dy))
        angle = math.atan2(dy, dx)
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        return [
            self._segment_control(mid_x, mid_y, length, angle, color, height=4, opacity=0.75),
            self._arrow_control(end, angle, color),
        ]

    def _arc_path_controls(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: str,
        *,
        high: bool,
    ) -> list[ft.Control]:
        lift = 64 if high else 36
        control = (
            (start[0] + end[0]) / 2,
            max(14, min(start[1], end[1]) - lift),
        )
        points = [self._quadratic_point(start, control, end, index / 14) for index in range(15)]
        controls = self._polyline_controls(points, color, height=4, opacity=0.78)
        angle = math.atan2(points[-1][1] - points[-2][1], points[-1][0] - points[-2][0])
        controls.append(self._arrow_control(end, angle, color))
        return controls

    def _rolling_path_controls(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: str,
    ) -> list[ft.Control]:
        points = [self._wave_point(start, end, index / 18) for index in range(19)]
        controls = self._polyline_controls(points, color, height=3, opacity=0.7, every_other=True)
        angle = math.atan2(points[-1][1] - points[-2][1], points[-1][0] - points[-2][0])
        controls.append(self._arrow_control(end, angle, color))
        return controls

    def _segment_between(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: str,
        *,
        height: int,
        opacity: float,
    ) -> ft.Control:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        return self._segment_control(
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2,
            max(8, math.hypot(dx, dy)),
            math.atan2(dy, dx),
            color,
            height=height,
            opacity=opacity,
        )

    def _polyline_controls(
        self,
        points: list[tuple[float, float]],
        color: str,
        *,
        height: int,
        opacity: float,
        every_other: bool = False,
    ) -> list[ft.Control]:
        controls: list[ft.Control] = []
        for index, (start, end) in enumerate(zip(points, points[1:])):
            if every_other and index % 2 == 1:
                continue
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            length = max(8, math.hypot(dx, dy))
            angle = math.atan2(dy, dx)
            controls.append(
                self._segment_control(
                    (start[0] + end[0]) / 2,
                    (start[1] + end[1]) / 2,
                    length,
                    angle,
                    color,
                    height=height,
                    opacity=opacity,
                )
            )
        return controls

    def _segment_control(
        self,
        center_x: float,
        center_y: float,
        length: float,
        angle: float,
        color: str,
        *,
        height: int,
        opacity: float,
    ) -> ft.Control:
        return ft.Container(
            left=center_x - length / 2,
            top=center_y - height / 2,
            width=length,
            height=height,
            bgcolor=color,
            opacity=opacity,
            border_radius=height,
            rotate=angle,
        )

    def _arrow_control(self, end: tuple[int, int], angle: float, color: str) -> ft.Control:
        return ft.Icon(
            ft.Icons.ARROW_FORWARD,
            left=end[0] - 6,
            top=end[1] - 12,
            size=22,
            color=color,
            rotate=angle,
        )

    def _quadratic_point(
        self,
        start: tuple[int, int],
        control: tuple[float, float],
        end: tuple[int, int],
        t: float,
    ) -> tuple[float, float]:
        inv = 1 - t
        return (
            inv * inv * start[0] + 2 * inv * t * control[0] + t * t * end[0],
            inv * inv * start[1] + 2 * inv * t * control[1] + t * t * end[1],
        )

    def _wave_point(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        t: float,
    ) -> tuple[float, float]:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = max(1, math.hypot(dx, dy))
        normal = (-dy / length, dx / length)
        bounce = math.sin(t * math.pi * 8) * 5
        return (
            start[0] + dx * t + normal[0] * bounce,
            start[1] + dy * t + normal[1] * bounce,
        )

    def _ball_marker(self, left: int, top: int, color: str) -> ft.Control:
        return ft.Container(
            left=left,
            top=top,
            width=20,
            height=20,
            bgcolor="#FFFDF7",
            border=ft.Border.all(3, color),
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("●", size=8, color=color),
        )

    def _ball_label(self, kind: str, state: str, left: int, top: int, color: str) -> ft.Control:
        return ft.Container(
            left=left,
            top=top,
            bgcolor="#FFFFFFDD",
            border=ft.Border.all(1, color),
            border_radius=theme.CARD_RADIUS,
            padding=ft.Padding(8, 5, 8, 5),
            content=ft.Row(
                spacing=6,
                controls=[
                    ft.Icon(ft.Icons.SPORTS_BASEBALL, size=14, color=color),
                    ft.Text(
                        self._visual_label_text(kind, state),
                        size=12,
                        color=theme.TEXT,
                        weight=ft.FontWeight.W_600,
                    ),
                ],
            ),
        )

    def _visual_label_text(self, kind: str, state: str) -> str:
        if kind == "返球":
            return "返球: ボールが向かう"
        if kind == "ボール":
            if state == "位置":
                return "ボールの位置"
            return f"ボール: {state}"
        return f"{kind}: {state}"


class QuestionPanel:
    def render(
        self,
        *,
        question: QuizQuestion,
        selected_option_id: str | None,
        on_select: Callable[[str], None],
    ) -> ft.Control:
        answered = selected_option_id is not None
        controls: list[ft.Control] = [
            ft.Text(kids_text(question.prompt), size=20, weight=ft.FontWeight.BOLD, color=theme.TEXT),
            ft.Text(
                kids_text(self._helper_text(question)),
                size=13,
                color=theme.TEXT_MUTED,
            ),
        ]
        for option in question.options:
            controls.append(
                OptionButton().render(
                    option=option,
                    answered=answered,
                    selected=selected_option_id == option.id,
                    on_select=on_select,
                )
            )

        return ft.Container(
            bgcolor=theme.SURFACE,
            border=ft.Border.all(1, theme.BORDER),
            border_radius=theme.CARD_RADIUS,
            padding=ft.Padding(18, 18, 18, 18),
            content=ft.Column(spacing=12, controls=controls),
        )

    def _helper_text(self, question: QuizQuestion) -> str:
        if question.scenario.runner_role is not None:
            return "えらんだ走る人として、つぎにすることをこたえてください。"
        if question.scenario.rule_topic is not None:
            return "ルールとして正しいものをえらんでください。"
        return "えらんだ場所の人として、いちばん先にすることをこたえてください。"


class OptionButton:
    def render(
        self,
        *,
        option: AnswerOption,
        answered: bool,
        selected: bool,
        on_select: Callable[[str], None],
    ) -> ft.Control:
        icon, color = self._state_icon(option, answered, selected)
        return ft.Button(
            disabled=answered,
            on_click=lambda _: on_select(option.id),
            content=ft.Container(
                padding=ft.Padding(12, 11, 12, 11),
                content=ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(icon, color=color, size=21),
                        ft.Text(
                            kids_text(option.text),
                            size=15,
                            color=theme.TEXT,
                            expand=True,
                        ),
                    ],
                ),
            ),
        )

    def _state_icon(
        self, option: AnswerOption, answered: bool, selected: bool
    ) -> tuple[ft.Icons, str]:
        if not answered:
            return ft.Icons.RADIO_BUTTON_UNCHECKED, theme.TEXT_MUTED
        if option.is_correct:
            return ft.Icons.CHECK_CIRCLE, theme.SUCCESS
        if selected:
            return ft.Icons.CANCEL, theme.ERROR
        return ft.Icons.CIRCLE_OUTLINED, theme.TEXT_MUTED


class FeedbackPanel:
    def render(self, question: QuizQuestion, selected_option_id: str | None) -> ft.Control:
        if selected_option_id is None:
            return ft.Container(
                bgcolor=theme.SURFACE_ALT,
                border_radius=theme.CARD_RADIUS,
                padding=ft.Padding(16, 14, 16, 14),
                content=ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(ft.Icons.LIGHTBULB, color=theme.WARNING),
                        ft.Text(
                            "こたえると、わけとポイントが出ます。",
                            color=theme.TEXT_MUTED,
                            size=13,
                            expand=True,
                        ),
                    ],
                ),
            )

        selected = next(option for option in question.options if option.id == selected_option_id)
        is_correct = selected.is_correct
        return ft.Container(
            bgcolor="#EEF8F1" if is_correct else "#FFF2F1",
            border=ft.Border.all(1, "#BFE4CA" if is_correct else "#F3C2BD"),
            border_radius=theme.CARD_RADIUS,
            padding=ft.Padding(16, 16, 16, 16),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE if is_correct else ft.Icons.ERROR,
                                color=theme.SUCCESS if is_correct else theme.ERROR,
                            ),
                            ft.Text(
                                "せいかい" if is_correct else "もう一歩",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=theme.SUCCESS if is_correct else theme.ERROR,
                            ),
                        ],
                    ),
                    ft.Text(kids_text(selected.feedback), color=theme.TEXT, size=14),
                    ft.Divider(height=1, color="#D7E4D7"),
                    ft.Text(
                        kids_text(f"ポイント: {question.principle}"),
                        color=theme.TEXT,
                        size=14,
                        weight=ft.FontWeight.W_600,
                    ),
                ],
            ),
        )


class ResultPanel:
    def render(
        self,
        *,
        score: int,
        total: int,
        on_restart: Callable[[ft.Event[ft.Button]], None],
    ) -> ft.Control:
        rate = score / total
        if rate >= 0.85:
            message = "よくできています。次は別のまもる場所にもチャレンジできます。"
            icon = ft.Icons.EMOJI_EVENTS
            color = theme.SUCCESS
        elif rate >= 0.6:
            message = "きほんはつかめています。フォースとタッチのちがいを見直すとさらによくなります。"
            icon = ft.Icons.TRENDING_UP
            color = theme.WARNING
        else:
            message = "まずは、近くて安全なアウトを一つとることからおぼえましょう。"
            icon = ft.Icons.MENU_BOOK
            color = theme.ERROR

        return ft.Container(
            bgcolor=theme.SURFACE,
            border=ft.Border.all(1, theme.BORDER),
            border_radius=theme.CARD_RADIUS,
            padding=ft.Padding(24, 24, 24, 24),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=18,
                controls=[
                    ft.Icon(icon, size=64, color=color),
                    ft.Text("けっか", size=26, weight=ft.FontWeight.BOLD, color=theme.TEXT),
                    ft.Text(
                        f"{total}もんのうち {score}もん せいかい",
                        size=22,
                        weight=ft.FontWeight.W_600,
                        color=theme.PRIMARY_DARK,
                    ),
                    ft.Text(kids_text(message), text_align=ft.TextAlign.CENTER, color=theme.TEXT_MUTED),
                    ft.Button(
                        content=kids_text("もう一度"),
                        icon=ft.Icons.REPLAY,
                        on_click=on_restart,
                    ),
                ],
            ),
        )


class NavigationBar:
    def render(
        self,
        *,
        answered: bool,
        is_finished: bool,
        on_next: Callable[[ft.Event[ft.Button]], None],
        on_restart: Callable[[ft.Event[ft.Button]], None],
    ) -> ft.Control:
        return ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Button(
                    content=kids_text("もう一度"),
                    icon=ft.Icons.REPLAY,
                    on_click=on_restart,
                ),
                ft.Button(
                    content=kids_text("けっかを見る") if is_finished else "つぎへ",
                    icon=ft.Icons.ARROW_FORWARD,
                    disabled=not answered,
                    on_click=on_next,
                ),
            ],
        )


def _status_chip(text: str, icon: ft.Icons, color: str) -> ft.Control:
    return ft.Container(
        bgcolor="#F4FAF6",
        border=ft.Border.all(1, theme.BORDER),
        border_radius=theme.CARD_RADIUS,
        padding=ft.Padding(10, 7, 10, 7),
        content=ft.Row(
            spacing=6,
            controls=[
                ft.Icon(icon, size=16, color=color),
                ft.Text(kids_text(text), size=13, weight=ft.FontWeight.W_600, color=theme.TEXT),
            ],
        ),
    )


def _info_line(label: str, value: str, icon: ft.Icons) -> ft.Control:
    return ft.Row(
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Icon(icon, size=18, color=theme.PRIMARY),
            ft.Column(
                spacing=2,
                expand=True,
                controls=[
                    ft.Text(kids_text(label), size=12, color=theme.TEXT_MUTED),
                    ft.Text(kids_text(value), size=14, color=theme.TEXT, weight=ft.FontWeight.W_600),
                ],
            ),
        ],
    )


def _role_banner(text: str, icon: ft.Icons) -> ft.Control:
    return ft.Container(
        bgcolor="#F4FAF6",
        border=ft.Border.all(1, "#BFE4CA"),
        border_radius=theme.CARD_RADIUS,
        padding=ft.Padding(12, 10, 12, 10),
        content=ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(icon, size=20, color=theme.PRIMARY),
                ft.Text(
                    kids_text(text),
                    size=15,
                    color=theme.PRIMARY_DARK,
                    weight=ft.FontWeight.BOLD,
                    expand=True,
                ),
            ],
        ),
    )


def _field_note_banner(text: str) -> ft.Control:
    return ft.Container(
        bgcolor="#F7FAF7",
        border=ft.Border.all(1, theme.BORDER),
        border_radius=theme.CARD_RADIUS,
        padding=ft.Padding(10, 7, 10, 7),
        content=ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.SPORTS_BASEBALL, size=16, color=theme.PRIMARY),
                ft.Text(
                    kids_text(text),
                    size=12,
                    color=theme.TEXT,
                    weight=ft.FontWeight.W_600,
                    expand=True,
                ),
            ],
        ),
    )


def _summary_tile(label: str, value: str, icon: ft.Icons, width: int) -> ft.Control:
    return ft.Container(
        width=width,
        bgcolor=theme.SURFACE,
        border=ft.Border.all(1, theme.BORDER),
        border_radius=theme.CARD_RADIUS,
        padding=ft.Padding(12, 10, 12, 10),
        content=ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Icon(icon, size=18, color=theme.PRIMARY),
                ft.Column(
                    spacing=2,
                    expand=True,
                    controls=[
                        ft.Text(kids_text(label), size=12, color=theme.TEXT_MUTED),
                        ft.Text(
                            kids_text(value),
                            size=15,
                            color=theme.TEXT,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                ),
            ],
        ),
    )
