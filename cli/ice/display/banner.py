from .console import console


def display_banner():
    banner_art = r"""   
 _(`-')    (`-')  _      (`-')                              
( (OO ).-> ( OO).-/     _(OO )   <-.        .->       .->   
 \    .'_ (,------.,--.(_/,-.\ ,--. )  (`-')----.  ,---(`-')
 '`'-..__) |  .---'\   \ / (_/ |  (`-')( OO).-.  ''  .-(OO )
 |  |  ' |(|  '--.  \   /   /  |  |OO )( _) | |  ||  | .-, \
 |  |  / : |  .--' _ \     /_)(|  '__ | \|  |)|  ||  | '.(_/
 |  '-'  / |  `---.\-'\   /    |     |'  '  '-'  '|  '-'  | 
 `------'  `------'    `-'     `-----'    `-----'  `-----'  
 """

    taglines = [
        "⚡ AI-POWERED LOG ANALYSIS ⚡",
        "🧠 Neural Pattern Detection",
        "⚙️ Auto-Learning Engine",
        "📊 100+ Log Types Supported",
        "🚀 Real-time Processing",
        "v2.0 PRO | Enterprise Ready"
    ]

    # Larghezza stimata della tabella
    table_width = 70
    terminal_width = console.size.width
    pad = max(0, (terminal_width - table_width) // 2)
    pad_str = " " * pad

    # Centrare ASCII art rispetto alla tabella
    art_lines = banner_art.split("\n")
    padded_banner = "\n".join(pad_str + line.center(table_width) for line in art_lines)
    
    console.print(padded_banner)
    console.print()
    
    for tagline in taglines:
        console.print(pad_str + tagline.center(table_width))

