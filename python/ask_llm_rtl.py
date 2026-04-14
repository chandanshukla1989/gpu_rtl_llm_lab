import torch
import numpy as np
import subprocess
import time
import os

vocab = {}

def tokenize(text):
    words = text.lower().split()
    tokens = []
    for w in words:
        if w not in vocab:
            vocab[w] = len(vocab)
        tokens.append(vocab[w])
    return tokens

dim = 4
device = "cuda" if torch.cuda.is_available() else "cpu"

embedding = torch.nn.Embedding(100, dim).to(device)
linear_weight = torch.randn(dim, dim).to(device)

question = input("\nAsk something: ")

tokens_list = tokenize(question)
tokens = torch.tensor(tokens_list, dtype=torch.long)
tokens = tokens[:4]

if len(tokens) < 4:
    pad = torch.zeros(4 - len(tokens), dtype=torch.long)
    tokens = torch.cat([tokens, pad])

tokens = tokens.to(device)

X = embedding(tokens)  # shape [4,4]

start = time.time()
Y_gpu = torch.matmul(X, linear_weight)
if device == "cuda":
    torch.cuda.synchronize()
gpu_time = time.time() - start

X_np = X.detach().cpu().numpy()
W_np = linear_weight.detach().cpu().numpy()

# Only first row goes to current RTL design
X_row = X_np[0:1, :]              # shape [1,4]
X_row_q = (X_row * 10).astype(np.int8)

# Pad to 4x4 so existing RTL input format stays valid
A_pad = np.zeros((4, 4), dtype=np.int8)
A_pad[0, :] = X_row_q[0]

W_q = (W_np * 10).astype(np.int8)

np.savetxt("A.txt", A_pad.flatten(), fmt="%d")
np.savetxt("B.txt", W_q.flatten(), fmt="%d")

exe_path = os.path.join(os.path.dirname(__file__), "..", "obj_dir", "Vmatmul")

start = time.time()
subprocess.run([exe_path], stdout=subprocess.DEVNULL, check=True)
rtl_time = time.time() - start

C_rtl = np.loadtxt("C.txt").reshape(1, 4)
C_rtl = C_rtl / 100.0

Y_gpu_np = Y_gpu.detach().cpu().numpy()
Y_gpu_row0 = Y_gpu_np[0:1, :]

def decode(arr):
    return " ".join(f"{x:.2f}" for x in arr.flatten())

answer_gpu = decode(Y_gpu_row0)
answer_rtl = decode(C_rtl)

error = np.abs(Y_gpu_row0 - C_rtl).mean()

# simple estimates
gpu_mem = X.element_size() * X.nelement() + linear_weight.element_size() * linear_weight.nelement()
rtl_mem = A_pad.nbytes + W_q.nbytes

ops = 4 * 4
gpu_energy = ops * 10
rtl_energy = ops * 1

print("\n==============================")
print("QUESTION:", question)

print("\n--- GPU ONLY ANSWER (row 0) ---")
print(answer_gpu)
print("Latency:", gpu_time)

print("\n--- GPU + RTL ANSWER (row 0) ---")
print(answer_rtl)
print("Latency (sim):", rtl_time)

print("\n--- ACCURACY ---")
print("Mean Error:", error)

print("\n--- MEMORY ---")
print("GPU bytes:", gpu_mem)
print("RTL bytes:", rtl_mem)

print("\n--- ENERGY ---")
print("GPU:", gpu_energy)
print("RTL:", rtl_energy)

print("\n--- INSIGHT ---")
print("RTL simulation is slower, but projected hardware is more energy-efficient for fixed-function compute.")
