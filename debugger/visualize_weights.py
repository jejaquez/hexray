import torch
import matplotlib.pyplot as plt
import seaborn as sns
from transformer_lens import HookedTransformer

def plot_weight_heatmap(weight_tensor: torch.Tensor, title: str = "", save_path: str = None):
    """
    Plots a heatmap of a 2D weight matrix or flattens higher dimensions.

    If the tensor has 3 dimensions (e.g., [n_heads, d_model, d_head]),
    it will plot a grid of subplots — one per head.
    """
    data = weight_tensor.detach().cpu().numpy()
    
    if data.ndim == 2:
        plt.figure(figsize=(10, 6))
        sns.heatmap(data, cmap="viridis", cbar=True)
        plt.title(title)
        plt.xlabel("Output Dimension")
        plt.ylabel("Input Dimension")
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        else:
            plt.savefig(save_path) if save_path else plt.show()
    
    elif data.ndim == 3:
        n_heads = data.shape[0]
        fig, axes = plt.subplots(nrows=1, ncols=n_heads, figsize=(4 * n_heads, 4), squeeze=False)
        for i in range(n_heads):
            sns.heatmap(data[i], cmap="viridis", cbar=False, ax=axes[0][i])
            axes[0][i].set_title(f"{title} (head {i})")
            axes[0][i].set_xlabel("Output")
            axes[0][i].set_ylabel("Input")
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        else:
            plt.savefig(save_path) if save_path else plt.show()
    
    else:
        raise ValueError(f"Unsupported tensor shape {data.shape} for heatmap.")

def get_weight_tensor(model: HookedTransformer, component: str, layer: int, weight_name: str) -> torch.Tensor:
    """
    Retrieves a specific weight matrix from a given model layer and component.

    Args:
        model (HookedTransformer): The TransformerLens model.
        component (str): 'attn' or 'mlp'.
        layer (int): The layer index.
        weight_name (str): Name of the weight ('W_Q', 'W_K', 'W_V', 'W_O', 'W_in', 'W_out').

    Returns:
        torch.Tensor: The weight tensor.
    """
    if component == "attn":
        layer_obj = model.blocks[layer].attn
    elif component == "mlp":
        layer_obj = model.blocks[layer].mlp
    else:
        raise ValueError("Component must be 'attn' or 'mlp'")

    weight_tensor = getattr(layer_obj, weight_name, None)
    if weight_tensor is None:
        raise AttributeError(f"{component} layer does not have weight {weight_name}")
    return weight_tensor
