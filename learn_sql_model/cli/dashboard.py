from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Static
import typer

from learn_sql_model.cli.common import verbose_callback
from learn_sql_model.models.hero import Heros

dashboard_app = typer.Typer()


@dashboard_app.callback()
def config(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    "dashboard cli"


class HeroName(Static):
    """A stopwatch widget."""


class DashboardApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield ScrollableContainer(*[HeroName(hero.name) for hero in Heros.list().heros])

    @property
    def ws(self):
        def connect():
            self._ws = create_connection(
                f"ws://{config.api_client.url.replace('https://', '')}/ws-heros"
            )

        if not hasattr(self, "_ws"):
            connect()
        if not self._ws.connected:
            connect()
        return self._ws

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


@dashboard_app.command()
def run(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    app = DashboardApp()
    app.run()
