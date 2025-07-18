import argparse
from transformer_lens import HookedTransformer
from debugger.tracer import trace_tokens
from debugger.attribution import get_logit_attribution


def main():
    parser = argparse.ArgumentParser(description="HexRay: Transformer introspection toolkit")
    parser.add_argument("--model", type=str, default="gpt2-small", help="Model name")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to analyze")
    parser.add_argument("--top-k-attribution", type=int, default=0, help="Number of top contributors to logit attribution")
    parser.add_argument("--token-index", type=int, default=-1, help="Which token in the prompt to attribute (default: last)")

    args = parser.parse_args()

    print(f"Loading model {args.model}...")
    model = HookedTransformer.from_pretrained(args.model)
    print(f"Loaded pretrained model {args.model} into HookedTransformer")

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
