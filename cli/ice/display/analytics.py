from .console import console

from collections import Counter, defaultdict
from rich.panel import Panel
from .charts import create_ascii_bar_chart, create_confidence_heatmap
from rich.tree import Tree
from rich.layout import Layout
from datetime import datetime


def display_pattern_tree(learning_stats):
    """Mostra albero dei pattern imparati con Neural Detector stats"""
    tree = Tree("🌳 [bold cyan]Pattern Learning Tree (Neural)[/bold cyan]")
    
    top_patterns = learning_stats.get('top_patterns', [])[:15]
    pattern_stats = learning_stats.get('pattern_stats', {})
    
    # Raggruppa per prefisso
    groups = defaultdict(list)
    for pattern, score in top_patterns:
        prefix = pattern.split('_')[0] if '_' in pattern else 'other'
        groups[prefix].append((pattern, score))
    
    for prefix, patterns in sorted(groups.items()):
        branch = tree.add(f"[yellow]{prefix.upper()}[/yellow]")
        for pattern, score in patterns[:5]:
            confidence = min(100, int((score / 100) * 100))
            branch.add(f"[green]{pattern}[/green] (matches: {score:.0f}, confidence: {confidence}%)")
    
    console.print(tree)

def display_advanced_stats(parser, results):
    """Statistiche avanzate con visualizzazioni (Neural Enhanced)"""
    layout = Layout()
    
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    
    layout["header"].update(Panel("[bold cyan]📊 Advanced Analytics Dashboard (Neural 2.0)[/bold cyan]", border_style="cyan"))
    
    # Body split in 2 columns
    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    
    # Left: Event distribution
    event_dist = Counter(r.get('event') for r in results)
    left_content = create_ascii_bar_chart(dict(event_dist.most_common(10)), title="Top Event Types")
    layout["left"].update(Panel(left_content, border_style="green", title="Event Distribution"))
    
    # Right: Confidence heatmap
    right_content = create_confidence_heatmap(results)
    layout["right"].update(Panel(right_content, border_style="yellow", title="Confidence Analysis"))
    
    # Footer with neural stats
    learning_stats = parser.get_learning_stats()
    detector_stats = learning_stats.get('detector_stats', {})
    footer_text = f"Total Events: {len(results)} | Neural Weights: {len(detector_stats.get('neural_weights', {}))} | Analyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    layout["footer"].update(Panel(footer_text, border_style="dim"))
    
    console.print(layout)

def display_neural_network_stats(detector_stats):
    """Display detailed neural network statistics"""
    content = f"""
[bold yellow]🧠 Neural Network Deep Dive[/bold yellow]

[bold]Processing Statistics:[/bold]
  • Total Lines Processed: [cyan]{detector_stats.get('total_lines', 0):,}[/cyan]
  • Successful Parses: [green]{detector_stats.get('successful_parses', 0):,}[/green]
  • Success Rate: [yellow]{detector_stats.get('successful_parses', 0) / max(detector_stats.get('total_lines', 1), 1):.1%}[/yellow]
  • Learning Events: [magenta]{detector_stats.get('learning_events', 0):,}[/magenta]

[bold]Neural Weights (Top 10):[/bold]
"""
    
    neural_weights = detector_stats.get('neural_weights', {})
    for event_type, weight in sorted(neural_weights.items(), key=lambda x: x[1], reverse=True)[:10]:
        bar = "█" * int(weight * 20)
        color = "green" if weight > 1.0 else "yellow" if weight > 0.8 else "red"
        content += f"  {event_type:25s} [{color}]{weight:.3f}[/{color}] {bar}\n"
    
    content += f"""
[bold]Feature Importance (Top 15):[/bold]
"""
    
    feature_importance = detector_stats.get('feature_importance', {})
    for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:15]:
        bar = "▪" * int(importance * 2)
        content += f"  {feature:25s} [cyan]{importance:.2f}[/cyan] {bar}\n"
    
    console.print(Panel(content, title="🔬 Neural Network Analysis", border_style="yellow"))

