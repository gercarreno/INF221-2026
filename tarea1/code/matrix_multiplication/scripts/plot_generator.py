import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.axes import Axes
import seaborn as sns
import glob
from pathlib import Path
from typing import List
from matplotlib.ticker import FuncFormatter

BASE_DIR = Path('data')
MEASUREMENTS_DIR = BASE_DIR / 'measurements'
PLOTS_DIR = BASE_DIR / 'plots'
ALGORITHMS = ['naive', 'strassen']

def setup_scientific_style():
    """Configura matplotlib para estilo de paper científico (ACM/IEEE)."""
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Computer Modern Roman", "DejaVu Serif"],
        "axes.labelsize": 10,       
        "font.size": 10,            
        "legend.fontsize": 8,       
        "xtick.labelsize": 8,       
        "ytick.labelsize": 8,
        "figure.dpi": 300,
        "lines.linewidth": 1.5,
        "lines.markersize": 5,
        "axes.grid": True,          
        "grid.alpha": 0.4,
        "grid.linestyle": "--",
        "grid.color": "#cccccc",
        "pdf.fonttype": 42,         
        "ps.fonttype": 42
    })
    sns.set_palette("colorblind")


def load_data(path_pattern: str) -> pd.DataFrame:
    files = glob.glob(path_pattern)
    if not files:
        print(f"Advertencia: No se encontraron archivos en '{path_pattern}'.")
        return pd.DataFrame()

    dataframes: List[pd.DataFrame] = []
    for file in files:
        try:
            df = pd.read_csv(file)
            df['n_dim'] = df['mat1_dims'].str.extract(r'(\d+)x').astype(int)
            
            nombres_archivos = df['output_file'].apply(lambda x: Path(x).name)
            df['data_type'] = nombres_archivos.str.extract(r'^\d+_([a-zA-Z]+)_')
            
            dataframes.append(df)
        except Exception as e:
            print(f"Error procesando {file}: {e}")

    if not dataframes:
        return pd.DataFrame()

    return pd.concat(dataframes, ignore_index=True)


def _format_pow2_label(val: float) -> str:
    if val <= 0 or not np.isfinite(val):
        return ""
    k = int(round(np.log2(val)))
    if np.isclose(val, 2 ** k):
        return rf"$2^{{{k}}}$"
    return ""


def _apply_pow2_xticks(ax: Axes, x_values: pd.Series) -> None:
    unique_n = sorted(set(int(n) for n in x_values if n > 0))
    if not unique_n:
        return
    try:
        ax.set_xscale('log', base=2) 
    except TypeError:
        ax.set_xscale('log', basex=2) 

    ax.set_xticks(unique_n)
    ax.get_xaxis().set_major_formatter(FuncFormatter(lambda v, pos: _format_pow2_label(v)))
    ax.set_xlim(min(unique_n), max(unique_n))


def generate_plots(df: pd.DataFrame) -> None:
    if df.empty:
        print("DataFrame vacío. No se generarán gráficos.")
        return

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    plot_df = df[df['data_type'] == 'densa']
    if plot_df.empty:
        print("No se encontraron datos de tipo 'densa'. Usando todos los datos.")
        plot_df = df

    grouped_df = plot_df.groupby(['algorithm', 'n_dim'], as_index=False).agg(
        avg_time_ns=('time_ns', 'mean'),
        avg_peak_kb=('peak_kb', 'mean')
    )

    # 1. Tiempo vs Dimensión 
    plt.figure(figsize=(3.5, 2.6))
    ax = sns.lineplot(
        data=plot_df,             
        x='n_dim', y='time_ns',   
        hue='algorithm', style='algorithm',
        markers=["o", "s"], dashes=True,
        hue_order=ALGORITHMS, style_order=ALGORITHMS,
        errorbar=None 
    )
    
    _apply_pow2_xticks(ax, plot_df['n_dim'])
    ax.set_yscale('log')
    ax.set_xlabel('Dimensión de la Matriz ($N$)')
    ax.set_ylabel('Tiempo Promedio (ns)') 
    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title=None, frameon=True, loc='best')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'tiempo_vs_dimension.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("Gráfico 'tiempo_vs_dimension.pdf' generado.")

    # 2. Memoria vs Dimensión 
    plt.figure(figsize=(3.5, 2.6))
    ax = sns.lineplot(
        data=plot_df,             
        x='n_dim', y='peak_kb',   
        hue='algorithm', style='algorithm',
        markers=["o", "s"], dashes=True,
        hue_order=ALGORITHMS, style_order=ALGORITHMS,
        errorbar=None 
    )
    
    _apply_pow2_xticks(ax, plot_df['n_dim']) 
    ax.set_yscale('log')
    ax.set_xlabel('Dimensión de la Matriz ($N$)')
    ax.set_ylabel('Memoria Promedio (KB)') 
    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title=None, frameon=True, loc='best')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'memoria_vs_dimension.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("Gráfico 'memoria_vs_dimension.pdf' generado.")

    # 3. Comparativa para mayor N 
    if not grouped_df.empty:
        largest_n = int(grouped_df['n_dim'].max())
        bar_df = grouped_df[grouped_df['n_dim'] == largest_n].copy()

       
        fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))
        sns.barplot(
            data=bar_df, x='algorithm', y='avg_time_ns',
            hue='algorithm', order=ALGORITHMS, edgecolor='black', linewidth=0.8, ax=axes[0], legend=False
        )
        axes[0].set_ylabel('Tiempo Promedio (ns)')
        axes[0].set_xlabel('Algoritmo')
        for c in axes[0].containers:
            axes[0].bar_label(c, fmt='%.0f', padding=3, fontsize=8)

        # Memoria (KB)
        sns.barplot(
            data=bar_df, x='algorithm', y='avg_peak_kb',
            hue='algorithm', order=ALGORITHMS, edgecolor='black', linewidth=0.8, ax=axes[1], legend=False
        )
        axes[1].set_ylabel('Memoria Promedio (KB)')
        axes[1].set_xlabel('Algoritmo')
        for c in axes[1].containers:
            axes[1].bar_label(c, fmt='%.0f', padding=3, fontsize=8)

        plt.tight_layout()
        plt.savefig(PLOTS_DIR / f'comparativa_n_{largest_n}.pdf', format='pdf', bbox_inches='tight')
        plt.close()
        print(f"Gráfico 'comparativa_n_{largest_n}.pdf' generado.")


def main() -> None:
    setup_scientific_style()
    print("Iniciando generación de gráficos...")
    df = load_data(str(MEASUREMENTS_DIR / '*.csv'))
    generate_plots(df)
    print("Proceso finalizado.")

if __name__ == '__main__':
    main()