from collections import defaultdict, Counter

def create_ascii_bar_chart(data, max_width=40, title="Distribution"):
    """Crea un grafico a barre ASCII"""
    if not data:
        return "No data"
    
    max_val = max(data.values())
    lines = [f"[bold]{title}[/bold]\n"]
    
    for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]:
        bar_len = int((value / max_val) * max_width) if max_val > 0 else 0
        bar = "█" * bar_len
        pct = (value / sum(data.values())) * 100 if sum(data.values()) > 0 else 0
        lines.append(f"{label:20s} [{value:5d}] [cyan]{bar}[/cyan] {pct:5.1f}%")
    
    return "\n".join(lines)

def create_confidence_heatmap(results):
    """Crea heatmap della confidence"""
    if not results:
        return "No data"
    
    bins = defaultdict(int)
    for r in results:
        conf = r.get('confidence', 1.0)
        bin_key = int(conf * 10) * 10
        bins[bin_key] += 1
    
    heatmap = ["[bold]Confidence Heatmap[/bold]\n"]
    max_count = max(bins.values()) if bins else 1
    
    for pct in range(100, -10, -10):
        count = bins.get(pct, 0)
        intensity = int((count / max_count) * 10) if max_count > 0 else 0
        
        if intensity > 7:
            color = "bright_green"
        elif intensity > 4:
            color = "yellow"
        elif intensity > 0:
            color = "red"
        else:
            color = "dim"
        
        bar = "█" * intensity + "░" * (10 - intensity)
        heatmap.append(f"{pct:3d}% [{color}]{bar}[/{color}] {count:4d}")
    
    return "\n".join(heatmap)

def create_timeline_view(results, granularity="hour"):
    """Crea timeline degli eventi"""
    if not results:
        return "No events"
    
    timeline = defaultdict(int)
    
    for r in results:
        ts = r.get('timestamp', '')
        if isinstance(ts, str) and len(ts) >= 10:
            if granularity == "hour":
                bucket = ts[:13]  # YYYY-MM-DD HH
            else:
                bucket = ts[:10]  # YYYY-MM-DD
            timeline[bucket] += 1
    
    if not timeline:
        return "No timeline data"
    
    lines = ["[bold]Event Timeline[/bold]\n"]
    max_count = max(timeline.values())
    
    for bucket in sorted(timeline.keys())[-20:]:
        count = timeline[bucket]
        bar_len = int((count / max_count) * 30) if max_count > 0 else 0
        bar = "█" * bar_len
        lines.append(f"{bucket:16s} [cyan]{bar}[/cyan] {count}")
    
    return "\n".join(lines)