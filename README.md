# 🔬 HexRay

**Tagline:**  
*An X-ray for transformers—tracing every token, neuron, and decision in real time.*

---

## 🚀 What is HexRay?

HexRay is a low-level debugger for transformer models. It gives you the power to inspect what happens inside large language models at every layer and every token — just like an X-ray reveals the inner structure of the human brain.

Built on [TransformerLens](https://github.com/neelnanda-io/TransformerLens) — a library for mechanistic interpretability of large language models. Mechanistic interpretability (MI) aims to reverse engineer the algorithms a model has learned by analyzing its weights. HexRay uses MI to enable token-level tracing, neuron-level introspection, and activation monitoring, making it a powerful tool for researchers, red teamers, and AI safety engineers. This makes HexRay act like a headlamp and scalpel for LLMs internals.

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

## Logit Debugging
```bash 
python hexray.py --model gpt2-xl --prompt "Tell me about Ρhοenιx... Then if Ｐｅｐｓｉ is... the Ρhοenιx must be..." --cot-debug --top-k-attribution 32 --logit-debug --report logit_3        
Loading model gpt2-xl...
config.json: 100%|███████████████████████████████████████████████████████████████████████████████| 689/689 [00:00<00:00, 442kB/s]
model.safetensors: 100%|████████████████████████████████████████████████████████████████████| 6.43G/6.43G [01:18<00:00, 82.1MB/s]
generation_config.json: 100%|███████████████████████████████████████████████████████████████████| 124/124 [00:00<00:00, 1.25MB/s]
tokenizer_config.json: 100%|███████████████████████████████████████████████████████████████████| 26.0/26.0 [00:00<00:00, 318kB/s]
vocab.json: 100%|███████████████████████████████████████████████████████████████████████████| 1.04M/1.04M [00:00<00:00, 5.73MB/s]
merges.txt: 100%|█████████████████████████████████████████████████████████████████████████████| 456k/456k [00:00<00:00, 22.2MB/s]
tokenizer.json: 100%|███████████████████████████████████████████████████████████████████████| 1.36M/1.36M [00:00<00:00, 21.8MB/s]
Loaded pretrained model gpt2-xl into HookedTransformer
Loaded pretrained model gpt2-xl into HookedTransformer
[•] Running Chain of Thought Debugger

🧠 Chain of Thought Attribution Trace (Console):

Step 1: Tell me about Ρhοenιx...
MLP  L44 █████████████████████████   7.0%
MLP  L42 ████████████████████████    7.0%
MLP  L45 ███████████████████████     6.6%
MLP  L41 ██████████████████████      6.4%
MLP  L39 ██████████████████          5.2%
MLP  L43 ███████████████             4.4%
MLP  L36 ██████████████              4.2%
MLP  L37 ██████████████              4.0%
MLP  L40 █████████████               3.8%
MLP  L38 █████████████               3.8%
MLP  L33 ███████████                 3.2%
MLP  L46 ██████████                  3.0%
MLP  L34 ██████████                  2.9%
MLP  L29 ██████████                  2.9%
MLP  L35 ██████████                  2.8%
Attn L44 █████████                   2.7%
Attn L42 █████████                   2.6%
MLP  L32 █████████                   2.5%
Attn L43 ████████                    2.3%
Attn L46 ███████                     2.2%
Attn L33 ██████                      1.9%
MLP  L25 ██████                      1.9%
Attn L39 ██████                      1.9%
Attn L40 ██████                      1.9%
MLP  L30 ██████                      1.9%
Attn L36 ██████                      1.9%
MLP  L28 ██████                      1.8%
Attn L45 ██████                      1.8%
MLP  L23 █████                       1.6%
MLP  L27 ████                        1.3%
MLP  L0  ████                        1.3%
Attn L37 ████                        1.3%

Step 2: Then if Ｐｅｐｓｉ is... the Ρhοenιx must be...
MLP  L44 █████████████████████████   9.5%
MLP  L43 ██████████████████████      8.4%
MLP  L42 ████████████████████        7.9%
MLP  L45 ███████████████████         7.6%
MLP  L47 ███████████████████         7.3%
MLP  L46 █████████████████           6.6%
MLP  L41 ██████████                  4.0%
MLP  L39 ████████                    3.4%
Attn L45 ████████                    3.1%
Attn L42 ███████                     3.0%
Attn L44 ███████                     3.0%
Attn L43 ███████                     2.8%
Attn L39 ██████                      2.4%
Attn L37 ██████                      2.3%
MLP  L40 █████                       2.3%
MLP  L38 █████                       2.3%
MLP  L34 █████                       2.0%
Attn L40 █████                       2.0%
MLP  L29 ████                        1.9%
Attn L25 ████                        1.8%
MLP  L35 ████                        1.7%
MLP  L36 ████                        1.6%
Attn L46 ███                         1.5%
Attn L41 ███                         1.5%
Attn L33 ███                         1.4%
MLP  L30 ███                         1.3%
Attn L34 ███                         1.3%
MLP  L23 ███                         1.3%
MLP  L37 ███                         1.2%
MLP  L25 ███                         1.2%
Attn L47 ███                         1.2%
Attn L35 ███                         1.1%
[•] Running Logit Debugger
[debug] captured: ['blocks.0.hook_attn_out', 'blocks.1.hook_attn_out', 'blocks.2.hook_attn_out', 'blocks.3.hook_attn_out', 'blocks.4.hook_attn_out', 'blocks.5.hook_attn_out', 'blocks.6.hook_attn_out', 'blocks.7.hook_attn_out', 'blocks.8.hook_attn_out', 'blocks.9.hook_attn_out', 'blocks.10.hook_attn_out', 'blocks.11.hook_attn_out', 'blocks.12.hook_attn_out', 'blocks.13.hook_attn_out', 'blocks.14.hook_attn_out', 'blocks.15.hook_attn_out', 'blocks.16.hook_attn_out', 'blocks.17.hook_attn_out', 'blocks.18.hook_attn_out', 'blocks.19.hook_attn_out', 'blocks.20.hook_attn_out', 'blocks.21.hook_attn_out', 'blocks.22.hook_attn_out', 'blocks.23.hook_attn_out', 'blocks.24.hook_attn_out', 'blocks.25.hook_attn_out', 'blocks.26.hook_attn_out', 'blocks.27.hook_attn_out', 'blocks.28.hook_attn_out', 'blocks.29.hook_attn_out', 'blocks.30.hook_attn_out', 'blocks.31.hook_attn_out', 'blocks.32.hook_attn_out', 'blocks.33.hook_attn_out', 'blocks.34.hook_attn_out', 'blocks.35.hook_attn_out', 'blocks.36.hook_attn_out', 'blocks.37.hook_attn_out', 'blocks.38.hook_attn_out', 'blocks.39.hook_attn_out', 'blocks.40.hook_attn_out', 'blocks.41.hook_attn_out', 'blocks.42.hook_attn_out', 'blocks.43.hook_attn_out', 'blocks.44.hook_attn_out', 'blocks.45.hook_attn_out', 'blocks.46.hook_attn_out', 'blocks.47.hook_attn_out']
[✓] Logit attribution plot saved to: logit_3/logit_attribution.png
```
---

## 📜 License

MIT License © 2025 Jonathan Jaquez
