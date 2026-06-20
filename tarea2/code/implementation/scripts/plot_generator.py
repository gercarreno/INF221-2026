import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr, spearmanr


# rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEASUREMENTS_CSV = os.path.join(DATA_DIR, "measurements", "measurements.csv")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")

os.makedirs(PLOTS_DIR, exist_ok=True)

# parametros del matplotlib
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Liberation Serif", "Georgia", "DejaVu Serif", "serif"],
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

ALG_ORDER = ["bf", "dp", "gh1", "gh2"]
ALG_LABELS = {
    "bf": "Fuerza bruta",
    "dp": "Prog. dinámica",
    "gh1": "Greedy ratio",
    "gh2": "Greedy max",
}
PALETTE = {"bf": "#d7191c", "dp": "#2c7bb6", "gh1": "#fdae61", "gh2": "#abd9e9"}
MARKERS = {"bf": "o", "dp": "s", "gh1": "^", "gh2": "D"}


def _save(fig, name):
    fig.savefig(os.path.join(PLOTS_DIR, name), bbox_inches="tight")
    plt.close(fig)


def load_and_prepare(path):
    df = pd.read_csv(path)

    df = df.rename(columns={"tiempo_ns": "tiempo_ns"})
    df["tiempo_ns"] = df["tiempo_ns"] / 1e6
    df["tiempo_s"] = df["tiempo_ns"] / 1e9

    df["algoritmo"] = pd.Categorical(
        df["algoritmo"], categories=ALG_ORDER, ordered=True
    )

    opt = df[df["algoritmo"] == "dp"][["id_archivo", "satisfaccion"]].rename(
        columns={"satisfaccion": "opt"}
    )
    df = df.merge(opt, on="id_archivo", how="left")
    df["calidad_pct"] = np.where(
        df["opt"] > 0, df["satisfaccion"] / df["opt"] * 100, np.nan
    )

    return df.sort_values("n_animes")


def plot_time_algorithms(df):
    g = sns.relplot(
        data=df,
        x="n_animes",
        y="tiempo_ns",
        col="algoritmo",
        hue="algoritmo",
        col_order=ALG_ORDER,
        hue_order=ALG_ORDER,
        kind="line",
        col_wrap=2,
        height=3.2,
        aspect=1.35,
        palette=PALETTE,
        marker="o",
        errorbar=None,
        facet_kws={"sharey": False, "sharex": True},
        legend=False,
    )
    g.set(yscale="log")

    for ax, alg in zip(g.axes.flat, ALG_ORDER):
        ax.set_title(ALG_LABELS.get(alg, alg))
        ax.set_xlabel("N animes")
        ax.set_ylabel("Tiempo (ns)")

    g.figure.suptitle("Tiempo de ejecución vs N", y=1.03)
    _save(g.figure, "tiempo_algoritmos.png")


def plot_time_scale(df):
    # Escalamiento polinomial vs exponencial.
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    poly = df[df["algoritmo"].isin(["dp", "gh1", "gh2"])]
    sns.lineplot(
        data=poly,
        x="n_animes",
        y="tiempo_ns",
        hue="algoritmo",
        style="algoritmo",
        hue_order=["dp", "gh1", "gh2"],
        palette=PALETTE,
        markers=MARKERS,
        errorbar=None,
        ax=axes[0],
    )
    axes[0].set(
        yscale="log", title="DP vs Greedy", xlabel="N animes", ylabel="Tiempo (ns)"
    )

    bf = df[df["algoritmo"] == "bf"]
    sns.lineplot(
        data=bf,
        x="n_animes",
        y="tiempo_ns",
        color=PALETTE["bf"],
        marker="o",
        errorbar=None,
        ax=axes[1],
    )
    axes[1].set(
        yscale="log",
        title="Fuerza bruta (N ≤ 25)",
        xlabel="N animes",
        ylabel="Tiempo (ns, log)",
    )

    fig.suptitle("Polinomial vs Exponencial", y=1.02)
    fig.tight_layout()
    _save(fig, "tiempo_escalamiento.png")


def plot_memory_algorithms(df):
    g = sns.relplot(
        data=df,
        x="n_animes",
        y="memoria_mb",
        col="algoritmo",
        hue="algoritmo",
        col_order=ALG_ORDER,
        hue_order=ALG_ORDER,
        kind="line",
        col_wrap=2,
        height=3.2,
        aspect=1.35,
        palette=PALETTE,
        marker="o",
        errorbar=None,
        facet_kws={"sharey": False, "sharex": True},
        legend=False,
    )

    for ax, alg in zip(g.axes.flat, ALG_ORDER):
        ax.set_title(ALG_LABELS.get(alg, alg))
        ax.set_xlabel("N animes")
        ax.set_ylabel("Memoria (MB)")

    g.figure.suptitle("Uso de memoria vs N", y=1.03)
    _save(g.figure, "memoria_algoritmos.png")


