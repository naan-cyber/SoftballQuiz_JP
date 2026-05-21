from __future__ import annotations

import flet as ft

from softball_quiz.data import (
    question_counts_by_position,
    question_counts_by_rule_topic,
    question_counts_by_runner_role,
    questions_for_position,
    questions_for_rule_topic,
    questions_for_runner_role,
)
from softball_quiz.models import DefensivePosition, RuleTopic, RunnerRole
from softball_quiz.services import QuizEngine
from softball_quiz.ui import theme
from softball_quiz.ui.components import (
    FeedbackPanel,
    FooterBar,
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
        self.selected_runner_role: RunnerRole | None = None
        self.selected_rule_topic: RuleTopic | None = None
        self.engine = QuizEngine(questions_for_position(self.selected_position))
        self.header = HeaderBar()
        self.position_selector = PositionSelector()
        self.scenario_panel = ScenarioPanel()
        self.question_panel = QuestionPanel()
        self.feedback_panel = FeedbackPanel()
        self.navigation = NavigationBar()
        self.result_panel = ResultPanel()
        self.footer = FooterBar()
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
        self.page.window.min_width = 320
        self.page.window.min_height = 720
        self.page.on_resized = lambda _: self._render()

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
                                selected_runner_role=self.selected_runner_role,
                                selected_rule_topic=self.selected_rule_topic,
                                position_counts=question_counts_by_position(),
                                runner_counts=question_counts_by_runner_role(),
                                rule_counts=question_counts_by_rule_topic(),
                                on_select_all=self._select_all,
                                on_select_position=self._select_position,
                                on_select_runner_role=self._select_runner_role,
                                on_select_rule_topic=self._select_rule_topic,
                            ),
                            self._render_body(),
                            self.footer.render(),
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
        is_narrow = (self.page.width or 0) < 760
        question_controls = ft.Column(
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
        )
        field_controls = self.scenario_panel.render_field(question)
        if is_narrow:
            play_area: ft.Control = ft.Column(
                spacing=14,
                controls=[
                    field_controls,
                    question_controls,
                ],
            )
        else:
            play_area = ft.Row(
                spacing=18,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        width=360,
                        content=field_controls,
                    ),
                    ft.Container(
                        expand=True,
                        content=question_controls,
                    ),
                ],
            )
        return ft.Column(
            spacing=16,
            controls=[
                self.scenario_panel.render(question),
                play_area,
            ],
        )

    def _select_answer(self, option_id: str) -> None:
        self.engine.select_answer(option_id)
        self._render()

    def _select_position(self, position: DefensivePosition | None) -> None:
        self.selected_position = position
        self.selected_runner_role = None
        self.selected_rule_topic = None
        self.engine = QuizEngine(questions_for_position(position))
        self.show_result = False
        self._render()

    def _select_runner_role(self, role: RunnerRole) -> None:
        self.selected_position = None
        self.selected_runner_role = role
        self.selected_rule_topic = None
        self.engine = QuizEngine(questions_for_runner_role(role))
        self.show_result = False
        self._render()

    def _select_rule_topic(self, topic: RuleTopic) -> None:
        self.selected_position = None
        self.selected_runner_role = None
        self.selected_rule_topic = topic
        self.engine = QuizEngine(questions_for_rule_topic(topic))
        self.show_result = False
        self._render()

    def _select_all(self) -> None:
        self.selected_position = None
        self.selected_runner_role = None
        self.selected_rule_topic = None
        self.engine = QuizEngine(questions_for_position(None))
        self.show_result = False
        self._render()

    def _next(self, _: ft.Event[ft.Button]) -> None:
        if self.engine.is_finished:
            self.show_result = True
        else:
            self.engine.move_next()
        self._render()

    def _restart(self, _: ft.Event[ft.Button]) -> None:
        if self.selected_rule_topic is not None:
            questions = questions_for_rule_topic(self.selected_rule_topic)
        elif self.selected_runner_role is not None:
            questions = questions_for_runner_role(self.selected_runner_role)
        else:
            questions = questions_for_position(self.selected_position)
        self.engine = QuizEngine(questions)
        self.show_result = False
        self._render()


def app_main(page: ft.Page) -> None:
    SoftballQuizApp(page).start()


def main() -> None:
    ft.run(app_main)
