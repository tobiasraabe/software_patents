import pandas as pd

from sklearn.metrics import confusion_matrix

from bld.project_paths import project_paths_join as ppj

TABLE = """\\begin{tabular}{@{}cp{0.5cm}cp{0.5cm}c@{}}
\t\\toprule
\t& &  Relevant & & Not Relevant \\\\ \\cline{1-1} \\cline{2-2} \\cline{3-3}
\tRetrieved & & TP & & FP \\\\
\tNot Retrieved & & FN & & TN \\\\
\t\\bottomrule
\\end{tabular}
"""

TABLE_WITH_INFO = """\\begin{tabular}{@{}cp{0.5cm}cp{0.5cm}c@{}}
\t\\toprule
\t& & Relevant & & Not Relevant \\\\ \\cline{1-1} \\cline{3-3} \\cline{5-5}
\tRetrieved & & TP (true-positive) & & FP (false-positive) \\\\
\tNot Retrieved & & FN (false-negative) & & TN (true-negative) \\\\
\t\\bottomrule
\\end{tabular}
"""


def create_confusion_matrix(actual_class, predicted_class, suffix):
    (tp, fn), (fp, tn) = confusion_matrix(
        actual_class, predicted_class, labels=['Software', 'Non-Software']
    )

    table = (
        TABLE_WITH_INFO.replace('TP', str(tp))
        .replace('FN', str(fn))
        .replace('FP', str(fp))
        .replace('TN', str(tn))
    )

    with open(ppj('OUT_TABLES', f'tab-cf-{suffix}.tex'), 'w') as file:
        file.write(table)


def create_confusion_matrix_with_info(actual_class, predicted_class, suffix):
    (tp, fn), (fp, tn) = confusion_matrix(
        actual_class, predicted_class, labels=['Software', 'Non-Software']
    )

    table = (
        TABLE.replace('TP', str(tp))
        .replace('FN', str(fn))
        .replace('FP', str(fp))
        .replace('TN', str(tn))
    )

    with open(ppj('OUT_TABLES', f'tab-cf-{suffix}.tex'), 'w') as file:
        file.write(table)


def main():
    df = pd.read_pickle(
        ppj('OUT_ANALYSIS', 'replication_bh_with_crawled_text.pkl')
    )

    create_confusion_matrix(
        df.CLASSIFICATION_MANUAL, df.CLASSIFICATION_ALGORITHM, 'bh2007'
    )
    create_confusion_matrix_with_info(
        df.CLASSIFICATION_MANUAL,
        df.CLASSIFICATION_REPLICATION,
        'replication-bh-with-crawled-text',
    )

    temp = pd.read_pickle(
        ppj('OUT_ANALYSIS', 'replication_bh_with_patent_db.pkl')
    )

    df = df[['ID', 'CLASSIFICATION_MANUAL']].merge(
        temp[['ID', 'CLASSIFICATION_REPLICATION']], on='ID', how='left'
    )

    create_confusion_matrix(
        df.CLASSIFICATION_MANUAL,
        df.CLASSIFICATION_REPLICATION,
        'replication-bh-with-patent-db',
    )


if __name__ == '__main__':
    main()
