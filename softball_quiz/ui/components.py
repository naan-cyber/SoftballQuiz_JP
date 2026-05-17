from __future__ import annotations

from collections.abc import Callable

import flet as ft

from softball_quiz.models import (
    AnswerOption,
    DefensivePosition,
    POSITION_ORDER,
    QuizQuestion,
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
                                        kids_text("まもる場所・ランナー・アウト・打ったボールを見て、はじめの動きをえらぶ"),
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
        counts: dict[DefensivePosition, int],
        on_select: Callable[[DefensivePosition | None], None],
    ) -> ft.Control:
        buttons = [
            self._button(
                label="ぜんぶ",
                count=sum(counts.values()),
                selected=selected_position is None,
                on_click=lambda: on_select(None),
            )
        ]
        for position in POSITION_ORDER:
            buttons.append(
                self._button(
                    label=position.label,
                    count=counts.get(position, 0),
                    selected=selected_position == position,
                    on_click=lambda position=position: on_select(position),
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
                                "まもる場所をえらぶ",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=theme.TEXT,
                            ),
                        ],
                    ),
                    ft.Row(spacing=8, run_spacing=8, wrap=True, controls=buttons),
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
                        ft.Text(label, size=13, weight=ft.FontWeight.W_600, color=theme.TEXT),
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
            bgcolor=theme.SURFACE,
            border=ft.Border.all(1, theme.BORDER),
            border_radius=theme.CARD_RADIUS,
            padding=ft.Padding(18, 18, 18, 18),
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            _status_chip(scenario.outs_label, ft.Icons.OUTBOUND, theme.PRIMARY),
                            _status_chip(scenario.difficulty.value, ft.Icons.SCHOOL, theme.WARNING),
                        ],
                    ),
                    self._field.render(scenario.runners, scenario.position),
                    ft.Column(
                        spacing=10,
                        controls=[
                            _info_line("まもる場所", scenario.position.label, ft.Icons.SHIELD),
                            _info_line("ランナー", scenario.runners.label, ft.Icons.DIRECTIONS_RUN),
                            _info_line("ボールの動き", kids_text(scenario.batted_ball), ft.Icons.SPORTS_BASEBALL),
                            _info_line("メモ", kids_text(scenario.fielding_note), ft.Icons.INFO),
                        ],
                    ),
                ],
            ),
        )


class FieldDiagram:
    def render(self, runners: RunnerState, position: DefensivePosition) -> ft.Control:
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
                    self._label("がいや", 136, 8),
                    self._base("二るい", runners.second, 134, 62),
                    self._base("三るい", runners.third, 48, 152),
                    self._base("一るい", runners.first, 220, 152),
                    self._base("本るい", False, 134, 286),
                    *self._fielders(position),
                ],
            ),
        )

    def _base(self, label: str, occupied: bool, left: int, top: int) -> ft.Control:
        return ft.Container(
            left=left,
            top=top,
            width=52,
            height=38,
            bgcolor=theme.BASE_OCCUPIED if occupied else theme.BASE_EMPTY,
            border=ft.Border.all(2, theme.PRIMARY if occupied else "#D8CBA7"),
            border_radius=6,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        ft.Icons.PERSON if occupied else ft.Icons.SQUARE_OUTLINED,
                        size=15,
                        color=theme.PRIMARY_DARK if occupied else theme.TEXT_MUTED,
                    ),
                    ft.Text(label, size=11, color=theme.TEXT),
                ],
            ),
        )

    def _label(self, text: str, left: int, top: int) -> ft.Control:
        return ft.Container(
            left=left,
            top=top,
            content=ft.Text(text, size=12, color=theme.TEXT_MUTED),
        )

    def _fielders(self, active_position: DefensivePosition) -> list[ft.Control]:
        spots = {
            DefensivePosition.PITCHER: ("ピッチャー", 126, 150),
            DefensivePosition.CATCHER: ("キャッチャー", 126, 315),
            DefensivePosition.FIRST_BASE: ("一るい", 238, 190),
            DefensivePosition.SECOND_BASE: ("二るい", 198, 106),
            DefensivePosition.THIRD_BASE: ("三るい", 18, 190),
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
            ft.Text(kids_text(question.prompt), size=22, weight=ft.FontWeight.BOLD, color=theme.TEXT),
            ft.Text(
                kids_text("えらんだ場所の人として、いちばん先にすることをこたえてください。"),
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
                    ft.Text(message, text_align=ft.TextAlign.CENTER, color=theme.TEXT_MUTED),
                    ft.Button(
                        content="もう一度",
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
                    content="もう一度",
                    icon=ft.Icons.REPLAY,
                    on_click=on_restart,
                ),
                ft.Button(
                    content="けっかを見る" if is_finished else "つぎへ",
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
                ft.Text(text, size=13, weight=ft.FontWeight.W_600, color=theme.TEXT),
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
                    ft.Text(label, size=12, color=theme.TEXT_MUTED),
                    ft.Text(value, size=14, color=theme.TEXT, weight=ft.FontWeight.W_600),
                ],
            ),
        ],
    )
