
from pathlib import Path
import pandas as pd
import csv
from time import time


DOWNLOAD_DIRECTORY = Path('src', 'data', 'downloaded')
DIRECTORY = Path('src', 'data', 'raw')


def split_csv_file(file):

    print(f'Start splitting file {file}')
    start = time()

    i = 1

    for chunk in pd.read_table(
        file,
        sep='\t',
        chunksize=50000,
        usecols=[1, 2],
        error_bad_lines=False,
        lineterminator='\n',
        encoding='ISO-8859-1',
        quoting=csv.QUOTE_NONE,
        header=0,
        names=['ID', 'DESCRIPTION'],
    ):
        start_chunk = time()
        # Drop all NaNs
        chunk.ID = pd.to_numeric(chunk.ID, downcast='integer', errors='coerce')
        chunk.dropna(inplace=True)
        chunk.ID = chunk.ID.astype('int64')

        chunk.to_parquet(DIRECTORY / (file.stem[:-4] + f'_{i}.parquet'))

        temp = time()

        print(
            f'Finished chunk {i} of file {file} in {temp - start_chunk} '
            'seconds.'
        )

        i += 1

    end = time()

    print(f'Finished file {file} in {end - start} seconds')


def main():
    files = DOWNLOAD_DIRECTORY.glob('detail_desc_text_*.tsv.zip')

    print('Start splitting files')

    for file in files:
        split_csv_file(file)

    print('Process finished')


if __name__ == '__main__':
    main()
