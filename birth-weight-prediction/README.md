# Newborn Birth-Weight Prediction from Maternal Features

**MSc Course — Introduction to Data Science** · University of Zagreb, FER · 2024
👥 *Three-person team project*

---

## Overview

An end-to-end data-science study that predicts a **newborn's birth weight** from
**maternal features** (e.g. age, health indicators, pregnancy data) using the
CBWDB dataset. Beyond building predictive models, the project **reproduces and
critically evaluates** the methodology of a published reference paper, testing
whether its reported results hold up under proper validation.

## What the project does

1. **Data preprocessing** — cleaning, encoding, handling missing values, and feature preparation
2. **Exploratory visualization** — distributions and relationships between maternal features and birth weight
3. **Paper reproduction** — re-implements the reference paper's models (Gaussian Naive Bayes, Random Forest Classifier) and asks *"are the paper's results valid?"*, exposing methodology issues such as data leakage / optimistic evaluation
4. **Regression** — predicting birth weight as a continuous value: Random Forest, Linear Regression, Support Vector Regression (evaluated with R² and RMSE)
5. **Classification** — predicting birth-weight categories: Logistic Regression, Random Forest, K-Nearest Neighbors, SVC, Gaussian Naive Bayes (evaluated with accuracy and F1)
6. **Hyperparameter tuning** — grid search over the strongest models
7. **Metaheuristic extension** — an additional optimization-based approach as a bonus exploration

## Key takeaway

A central finding is that the reference paper's headline accuracy did not survive
a leakage-free, properly held-out evaluation — a reminder that validation
methodology matters as much as model choice.

## Tech Stack

`Python` · `scikit-learn` · `Pandas` · `NumPy` · `Matplotlib` / `Seaborn`

## Files

| File | Description |
|---|---|
| `birth_weight_prediction.ipynb` | Full team notebook: preprocessing → visualization → paper reproduction → regression & classification → tuning |
| `CBWDB.csv` | Maternal-features birth-weight dataset |

## Run

```bash
pip install scikit-learn pandas numpy matplotlib seaborn
jupyter notebook birth_weight_prediction.ipynb
```

> The notebook narrative is written in Croatian; code, model names, and metrics
> are standard and language-independent.
