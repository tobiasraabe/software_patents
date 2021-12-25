import matplotlib.pyplot as plt
import pandas as pd
import pytask

from src.config import BLD
from src.figures.auxiliaries import format_thousands_with_comma


def plot_distribution_of_patents(df, path):
    fig, ax = plt.subplots()

    x = list(range(1976, 2019))
    y = df.groupby(df.DATE.dt.year).ID.count().values

    ax.bar(x, y)

    ax.set_xticks(range(1975, 2019, 5))

    ax.set_ylim(0, 330_000)

    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_thousands_with_comma))

    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Patents")

    ax.legend(labels=["Utility Patents"], title="Patent Type")

    ax.grid(axis="y", linestyle="--", color="grey")

    plt.tight_layout()

    plt.savefig(path)
    plt.close()


def plot_distribution_of_patents_software_vs_non_software(df, path):
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

    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_thousands_with_comma))

    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Patents")

    ax.legend(labels=["Non-Software", "Software"], title="Patent Type")

    ax.grid(axis="y", linestyle="--", color="grey")

    plt.tight_layout()

    plt.savefig(path)
    plt.close()


def plot_distribution_of_patents_software_vs_non_software_shares(df, path):
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

    ax.set_xlabel("Year")
    ax.set_ylabel("Share of Patents")

    ax.legend(labels=["Non-Software", "Software"], title="Patent Type")

    ax.grid(axis="y", linestyle="--", color="grey")

    plt.tight_layout()

    plt.savefig(path)
    plt.close()


@pytask.mark.depends_on(
    {
        "bh_with_patent_db": BLD / "analysis" / "bh_with_patent_db.pkl",
        "patent": BLD / "data" / "patent.pkl",
    }
)
@pytask.mark.produces(
    {
        "dist": BLD / "figures" / "fig-patents-distribution.pdf",
        "dist_vs": BLD / "figures" / "fig-patents-distribution-vs.pdf",
        "dist_vs_shares": BLD / "figures" / "fig-patents-distribution-vs-shares.pdf",
    }
)
def task_visualize_distributions(depends_on, produces):
    # Prepare data by merging the publication date to classified patents
    bh = pd.read_pickle(depends_on["bh_with_patent_db"])
    date = pd.read_pickle(depends_on["patent"])
    df = bh.merge(date, on="ID", how="inner", validate="1:1")

    plot_distribution_of_patents(df, produces["dist"])

    plot_distribution_of_patents_software_vs_non_software(df, produces["dist_vs"])

    plot_distribution_of_patents_software_vs_non_software_shares(
        df, produces["dist_vs_shares"]
    )
