from .console import console
from rich.tree import Tree

def display_log_signatures(parser):
    """Display comprehensive log signature coverage (100+)"""
    detector = parser.detector
    signatures = detector.log_signatures
    
    tree = Tree(f"[bold cyan]📋 Log Signature Database ({len(signatures)} types)[/bold cyan]")
    
    # Group by category
    categories = {
        'Web Servers': ['nginx', 'apache', 'iis', 'haproxy', 'traefik', 'caddy'],
        'Languages': ['python', 'java', 'javascript', 'php', 'ruby', 'golang', 'csharp', 'rust'],
        'Databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'oracle', 'mssql'],
        'Cloud': ['aws_', 'gcp_', 'azure_'],
        'Containers': ['docker', 'kubernetes', 'containerd', 'podman', 'nomad'],
        'Message Queues': ['rabbitmq', 'kafka', 'activemq', 'nats'],
        'Mail': ['postfix', 'dovecot', 'exim', 'sendmail'],
        'Security': ['ssh', 'auth', 'pam', 'sudo', 'auditd', 'selinux', 'apparmor'],
        'Firewall': ['iptables', 'ufw', 'pfsense', 'cisco', 'palo_alto', 'fortinet'],
        'Monitoring': ['prometheus', 'grafana', 'datadog', 'newrelic', 'splunk', 'zabbix', 'nagios'],
        'CI/CD': ['jenkins', 'gitlab', 'github', 'circleci', 'travis'],
        'Other': []
    }
    
    categorized = {cat: [] for cat in categories.keys()}
    
    for sig_name, sig_data in signatures.items():
        found = False
        for cat, prefixes in categories.items():
            if any(prefix in sig_name for prefix in prefixes):
                categorized[cat].append((sig_name, sig_data))
                found = True
                break
        if not found:
            categorized['Other'].append((sig_name, sig_data))
    
    for category, sigs in categorized.items():
        if sigs:
            branch = tree.add(f"[bold yellow]{category}[/bold yellow] ({len(sigs)})")
            for sig_name, sig_data in sorted(sigs)[:10]:  # Show first 10 per category
                weight = sig_data.get('weight', 0)
                pattern_count = len(sig_data.get('patterns', []))
                branch.add(f"[green]{sig_name}[/green] (weight: {weight}, patterns: {pattern_count})")
            
            if len(sigs) > 10:
                branch.add(f"[dim]... and {len(sigs) - 10} more[/dim]")
    
    console.print(tree)
    console.print(f"\n[bold cyan]Total Coverage: {len(signatures)} log types across {len([c for c, s in categorized.items() if s])} categories[/bold cyan]\n")


