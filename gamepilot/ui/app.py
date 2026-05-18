"""gamepilot UI — TUI com Textual."""

from typing import List, Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Log, Select, Static
from textual.containers import Horizontal, Vertical

from .. import config, manifests, scanner, wine
from ..i18n import t
from ..models import ModTool, ScannerResult
from . import actions


DEFAULT_CSS = """
Screen {
    background: $surface;
    color: $text;
}

#shell {
    height: 1fr;
    padding: 1 2;
}

#shell.compact {
    padding: 0 1;
}

#hero {
    padding: 0 1 1 1;
    text-style: bold;
    color: $accent;
    content-align: center middle;
}

#hero.compact {
    padding: 0 0 0 0;
}

#hero_subtitle {
    padding: 0 1 1 1;
    color: $text-muted;
    content-align: center middle;
}

#hero_subtitle.compact,
#hero_subtitle.tight {
    display: none;
}

#content {
    height: 1fr;
}

#content.compact {
    layout: vertical;
}

.panel {
    border: round $panel;
    background: $surface;
    padding: 1;
}

.panel.compact {
    padding: 0 1;
}

.panel.active-section {
    border: round $accent;
}

#games_panel {
    width: 1.1fr;
    margin-right: 1;
}

#games_panel.compact {
    width: 100%;
    margin-right: 0;
    margin-bottom: 1;
}

#tools_panel {
    width: 1fr;
}

#tools_panel.compact {
    width: 100%;
}

.section_label {
    text-style: bold;
    color: $accent;
    margin-bottom: 1;
}

.panel.active-section .section_label {
    color: $warning;
}

#games_count,
#selection_summary,
#selection_detail,
#status {
    padding: 0 1;
}

#games_count {
    color: $text-muted;
    margin-bottom: 1;
}

#games_count.compact {
    margin-bottom: 0;
}

#selection_summary {
    color: $text;
    text-style: bold;
}

#selection_detail {
    color: $text-muted;
    margin-bottom: 1;
}

#selection_detail.compact {
    margin-bottom: 0;
}

#games_actions,
#tool_actions {
    margin-bottom: 1;
}

#tool_actions.compact {
    layout: vertical;
    margin-bottom: 0;
}

#tool_actions.tight {
    height: auto;
}

#games_table {
    height: 1fr;
    min-height: 8;
    border: round $primary;
    background: $surface-darken-1;
}

#games_table.compact {
    min-height: 6;
}

#games_table:focus {
    border: round $accent;
}

#tools {
    width: 100%;
    margin-bottom: 1;
}

#tools.compact {
    margin-bottom: 0;
}

#status {
    color: $text-muted;
    border-left: tall $panel;
    margin-bottom: 1;
}

#status.compact {
    margin-bottom: 0;
}

#status.tight {
    display: none;
}

#log {
    height: 1fr;
    min-height: 8;
    border: round $panel;
    background: $surface-darken-1;
    padding: 1;
}

#log.compact {
    min-height: 6;
    padding: 0 1;
}

#log.tight {
    display: none;
}

#help_strip {
    padding: 0 1;
    background: $surface-darken-2;
    border-top: heavy $panel;
    color: $text-muted;
    text-style: italic;
}

Horizontal > Button {
    width: auto;
    height: 3;
    min-width: 10;
    margin-right: 1;
}

Horizontal.compact > Button {
    width: 100%;
    height: 3;
    min-width: 0;
    margin-right: 0;
}

Horizontal > Button:last-child {
    margin-right: 0;
}
"""


