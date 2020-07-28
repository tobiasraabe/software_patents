import matplotlib.pyplot as plt
import pandas as pd

from bld.project_paths import project_paths_join as ppj
from src.figures.auxiliaries import format_thousands_with_comma


def plot_distribution_of_patents(df):
    fig, ax = plt.subplots()

    x = list(range(1976, 2019))
    y = df.groupby(df.DATE.dt.year).ID.count().values

    ax.bar(x, y)

    ax.set_xticks(range(1975, 2019, 5))

    ax.set_ylim(0, 330_000)

    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(format_thousands_with_comma)
    )

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Patents')

    ax.legend(labels=['Utility Patents'], title='Patent Type')

    ax.grid(axis='y', linestyle='--', color='grey')

    plt.tight_layout()

    plt.savefig(ppj('OUT_FIGURES', 'fig-patents-distribution.png'))
    plt.close()


def plot_distribution_of_patents_software_vs_non_software(df):
    fig, ax = plt.subplots()

    x = list(range(1976, 2019))
    y = (
        df.groupby([df.DATE.dt.year, df.CLASSIFICATION_REPLICATION])
        .ID.count()
        .unstack()
        .values.T
    )

    ax.bar(x, y[0])
    ax.bar(x, y[1])

    ax.set_xticks(range(1975, 2019, 5))

    ax.set_ylim(0, 330_000)

    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(format_thousands_with_comma)
    )

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Patents')

    ax.legend(labels=['Non-Software', 'Software'], title='Patent Type')

    ax.grid(axis='y', linestyle='--', color='grey')

    plt.tight_layout()

    plt.savefig(ppj('OUT_FIGURES', 'fig-patents-distribution-vs.png'))
    plt.close()


def plot_distribution_of_patents_software_vs_non_software_shares(df):
    fig, ax = plt.subplots()

    x = list(range(1976, 2019))
    y = (
        df.groupby([df.DATE.dt.year, df.CLASSIFICATION_REPLICATION])
        .ID.count()
        .unstack()
        .apply(lambda x: x / x.sum(), axis=1)
        .values.T
    )

    ax.bar(x, y[0])
    ax.bar(x, y[1])

    ax.set_xticks(range(1975, 2019, 5))

    ax.set_xlabel('Year')
    ax.set_ylabel('Share of Patents')

    ax.legend(labels=['Non-Software', 'Software'], title='Patent Type')

    ax.grid(axis='y', linestyle='--', color='grey')

    plt.tight_layout()

    plt.savefig(ppj('OUT_FIGURES', 'fig-patents-distribution-vs-shares.png'))
    plt.close()


def main():
    # Prepare data by merging the publication date to classified patents
    bh = pd.read_pickle(ppj('OUT_ANALYSIS', 'bh_with_patent_db.pkl'))
    date = pd.read_pickle(ppj('OUT_DATA', 'patent.pkl'))
    df = bh.merge(date, on='ID', how='inner', validate='1:1')

    plot_distribution_of_patents(df)

    plot_distribution_of_patents_software_vs_non_software(df)

    plot_distribution_of_patents_software_vs_non_software_shares(df)


if __name__ == '__main__':
    main()
