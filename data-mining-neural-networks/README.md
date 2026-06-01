# Data Mining & Neural Networks

**MSc Course** · KU Leuven, Faculty of Engineering Science · 2023–2024

---

## Overview

Lab exercises from the Data Mining and Neural Networks course at KU Leuven, covering foundations of neural networks through to advanced architectures. Implemented from scratch and with PyTorch/Scikit-Learn.

---

## Exercise 1 — Backpropagation & Regression

[`exercise1-backprop-regression/`](exercise1-backprop-regression/)

**Topics:** Manual backpropagation, learning rate sensitivity, multi-output regression, function approximation with noise.

- Implemented backprop from scratch in `backprop.py`
- Explored effect of learning rate (0.002 → 4) on convergence
- Compared multiple optimizers (SGD, Adam, etc.) at different iteration counts
- Approximated noisy nonlinear functions with varying network sizes
- Regression on 2D surface data

**Skills:** NumPy, gradient descent, optimizer comparison, overfitting/underfitting analysis

---

## Exercise 2 — Time Series, Classification & Self-Organizing Maps

[`exercise2-timeseries-clustering/`](exercise2-timeseries-clustering/)

**Topics:** Temporal forecasting, density estimation, unsupervised clustering, dimensionality reduction.

- **Time series forecasting** on global temperature data (Zagreb, Budapest) with lag analysis
- **Classification** with density estimation — Naive Bayes, histogram-based approaches
- **Self-Organizing Maps (SOM)** on the Iris dataset — trained for 1 to 1000 epochs, visualized U-matrix
- **ARD (Automatic Relevance Determination)** — Bayesian feature selection

**Dataset:** Global Land Temperatures by City (Kaggle) — [*Climate Change: Earth Surface Temperature Data*](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data). The `GlobalLandTemperaturesByCity.csv` file (~230 MB) is not committed; download it from Kaggle and place it in `exercise2-timeseries-clustering/` to run the notebooks.

**Skills:** Time series analysis, SOM, Bayesian methods, clustering visualization

---

## Exercise 3 — CNNs, Attention & PCA

[`exercise3-cnn-attention-pca/`](exercise3-cnn-attention-pca/)

**Topics:** Convolutional networks, transfer learning, attention mechanisms, dimensionality reduction.

- **CNNs** — image classification, ResNet fine-tuning, architecture search (8 model variants)
- **Attention** — self-attention mechanism implementation and visualization
- **PCA** — manual implementation, comparison with sklearn, dimensionality reduction on image data

**Skills:** PyTorch, ResNet, transfer learning, attention, sklearn PCA

---

## Tech Stack

`Python` · `PyTorch` · `Scikit-Learn` · `NumPy` · `Pandas` · `Matplotlib`
