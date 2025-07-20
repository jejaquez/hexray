
import re
from graphviz import Digraph

def parse_arithmetic_prompt(prompt):
    # Strip and normalize input
    prompt = prompt.strip().lower()

    # Extract the first arithmetic expression found (e.g., "50 + 15 * 2")
    expr = re.findall(r"(\d+\s*[-+*/]\s*\d+(?:\s*[-+*/]\s*\d+)*)", prompt)
    if not expr:
        return None
    try:
        clean_expr = expr[0].strip()
        result = eval(clean_expr)
        return clean_expr, result
    except Exception:
        return None

def last_digit(n):
    return n % 10

def get_range(n):
    base = (n // 10) * 10
    return f"{base}-{base+9}"

def generate_graph(prompt, output_path):
    parsed = parse_arithmetic_prompt(prompt)
    if not parsed:
        print("[arithmetic_graph] No valid arithmetic expression found.")
        return None

    expr, result = parsed
    tokens = re.findall(r"(\d+|[+\-*/])", expr)

    if len(tokens) < 3:
        print("[arithmetic_graph] Too simple to visualize meaningfully.")
        return None

    dot = Digraph(comment='Arithmetic Reasoning Graph')
    dot.attr('node', shape='box', style='filled')

    dot.node('Q', f'What is {expr}?', shape='rectangle', fillcolor='#f0f0f0')

    op_node = None
    approx_parts = []
    digit_parts = []

    for i, token in enumerate(tokens):
        if token.isdigit():
            n = int(token)
            lid = last_digit(n)
            rlabel = get_range(n)
            nid = f"N{i}"
            rid = f"R{i}"
            dot.node(nid, f"number ending in {lid}", fillcolor="#e0d4f7")
            dot.node(rid, f"{n} → group {rlabel}", fillcolor="#d4ecff")
            dot.edge("Q", nid)
            dot.edge("Q", rid)
            digit_parts.append((lid, nid))
            approx_parts.append(rid)
        else:
            op_node = token

    # Last digit reasoning
    if len(digit_parts) >= 2 and op_node:
        lid1, id1 = digit_parts[0]
        lid2, id2 = digit_parts[1]
        try:
            last_res = eval(f"{lid1}{op_node}{lid2}") % 10
        except Exception:
            last_res = "?"
        lid_node = f"LastDigit"
        dot.node(lid_node, f"{lid1} {op_node} {lid2} → ends in {last_res}", style="rounded,filled", fillcolor="#fbeaff")
        dot.edge(id1, lid_node)
        dot.edge(id2, lid_node)

    # Approximate reasoning
    if len(approx_parts) >= 2:
        approx_label = f"{tokens[0]} {op_node} {tokens[2]}"
        dot.node("Estimate", f"estimate: {approx_label}", fillcolor="#d4ecff")
        dot.node("SumApprox", f"sum ≈ {int(result)}", fillcolor="#d4ecff")
        dot.edge(approx_parts[0], "Estimate")
        dot.edge(approx_parts[1], "Estimate")
        dot.edge("Estimate", "SumApprox")

    # Final answer
    dot.node("Result", f"✅ sum = {result}", shape='doublecircle', fillcolor="#ffd7c2")
    if any('LastDigit' in line for line in dot.body):
        dot.edge("LastDigit", "Result")
    if any('SumApprox' in line for line in dot.body):
        dot.edge("SumApprox", "Result")

    dot.render(output_path, format='png', cleanup=True)
    return output_path + ".png"
