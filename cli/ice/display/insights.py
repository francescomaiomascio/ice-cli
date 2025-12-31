from .console import console
from collections import Counter
from rich.panel import Panel


def display_ai_insights(parser, results):
    """Mostra insights AI avanzati con Neural Detector 2.0"""
    learning_stats = parser.get_learning_stats()
    
    total = len(results)
    if total == 0:
        console.print("[yellow]No results to analyze[/yellow]")
        return
    
    status_dist = Counter(r.get('status') for r in results)
    confidence_avg = sum(r.get('confidence', 0) for r in results) / total
    severity_avg = sum(r.get('severity', 0) for r in results) / total
    
    # Pattern diversity
    event_types = len(set(r.get('event') for r in results))
    learned_structures = learning_stats.get('learned_structures', 0)
    
    # Neural metrics
    detector_stats = learning_stats.get('detector_stats', {})
    neural_weights_count = len(detector_stats.get('neural_weights', {}))
    avg_neural_weight = sum(detector_stats.get('neural_weights', {}).values()) / max(neural_weights_count, 1)
    
    # Feature extraction stats
    feature_extractions = detector_stats.get('feature_extractions', 0)
    
    # Health score (enhanced)
    health = min(100, int(
        (status_dist.get('success', 0) / total * 40) +
        (confidence_avg * 30) +
        (20 if learned_structures > 5 else learned_structures * 4) +
        (10 if neural_weights_count > 10 else neural_weights_count)
    ))
    
    health_color = "green" if health > 70 else "yellow" if health > 40 else "red"
    
    insights = f"""
[bold cyan]🧠 AI Insights & Neural Analysis[/bold cyan]

[bold]System Health Score:[/bold] [{health_color}]{health}/100[/{health_color}]

[bold]Neural Network Status:[/bold]
  • Active Neural Weights: [cyan]{neural_weights_count}[/cyan]
  • Avg Weight Value: [yellow]{avg_neural_weight:.3f}[/yellow]
  • Feature Extractions: [green]{feature_extractions:,}[/green]
  • Learning Mode: [magenta]{'ACTIVE' if learning_stats.get('learning_mode', True) else 'INACTIVE'}[/magenta]

[bold]Pattern Recognition:[/bold]
  • Unique Event Types: [cyan]{event_types}[/cyan]
  • Learned Structures: [green]{learned_structures}[/green]
  • Avg Confidence: [yellow]{confidence_avg:.1%}[/yellow]
  • Avg Severity: [magenta]{severity_avg:.1f}/10[/magenta]

[bold]Event Distribution:[/bold]
  • Success Rate: [green]{status_dist.get('success', 0) / total:.1%}[/green]
  • Warning Rate: [yellow]{status_dist.get('warning', 0) / total:.1%}[/yellow]
  • Failure Rate: [red]{status_dist.get('failed', 0) / total:.1%}[/red]

[bold]AI Recommendations:[/bold]
"""
    
    # Smart recommendations
    if confidence_avg < 0.6:
        insights += "  ⚠️  Low avg confidence - consider manual training\n"
    if status_dist.get('failed', 0) / total > 0.3:
        insights += "  🚨 High failure rate - investigate critical issues\n"
    if learned_structures < 3:
        insights += "  💡 Few learned patterns - more data needed\n"
    if event_types > 20:
        insights += "  ✨ High diversity - excellent pattern coverage\n"
    if neural_weights_count < 5:
        insights += "  🔄 Neural network warming up - continue processing\n"
    if avg_neural_weight > 1.2:
        insights += "  🚀 Neural network highly optimized!\n"
    
    console.print(Panel(insights, border_style="cyan"))