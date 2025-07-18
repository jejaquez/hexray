# 🔬 HexRay

**Tagline:**  
*An X-ray for transformers—tracing every token, neuron, and decision in real time.*

---

## 🚀 What is HexRay?

HexRay is a low-level debugger for transformer models. It gives you the power to inspect what happens inside large language models at every layer and every token — just like an X-ray reveals the inner structure of the human body.

Built on [TransformerLens](https://github.com/neelnanda-io/TransformerLens), HexRay supports token-level tracing, neuron-level introspection, and activation monitoring for researchers, red teamers, and AI safety engineers.

---

## ✨ Features (v1)

- Token-by-token tracing of residual streams
- CLI interface for easy model and prompt selection
- Hook-based tracing with TransformerLens
- Logs activations per layer for prompt analysis
- Modular design for future fuzzing and visualization tools

---

## 🔧 Usage

```bash
python hexray.py --model gpt2-small --prompt "The sky was blue because"
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
