import torch
from transformer_lens import HookedTransformer
from transformer_lens.utils import get_act_name


def get_logit_attribution(model: HookedTransformer, prompt: str, token_index: int = -1, top_k: int = 5):
    """
    Analyze attribution of attention heads and MLP neurons to the selected token's logits.
    Returns a sorted list of contributors.
    """
    tokens = model.to_tokens(prompt)
    logits, cache = model.run_with_cache(tokens)

    # Get the final logit vector for the specified token
    token_logits = logits[0, token_index]
    predicted_token_id = torch.argmax(token_logits).item()
    predicted_token_str = model.to_string(predicted_token_id)

    # Residual stream at the target token position
    resid = cache[get_act_name("resid_post", model.cfg.n_layers - 1)][0, token_index]

    # Unembedding matrix
    W_U = model.W_U
    final_logit_vector = W_U[:, predicted_token_id]  # shape: [d_model]

    # Attribution: dot product between components and final logit vector
    contributions = []

    # Layer-wise attention and MLP contributions
    for layer in range(model.cfg.n_layers):
        attn = cache[get_act_name("attn_out", layer)][0, token_index]  # [d_model]
        mlp = cache[get_act_name("mlp_out", layer)][0, token_index]    # [d_model]

        attn_score = torch.dot(attn, final_logit_vector).item()
        mlp_score = torch.dot(mlp, final_logit_vector).item()

        contributions.append((f"Attn L{layer}", attn_score))
        contributions.append((f"MLP  L{layer}", mlp_score))

    # Sort and normalize
    contributions.sort(key=lambda x: abs(x[1]), reverse=True)
    total = sum(abs(score) for _, score in contributions[:top_k]) or 1e-6

    top_contributors = [(name, score, abs(score) / total * 100) for name, score in contributions[:top_k]]

    return predicted_token_str, top_contributors