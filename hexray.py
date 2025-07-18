import argparse
from debugger.tracer import trace_tokens
from transformer_lens import HookedTransformer

def main():
    parser = argparse.ArgumentParser(description="HexRay - An X-ray for transformers.")
    parser.add_argument("--model", type=str, default="gpt2-small", help="Name of HuggingFace-compatible model")
    parser.add_argument("--prompt", type=str, required=True, help="Text prompt to trace through the model")
    args = parser.parse_args()

    print(f"Loading model {args.model}...")
    model = HookedTransformer.from_pretrained(args.model)
    trace_tokens(model, args.prompt)

if __name__ == "__main__":
    main()
