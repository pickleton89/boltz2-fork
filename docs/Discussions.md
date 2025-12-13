
[Boltz2 Notes.md](hook://file/2fH7Jyskg?p=T2JzaWRpYW4vTXlfVmF1bHQ=&n=Boltz2%20Notes%2Emd)
[pickleton89/boltz2-fork:…](https://github.com/pickleton89/boltz2-fork)

[[Gemini3.5]]

Yes, **Boltz-2** has its own separate GitHub repository.

While the paper you uploaded focuses on **BoltzGen** (a design model), **Boltz-2** is the underlying structure and affinity prediction model it builds upon.

Here are the details for both repositories to avoid confusion:

### 1. Boltz-2 (Structure & Affinity Prediction)

- **Repo:** `jwohlwend/boltz`
    
- **Purpose:** This is the "foundation model" mentioned in the paper. It is used for predicting the 3D structure of biomolecular complexes (folding) and predicting binding affinity (how tight a binder is).
    
- **Key Capabilities:** Matches AlphaFold3 accuracy, predicts protein-ligand binding affinity, and supports "method conditioning" (emulating specific experimental conditions).
    

### 2. BoltzGen (Generative Design)

- **Repo:** `HannesStark/boltzgen`
    
- **Purpose:** This is the **generative** model described in your uploaded document. It uses the Boltz-2 architecture to _create new_ binders (proteins, peptides, nanobodies) rather than just predicting the structure of existing ones.
    
- **Key Capabilities:** All-atom generation, binder design, and the "design specification language" detailed in the paper.
    

**In summary:** If you want to **predict** how a molecule binds or folds, use the **Boltz-2** repo. If you want to **design** a new molecule from scratch, use the **BoltzGen** repo.

# Can one install locally
Yes, you can download and use **Boltz-2** locally. The model is open-source, and the developers provide a public GitHub repository with installation instructions, model weights, and inference code.

### **1. GitHub Repository & License**

- **Repository:** `jwohlwend/boltz` (Official repo for Boltz-1 and Boltz-2)
    
- **License:** **MIT License**. This is a permissive license that allows for both academic and commercial use, modification, and distribution without significant restrictions.
    

### **2. Installation for Local Use**

You can install the package directly into a Python environment. A Linux system with a CUDA-enabled GPU (NVIDIA) is strongly recommended for reasonable performance, as the CPU version is significantly slower.

**Quick Install Command:**

Bash

```
# Recommended: Create a fresh environment first (e.g., conda create -n boltz python=3.10)
pip install boltz[cuda]
```

**From Source (for latest updates):**

Bash

```
git clone https://github.com/jwohlwend/boltz.git
cd boltz
pip install -e .[cuda]
```

### **3. Downloading Model Weights**

- **Automatic Download:** When you run your first prediction command (e.g., `boltz predict ...`), the model will automatically attempt to download the necessary weights and cache them on your machine.
    
- **Docker:** If you prefer using Docker, there are instructions to build an image that "bakes in" the weights so you don't have to download them every time you spin up a container.
    

### **4. System Requirements**

- **OS:** Linux is the primary supported OS (tested on Ubuntu/CentOS).
    
- **Hardware:** An NVIDIA GPU with CUDA support is highly recommended. The model leverages NVIDIA `cuEquivariance` kernels for acceleration. While CPU usage is possible, it is not practical for large batches or production use due to speed constraints.
    
- **Disk Space:** Ensure you have sufficient disk space (approx. several GBs) for the model weights and any database files (like MSA databases) you might need if running fully offline.
    

### **5. Running Predictions Locally**

Once installed, you can run predictions using the command line interface (CLI). You will typically provide a generic input file (YAML or FASTA) describing your target.

**Example Command:**

Bash

```
boltz predict my_target.yaml --use_msa_server
```

- **Offline MSA:** The `--use_msa_server` flag relies on an external server to generate Multiple Sequence Alignments (MSAs). For a completely offline/local setup, you would need to install tools like `mmseqs2` locally and download the relevant sequence databases (which can be massive, often terabytes in size).
    

### **Summary of Local Capabilities**

| **Feature**   | **Local Support?** | **Notes**                                                                                                            |
| ------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| **Inference** | ✅ Yes              | Can run entirely on your local GPU.                                                                                  |
| **Weights**   | ✅ Yes              | Downloaded automatically or manually cached.                                                                         |
| **Training**  | ⚠️ Partial         | Training code is open, but re-training from scratch requires massive compute resources.                              |
| **MSAs**      | ⚠️ Complicated     | Generating MSAs locally requires huge databases. Most users rely on the remote MSA server or pre-computed MSA files. |

---

# Run on local m3 mac
Actually, **you absolutely can run Boltz-2 on your M3 Mac Ultra**, and your 256GB of unified memory gives you a massive advantage over most NVIDIA GPU users.

While the "official" high-speed path is optimized for NVIDIA CUDA (Linux), the model supports Apple Silicon via Metal Performance Shaders (MPS) or CPU fallback. Because Boltz-2 is memory-hungry, your 256GB RAM allows you to fold massive complexes that would crash on an RTX 4090 (which only has 24GB VRAM).

Here is how to make it work on your Mac:

### 1. The "Easy" Way: UCSF ChimeraX

The easiest way to run Boltz-2 on a Mac right now is through **UCSF ChimeraX** (daily builds). They have already integrated Boltz-2 support specifically for Apple Silicon.

- **Download:** Get the latest ChimeraX "Daily Build" (version 1.8 or newer).
    
- **Run:** Tools > Structure Prediction > Boltz.
    
- **Performance:** It utilizes your Mac's MPS acceleration. While it might be ~2-3x slower than a top-tier NVIDIA card, your massive RAM allows you to handle systems with thousands of residues that consumer GPUs simply cannot fit.
    

### 2. The "Developer" Way: Local Python Install

If you prefer the command line, you can install the Python package directly. You just need to omit the CUDA dependencies.

**Installation Command:**

Bash

```
# 1. Create a clean environment (Recommended)
conda create -n boltz python=3.10
conda activate boltz

# 2. Install WITHOUT the [cuda] tag
pip install boltz
# OR from source if you want the absolute latest fixes
pip install git+https://github.com/jwohlwend/boltz.git
```

Running it:

When you run boltz predict, the code uses PyTorch. On modern PyTorch versions, it should detect your M3 chip. If it defaults to CPU (which will be slow), you may need to check if the specific version of Boltz you installed exposes a --accelerator mps or --device mps flag, as MPS support was recently added to the codebase.

### Summary of Trade-offs for M3 Ultra

- **Speed:** Slower than NVIDIA H100/4090 (likely 2-3x slower).
    
- **Capacity:** **Superior.** You can process huge multimers (large protein complexes) that would cause "Out of Memory" errors on almost any standard GPU server because you have 256GB of addressable high-speed memory.
    

Would you like me to walk you through the specific `boltz predict` command flags to ensure it doesn't try to look for a CUDA device?

---

# What flag option for local

Yes, there are specific flags you can use to force Boltz-2 to behave on your Mac.

Because Boltz-2 is built on **PyTorch Lightning**, it inherits standard flags for controlling hardware. You can use these to explicitly tell it _not_ to look for NVIDIA CUDA cores and instead use your M3's CPU or MPS (Metal Performance Shaders) acceleration.

Here are the flags to add to your `boltz predict` command:

### 1. The "Force Mac" Flags

When running your prediction, append these arguments:

Bash

```
boltz predict my_target.yaml --accelerator mps --devices 1 --no_kernels
```

- **`--accelerator mps`**: This is the critical flag. It tells PyTorch to use Apple’s **Metal Performance Shaders** (MPS) instead of CUDA.
    
    - _Note:_ If `mps` throws an error (support was only recently added), switch this to `--accelerator cpu`. It will be slower but will 100% work with your RAM capacity.
        
- **`--no_kernels`**: This disables the custom NVIDIA `cuEquivariance` kernels that speed up the model on Linux but are incompatible with Mac. If you don't include this, the model might crash looking for compiled CUDA binaries.
    
- **`--devices 1`**: Explicitly tells it to use a single "device" (your M3 chip) rather than trying to find a distributed cluster.
    

### 2. Verify Your "Device" Visibility

Before running a big job, you can verify if Boltz sees your M3 chip by running this quick Python snippet in your Boltz environment:

Python

```
import torch
print(torch.backends.mps.is_available())
# Should print: True
```

### 3. Summary of Command Line Arguments

Here is a quick reference table of the relevant flags found in the documentation:

|**Flag**|**Value for Mac**|**Why?**|
|---|---|---|
|`--accelerator`|`mps` (or `cpu`)|Forces use of Apple Silicon (Metal) or CPU fallback.|
|`--no_kernels`|`True` (flag present)|Disables NVIDIA-only optimizations that crash on Mac.|
|`--precision`|`32` or `16`|`bf16` (Brain Float 16) is often default for NVIDIA but can be buggy on some MPS versions. If you get numerical errors, force `32`.|

**Next Step:** Try running `boltz predict --help` in your terminal. If you see `--accelerator` listed, you are good to go with the flags above.