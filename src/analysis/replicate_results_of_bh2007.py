import pandas as pd

from bld.project_paths import project_paths_join as ppj


def main():
    for file_in, file_out in [
        ('bh_with_crawled_text.pkl', 'replication_bh_with_crawled_text.pkl'),
        ('bh_with_patent_db.pkl', 'replication_bh_with_patent_db.pkl'),
    ]:
        bh = pd.read_pickle(ppj('OUT_DATA', 'bh.pkl'))
        replication = pd.read_pickle(ppj('OUT_ANALYSIS', file_in))

        bh = bh.merge(replication, on='ID', how='inner', validate='1:1')

        bh.to_pickle(ppj('OUT_ANALYSIS', file_out))


if __name__ == '__main__':
    main()