class MainScreen(Screen):
    """Container principal com navegação por seções."""

    BINDINGS = [
        Binding("q", "quit", "Sair", show=True, priority=True),
        Binding("s", "scan", "Escanear", show=True, priority=True),
        Binding("i", "install", "Instalar", show=True, priority=True),
        Binding("r", "launch", "Lançar", show=True, priority=True),
        Binding("c", "shortcut", "Atalho", show=True, priority=True),
        Binding("1", "focus_games", "Games", show=True, priority=True),
        Binding("g", "focus_games", "Games", show=False, priority=True),
        Binding("2", "focus_tools", "Tools", show=True, priority=True),
        Binding("t", "focus_tools", "Tools", show=False, priority=True),
        Binding("3", "focus_log", "Log", show=True, priority=True),
        Binding("l", "focus_log", "Log", show=False, priority=True),
        Binding("enter", "select", "Selecionar", show=False),
        Binding("j", "move_down", "↓", show=False),
        Binding("k", "move_up", "↑", show=False),
        Binding("escape", "quit", "Esc Sair", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Static(t("welcome"), id="hero"),
            Static(
                "Scan, escolha uma ferramenta e execute sem sair da TUI.",
                id="hero_subtitle",
            ),
            Horizontal(
                Vertical(
                    Static("Jogos encontrados", classes="section_label"),
                    Button(t("scan_games"), id="scan", variant="primary"),
                    Static(t("no_games_scanned"), id="games_count"),
                    DataTable(id="games_table", show_header=True, zebra_stripes=True),
                    id="games_panel",
                    classes="panel",
                ),
                Vertical(
                    Static("Seleção e ações", classes="section_label"),
                    Static("Nenhum jogo selecionado", id="selection_summary"),
                    Static(
                        "Escaneie e mova o cursor para ver as ferramentas disponíveis.",
                        id="selection_detail",
                    ),
                    Static(t("dependencies_mods"), id="tools_label", classes="section_label"),
                    Select([], id="tools"),
                    Horizontal(
                        Button(t("install_tool"), id="install", variant="success"),
                        Button(t("launch_tool"), id="launch", variant="warning"),
                        Button("🖥️ Shortcut", id="shortcut", variant="primary"),
                        id="tool_actions",
                    ),
                    Static("Estado: aguardando escaneamento", id="status"),
                    Log(id="log", highlight=True, max_lines=500),
                    id="tools_panel",
                    classes="panel",
                ),
                id="content",
            ),
            Static(
                "Hotkeys: 1/g jogos • 2/t ferramentas • 3/l log • s escanear • i instalar • r lançar • c atalho • q/esc sair",
                id="help_strip",
            ),
            id="shell",
        )
        yield Footer()

    async def on_mount(self) -> None:
        self.app_cfg = config.load_config()
        self.available_games: List[ScannerResult] = []
        self.available_tools: List[ModTool] = []
        self.selected_game: Optional[ScannerResult] = None
        self.selected_tool: Optional[ModTool] = None
        self._focused_section = "games"
        table = self.query_one("#games_table", DataTable)
        table.add_column("Game", key="game")
        table.add_column("Source", key="source")
        table.add_column("Prefix", key="prefix")
        table.cursor_type = "row"

        self._compact_mode = None
        self._tight_mode = None
        self._apply_responsive_layout(self.size.width, self.size.height)
        self._set_active_section("games")
        self._set_action_state()
        self._refresh_selection_panel()

        try:
            self.manifests = manifests.load_manifests()
        except Exception as exc:
            self.manifests = []
            self._log().write_line(f"⚠️ Falha ao carregar manifestos: {exc}")
            self._set_status("Manifestos indisponíveis")

        initial_game = getattr(self, "_initial_game", None)
        if initial_game:
            self._set_status(f"Buscando jogo: {initial_game}")
            self._log().write_line(f"🎮 Procurando jogo: {initial_game}...")
            await self._auto_scan(initial_game)

    def _log(self) -> Log:
        return self.query_one("#log", Log)

    def _set_status(self, message: str) -> None:
        self.query_one("#status", Static).update(f"Estado: {message}")

    def _set_active_section(self, section: str) -> None:
        """Atualiza a seção ativa com destaque visual."""
        self._focused_section = section
        for sec_id in ("games_panel", "tools_panel"):
            panel = self.query_one(f"#{sec_id}", Vertical)
            panel.set_class(section in (sec_id.replace("_panel", ""), "log") and sec_id == "tools_panel", "active-section")
        # Se a seção for 'log', também destacamos tools_panel (pois log está dentro)
        if section == "log":
            self.query_one("#tools_panel", Vertical).set_class(True, "active-section")

    def _section_widgets(self, section: str) -> List:
        """Retorna widgets focáveis de uma seção."""
        if section == "games":
            return [self.query_one("#games_table", DataTable)]
        if section == "tools":
            widgets = [self.query_one("#tools", Select)]
            for btn_id in ("install", "launch", "shortcut"):
                btn = self.query_one(f"#{btn_id}", Button)
                if not btn.disabled:
                    widgets.append(btn)
            return widgets
        if section == "log":
            return [self.query_one("#log", Log)]
        return []

    def _focus_section(self, section: str, index: int = 0) -> None:
        """Foca um widget específico de uma seção."""
        self._set_active_section(section)
        widgets = self._section_widgets(section)
        if widgets:
            idx = max(0, min(index, len(widgets) - 1))
            widgets[idx].focus()

    def _move_focus_in_section(self, direction: int) -> bool:
        """Move foco dentro da seção atual. Retorna True se conseguiu."""
        section = self._focused_section
        widgets = self._section_widgets(section)
        if not widgets:
            return False

        focused = self.focused
        if focused is None:
            widgets[0].focus()
            return True

        try:
            current_idx = widgets.index(focused)
        except ValueError:
            widgets[0].focus()
            return True

        new_idx = current_idx + direction
        if 0 <= new_idx < len(widgets):
            widgets[new_idx].focus()
            return True
        return False

    def _apply_responsive_layout(self, width: int, height: int) -> None:
        compact = width < 110
        tight = height < 28
        if compact == getattr(self, "_compact_mode", None) and tight == getattr(self, "_tight_mode", None):
            return

        self._compact_mode = compact
        self._tight_mode = tight

        shell = self.query_one("#shell", Vertical)
        content = self.query_one("#content", Horizontal)
        hero = self.query_one("#hero", Static)
        subtitle = self.query_one("#hero_subtitle", Static)
        games_count = self.query_one("#games_count", Static)
        selection_detail = self.query_one("#selection_detail", Static)
        status = self.query_one("#status", Static)
        tool_actions = self.query_one("#tool_actions", Horizontal)
        games_panel = self.query_one("#games_panel", Vertical)
        tools_panel = self.query_one("#tools_panel", Vertical)
        games_table = self.query_one("#games_table", DataTable)
        log = self._log()
        tools = self.query_one("#tools", Select)

        for widget in (shell, content, hero, subtitle, games_count, selection_detail, status, tool_actions, games_panel, tools_panel, games_table, log, tools):
            widget.set_class(compact, "compact")
            widget.set_class(tight, "tight")

        if compact:
            self.query_one("#install", Button).label = "Inst."
            self.query_one("#launch", Button).label = "Run"
            self.query_one("#shortcut", Button).label = "Link"
            self.query_one("#scan", Button).label = "Scan"
            self.query_one("#help_strip", Static).update(
                "1/g games • 2/t tools • 3/l log • s scan • i inst. • r run • c link • q/esc"
            )
        else:
            self.query_one("#install", Button).label = t("install_tool")
            self.query_one("#launch", Button).label = t("launch_tool")
            self.query_one("#shortcut", Button).label = "🖥️ Shortcut"
            self.query_one("#scan", Button).label = t("scan_games")
            self.query_one("#help_strip", Static).update(
                "Hotkeys: 1/g jogos • 2/t ferramentas • 3/l log • s escanear • i instalar • r lançar • c atalho • q/esc sair"
            )

    def on_resize(self, event) -> None:
        self._apply_responsive_layout(event.size.width, event.size.height)

    def _set_action_state(self) -> None:
        has_game = self.selected_game is not None
        has_tool = self.selected_tool is not None
        self.query_one("#install", Button).disabled = not (has_game and has_tool)
        self.query_one("#launch", Button).disabled = not (has_game and has_tool)
        self.query_one("#shortcut", Button).disabled = not has_game
        tools_select = self.query_one("#tools", Select)
        tools_select.disabled = not has_game or not self.available_tools

    def _refresh_selection_panel(self) -> None:
        game = self.selected_game
        tool = self.selected_tool

        if game is None:
            summary = "Nenhum jogo selecionado"
            detail = "Escaneie para preencher a lista de jogos e manifestos."
        else:
            summary = f"Jogo: {game.name}"
            details = [f"Fonte: {game.source}"]
            if game.prefix_path:
                details.append(f"Prefixo: {game.prefix_path}")
            detail = " • ".join(details)

        if tool is None:
            tool_text = "Ferramenta: nenhuma disponível"
            if game is not None and self.available_tools:
                tool_text = "Escolha uma ferramenta para instalar ou lançar."
        else:
            tool_text = f"Ferramenta: {tool.name}"

        self.query_one("#selection_summary", Static).update(summary)
        self.query_one("#selection_detail", Static).update(f"{detail}\n{tool_text}")
        self._set_action_state()

    async def _run_scan(self) -> List[ScannerResult]:
        log = self._log()
        self._set_status("escaneando jogos")
        log.write_line("🔍 " + t("scan_games") + "...")
        games = await scanner.scan_all_games()
        self.available_games = games

        table = self.query_one("#games_table", DataTable)
        table.clear()
        for game in games:
            prefix = str(game.prefix_path) if game.prefix_path else "—"
            table.add_row(game.name, game.source, prefix)

        count_text = f"{len(games)} jogo{'s' if len(games) != 1 else ''} carregado{'s' if len(games) != 1 else ''}"
        self.query_one("#games_count", Static).update(count_text if games else t("no_games_found"))
        if games:
            log.write_line(f"✅ {len(games)} jogos encontrados.")
            self._set_status(count_text)
        else:
            log.write_line(f"ℹ️ {t('no_games_found')}")
            self._set_status(t("no_games_found"))

        if self.selected_game and not any(g.name == self.selected_game.name for g in games):
            self.selected_game = None
            self.selected_tool = None
            self.available_tools = []
            self._set_tools_for_game(None)

        self._refresh_selection_panel()
        return games

    def _set_tools_for_game(self, game: Optional[ScannerResult]) -> None:
        select = self.query_one("#tools", Select)
        if game is None:
            self.available_tools = []
            select.set_options([("(no tools)", "(no tools)")])
            try:
                select.value = "(no tools)"
            except Exception:
                pass
            self.selected_tool = None
            return

        self.available_tools = actions.tools_for_game(game, self.manifests)
        if self.available_tools:
            select.set_options([(tool.name, tool.name) for tool in self.available_tools])
            self.selected_tool = self.available_tools[0]
            try:
                select.value = self.available_tools[0].name
            except Exception:
                pass
        else:
            select.set_options([("(no tools)", "(no tools)")])
            try:
                select.value = "(no tools)"
            except Exception:
                pass
            self.selected_tool = None

    def _apply_game_selection(self, game: ScannerResult) -> None:
        self.selected_game = game
        self._set_tools_for_game(game)
        self._set_active_section("games")
        if self.selected_tool is not None:
            self._set_status(f"selecionado: {game.name} / {self.selected_tool.name}")
        else:
            self._set_status(f"selecionado: {game.name}")
        self._refresh_selection_panel()

    async def _auto_scan(self, game_name: str) -> None:
        log = self._log()
        games = await self._run_scan()
        for game in games:
            if game_name.lower() in game.name.lower():
                self._apply_game_selection(game)
                log.write_line(f"✅ Jogo encontrado: {game.name}")
                return
        log.write_line(f"⚠️ Jogo '{game_name}' não encontrado.")
        self._set_status(f"'{game_name}' não encontrado")

    async def _install_selected(self) -> None:
        self._set_status("instalando ferramenta")
        result = await actions.install_tool_action(
            self.selected_game,
            self.selected_tool,
            self._log().write_line,
        )
        if result == wine.InstallResult.INSTALLED:
            self._set_status("instalação concluída")
        elif result == wine.InstallResult.DELEGATED_TO_BROWSER:
            self._set_status("instalação aberta no navegador")
        else:
            self._set_status("instalação falhou")

    async def _launch_selected(self) -> None:
        self._set_status("lançando ferramenta")
        rc = await actions.launch_tool_action(
            self.selected_game,
            self.selected_tool,
            self._log().write_line,
        )
        self._set_status("ferramenta lançada" if rc == 0 else "falha ao lançar")

    def _create_shortcut(self) -> None:
        result = actions.create_shortcut_action(self.selected_game, self._log().write_line)
        if result is not None:
            self._set_status(f"atalho criado: {result.name}")
        else:
            self._set_status("não foi possível criar atalho")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "scan":
            await self._run_scan()
        elif btn == "install":
            await self._install_selected()
        elif btn == "launch":
            await self._launch_selected()
        elif btn == "shortcut":
            self._create_shortcut()

    def on_data_table_row_highlighted(self, event) -> None:
        self._set_active_section("games")
        row_key = event.row_key
        if row_key is None:
            return
        try:
            name = self.query_one("#games_table", DataTable).get_row(row_key)[0]
        except Exception:
            return
        for game in self.available_games:
            if game.name == name:
                self._apply_game_selection(game)
                break

    def on_select_changed(self, event) -> None:
        if event.control.id != "tools":
            return
        self._set_active_section("tools")
        value = event.value
        if value is None or value == Select.BLANK or value == "(no tools)":
            return
        if self.selected_game is None:
            return
        for tool in actions.tools_for_game(self.selected_game, self.manifests):
            if tool.name == value:
                self.selected_tool = tool
                self._set_status(f"ferramenta selecionada: {tool.name}")
                self._refresh_selection_panel()
                return

    async def action_scan(self) -> None:
        await self._run_scan()

    async def action_install(self) -> None:
        await self._install_selected()

    async def action_launch(self) -> None:
        await self._launch_selected()

    def action_shortcut(self) -> None:
        self._create_shortcut()

    def action_focus_games(self) -> None:
        self._focus_section("games")

    def action_focus_tools(self) -> None:
        self._focus_section("tools")

    def action_focus_log(self) -> None:
        self._focus_section("log")

    def action_move_down(self) -> None:
        section = self._focused_section
        focused = self.focused

        if section == "games" and focused is not None:
            # DataTable: usar cursor down nativo
            fn = getattr(focused, "action_cursor_down", None)
            if callable(fn):
                fn()
                return

        if section == "log" and focused is not None:
            # Log: scroll down
            fn = getattr(focused, "scroll_down", None)
            if callable(fn):
                fn()
                return

        # Tools (ou fallback): mover foco para próximo widget na seção
        if self._move_focus_in_section(1):
            return

    def action_move_up(self) -> None:
        section = self._focused_section
        focused = self.focused

        if section == "games" and focused is not None:
            fn = getattr(focused, "action_cursor_up", None)
            if callable(fn):
                fn()
                return

        if section == "log" and focused is not None:
            fn = getattr(focused, "scroll_up", None)
            if callable(fn):
                fn()
                return

        if self._move_focus_in_section(-1):
            return

    def action_select(self) -> None:
        focused = self.focused
        if focused is None:
            return

        section = self._focused_section

        if section == "tools" and isinstance(focused, Select):
            for method in ("action_show_overlay", "action_select"):
                fn = getattr(focused, method, None)
                if fn is not None:
                    fn()
                    return

        if section == "tools" and isinstance(focused, Button):
            press = getattr(focused, "press", None)
            if callable(press):
                press()
            return

        if section == "games" and isinstance(focused, DataTable):
            # Enter em DataTable seleciona a linha atual
            fn = getattr(focused, "action_select_cursor", None)
            if fn is not None:
                fn()
            return

        for method in ("action_select_cursor", "action_show_overlay", "action_select"):
            fn = getattr(focused, method, None)
            if fn is not None:
                fn()
                return


class GamePiLotApp(App):
    """Aplicação principal."""

    CSS = DEFAULT_CSS
    TITLE = "GamePiLot"

    def __init__(self, game_name: str | None = None) -> None:
        super().__init__()
        self._game_name = game_name

    def on_mount(self) -> None:
        screen = MainScreen()
        screen._initial_game = self._game_name
        self.push_screen(screen)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="GamePiLot — Gerenciador de mods")
    parser.add_argument("--game", help="Nome do jogo para abrir diretamente")
    args = parser.parse_args()
    app = GamePiLotApp(game_name=args.game)
    app.run()
