from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Static
import typer
from websocket import create_connection

from learn_sql_model.cli.common import verbose_callback

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


class HerosDisplay(Static):
    """A stopwatch widget."""

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

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        for hero in self.heros:
            yield HeroName(hero.name)


class DashboardApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    # heros = reactive(Heros.list())

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield ScrollableContainer(HerosDisplay())

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
