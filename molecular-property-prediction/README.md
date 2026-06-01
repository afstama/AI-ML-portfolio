# Molecular Property Prediction via Cross-Modal Representation Fusion

**Master's Thesis** · University of Zagreb, FER · 2025  
🏆 *Recipient of the GDi Excellence Award for exceptional Master Thesis*  
🔬 *Presented at the 10th Symposium of Chemistry Students*

---

## Overview

This project tackles **lipophilicity (logD) prediction** on the MolNet Lipophilicity dataset (~4,200 molecules) by fusing multiple molecular representations — a cross-modal approach that outperforms any single representation alone.

Lipophilicity is a key ADMET property in drug discovery, influencing membrane permeability, solubility, and metabolic stability. Accurate prediction from molecular structure reduces the need for expensive wet-lab assays.

## Approach

Three complementary views of molecules are combined:

| Representation | Type | Description |
|---|---|---|
| **Molecular Descriptors** | Numerical | 2D & 3D Mordred descriptors (1,600+ features) with automated feature selection (variance threshold, correlation filtering, RFECV) |
| **Molecular Fingerprints** | Binary vectors | MACCS keys (167-bit), ECFP/Morgan (512-bit), ErG pharmacophore fingerprints |
| **Mol2Vec / ChemBERTa** | Embeddings | NLP-inspired molecular embeddings (Word2Vec on molecular substructures; transformer fine-tuned on SMILES) |

**Fusion strategies explored:** early fusion (concatenation), late fusion (ensemble), and stacked generalization.

**Models used:** Random Forest, Gradient Boosting, SVR, SGDRegressor, neural networks (MLP), and fine-tuned transformer (ChemBERTa via MLM pre-training).

**Validation:** Bemis-Murcko scaffold split + 5-fold scaffold cross-validation (to prevent data leakage between structurally similar molecules).

## Key Results

- Scaffold-aware CV ensures generalization to structurally novel molecules
- Multi-modal fusion consistently improves MAE/RMSE over single-representation baselines
- ChemBERTa MLM fine-tuning on domain-specific SMILES improves embedding quality

## Tech Stack

`Python` · `PyTorch` · `DeepChem` · `RDKit` · `Mordred` · `Scikit-Learn` · `HuggingFace Transformers` · `Mol2Vec`

## Files

| File | Description |
|---|---|
| `dipl_rad_v4.ipynb` | Main notebook: full pipeline (latest version) |
| `dipl_rad_v3.ipynb` | Earlier pipeline iteration |
| `dipl_rad_v3_data2.ipynb` | Variant with secondary dataset |
| `dopamine.csv` | Sample molecule data |

## Setup

```bash
pip install deepchem rdkit-pypi mordred mol2vec transformers torch scikit-learn pandas numpy
```

> **Note:** Large model checkpoints (ChemBERTa fine-tuned weights) and precomputed descriptor caches are not included in this repo due to size. The notebooks include code to recompute them.