def _sanity_check_bf_dp(df):
    # Verifica discrepancias de satisfacción entre Fuerza Bruta y DP.
    piv = df.pivot_table(index="id_archivo", columns="algoritmo", values="satisfaccion")
    if "bf" in piv and "dp" in piv:
        mismatches = piv.dropna(subset=["bf", "dp"]).query("bf != dp")
        if not mismatches.empty:
            print(f"Advertencia: bf y dp difieren en {len(mismatches)} casos.")


def plot_quality_finput(df):
    # Analiza cómo las variables de entrada afectan la calidad heurística.
    _sanity_check_bf_dp(df)

    heur = (
        df[df["algoritmo"].isin(["gh1", "gh2"])].dropna(subset=["calidad_pct"]).copy()
    )
    if heur.empty:
        return

    variables = [
        ("n_animes", "N animes"),
        ("total_capitulos", "Total capítulos"),
        ("minutos_m", "Minutos disponibles"),
        ("energia_e", "Energía disponible"),
    ]

    fig, axes = plt.subplots(2, 4, figsize=(16, 6.5), sharey=True)

    for col_idx, (var, label) in enumerate(variables):
        for row_idx, alg in enumerate(["gh1", "gh2"]):
            ax = axes[row_idx, col_idx]
            subset = heur[heur["algoritmo"] == alg]
            ax.scatter(
                subset[var],
                subset["calidad_pct"],
                color=PALETTE[alg],
                alpha=0.7,
                s=45,
                edgecolor="white",
            )
            ax.axhline(100, color="black", ls="--", alpha=0.5)
            ax.set(xlabel=label, ylim=(0, 110))
            if col_idx == 0:
                ax.set_ylabel(f"{ALG_LABELS[alg]}\n% del óptimo")

            if len(subset) >= 3 and subset[var].nunique() > 1:
                r_p, p_p = pearsonr(subset[var], subset["calidad_pct"])
                r_s, p_s = spearmanr(subset[var], subset["calidad_pct"])
                sig_p = "*" if p_p < 0.05 else ""
                sig_s = "*" if p_s < 0.05 else ""
                text = f"Pearson r={r_p:.2f}{sig_p}\nSpearman ρ={r_s:.2f}{sig_s}"
            else:
                text = "N insuficiente"

            ax.text(
                0.97, 0.05, text,
                transform=ax.transAxes,
                ha="right", va="bottom",
                fontsize=8,
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="lightgray"),
            )



    fig.suptitle("Impacto de variables en la calidad heurística", y=1.02)
    fig.tight_layout()
    _save(fig, "calidad_inputs.png")


def plot_quality_greedys(df):
    piv = df.pivot_table(
        index=["id_archivo", "n_animes"], columns="algoritmo", values="calidad_pct"
    ).reset_index()
    if "gh1" not in piv or "gh2" not in piv:
        return

    piv = piv.dropna(subset=["gh1", "gh2"])
    if piv.empty:
        return

    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    sc = ax.scatter(
        piv["gh1"],
        piv["gh2"],
        c=piv["n_animes"],
        cmap="viridis",
        s=65,
        edgecolor="white",
    )

    lims = [0, 110]
    ax.plot(lims, lims, "k--", alpha=0.5, label="Empate")
    ax.set(
        xlim=lims,
        ylim=lims,
        xlabel=f"Calidad {ALG_LABELS['gh1']} (%)",
        ylabel=f"Calidad {ALG_LABELS['gh2']} (%)",
        title="Greedy ratio vs Greedy max",
        aspect="equal",
    )

    fig.colorbar(sc, ax=ax, shrink=0.75).set_label("N animes")
    ax.legend(loc="lower right")
    fig.tight_layout()
    _save(fig, "calidad_greedys.png")


def plot_quality_distribution(df):
    # Distribución estadística de la calidad heurística.
    heur = df[df["algoritmo"].isin(["gh1", "gh2"])].dropna(subset=["calidad_pct"])
    if heur.empty:
        return

    fig, ax = plt.subplots(figsize=(6.5, 5))
    sns.boxplot(
        data=heur,
        x="algoritmo",
        y="calidad_pct",
        order=["gh1", "gh2"],
        hue="algoritmo",
        palette=PALETTE,
        legend=False,
        ax=ax,
        fliersize=0,
        width=0.5,
    )
    sns.stripplot(
        data=heur,
        x="algoritmo",
        y="calidad_pct",
        order=["gh1", "gh2"],
        color="black",
        alpha=0.5,
        size=4,
        ax=ax,
    )

    ax.axhline(100, color="green", ls="--", alpha=0.6, label="Óptimo")
    ax.set(
        title="Distribución de calidad",
        xlabel="",
        ylabel="Satisfacción (% del óptimo)",
        xticks=[0, 1],
    )
    ax.set_xticklabels([ALG_LABELS["gh1"], ALG_LABELS["gh2"]])
    ax.legend()
    fig.tight_layout()
    _save(fig, "distribucion.png")


