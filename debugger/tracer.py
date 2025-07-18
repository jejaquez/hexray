import torch

def trace_tokens(model, prompt):
    tokens = model.to_tokens(prompt)
    with torch.no_grad():
        _, cache = model.run_with_cache(tokens)

    print(f"Tracing prompt: {prompt}")
    for layer in range(model.cfg.n_layers):
        resid = cache[f'blocks.{layer}.hook_resid_pre']
        print(f"Layer {layer:02d} | Residual shape: {tuple(resid.shape)}")
