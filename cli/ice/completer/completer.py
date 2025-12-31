"""
===========================================
FILE 2: completer.py
===========================================
Dynamic Auto-Completer using Command Registry
"""

from prompt_toolkit.completion import Completer, Completion, PathCompleter
from typing import Iterable


class DynamicLogParserCompleter(Completer):
    """Dynamic autocomplete that discovers commands from registry"""
    
    def __init__(self, shell):
        self.shell = shell
        self.path_completer = PathCompleter(expanduser=True)
    
    def get_completions(self, document, complete_event) -> Iterable[Completion]:
        text = document.text_before_cursor
        words = text.split()
        
        # Empty line - suggest all commands
        if not words:
            for cmd in self._get_all_commands():
                yield Completion(
                    cmd.name,
                    start_position=0,
                    display_meta=self._get_command_description(cmd)
                )
            return
        
        # First word - command completion
        if len(words) == 1 and not text.endswith(' '):
            word = words[0]
            for cmd in self._get_all_commands():
                if cmd.name.startswith(word.lower()):
                    yield Completion(
                        cmd.name,
                        start_position=-len(word),
                        display_meta=self._get_command_description(cmd)
                    )
                # Also check aliases
                for alias in cmd.aliases:
                    if alias.startswith(word.lower()) and alias != cmd.name:
                        yield Completion(
                            alias,
                            start_position=-len(word),
                            display_meta=f"→ {cmd.name}"
                        )
            return
        
        # Get command
        command_name = words[0].lower()
        command = self.shell.registry.get(command_name)
        
        if not command:
            return
        
        current_word = words[-1] if not text.endswith(' ') else ''
        
        # Flag completion from command hints
        if current_word.startswith('-'):
            for hint in command.get_completion_hints():
                if hint.startswith(current_word):
                    yield Completion(
                        hint,
                        start_position=-len(current_word),
                        display_meta=self._get_hint_meta(command_name, hint)
                    )
            return
        
        # Context-specific completions
        yield from self._get_context_completions(command, words, current_word)
    
    def _get_all_commands(self):
        """Get all unique commands from registry"""
        return self.shell.registry.get_all()
    
    def _get_command_description(self, command) -> str:
        """Extract first line of help as description"""
        help_text = command.get_help()
        first_line = help_text.split('\n')[0]
        return first_line[:50] if len(first_line) > 50 else first_line
    
    def _get_hint_meta(self, command_name: str, hint: str) -> str:
        """Get metadata for a completion hint"""
        hint_descriptions = {
            '--recursive': 'include subdirs',
            '-r': 'recursive',
            '--pattern': 'file pattern',
            '-p': 'pattern',
            '--sort': 'sort by',
            '-s': 'sort/summary',
            '--detailed': 'detailed view',
            '-d': 'detailed',
            '--confirm': 'skip confirmation',
            '-y': 'yes',
            '--conf': 'confidence',
            '-c': 'conf/case/clear',
            '--limit': 'max results',
            '-l': 'limit/last/live',
            '--file': 'specific file',
            '-f': 'file/filter/field',
            '--no-plugins': 'disable plugins',
            '--show': 'show config',
            '--set': 'set value',
        }
        return hint_descriptions.get(hint, 'flag')
    
    def _get_context_completions(self, command, words, current_word):
        """Context-aware completions based on command"""
        
        # Path completions for add/predict commands
        if command.name in ['add', 'predict']:
            for completion in self.path_completer.get_completions(
                type('Doc', (), {'text_before_cursor': current_word})(), None
            ):
                yield completion
            return
        
        # Database file ID completions for remove
        if command.name == 'remove':
            try:
                logs = self.shell.parser.list_paths()
                for idx, log in enumerate(logs):
                    id_str = str(idx)
                    if id_str.startswith(current_word):
                        yield Completion(
                            id_str,
                            start_position=-len(current_word),
                            display_meta=log.name
                        )
            except:
                pass
            return
        
        # Status completions for filter command
        if command.name == 'filter' and '--event' not in words:
            statuses = ['success', 'warning', 'failed']
            for status in statuses:
                if status.startswith(current_word):
                    yield Completion(
                        status,
                        start_position=-len(current_word),
                        display_meta="status"
                    )
            return
        
        # Event type completions from results
        if command.name == 'filter' and '--event' in words:
            try:
                events = set(r.get('event', '') for r in self.shell.last_results)
                for event in sorted(events):
                    if event.startswith(current_word):
                        count = sum(1 for r in self.shell.last_results if r.get('event') == event)
                        yield Completion(
                            event,
                            start_position=-len(current_word),
                            display_meta=f"{count} events"
                        )
            except:
                pass
            return
        
        # Sort options for list command
        if command.name == 'list' and ('--sort' in words or '-s' in words):
            for option in ['size', 'name']:
                if option.startswith(current_word):
                    yield Completion(
                        option,
                        start_position=-len(current_word),
                        display_meta="sort by"
                    )
            return
        
        # Config key completions
        if command.name == 'config' and '--set' in words:
            for key in self.shell.config.keys():
                suggestion = f"{key}="
                if suggestion.startswith(current_word):
                    yield Completion(
                        suggestion,
                        start_position=-len(current_word),
                        display_meta=f"= {self.shell.config[key]}"
                    )
            return


