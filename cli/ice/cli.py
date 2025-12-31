"""
DevLog CLI Shell - Updated for DevLog name
"""

import shlex
from pathlib import Path
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

# Import shared commands
from devlog.commands import CommandContext, registry, register_all_commands

# Import completer (CLI specific)
from devlog.cli.completer.completer import DynamicLogParserCompleter


HISTORY_FILE = Path.home() / ".devlog_history"

style = Style.from_dict({
    'prompt': 'cyan bold',
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'completion-menu.meta.completion': 'bg:#444444 #ffffff',
    'completion-menu.meta.completion.current': 'bg:#00aaaa #000000',
})


class DevLogShell:
    """
    Modern shell for DevLog using shared commands layer
    """
    
    def __init__(self, api=None, debug=False):
        self.console = Console()
        self.api = api  # API Layer
        self.debug = debug
        self.last_results = []
        
        # Config
        self.config = {
            'max_display': 20,
            'auto_save': False,
            'show_confidence': True,
        }
        
        # Use global registry with shared commands
        register_all_commands()
        self.registry = registry
        
        # Add CLI-specific utility commands
        self._register_cli_commands()
        
        # Dynamic completer
        completer = DynamicLogParserCompleter(self)
        
        # Prompt session
        self.session = PromptSession(
            history=FileHistory(str(HISTORY_FILE)),
            completer=completer,
            style=style,
        )
        
        self.running = True
    
    def _register_cli_commands(self):
        """Register CLI-specific commands (help, exit, config, cls)"""
        from devlog.commands.utility import (
            HelpCommand, ExitCommand, ConfigCommand, ClearScreenCommand
        )
        
        self.registry.register(HelpCommand())
        self.registry.register(ExitCommand())
        self.registry.register(ConfigCommand())
        self.registry.register(ClearScreenCommand())
    
    def get_prompt(self):
        """Return formatted prompt"""
        return HTML('<prompt>❯</prompt> ')
    
    def cmdloop(self):
        """Main command loop"""
        self.console.print("\n[bold cyan]DevLog Shell[/bold cyan]")
        self.console.print("[dim]Type 'help' for commands, Tab for autocompletion[/dim]")
        self.console.print("[dim]Use ↑↓ for history[/dim]\n")
        
        while self.running:
            try:
                text = self.session.prompt(self.get_prompt())
                
                if not text.strip():
                    continue
                
                parts = shlex.split(text)
                if not parts:
                    continue
                
                command_name = parts[0].lower()
                args = parts[1:]
                
                command = self.registry.get(command_name)
                
                if command:
                    # Create context with API
                    ctx = CommandContext(
                        api=self.api,
                        console=self.console,
                        args=args,
                        raw_input=text,
                        gui_callback=None  # CLI doesn't use callbacks
                    )
                    
                    should_continue = command.execute(ctx)
                    if not should_continue:
                        break
                else:
                    self.console.print(f"[red]Unknown command: {command_name}[/red]")
                    self.console.print("[dim]Type 'help' for available commands[/dim]")
            
            except KeyboardInterrupt:
                self.console.print("\n[dim]Use 'exit' to leave[/dim]")
            except EOFError:
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                if self.debug:
                    import traceback
                    traceback.print_exc()


def main(debug=False, file_path=None):
    """Main entry point for DevLog CLI"""
    console = Console()
    
    try:
        # Display banner
        try:
            from devlog.cli.display.banner import display_banner
            display_banner()
        except:
            console.print("[bold cyan]DevLog - Advanced Log Analysis v2.0[/bold cyan]\n")
        
        # Initialize API layer
        try:
            from devlog.api import create_api
            api = create_api(debug=debug)
            console.print("[green]✓ API initialized[/green]")
        except Exception as e:
            console.print(f"[red]✗ Failed to initialize API: {e}[/red]")
            if debug:
                import traceback
                traceback.print_exc()
            return 1
        
        # If file provided, analyze it directly
        if file_path:
            console.print(f"[yellow]Analyzing file: {file_path}[/yellow]")
            try:
                # Quick analysis mode
                from devlog.core.parsing.processor import LogProcessor
                processor = LogProcessor()
                processor.add_file(file_path)
                
                events = list(processor.process_all())
                console.print(f"[green]✓ Parsed {len(events)} events[/green]")
                
                # Show basic stats
                from devlog.engine.analysis.stats import StatsCalculator
                stats = StatsCalculator().calculate_stats(events)
                
                console.print(f"\n[bold]Summary:[/bold]")
                console.print(f"  Events: {stats['total_events']}")
                console.print(f"  Levels: {stats.get('level_distribution', {})}")
                console.print(f"  Types: {stats.get('event_type_distribution', {})}")
                
            except Exception as e:
                console.print(f"[red]✗ File analysis failed: {e}[/red]")
                return 1
        
        # Initialize shell with API
        shell = DevLogShell(api=api, debug=debug)
        
        # Run shell
        with api:  # Context manager for cleanup
            shell.cmdloop()
        
        return 0
        
    except KeyboardInterrupt:
        console.print("\n[cyan]Session interrupted[/cyan]")
        return 0
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]")
        if debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    debug = '--debug' in sys.argv
    sys.exit(main(debug=debug))