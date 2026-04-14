# 🚀 Hybrid LLM Inference: GPU + Verilog (RTL) Accelerator

This repository demonstrates an **end-to-end working lab** where a mini LLM-style pipeline runs across:

* **GPU (PyTorch)** → embedding + baseline compute
* **Verilog RTL (VLSI-style accelerator)** → quantized linear layer
* **Verilator** → RTL simulation
* **C++ bridge** → connects Python ↔ RTL

---

## 🧠 What this project shows

👉 LLMs are mostly matrix multiplications
👉 These can run on:

* GPU → flexible, general-purpose
* RTL / ASIC → fixed-function, efficient

This repo demonstrates:

> Offloading a part of LLM computation (linear layer) to a custom Verilog accelerator and comparing it with GPU execution.

---

## 📂 Project Structure

```
gpu_rtl_llm_lab/
├── rtl/
│   └── matmul.v          # Verilog accelerator
├── sim/
│   └── main.cpp         # C++ RTL runner (Verilator)
├── python/
│   └── ask_llm_rtl.py   # Main pipeline (GPU + RTL)
├── obj_dir/             # Generated after build
```

---

## ⚙️ Prerequisites

Install required tools:

```bash
# Python deps
pip install torch numpy

# Verilator (Ubuntu/Debian)
apt update
apt install -y verilator make g++
```

👉 If Verilator not available:

```bash
docker run -it verilator/verilator bash
```

---

## 🛠️ Build RTL (VERY IMPORTANT)

Run from project root:

```bash
verilator -cc rtl/matmul.v --exe sim/main.cpp
make -C obj_dir -j -f Vmatmul.mk
```

👉 This generates:

```
obj_dir/Vmatmul   # executable
```

---

## ▶️ Run the Full Pipeline

```bash
cd python
python ask_llm_rtl.py
```

---

## 🧪 Example Run

```
Ask something: hi

--- GPU ONLY ANSWER (row 0) ---
-0.22 1.18 -0.19 -0.62

--- GPU + RTL ANSWER (row 0) ---
-0.28 0.98 -0.11 -0.56

Mean Error: ~0.10
```

---

## 📊 Output Explanation

| Metric     | Meaning                       |
| ---------- | ----------------------------- |
| GPU ONLY   | Full compute on GPU           |
| GPU + RTL  | Linear layer offloaded to RTL |
| Mean Error | Quantization difference       |
| Memory     | GPU vs RTL footprint          |
| Energy     | Estimated compute cost        |

---

## 🔥 Key Insights

* ✔ RTL output closely matches GPU
* ✔ Quantized compute reduces memory
* ✔ Estimated energy is much lower in RTL
* ✔ Hardware execution is deterministic

---

## ⚠️ Important Notes

* RTL runs in **simulation (Verilator)**
* Simulation latency ≠ real hardware latency
* Real benefit appears when mapped to:

  * FPGA
  * ASIC

---

## 🧠 Conceptual Flow

```
User Input
   ↓
Tokenization
   ↓
Embedding (GPU)
   ↓
Linear Layer
   ├── GPU (baseline)
   └── RTL (Verilog)
   ↓
Compare Outputs
```

---

## 🚀 Why this matters

Modern AI is moving toward:

* hardware-aware models
* custom accelerators
* GPU + ASIC hybrid systems

This project is a **hands-on introduction to hardware-software co-design in AI**.

---

## 🔥 Future Improvements

* Full transformer layer offload
* Multi-head attention in RTL
* Larger tensor support
* Real FPGA deployment
* Performance visualization

---

## 💣 TL;DR

> Run a mini LLM pipeline where GPU handles embeddings and a custom Verilog RTL accelerator executes the core compute, demonstrating accuracy, memory, and energy trade-offs.

---

## ⭐ If you like it

Give a ⭐ and share your thoughts!

---
