# 🔬 HexRay

**Tagline:**  
*An X-ray for transformers—tracing every token, neuron, and decision in real time.*

---

## 🚀 What is HexRay?

HexRay is a low-level debugger for transformer models. It gives you the power to inspect what happens inside large language models at every layer and every token — just like an X-ray reveals the inner structure of the human brain.

Built on [TransformerLens](https://github.com/neelnanda-io/TransformerLens) — a library for mechanistic interpretability of GPT-2-style language models. Mechanistic interpretability aims to reverse engineer the algorithms a model has learned by analyzing its weights. HexRay enables token-level tracing, neuron-level introspection, and activation monitoring, making it a powerful tool for researchers, red teamers, and AI safety engineers.

---

## ✨ Features (v1)

- Token-by-token tracing of residual streams
- CLI interface for easy model and prompt selection
- Hook-based tracing with TransformerLens
- Logs activations per layer for prompt analysis
- Modular design for future fuzzing and visualization tools

---

## 🔧 Basic Usage

```bash
python hexray.py --prompt "Why do bees buzz?" --top-k-attribution 10  
```

---

## 🟩 Output

```bash
Loading model gpt2-small...
Loaded pretrained model gpt2-small into HookedTransformer
Loaded pretrained model gpt2-small into HookedTransformer

Token: "
" (index -1)
Top Contributors to Final Logit:
- MLP  L9 : +46.16 (24.3%)
- MLP  L11: +35.61 (18.8%)
- MLP  L10: +30.14 (15.9%)
- MLP  L8 : +19.81 (10.4%)
- Attn L11: +14.21 (7.5%)
- MLP  L0 : +10.53 (5.5%)
- Attn L10: +9.93 (5.2%)
- Attn L0 : +9.62 (5.1%)
- Attn L7 : +7.67 (4.0%)
- MLP  L2 : +6.20 (3.3%)
```

# 🔧 Chain of Though Debugging

```bash
python hexray.py --prompt "If John has 3 apples..." --cot-debug --top-k-attribution 10
```

---

## 🟩 Output

```bash
Loading model gpt2-small...
Loaded pretrained model gpt2-small into HookedTransformer
Loaded pretrained model gpt2-small into HookedTransformer

🧠 Chain of Thought Attribution Trace (Console):

Step 1: If John has 3 apples...
MLP  L10 █████████████████████████  23.2%
MLP  L8  █████████████              12.6%
MLP  L0  ████████████               11.5%
Attn L11 ████████████               11.3%
Attn L0  ██████████                  9.7%
MLP  L7  █████████                   9.0%
MLP  L11 ████████                    7.9%
MLP  L6  ██████                      6.3%
Attn L8  █████                       4.7%
Attn L9  ███                         3.7%
```

---

## 📁 Project Structure

```
hexray/
├── hexray.py              # CLI entry point
├── debugger/
│   └── tracer.py          # Residual tracer module
├── README.md
└── examples/
```

---

## 📜 License

MIT License © 2025 Jonathan Jaquez
