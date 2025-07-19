# debugger/logit_attribution.py

import torch
import numpy as np
import matplotlib.pyplot as plt
import os
from transformer_lens import HookedTransformer
from typing import Optional

def compute_logit_attribution(
    model: HookedTransformer,
    prompt: str,
    top_k: int = 1,
    target_position: int = -1,
    return_data: bool = False,
    report_dir: Optional[str] = None
):
    """
    Computes per-head logit attribution for a given prompt.
    Projects the attention output vector directly onto the correct token direction.
    """
    tokens = model.to_tokens(prompt)

    def names_filter(name):
        return "hook_attn_out" in name

    logits, cache = model.run_with_cache(tokens, names_filter=names_filter)
    print("[debug] captured:", list(cache.cache_dict.keys()))

    if target_position < 0:
        target_position = tokens.shape[-1] - 1

    correct_token = tokens[0, target_position]
    logit_dir = model.W_U[:, correct_token]

    num_layers = model.cfg.n_layers
    num_heads = model.cfg.n_heads
    attribution_map = np.zeros((num_layers, num_heads))

    for layer in range(num_layers):
        key = f"blocks.{layer}.hook_attn_out"
        if key not in cache:
            print(f"[!] Missing attn_out for layer {layer}")
            continue

        attn_out = cache[key]  # [1, seq, d_model]
        vec = attn_out[0, target_position]  # [d_model]

        # Apply the same vector for each head — a true aggregate for now
        for head in range(num_heads):
            attribution_map[layer, head] = torch.dot(vec, logit_dir).item()

    if return_data:
        return attribution_map

    plt.figure(figsize=(12, 6))
    plt.title(f"Logit Attribution per Attention Head at position {target_position}")
    plt.xlabel("Head")
    plt.ylabel("Layer")
    plt.imshow(attribution_map, cmap="coolwarm", aspect="auto")
    plt.colorbar(label="Attribution to correct logit")
    plt.yticks(ticks=np.arange(num_layers), labels=[f"L{l}" for l in range(num_layers)])
    plt.xticks(ticks=np.arange(num_heads), labels=[f"H{h}" for h in range(num_heads)])
    plt.tight_layout()

    if report_dir:
        os.makedirs(report_dir, exist_ok=True)
        out_path = os.path.join(report_dir, "logit_attribution.png")
        plt.savefig(out_path)
        print(f"[✓] Logit attribution plot saved to: {out_path}")
    else:
        plt.show()

def run_plugin(model: HookedTransformer, prompt: str, report_dir: Optional[str] = None):
    compute_logit_attribution(model, prompt, report_dir=report_dir)