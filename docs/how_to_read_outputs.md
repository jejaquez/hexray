# 📖 How to Read HexRay Output

HexRay prints transformer internals like this:

```
Layer 00 | Residual shape: (1, 6, 768)
```

Understanding this output is essential for interpreting transformer behavior.

---

## 🔍 What Does `Residual shape: (1, 6, 768)` Mean?

This describes the shape of the **residual stream tensor** at a specific transformer layer:

| Dimension | Meaning |
|----------:|---------|
| `1`       | **Batch size** – the number of prompts processed at once. In HexRay, it's usually 1. |
| `6`       | **Sequence length** – number of tokens in your prompt after tokenization. E.g., `"Why do bees buzz?"` → 6 tokens. |
| `768`     | **Hidden size** – dimensionality of each token representation in `gpt2-small`. Each token is a 768-dimensional vector. |

---

## 🧠 What is the Residual Stream?

The **residual stream** is the internal memory space that passes through each transformer layer. Every layer modifies it via attention and MLP blocks. It:

- Holds the representation of each token
- Evolves across layers as the model "thinks"
- Is what attention heads and neurons read from and write to

You can think of it as the model's evolving workspace for your prompt.

---

## 🧪 Why Does HexRay Show This?

HexRay helps you trace how the residual stream changes:

- **Per token**: Track how representations shift
- **Per layer**: See how deeper layers refine or amplify meanings
- **Across prompts**: Compare clean vs. perturbed token activations

---

## 📊 Visual Debugging

In later updates, you’ll also see color-coded bar plots per token, normalized per layer. These highlight:

- Strong positive activations (🟩 green)
- Strong negative activations (🟥 red)
- How changes in prompts affect individual tokens

---

## ✅ Example

```bash
python hexray.py --model gpt2-small --prompt "Why do bees buzz?"                               
```

Expect output like:

```
Loading model gpt2-small...
Loaded pretrained model gpt2-small into HookedTransformer
Tracing prompt: Why do bees buzz?
Layer 00 | Residual shape: (1, 6, 768)
Layer 01 | Residual shape: (1, 6, 768)
Layer 02 | Residual shape: (1, 6, 768)
Layer 03 | Residual shape: (1, 6, 768)
Layer 04 | Residual shape: (1, 6, 768)
Layer 05 | Residual shape: (1, 6, 768)
Layer 06 | Residual shape: (1, 6, 768)
Layer 07 | Residual shape: (1, 6, 768)
Layer 08 | Residual shape: (1, 6, 768)
Layer 09 | Residual shape: (1, 6, 768)
Layer 10 | Residual shape: (1, 6, 768)
Layer 11 | Residual shape: (1, 6, 768)
```

This lets you inspect the internal reasoning process of a transformer model token-by-token and layer-by-layer.

---

For more, see: `README.md`, or reach out with feedback/contributions!
