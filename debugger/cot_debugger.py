import re
from transformer_lens import HookedTransformer
from debugger.attribution import get_logit_attribution


def extract_cot_steps(prompt: str):
    """Segment the prompt into reasoning steps using simple heuristics."""
    steps = re.split(r"(?<=[.!?])\s+(?=[A-Z])", prompt.strip())
    return [s.strip() for s in steps if s]


def trace_cot_logit_attribution(model: HookedTransformer, prompt: str, top_k: int = 5):
    """Trace attribution through each CoT reasoning step."""
    steps = extract_cot_steps(prompt)
    results = []

    for step in steps:
        if not step: continue
        try:
            token_str, contributors = get_logit_attribution(model, step, token_index=-1, top_k=top_k)
            results.append({
                "step": step,
                "token": token_str,
                "attribution": contributors
            })
        except Exception as e:
            results.append({"step": step, "error": str(e)})

    return results


def print_cot_trace(results):
    print("\n🧠 Chain of Thought Attribution Trace:")
    for i, r in enumerate(results):
        print(f"\nStep {i+1}: {r['step']}")
        if 'error' in r:
            print(f"❌ Error: {r['error']}")
            continue
        print(f"Token: \"{r['token']}\"")
        for name, score, percent in r['attribution']:
            print(f"- {name:<8}: {score:+.2f} ({percent:.1f}%)")


def print_cot_bar_chart(results):
    max_bar_width = 25
    print("\n🧠 Chain of Thought Attribution Trace (Console):")
    for i, r in enumerate(results):
        print(f"\nStep {i+1}: {r['step']}")
        if 'error' in r:
            print(f"❌ Error: {r['error']}")
            continue
        top_score = max(abs(score) for _, score, _ in r['attribution']) or 1e-6
        for name, score, percent in r['attribution']:
            bar_len = int((abs(score) / top_score) * max_bar_width)
            bar = "█" * bar_len
            print(f"{name:<8} {bar:<25} {percent:5.1f}%")
