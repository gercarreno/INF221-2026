import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from pathlib import Path

BASE_DIR = Path('data')
MEASUREMENTS_DIR = BASE_DIR / 'measurements'
ALGORITHMS = ['sort', 'merge', 'quick']
PLOTS_DIR = BASE_DIR / 'plots'

# Usamos una paleta apta para daltonismo (muy valorado en papers científicos)
PALETTE = sns.color_palette("colorblind", n_colors=len(ALGORITHMS))

def setup_paper_style():
    # Usar estilo base de seaborn limpio
    sns.set_theme(style="ticks", context="paper")
    
    # Configuraciones globales de matplotlib
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Computer Modern Roman", "DejaVu Serif"],
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "legend.title_fontsize": 9,
        "lines.linewidth": 1.5,
        "lines.markersize": 4,
        "grid.alpha": 0.5,
        "grid.linestyle": "--",
        "grid.color": "#CCCCCC"
    })

def load_and_combine_data(directory: Path) -> pd.DataFrame:
    """Carga y combina todos los archivos CSV desde el directorio especificado."""
    all_files = list(directory.glob('*.csv'))
    if not all_files:
        print(f" No se encontraron archivos CSV en '{directory}'.")
        return pd.DataFrame()

    df_list = []
    for file in all_files:
        try:
            df = pd.read_csv(file)
            df['data_type'] = df['input_file'].apply(
                lambda x: re.search(r'(\d+)_(aleatorio|ascendente|descendente)', x).group(2)
            )
            df_list.append(df)
        except Exception as e:
            print(f" Error al procesar {file.name}: {e}")

    if not df_list:
        print(" No se pudo cargar ningún archivo correctamente.")
        return pd.DataFrame()

    return pd.concat(df_list, ignore_index=True)


def create_plots(df: pd.DataFrame) -> None:
    """Genera todos los gráficos de rendimiento y memoria."""
    if df.empty:
        print(" DataFrame vacío. No se generarán gráficos.")
        return

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Tiempo vs N
    for data_type in df['data_type'].unique():
        print(f" Generando gráfico de tiempo para datos '{data_type}'...")
        plt.figure(figsize=(3.5, 2.8))

        subset_df = df[df['data_type'] == data_type]
        plot_df = subset_df.groupby(['algorithm', 'n_elems'])['time_ns'].mean().reset_index()

        ax = sns.lineplot(
            data=plot_df,
            x='n_elems',
            y='time_ns',
            hue='algorithm',
            style='algorithm',
            markers=True,
            dashes=True, 
            hue_order=ALGORITHMS,
            style_order=ALGORITHMS,
            palette=PALETTE
        )

        ax.set_xscale('log')
        ax.set_yscale('log')
        
        ax.set_xlabel('Cantidad de Elementos ($N$)')
        ax.set_ylabel('Tiempo Promedio (ns)')
        ax.grid(True, which="major", ls="--", lw=0.5)
        
        sns.despine()

        ax.legend(title='Algoritmo', loc='upper left', frameon=True, fancybox=False, edgecolor='k')

        plt.tight_layout()
        output_file = PLOTS_DIR / f'tiempo_vs_n_{data_type}.pdf'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Guardado: {output_file}")

    # 2. Uso de Memoria vs N (Comparando Tipos de Datos)
    print(" Generando gráfico de memoria comparando tipos de datos...")
    mem_df = df[df['n_elems'] <= 100000].copy()
    
    mem_df = (
        mem_df.groupby(['algorithm', 'n_elems', 'data_type'])['peak_kb']
        .mean()
        .reset_index()
    )

   
    plt.figure(figsize=(7.0, 3.0))
    ax = sns.lineplot(
        data=mem_df,
        x='n_elems',
        y='peak_kb',
        hue='algorithm',      
        style='data_type',    
        markers=True,
        dashes=True,
        hue_order=ALGORITHMS,
        palette=PALETTE
    )

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Cantidad de Elementos ($N$)')
    ax.set_ylabel('Memoria Promedio (KB)')
    ax.grid(True, which="major", ls="--", lw=0.5)
    sns.despine()
    
   
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title='Leyenda', bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)

    plt.tight_layout()
    output_file = PLOTS_DIR / 'memoria_vs_n_comparativo.pdf'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Guardado: {output_file}")

    # 3. Comparativa de tiempo para N = 100000
    large_n = 100000
    print(f" Generando gráfico de barras para N = {large_n}...")

    bar_df = df[df['n_elems'] == large_n].groupby(['algorithm', 'data_type'])['time_ns'].mean().reset_index()

    plt.figure(figsize=(3.5, 2.8))
    ax = sns.barplot(
        data=bar_df,
        x='algorithm',
        y='time_ns',
        hue='data_type',
        order=ALGORITHMS,
        palette="Greys" 
    )

    ax.set_yscale('log')
    ax.set_xlabel('Algoritmo')
    ax.set_ylabel('Tiempo Promedio (ns)')
    ax.grid(True, axis='y', ls="--", lw=0.5)
    sns.despine()
    
    ax.legend(title='Distribución', fontsize=7, title_fontsize=8)
    plt.xticks(rotation=45, ha='right') # Acomodar etiquetas del eje X

    plt.tight_layout()
    output_file = PLOTS_DIR / f'comparativa_tiempo_n{large_n}.pdf'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f" Guardado: {output_file}")


def main():
    setup_paper_style()
    print(" Iniciando generador de gráficos para algoritmos de ordenamiento...")
    df = load_and_combine_data(MEASUREMENTS_DIR)

    if not df.empty:
        create_plots(df)
        print("Proceso de generación de gráficos finalizado con éxito.")
    else:
        print("El script terminó sin generar gráficos por falta de datos válidos.")


if __name__ == '__main__':
    main()