import pandas as pd
from bld.project_paths import project_paths_join as ppj
import matplotlib.pyplot as plt


def plot_distribution_of_patents(df):
    x = df.YEAR.unique()
    y = df.groupby('YEAR').PATENTNR.count().values

    fig, ax = plt.subplots()

    ax.bar(x, y)

    ax.set_xticks(range(1975, 2016, 5))

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Patents')

    plt.savefig(ppj('OUT_FIGURES', 'fig_patents_distribution.png'))


def plot_distribution_of_patents_software_vs_non_software(df):
    x = df.YEAR.unique()
    y_1 = (
        df.loc[df.CLASSIFICATION_REPLICATION == 'Non-Software']
        .groupby('YEAR')
        .PATENTNR.count()
        .values
    )
    y_2 = (
        df.loc[df.CLASSIFICATION_REPLICATION == 'Software']
        .groupby('YEAR')
        .PATENTNR.count()
        .values
    )

    fig, ax = plt.subplots()

    ax.bar(x, y_1, label='Non-Software')
    ax.bar(x, y_2, label='Software')

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Patents')

    ax.legend()

    plt.savefig(ppj('OUT_FIGURES', 'fig_patents_distribution_vs.png'))


def plot_distribution_of_patents_software_vs_non_software_shares(df):
    x = df.YEAR.unique()
    y_1 = (
        df.loc[df.CLASSIFICATION_REPLICATION == 'Non-Software']
        .groupby('YEAR')
        .PATENTNR.count()
        .values
    )
    y_2 = (
        df.loc[df.CLASSIFICATION_REPLICATION == 'Software']
        .groupby('YEAR')
        .PATENTNR.count()
        .values
    )

    y_1, y_2 = y_1 / (y_1 + y_2), y_2 / (y_1 + y_2)

    fig, ax = plt.subplots()

    ax.bar(x, y_1, label='Non-Software')
    ax.bar(x, y_2, label='Software')

    ax.set_xlabel('Year')
    ax.set_ylabel('Share of Patents')

    ax.legend()

    plt.savefig(ppj('OUT_FIGURES', 'fig_patents_distribution_vs_shares.png'))


if __name__ == '__main__':
    df = pd.read_pickle(
        ppj('OUT_ANALYSIS', 'patents_classified_with_bh2007.pkl')
    )

    plot_distribution_of_patents(df)

    plot_distribution_of_patents_software_vs_non_software(df)

    plot_distribution_of_patents_software_vs_non_software_shares(df)