def plot_behavior(df):
    # Relación entre satisfacción total y variables de entrada.
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    variables = [
        ("n_animes", "N animes"),
        ("total_capitulos", "Total de capítulos"),
        ("minutos_m", "Minutos disponibles"),
        ("energia_e", "Energía disponible"),
    ]

    for ax, (col, label) in zip(axes.flat, variables):
        sns.scatterplot(
            data=df,
            x=col,
            y="satisfaccion",
            hue="algoritmo",
            style="algoritmo",
            hue_order=ALG_ORDER,
            palette=PALETTE,
            markers=MARKERS,
            alpha=0.8,
            s=55,
            ax=ax,
            legend=(col == "n_animes"),
        )
        ax.set(
            title=f"Satisfacción vs {label}", xlabel=label, ylabel="Satisfacción total"
        )

    fig.suptitle("Comportamiento de la satisfacción", y=1.01)
    fig.tight_layout()
    _save(fig, "comportamiento_recursos.png")


def plot_complexity_empirical(df):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    dp = df[df["algoritmo"] == "dp"].copy()
    dp["trabajo"] = dp["minutos_m"] * dp["energia_e"] * dp["total_capitulos"]

    sns.scatterplot(
        data=dp, x="trabajo", y="tiempo_ns", color=PALETTE["dp"], s=60, ax=axes[0]
    )

    x = np.log10(dp["trabajo"].replace(0, np.nan))
    y = np.log10(dp["tiempo_ns"].replace(0, np.nan))
    m = np.isfinite(x) & np.isfinite(y)

    if m.sum() >= 2:
        slope, b = np.polyfit(x[m], y[m], 1)
        xs = np.linspace(x[m].min(), x[m].max(), 50)
        axes[0].plot(
            10**xs, 10 ** (b + slope * xs), "k--", label=f"Pendiente ≈ {slope:.2f}"
        )
        axes[0].legend()

    axes[0].set(
        xscale="log",
        yscale="log",
        title="DP: Complejidad Empírica",
        xlabel="Trabajo (M*E*Caps)",
        ylabel="Tiempo (ns)",
    )

    bf = df[df["algoritmo"] == "bf"]
    sns.scatterplot(
        data=bf, x="n_animes", y="tiempo_ns", color=PALETTE["bf"], s=60, ax=axes[1]
    )
    axes[1].set(
        yscale="log",
        title="Fuerza Bruta: Complejidad Empírica",
        xlabel="N animes",
        ylabel="Tiempo (ns, log)",
    )

    fig.tight_layout()
    _save(fig, "complejidad_empirica.png")


def plot_tradeoff(df):
    d = df.dropna(subset=["calidad_pct"])
    if d.empty:
        return

    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    sns.scatterplot(
        data=d,
        x="tiempo_ns",
        y="calidad_pct",
        hue="algoritmo",
        style="algoritmo",
        hue_order=ALG_ORDER,
        palette=PALETTE,
        markers=MARKERS,
        s=80,
        alpha=0.85,
        ax=ax,
    )

    ax.axhline(100, color="black", ls="--", alpha=0.5)
    ax.set(
        xscale="log",
        ylim=(0, 110),
        title="Calidad vs Tiempo",
        xlabel="Tiempo (ns, log)",
        ylabel="Satisfacción (%)",
    )

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        [ALG_LABELS.get(l, l) for l in labels],
        loc="lower right",
        title="Algoritmo",
    )
    fig.tight_layout()
    _save(fig, "tradeoff_calidad_tiempo.png")


def plot_winrate(df):
    piv = df.pivot_table(index="id_archivo", columns="algoritmo", values="satisfaccion")
    if not {"gh1", "gh2"}.issubset(set(piv.columns)):
        return

    piv = piv.dropna(subset=["gh1", "gh2"])
    counts = {
        "Greedy ratio >": int((piv["gh1"] > piv["gh2"]).sum()),
        "Empate": int((piv["gh1"] == piv["gh2"]).sum()),
        "Greedy max >": int((piv["gh1"] < piv["gh2"]).sum()),
    }

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.bar(
        list(counts.keys()),
        list(counts.values()),
        color=[PALETTE["gh1"], "#999999", PALETTE["gh2"]],
        edgecolor="black",
    )

    for i, v in enumerate(counts.values()):
        ax.text(i, v, str(v), ha="center", va="bottom")

    ax.set(title="Entre heurísticas", ylabel="Nº de casos")
    fig.tight_layout()
    _save(fig, "greedy_winrate.png")


def main():
    if not os.path.exists(MEASUREMENTS_CSV):
        print(f"archivo {MEASUREMENTS_CSV} no encontrado.")
        return

    df = load_and_prepare(MEASUREMENTS_CSV)

    plot_time_algorithms(df)
    plot_time_scale(df)
    plot_memory_algorithms(df)
    plot_quality_finput(df)
    plot_quality_greedys(df)
    plot_quality_distribution(df)
    plot_behavior(df)
    plot_complexity_empirical(df)
    plot_tradeoff(df)
    plot_winrate(df)

    print(f"Gráficos generados - {PLOTS_DIR}")


if __name__ == "__main__":
    main()
