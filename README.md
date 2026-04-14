🚀 **Repo: Hybrid LLM Inference with GPU + Verilog (RTL) Accelerator**

This repository demonstrates a simple but powerful idea:

👉 What happens when we offload part of an LLM computation from GPU to a custom VLSI-style accelerator?

---

## 🧠 What’s inside

This is an **end-to-end working lab** that simulates a mini LLM pipeline:

* Input question → tokenization
* Embedding layer → runs on GPU (PyTorch)
* Linear layer → runs in two modes:

  * GPU (baseline)
  * Verilog RTL (via Verilator simulation)
* Outputs are compared for:

  * accuracy
  * latency
  * memory usage
  * projected energy

---

## ⚙️ Tech stack

* **PyTorch (GPU)** → for embedding and baseline compute
* **Verilog (RTL)** → custom INT8 matrix multiply accelerator
* **Verilator** → compiles RTL into a cycle-accurate C++ model
* **C++ bridge** → connects Python data to RTL simulation

---

## 🔬 What this repo proves

* LLMs are fundamentally built on **matrix multiplications**
* These compute blocks can be:

  * executed on GPU (flexible, general-purpose)
  * or offloaded to **custom hardware (RTL / ASIC style)**

---

## 📊 Key observations

* RTL output closely matches GPU (low quantization error)
* Memory footprint is reduced using quantized data
* Energy model shows **~10x improvement for fixed-function compute**
* Execution is **deterministic** in hardware vs dynamic scheduling on GPU

---

## ⚠️ Important note

This repo uses **simulation (Verilator)**, not real FPGA/ASIC hardware.

👉 So latency comparisons are **not hardware-accurate**
👉 The real benefit is in:

* **energy efficiency**
* **memory optimization**
* **hardware specialization**

---

## 💡 Why this matters

Modern AI systems are no longer just models.

They are:

* hardware-aware
* performance-optimized
* co-designed across software and silicon

This repo is a small step toward understanding:

👉 **how GPUs and custom accelerators can coexist in LLM workloads**

---

## 🚀 Use cases

* Learning hardware-aware AI design
* Exploring GPU vs ASIC trade-offs
* Understanding LLM compute internals
* Building custom AI accelerators

---

## 🔥 TL;DR

> A minimal hybrid AI pipeline where GPU handles flexible compute and Verilog RTL handles fixed-function acceleration — demonstrating the future direction of AI systems.

---
