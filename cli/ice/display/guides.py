from rich.table import Table
from rich import box
from .console import console


def display_quick_guide():
    sections = [
        ("📁 Setup & Management", [
            ("add <path> [--recursive] [--pattern *.log]", "Add files with filters"),
            ("list [--sort size|name] [--detailed]", "Show database with stats"),
            ("clear [--confirm]", "Remove all paths"),
            ("remove <id>", "Remove specific file")
        ]),
        ("🔍 Analysis & Scanning", [
            ("scan [--conf 0.7] [--limit 100] [--file X]", "Smart scan with filters"),
            ("quick [--summary]", "Fast report generation"),
            ("analyze [--deep]", "Deep pattern analysis"),
            ("filter <status> [--severity N]", "Multi-filter results"),
            ("search <text> [--regex] [--case]", "Search in events"),
            ("top [N] [--by type|severity|confidence]", "Top items analysis")
        ]),
        ("🤖 AI & Machine Learning", [
            ("stats [--visual] [--export]", "AI statistics dashboard"),
            ("learning [--patterns] [--evolution]", "Pattern learning analysis"),
            ("confidence [--heatmap] [--threshold X]", "Confidence distribution"),
            ("patterns [--learned] [--top N]", "Pattern explorer"),
            ("predict <file>", "Predict log type/issues"),
            ("train [--iterations N]", "Manual training boost"),
            ("neural [--weights] [--evolution]", "Neural network stats"),
            ("signatures [--coverage]", "Show log signatures (100+)")
        ]),
        ("📊 Reports & Export", [
            ("export <format> [--output file] [--filter]", "Export with options"),
            ("report [--detailed] [--html] [--dashboard]", "Generate reports"),
            ("compare <file1> <file2>", "Compare log files"),
            ("timeline [--granularity hour|day]", "Event timeline"),
            ("dashboard [--live] [--refresh 5]", "Live monitoring"),
            ("anomaly [--threshold 0.7]", "Show anomalies")
        ]),
        ("🔧 Advanced & Utility", [
            ("debug [--verbose] [--detector]", "Deep diagnostics"),
            ("benchmark", "Performance test"),
            ("config [--show] [--set key=value]", "Configuration"),
            ("history [--clear]", "Command history"),
            ("plugin [list|load|unload] <name>", "Plugin management"),
            ("features [--all]", "Show feature extraction"),
            ("help <command>", "Detailed help"),
            ("exit / quit", "Exit session")
        ])
    ]

    table = Table(show_header=False, box=box.HORIZONTALS, expand=False, pad_edge=True, show_lines=False)
    table.add_column("Command", justify="left", ratio=2)
    table.add_column("Description", justify="left", ratio=3)

    first_section = True
    for section_title, commands in sections:
        if not first_section:
            table.add_row("", "", end_section=True)
        first_section = False

        # Titolo leggermente a sinistra (come banner)
        table.add_row(f"[bold cyan]{section_title}[/bold cyan]", "")
        for cmd, desc in commands:
            table.add_row(cmd, f"- {desc}")

    console.print()
    console.print(table, justify="center")
