import os
import subprocess
from collections import defaultdict, deque

# Lightweight DAG paths without external deps
graph = defaultdict(list)
graph['Initial_Access'].append('Privilege_Escalation')
graph['Privilege_Escalation'].append('Persistence')
graph['Persistence'].append('Data_Exfiltration')


def all_simple_paths(graph_dict, source, target):
    stack = [(source, [source])]
    while stack:
        node, path = stack.pop()
        for neighbor in graph_dict.get(node, []):
            if neighbor in path:
                continue
            new_path = path + [neighbor]
            if neighbor == target:
                yield new_path
            else:
                stack.append((neighbor, new_path))


paths = list(all_simple_paths(graph, 'Initial_Access', 'Data_Exfiltration'))
for p in paths:
    print("Possible attack chain:", " -> ".join(p))

# Optional: write Mermaid diagram
if os.getenv('WRITE_MERMAID', '0').strip() in {'1', 'true', 'True', 'yes'}:
    lines = ["graph TD"]
    for src, dsts in graph.items():
        for dst in dsts:
            lines.append(f"  {src}--> {dst}")
    content = "\n".join(lines) + "\n"
    with open('attack_chain.mmd', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Wrote Mermaid diagram to attack_chain.mmd")

    if os.getenv('EXPORT_PNG', '0').strip() in {'1', 'true', 'True', 'yes'}:
        mmdc = os.getenv('MMDC', 'mmdc')
        try:
            subprocess.run([mmdc, '-i', 'attack_chain.mmd', '-o', 'attack_chain.png', '-b', 'transparent', '--quiet'], check=True)
            print("Wrote PNG diagram to attack_chain.png")
        except FileNotFoundError:
            print("Mermaid CLI 'mmdc' not found. Skipping PNG export.")
        except subprocess.CalledProcessError as e:
            print(f"mmdc failed (exit {e.returncode}). Skipping PNG export.")
