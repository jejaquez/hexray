import argparse
import os
import re
os.environ["TOKENIZERS_PARALLELISM"] = "true"
from transformer_lens import HookedTransformer
from debugger.tracer import trace_tokens
from debugger.attribution import get_logit_attribution
from debugger import logit_attribution
from debugger import arithmetic_graph
from debugger.visualize_weights import get_weight_tensor, plot_weight_heatmap
from debugger.cot_debugger import trace_cot_logit_attribution, print_cot_bar_chart


def main():
    parser = argparse.ArgumentParser(
    description="HexRay: Transformer introspection toolkit")
    parser.add_argument("--model", type=str, default="gpt2-small", help="Model name")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to analyze")
    parser.add_argument("--weight-heatmap", type=str, help="Visualize heatmap")
    parser.add_argument("--top-k-attribution", type=int, default=0, help="Number of top contributors to logit attribution")
    parser.add_argument("--token-index", type=int, default=-1, help="Which token in the prompt to attribute (default: last)")
    parser.add_argument("--cot-debug", action="store_true", help="Enable chain-of-thought attribution tracing")
    parser.add_argument("--logit-debug", action="store_true", help="Run top-k logit attribution debug")
    parser.add_argument("--report", type=str, help="Output folder for saving reports")
    parser.add_argument("--arithmetic-graph", action="store_true", help="Generate arithmetic reasoning diagram")  # ✅ must be here

    args = parser.parse_args()

    print(f"Loading model {args.model}...")
    model = HookedTransformer.from_pretrained(args.model, device="cpu")
    print(f"Loaded pretrained model {args.model} into HookedTransformer")
    
    if args.arithmetic_graph and any(op in args.prompt for op in ["+", "-", "*"]):
        if not args.report:
            print("[!] --arithmetic-graph requires --report to specify output directory.")
        else:
            print("[✓] Generating arithmetic reasoning graph...")
            arithmetic_graph.generate_graph(args.prompt, os.path.join(args.report, "arithmetic_graph"))

    if args.cot_debug:
        print("[•] Running Chain of Thought Debugger")
        results = trace_cot_logit_attribution(model, args.prompt, args.top_k_attribution or 5)
        print_cot_bar_chart(results)
    if args.logit_debug:
        print("[•] Running Logit Debugger")
        logit_attribution.run_plugin(model, args.prompt, report_dir=args.report)
    if args.weight_heatmap:
        pattern = r"^(attn|mlp)\.L(\d+)\.(W_[A-Za-z]+)$"
        match = re.match(pattern, args.weight_heatmap)
        if not match:
            raise ValueError("Invalid format. Use: attn.L10.W_Q or mlp.L6.W_in")

        component, layer, weight_name = match.groups()
        layer = int(layer)
        print(f"[•] Visualizing weight matrix: {component} layer {layer}, weight {weight_name}")

        tensor = get_weight_tensor(model, component, layer, weight_name)

        filename = f"{component}_L{layer}_{weight_name}.png"
        save_path = os.path.join(args.report, filename)
        print(f"[✓] Saving heatmap to: {save_path}")

        plot_weight_heatmap(tensor, title=f"{component.upper()} L{layer} {weight_name}", save_path=save_path)
    if args.top_k_attribution > 0:
        predicted_token, contributors = get_logit_attribution(model, args.prompt, args.token_index, args.top_k_attribution)
        print(f"\nToken: \"{predicted_token}\" (index {args.token_index})")
        print("Top Contributors to Final Logit:")
        for name, score, percent in contributors:
            print(f"- {name:<8}: {score:+.2f} ({percent:.1f}%)")
    else:
        trace_tokens(model, args.prompt)


if __name__ == "__main__":
    main()
