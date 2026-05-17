from __future__ import annotations

import flet as ft

from softball_quiz.data import question_counts_by_position, questions_for_position
from softball_quiz.models import DefensivePosition
from softball_quiz.services import QuizEngine
from softball_quiz.ui import theme
from softball_quiz.ui.components import (
    FeedbackPanel,
    HeaderBar,
    NavigationBar,
    PositionSelector,
    QuestionPanel,
    ResultPanel,
    ScenarioPanel,
)


class SoftballQuizApp:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.selected_position: DefensivePosition | None = None
        self.engine = QuizEngine(questions_for_position(self.selected_position))
        self.header = HeaderBar()
        self.position_selector = PositionSelector()
        self.scenario_panel = ScenarioPanel()
        self.question_panel = QuestionPanel()
        self.feedback_panel = FeedbackPanel()
        self.navigation = NavigationBar()
        self.result_panel = ResultPanel()
        self.show_result = False

    def start(self) -> None:
        self._configure_page()
        self._render()

    def _configure_page(self) -> None:
        self.page.title = theme.APP_TITLE
        self.page.bgcolor = theme.BACKGROUND
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(color_scheme_seed=theme.PRIMARY)
        self.page.window.min_width = 760
        self.page.window.min_height = 720

    def _render(self) -> None:
        self.page.controls.clear()
        self.page.add(
            ft.SafeArea(
                content=ft.Container(
                    padding=ft.Padding(20, 20, 20, 20),
                    content=ft.Column(
                        spacing=18,
                        controls=[
                            self.header.render(
                                current_number=self.engine.current_number,
                                total=self.engine.total,
                                score=self.engine.score,
                                progress=self.engine.progress,
                                on_reset=self._restart,
                            ),
                            self.position_selector.render(
                                selected_position=self.selected_position,
                                counts=question_counts_by_position(),
                                on_select=self._select_position,
                            ),
                            self._render_body(),
                        ],
                    ),
                )
            )
        )
        self.page.update()

    def _render_body(self) -> ft.Control:
        if self.show_result:
            return self.result_panel.render(
                score=self.engine.score,
                total=self.engine.total,
                on_restart=self._restart,
            )

        question = self.engine.current_question
        return ft.Row(
            spacing=18,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=360,
                    content=self.scenario_panel.render(question),
                ),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            self.question_panel.render(
                                question=question,
                                selected_option_id=self.engine.selected_option_id,
                                on_select=self._select_answer,
                            ),
                            self.feedback_panel.render(
                                question,
                                self.engine.selected_option_id,
                            ),
                            self.navigation.render(
                                answered=self.engine.answered,
                                is_finished=self.engine.is_finished,
                                on_next=self._next,
                                on_restart=self._restart,
                            ),
                        ],
                    ),
                ),
            ],
        )

    def _select_answer(self, option_id: str) -> None:
        self.engine.select_answer(option_id)
        self._render()

    def _select_position(self, position: DefensivePosition | None) -> None:
        self.selected_position = position
        self.engine = QuizEngine(questions_for_position(position))
        self.show_result = False
        self._render()

    def _next(self, _: ft.Event[ft.Button]) -> None:
        if self.engine.is_finished:
            self.show_result = True
        else:
            self.engine.move_next()
        self._render()

    def _restart(self, _: ft.Event[ft.Button]) -> None:
        self.engine = QuizEngine(questions_for_position(self.selected_position))
        self.show_result = False
        self._render()


def app_main(page: ft.Page) -> None:
    SoftballQuizApp(page).start()


def main() -> None:
    ft.run(app_main)
