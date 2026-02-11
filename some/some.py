"""Main Steam Quest application."""
import reflex as rx
from some.state import QuizState
from some.components import game_card, quiz_component


def navbar() -> rx.Component:
    """Render the navigation bar."""
    return rx.box(
        rx.box(
            rx.flex(
                rx.box(
                    rx.text.span(
                        "STEAM",
                        background="#2563eb",
                        padding_x="0.5rem",
                        padding_y="0.125rem",
                        border_radius="0.125rem",
                    ),
                    rx.text.span(
                        "QUEST",
                        color="#60a5fa",
                        margin_left="0.5rem",
                    ),
                    font_size="1.5rem",
                    font_weight="900",
                    color="white",
                    cursor="pointer",
                    letter_spacing="-0.05em",
                    display="flex",
                    align_items="center",
                    gap="0.5rem",
                    on_click=lambda: QuizState.set_view("welcome"),
                ),
                rx.form(
                    rx.input(
                        type="text",
                        placeholder="Search specific game...",
                        value=QuizState.search_query,
                        on_change=QuizState.set_search_query,
                        width="100%",
                        background="rgba(0, 0, 0, 0.5)",
                        border="1px solid rgba(255, 255, 255, 0.1)",
                        border_radius="0.25rem",
                        padding_x="1.25rem",
                        padding_y="0.75rem",
                        font_size="0.875rem",
                        color="white",
                        _focus={
                            "outline": "none",
                            "border_color": "#3b82f6",
                        },
                        transition="border-color 0.3s",
                    ),
                    on_submit=QuizState.search_game,
                    width=["100%", "100%", "24rem"],
                ),
                direction=["column", "column", "row"],
                justify="space-between",
                align_items="center",
                gap="1.5rem",
            ),
            max_width="80rem",
            margin_x="auto",
        ),
        padding="1.5rem",
        border_bottom="1px solid rgba(255, 255, 255, 0.05)",
        margin_bottom="2rem",
        position="sticky",
        top="0",
        background="rgba(23, 26, 33, 0.95)",
        backdrop_filter="blur(12px)",
        z_index="50",
    )


def welcome_view() -> rx.Component:
    """Render the welcome screen."""
    return rx.box(
        rx.heading(
            rx.text("FIND YOUR NEXT", display="block"),
            rx.text("STEAM ADVENTURE", color="#60a5fa", display="block"),
            size="9",
            font_weight="900",
            color="white",
            margin_bottom="2rem",
            letter_spacing="-0.05em",
            text_align="center",
        ),
        rx.text(
            "Answer a few questions about your playstyle and availability to discover hand-picked Steam games with estimated playtimes and trailers.",
            color="#9ca3af",
            margin_bottom="3rem",
            max_width="42rem",
            margin_x="auto",
            text_align="center",
        ),
        rx.button(
            "START THE QUIZ",
            on_click=lambda: QuizState.set_view("quiz"),
            padding_x="3rem",
            padding_y="1.25rem",
            background="#2563eb",
            color="white",
            border_radius="0.25rem",
            font_weight="900",
            font_size="1.25rem",
            box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1)",
            transition="all 0.3s",
            _hover={
                "background": "#1d4ed8",
            },
            _active={
                "transform": "scale(0.95)",
            },
        ),
        rx.cond(
            QuizState.error_message != "",
            rx.box(
                QuizState.error_message,
                margin_top="2rem",
                padding="1rem",
                background="rgba(127, 29, 29, 0.2)",
                border="1px solid rgba(239, 68, 68, 0.3)",
                color="#fca5a5",
                font_family="'JetBrains Mono', monospace",
                font_size="0.875rem",
                border_radius="0.25rem",
                max_width="28rem",
                margin_x="auto",
            ),
        ),
        text_align="center",
        padding_y="8rem",
    )


def loading_view() -> rx.Component:
    """Render the loading screen."""
    return rx.box(
        rx.box(
            rx.spinner(
                size="3",
                color="#3b82f6",
            ),
            margin_bottom="1.5rem",
        ),
        rx.heading(
            "Consulting the Archives...",
            size="7",
            font_weight="900",
            color="white",
            letter_spacing="0.1em",
            text_transform="uppercase",
        ),
        padding_y="10rem",
        text_align="center",
        display="flex",
        flex_direction="column",
        align_items="center",
    )


def results_view() -> rx.Component:
    """Render the results screen."""
    return rx.box(
        # Accuracy card
        rx.box(
            rx.flex(
                rx.box(
                    rx.heading(
                        "Quiz Match Accuracy",
                        size="7",
                        font_weight="900",
                        color="white",
                        text_transform="uppercase",
                        letter_spacing="-0.025em",
                    ),
                    rx.text(
                        QuizState.accuracy_reasoning,
                        color="#9ca3af",
                        max_width="42rem",
                    ),
                ),
                rx.text(
                    f"{QuizState.accuracy_percentage}%",
                    font_size="3rem",
                    font_family="'JetBrains Mono', 'Space Mono', monospace",
                    color="#60a5fa",
                ),
                direction=["column", "column", "row"],
                justify="space-between",
                align_items="center",
                gap="1.5rem",
            ),
            margin_bottom="3rem",
            padding="2rem",
            background_color="rgba(22, 32, 45, 0.8)",
            border_left="4px solid #3b82f6",
            border_radius="0 0.5rem 0.5rem 0",
        ),
        # Game cards grid
        rx.box(
            rx.foreach(
                QuizState.recommendations,
                game_card,
            ),
            display="grid",
            grid_template_columns=[
                "repeat(1, minmax(0, 1fr))",
                "repeat(2, minmax(0, 1fr))",
                "repeat(3, minmax(0, 1fr))",
            ],
            gap="2.5rem",
        ),
        # Return to quiz button
        rx.box(
            rx.button(
                "← Take the quiz again",
                on_click=lambda: QuizState.set_view("quiz"),
                color="#60a5fa",
                text_transform="uppercase",
                font_weight="900",
                letter_spacing="0.1em",
                font_size="0.875rem",
                background="transparent",
                _hover={
                    "color": "white",
                },
                transition="colors 0.3s",
            ),
            margin_top="4rem",
            text_align="center",
        ),
    )


def index() -> rx.Component:
    """Main application component."""
    return rx.box(
        navbar(),
        rx.box(
            rx.cond(
                QuizState.view == "welcome",
                welcome_view(),
            ),
            rx.cond(
                QuizState.view == "loading",
                loading_view(),
            ),
            rx.cond(
                QuizState.view == "results",
                results_view(),
            ),
            rx.cond(
                QuizState.view == "quiz",
                quiz_component(),
            ),
            max_width="80rem",
            margin_x="auto",
            padding_x="1.5rem",
        ),
        min_height="100vh",
        background="linear-gradient(135deg, #171a21 0%, #1b2838 100%)",
        padding_bottom="5rem",
    )


# Add custom styles
style = {
    "font_family": "'Inter', sans-serif",
    "background_color": "#1b2838",
    "color": "#c7d5e0",
}

# Custom stylesheets
stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap",
]

# Create the app
app = rx.App(
    style=style,
    stylesheets=stylesheets,
)
app.add_page(index, route="/")
