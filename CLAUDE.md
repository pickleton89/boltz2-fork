# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Boltz is a family of deep learning models for biomolecular interaction prediction. This repository contains both Boltz-1 and Boltz-2 models:
- **Boltz-1**: First fully open-source model approaching AlphaFold3 accuracy for structure prediction
- **Boltz-2**: Foundation model that jointly models complex structures and binding affinities, approaching FEP accuracy while running 1000x faster

## Development Commands

### Environment Setup
```bash
# Install with CUDA support (recommended)
pip install -e .[cuda]

# Install without CUDA (slower, for CPU-only systems)
pip install -e .
```

### Linting and Formatting
```bash
uv run ruff check .                    # Lint code
uv run ruff check . --fix              # Auto-fix linting issues
uv run ruff format .                   # Format code
```

### Running Tests
```bash
uv run pytest                          # Run all tests
uv run pytest -m "not slow"            # Skip slow tests
uv run pytest -m "not regression"      # Skip regression tests
uv run pytest tests/test_kernels.py   # Run single test file
```

### Inference
```bash
# Basic prediction (downloads models automatically to ~/.boltz)
boltz predict input.yaml --use_msa_server

# With more samples and recycling (AlphaFold3-like settings)
boltz predict input.yaml --use_msa_server --recycling_steps 10 --diffusion_samples 25

# Use Boltz-1 instead of Boltz-2
boltz predict input.yaml --use_msa_server --model boltz1

# Enable inference-time potentials for better physical plausibility
boltz predict input.yaml --use_msa_server --use_potentials
```

### Training
```bash
# Debug mode (single device, no DDP, no wandb)
python scripts/train/train.py scripts/train/configs/structure.yaml debug=1

# Full training
python scripts/train/train.py scripts/train/configs/structure.yaml

# Confidence model training
python scripts/train/train.py scripts/train/configs/confidence.yaml
```

## Architecture Overview

### Core Structure (`src/boltz/`)

**Entry Point**: `main.py` - CLI interface via Click, handles prediction workflow:
1. Downloads models/CCD data to cache (`~/.boltz` or `$BOLTZ_CACHE`)
2. Parses YAML/FASTA inputs
3. Generates MSAs via mmseqs2 server if needed
4. Runs structure prediction with diffusion model
5. Optionally runs affinity prediction

**Model Hierarchy**:
- `model/models/boltz1.py`, `model/models/boltz2.py` - Lightning modules wrapping full model
- `model/modules/` - Core neural network components:
  - `trunkv2.py` - Input embedding, MSA module, template module
  - `transformersv2.py` - Transformer blocks
  - `diffusionv2.py` - Atom-level diffusion for structure generation
  - `confidencev2.py` - Confidence prediction (pLDDT, PAE, PDE)
  - `affinity.py` - Binding affinity prediction module
- `model/layers/` - Building blocks (attention, pairformer, triangular updates)

**Data Pipeline** (`data/`):
- `parse/` - Input parsers: YAML (`yaml.py`), FASTA (`fasta.py`), A3M MSAs (`a3m.py`), mmCIF/PDB structures
- `tokenize/` - Converts parsed data to model tokens (`boltz2.py` for v2 tokenization)
- `feature/` - Featurization for model input
- `crop/` - Cropping strategies for large structures
- `module/` - PyTorch Lightning data modules for inference and training
- `write/` - Output writers for mmCIF/PDB formats

### Key Data Types (`data/types.py`)
- `Structure` - Atom coordinates and features
- `Record` - Metadata for a prediction target
- `Manifest` - Collection of records for batch processing
- `MSA` - Multiple sequence alignment data

### Version Differences (v1 vs v2)
Files with `v2` suffix (e.g., `featurizerv2.py`, `trunkv2.py`) are Boltz-2 specific. Boltz-2 uses:
- 64 pairformer blocks (vs 48 in Boltz-1)
- Different diffusion parameters
- Paired MSA features
- Affinity prediction capability

### Training Data Processing (`scripts/process/`)
- `rcsb.py` - Process PDB/mmCIF structures
- `msa.py` - Process raw MSAs with taxonomy annotation
- `cluster.py` - Sequence clustering (40% similarity for proteins)
- `ccd.py` - Process Chemical Component Dictionary

## Input Format

Boltz uses YAML format for input specification (FASTA is deprecated):

```yaml
sequences:
  - protein:
      id: A
      sequence: MVTPEGN...
      msa: ./path/to/msa.a3m  # Optional if using --use_msa_server
  - ligand:
      id: B
      smiles: 'CC1=CC=CC=C1'  # Or use ccd: ATP
properties:
  - affinity:
      binder: B  # For binding affinity prediction
```

## Environment Variables

- `BOLTZ_CACHE` - Override default cache directory (~/.boltz)
- `BOLTZ_MSA_USERNAME` / `BOLTZ_MSA_PASSWORD` - MSA server basic auth
- `MSA_API_KEY_VALUE` - MSA server API key authentication

## Ruff Configuration

Uses numpy docstring convention. Key ignores: missing module/package docstrings (D100/D104), too many arguments (PLR0913). See `pyproject.toml` for full config.
