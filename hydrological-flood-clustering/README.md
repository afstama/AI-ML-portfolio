# Hydrological Flood Clustering on the Sava River

**Bachelor's Thesis** · University of Zagreb, FER · 2023  
📄 *Published: "A Multivariate Approach to the Classification of Historical Floods on the Sava River in Zagreb" — Conference contribution, 2023*  
🤝 *Interdisciplinary collaboration with the Faculty of Civil Engineering*

---

## Overview

This project applies statistical and machine learning methods to **classify 60+ years of historical flood events** on the Sava River in Zagreb and Kupljenovo (1951–2021). The goal was to identify recurring flood wave patterns to support flood risk assessment and water resource management.

## Problem

Flood hydrographs (river discharge over time) have complex shapes. Traditional analysis treats each flood independently. By clustering similar flood shapes, engineers can identify recurring patterns, improve forecasting models, and better understand the river's behavior.

## Approach

1. **Data preprocessing** — cleaned 60 years of daily discharge measurements, handled missing values, filtered outliers
2. **Flood wave extraction** — isolated individual flood events from continuous time series using peak detection
3. **Shape interpolation** — B-spline and Fourier series representations to normalize floods of different durations to a common basis for comparison
4. **Feature engineering** — derived hydrological parameters (peak flow, volume, duration, rise/recession times, baseflow)
5. **Clustering** — k-means clustering on interpolated shapes and derived features; explored k=2 through k=7
6. **Visualization & analysis** — facet plots, U-matrix, hodograms, cluster profile comparison

## Key Findings

- Identified distinct flood typologies (e.g., sharp-peak vs. slow-rising events) consistent with different meteorological drivers
- B-spline representation better preserved shape nuance than Fourier for this dataset
- Cluster structure was stable across both Zagreb and Kupljenovo gauging stations

## Tech Stack

`R` · `ggplot2` · `dplyr` · `tidyr` · `splines` · `R Markdown`

## Files

| File | Description |
|---|---|
| `AFStamaZavrsni.Rmd` | Main R Markdown report — full analysis |
| `clusters.Rmd` / `clustersStandardized.Rmd` | Clustering experiments |
| `Zagreb-AM_v5.Rmd` | Zagreb station analysis |
| `Kupljenovo.Rmd` | Kupljenovo station analysis |
| `Kupljenovo_cleaning.R` | Data cleaning pipeline |
| `expl.R`, `explAnalysis.Rmd` | Exploratory data analysis |
| `Zagreb_dnevniQ-*.csv` | Daily discharge data (Zagreb, 1951–2021) |
| `Kupljenovo_dnevniQ-*.csv` | Daily discharge data (Kupljenovo, 1964–2021) |
| `Ana_Francesca_Stama_Zavrsni_Rad.pdf` | Full Bachelor's Thesis (Croatian) |

## Setup

```r
install.packages(c("ggplot2", "dplyr", "tidyr", "lubridate", "splines", "rmarkdown"))
```

Render the report:
```r
rmarkdown::render("AFStamaZavrsni.Rmd")
```
