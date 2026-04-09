# Spotify Track Analysis

Statistical analysis of Spotify track data across genres, examining popularity, danceability, and tempo using non-parametric tests and visualizations.

## Overview

This project analyzes a Spotify dataset to compare musical characteristics across four genres: **pop**, **rock**, **hip-hop**, and **classical**. It applies rigorous statistical tests to determine whether observed differences between genres are statistically significant.

## Analysis Pipeline

### 1. Descriptive Statistics

Computes mean, median, mode, and standard deviation for each variable across the full dataset.

### 2. Shapiro-Wilk Test

Tests whether each variable follows a normal distribution (H₀: data is normally distributed). A sample of 1 000 observations is used, as Shapiro-Wilk requires n < 5 000.

### 3. Levene's Test

Tests for homogeneity of variance across genres (H₀: equal variance in all groups).

### 4. Kruskal-Wallis Test

A non-parametric test used when normality cannot be assumed. Tests whether at least one genre differs significantly from the others (H₀: all genres share the same distribution).

## Visualizations

| File                    | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `histogram.png`         | Distribution of popularity, danceability, and tempo across all tracks |
| `boxplot_genres.png`    | Per-genre boxplots for each variable                                  |
| `scatter_dance_pop.png` | Density plots of danceability vs. popularity, one panel per genre     |
| `medelvarden_genre.png` | Mean values per genre (bar charts)                                    |

## Requirements

```
pandas
numpy
matplotlib
seaborn
scipy
```

Install with:

```bash
pip install pandas numpy matplotlib seaborn scipy
```

## Usage

1. Place `dataset.csv` in the project root directory.
2. Run the analysis:

```bash
python analysis.py
```

The script prints statistical results to the terminal and saves four plot files to the project root.

## Dataset

The script expects a CSV file named `dataset.csv` with at least the following columns:

| Column         | Description                                              |
| -------------- | -------------------------------------------------------- |
| `track_genre`  | Genre label (e.g. `pop`, `rock`, `hip-hop`, `classical`) |
| `popularity`   | Spotify popularity score (0–100)                         |
| `danceability` | Danceability score (0.0–1.0)                             |
| `tempo`        | Tempo in BPM                                             |
