import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEASUREMENTS_CSV = os.path.join(DATA_DIR, "measurements", "measurements.csv")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")

os.makedirs(PLOTS_DIR, exist_ok=True)


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "serif"],
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "axes.facecolor": "white",
        "figure.facecolor": "white",
    }
)

# paleta
palette = {"bf": "#d7191c", "dp": "#2c7bb6", "gh1": "#fdae61", "gh2": "#abd9e9"}
markers = {"bf": "o", "dp": "s", "gh1": "^", "gh2": "D"}
dashes = {"bf": (1, 0), "dp": (2, 2), "gh1": (4, 2), "gh2": (1, 1)}


def plot_execution_time(df):
    plt.figure(figsize=(7, 5))
    sns.lineplot(
        data=df,
        x="n_animes",
        y="tiempo_ms",
        hue="algoritmo",
        style="algoritmo",
        markers=markers,
        dashes=dashes,
        palette=palette,
    )

    plt.title("Execution Time vs. Input Size (N)")
    plt.xlabel("Number of Animes (N)")
    plt.ylabel("Execution Time (ms)")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "tiempo_vs_n.png"))
    plt.close()


def plot_memory_usage(df):
    plt.figure(figsize=(7, 5))
    sns.lineplot(
        data=df,
        x="n_animes",
        y="memoria_mb",
        hue="algoritmo",
        style="algoritmo",
        markers=markers,
        dashes=dashes,
        palette=palette,
    )

    plt.title("Memory Usage vs. Input Size (N)")
    plt.xlabel("Number of Animes (N)")
    plt.ylabel("Memory Usage (MB)")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "memoria_vs_n.png"))
    plt.close()


def plot_quality_gap(df):
    df_pivot = df.pivot_table(
        index=["id_archivo", "n_animes"], columns="algoritmo", values="satisfaccion"
    ).reset_index()

    if "dp" not in df_pivot.columns:
        print("No hay datos de DP")
        return

    for alg in ["gh1", "gh2"]:
        if alg in df_pivot.columns:
            df_pivot[f"calidad_{alg}"] = (df_pivot[alg] / df_pivot["dp"]) * 100

    melted = df_pivot.melt(
        id_vars=["n_animes"],
        value_vars=[col for col in df_pivot.columns if col.startswith("calidad_")],
        var_name="Heuristica",
        value_name="Porcentaje_Optimo",
    )

    plt.figure(figsize=(7, 5))
    sns.scatterplot(
        data=melted,
        x="n_animes",
        y="Porcentaje_Optimo",
        hue="Heuristica",
        style="Heuristica",
        palette=["#fdae61", "#abd9e9"],
    )

    plt.axhline(100, color="black", linestyle="--", label="Optimal (DP)", alpha=0.7)
    plt.title("Heuristic Quality vs. Optimal Solution")
    plt.xlabel("Number of Animes (N)")
    plt.ylabel("Satisfaction (% of Optimal)")
    plt.ylim(0, 110)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "calidad_heuristicas.png"))
    plt.close()


def plot_behavior_variables(df):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    sns.scatterplot(
        data=df,
        x="minutos_m",
        y="satisfaccion",
        hue="algoritmo",
        style="algoritmo",
        markers=markers,
        palette=palette,
        alpha=0.8,
        ax=axes[0],
    )
    axes[0].set_title("Satisfaction vs. Available Time")
    axes[0].set_xlabel("Available Minutes (M)")
    axes[0].set_ylabel("Total Satisfaction")

    sns.scatterplot(
        data=df,
        x="energia_e",
        y="satisfaccion",
        hue="algoritmo",
        style="algoritmo",
        markers=markers,
        palette=palette,
        alpha=0.8,
        ax=axes[1],
    )
    axes[1].set_title("Satisfaction vs. Available Energy")
    axes[1].set_xlabel("Available Energy (E)")
    axes[1].set_ylabel("Total Satisfaction")

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "comportamiento_recursos.png"))
    plt.close()


def main():
    if not os.path.exists(MEASUREMENTS_CSV):
        print(f"Archivo {MEASUREMENTS_CSV} no encontrado.")
        return

    df = pd.read_csv(MEASUREMENTS_CSV)

    plot_execution_time(df)
    plot_memory_usage(df)
    plot_quality_gap(df)
    plot_behavior_variables(df)


if __name__ == "__main__":
    main()
