import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, levene, kruskal

# ============================================================
# LADDA DATA
# OBS: Lägg dataset.csv i samma mapp som denna fil
# ============================================================
df = pd.read_csv('dataset.csv')

VARIABLES = ['popularity', 'danceability', 'tempo']
GENRES    = ['pop', 'rock', 'hip-hop', 'classical']

df_genres = (
    df[df['track_genre'].isin(GENRES)][VARIABLES + ['track_genre']]
    .dropna()
)

# ============================================================
# 1. GRUNDLÄGGANDE STATISTIK
# ============================================================
print("=" * 50)
print("GRUNDLÄGGANDE STATISTIK")
print("=" * 50)
for var in VARIABLES:
    print(f"\n{var.upper()}")
    print(f"  Medelvärde (mean):   {df[var].mean():.2f}")
    print(f"  Median:              {df[var].median():.2f}")
    print(f"  Typvärde (mode):     {df[var].mode()[0]:.2f}")
    print(f"  Standardavvikelse:   {df[var].std():.2f}")

# ============================================================
# 2. NORMALITETSTEST — Shapiro-Wilk
#    Testar om data följer en normalfördelning.
#    H0: data är normalfördelad
#    Om p < 0.05 → förkasta H0 → inte normalfördelad
#    (Vi samplar 1000 obs eftersom Shapiro kräver n < 5000)
# ============================================================
print("\n" + "=" * 50)
print("SHAPIRO-WILK TEST (normalfördelning, n=1000)")
print("=" * 50)
for var in VARIABLES:
    sample = df[var].dropna().sample(1000, random_state=42)
    stat, p = shapiro(sample)
    result = "Normalfördelad" if p > 0.05 else "INTE normalfördelad → använd icke-parametrisk test"
    print(f"{var}: W={stat:.4f}, p={p:.4f} → {result}")

# ============================================================
# 3. LEVENE'S TEST — homogenitet av varians
#    Testar om variansen är lika mellan genrerna.
#    H0: variansen är lika i alla grupper
#    Om p < 0.05 → variansen är INTE homogen
# ============================================================
print("\n" + "=" * 50)
print("LEVENE'S TEST (homogenitet av varians)")
print("=" * 50)
for var in VARIABLES:
    groups = [df_genres[df_genres['track_genre'] == g][var] for g in GENRES]
    stat, p = levene(*groups)
    result = "Homogen varians" if p > 0.05 else "INTE homogen varians"
    print(f"{var}: stat={stat:.4f}, p={p:.4f} → {result}")

# ============================================================
# 4. KRUSKAL-WALLIS TEST — jämförelse mellan genrer
#    Icke-parametrisk (används när data inte är normalfördelad).
#    Jämför om minst en genre skiljer sig signifikant från de andra.
#    H0: alla genrer har samma fördelning
#    Om p < 0.05 → signifikant skillnad mellan genrerna
# ============================================================
print("\n" + "=" * 50)
print("KRUSKAL-WALLIS TEST (skillnader mellan genrer)")
print("=" * 50)
print(f"Genrer jämförda: {GENRES}\n")
for var in VARIABLES:
    groups = [df_genres[df_genres['track_genre'] == g][var] for g in GENRES]
    stat, p = kruskal(*groups)
    result = "Signifikant skillnad (p < 0.05)" if p < 0.05 else "Ingen signifikant skillnad"
    print(f"{var}: H={stat:.2f}, p={p:.4f} → {result}")

# ============================================================
# 5. VISUALISERINGAR
# ============================================================
sns.set_theme(style="whitegrid", palette="Set2")

# --- Bild 1: Histogram för varje variabel ---
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Fördelning av popularity, danceability och tempo", fontsize=14, fontweight='bold')

for i, var in enumerate(VARIABLES):
    sns.histplot(df[var].dropna(), kde=True, ax=axes[i], color='steelblue', bins=30)
    axes[i].set_title(var.capitalize())
    axes[i].set_xlabel(var)
    axes[i].set_ylabel("Antal låtar")

plt.tight_layout()
plt.savefig('histogram.png', dpi=150, bbox_inches='tight')
print("\nSparad: histogram.png")
plt.close()

# --- Bild 2: Boxplot per genre ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Jämförelse mellan genrer", fontsize=14, fontweight='bold')

for i, var in enumerate(VARIABLES):
    sns.boxplot(x='track_genre', y=var, data=df_genres, ax=axes[i], palette='Set2')
    axes[i].set_title(var.capitalize())
    axes[i].set_xlabel("Genre")
    axes[i].set_ylabel(var)

plt.tight_layout()
plt.savefig('boxplot_genres.png', dpi=150, bbox_inches='tight')
print("Sparad: boxplot_genres.png")
plt.close()

# --- Bild 3: Densitetsplot — danceability vs popularity per genre ---
colors = {'pop': '#4c72b0', 'rock': '#dd8452', 'hip-hop': '#55a868', 'classical': '#c44e52'}
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.suptitle("Popularitet vs Dansbarhet per genre (densitet)", fontsize=14, fontweight='bold')

for ax, genre in zip(axes.flat, GENRES):
    subset = df_genres[df_genres['track_genre'] == genre]
    sns.kdeplot(
        x=subset['danceability'], y=subset['popularity'],
        fill=True, cmap='Blues' if genre == 'pop' else
                       'Oranges' if genre == 'rock' else
                       'Greens' if genre == 'hip-hop' else 'Reds',
        thresh=0.05, levels=10, ax=ax
    )
    ax.set_title(genre.capitalize(), fontsize=12, fontweight='bold', color=colors[genre])
    ax.set_xlabel("Danceability")
    ax.set_ylabel("Popularity")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('scatter_dance_pop.png', dpi=150, bbox_inches='tight')
print("Sparad: scatter_dance_pop.png (densitetsplot)")
plt.close()

# --- Bild 4: Medelvärden per genre (stapeldiagram) ---
means = df_genres.groupby('track_genre')[VARIABLES].mean().reset_index()
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Medelvärden per genre", fontsize=14, fontweight='bold')

for i, var in enumerate(VARIABLES):
    sns.barplot(x='track_genre', y=var, data=means, ax=axes[i], palette='Set2')
    axes[i].set_title(var.capitalize())
    axes[i].set_xlabel("Genre")
    axes[i].set_ylabel(f"Medel {var}")

plt.tight_layout()
plt.savefig('medelvarden_genre.png', dpi=150, bbox_inches='tight')
print("Sparad: medelvarden_genre.png")
plt.close()

print("\nKlart! Alla grafer sparade.")
