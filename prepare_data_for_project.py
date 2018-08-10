import csv
import hashlib

from pathlib import Path
from time import time
from typing import Dict, List

import click
import pandas as pd
import requests

from tqdm import tqdm

CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}

PV_LAST_UPDATE = '20180528'
"""str: Date of newest data release."""
PV_DOWNLOAD_LINK = (
    f'http://s3.amazonaws.com/data-patentsview-org/{PV_LAST_UPDATE}/download'
)
"""str: Base url for downloading data from PatentsView."""
DB_DOWNLOAD_LINK = 'http://dl.dropboxusercontent.com/s/'
"""str: Base url for downloading data from Dropbox."""


FILES_RAW: Dict[str, List[str]] = {
    'brf_sum_text.tsv.zip': [
        f'{PV_DOWNLOAD_LINK}/brf_sum_text.tsv.zip',
        'bd3e6e8e7ee7034a3734d35086bc50afbeabe13da45a41b2ec855f013cea7de2',
    ],
    'detail_desc_text_1.tsv.zip': [
        f'{PV_DOWNLOAD_LINK}/detail_desc_text_1.tsv.zip',
        'f2b3de3fb01690c2c0d1407f195530b6b95a6f0d9e20be903683697d82587fef',
    ],
    'detail_desc_text_2.tsv.zip': [
        f'{PV_DOWNLOAD_LINK}/detail_desc_text_2.tsv.zip',
        '2850812c89df4d8d7830ad5e1ef30b0913fc889fc00ce3c4ce09436541e3076e',
    ],
    'detail_desc_text_3.tsv.zip': [
        f'{PV_DOWNLOAD_LINK}/detail_desc_text_3.tsv.zip',
        '5d1a2977843e13adc6b85d268f16cf9bc688c9f60a5ca203bae1048a3cefc35a',
    ],
    'detail_desc_text_4.tsv.zip': [
        f'{PV_DOWNLOAD_LINK}/detail_desc_text_4.tsv.zip',
        '85240f465d4213c9afb38218f6046544cc9a16ec5840717bf6ecff9b20647d24',
    ],
    'detail_desc_text_5.tsv.zip': [
        f'{PV_DOWNLOAD_LINK}/detail_desc_text_5.tsv.zip',
        '29562dab3c5b9d180c8e3c1761f06b32db0ffe82131d2847a481cced209d7b5c',
    ],
    'patent.tsv.zip': [
        f'{PV_DOWNLOAD_LINK}/patent.tsv.zip',
        'b2822a0749b01a373de0ac6e3073ea36310556990149854b82db608255cb67cb',
    ],
}
"""Dict[str, List[str]]: Contains file information for raw data.

The keys of the dictionary are the file names on the disk. The values are a
list containing urls in the first and file hashes in the second position.

The has can be computed in Powershell with ``Get-FileHash <file>``. Notice
that Powershell returns uppercase letters and Python lowercase.

"""


FILES_REPLICATION: Dict[str, List[str]] = {
    'indicators_abstract.pkl': [
        f'{DB_DOWNLOAD_LINK}ckleerbtm54ddpm/indicators_abstract.pkl?dl=0',
        '9b63982838f08f162af59019a3e68b33a3e87aaac97df637b98cf15d42530bcc',
    ],
    'indicators_description_1.pkl': [
        f'{DB_DOWNLOAD_LINK}tfhzex5o18ocugu/indicators_description_1.pkl?dl=0',
        '1ff8899dcb3843f46fd6f92b04a5112632d6e8e9a9f331bd4c84d7374133143f',
    ],
    'indicators_description_2.pkl': [
        f'{DB_DOWNLOAD_LINK}ayvvzdzr8kihx4e/indicators_description_2.pkl?dl=0',
        'a4a3cab87a1201fe74b1f85a8ae88c92f0e3fdbea5f7b55e6ef0b2aa99f6c93c',
    ],
    'indicators_description_3.pkl': [
        f'{DB_DOWNLOAD_LINK}frnos85yq97sps4/indicators_description_3.pkl?dl=0',
        'b408815666381c3d6f307eef92c21a3670caea2911431c078732c2d069fd2744',
    ],
    'indicators_description_4.pkl': [
        f'{DB_DOWNLOAD_LINK}hsswas2hgwvb8et/indicators_description_4.pkl?dl=0',
        '7f58681c7095b5b93e6449fed67f8baa7e160f3b8aeaaf589a111399fdb3e966',
    ],
    'indicators_description_5.pkl': [
        f'{DB_DOWNLOAD_LINK}42but1qhjil1trg/indicators_description_5.pkl?dl=0',
        '7ca0c1092bf0c555fe1d065abdf20db10faa5dcd685eedb8896f66cbb0377157',
    ],
    'indicators_title.pkl': [
        f'{DB_DOWNLOAD_LINK}0fxqnvyhsljwprt/indicators_title.pkl?dl=0',
        '1dcedef7f60f2ad0a2b9b2b9124fb690ed88afec39e9d65967b1ca898f281b79',
    ],
    'patent.pkl': [
        f'{DB_DOWNLOAD_LINK}atu4974la2p8d5s/patent.pkl?dl=0',
        'a6ad32258040fa6bdf7abd583038ceec1adae6ab19f028c9a98ab3473fd9b6fd',
    ],
    'indicators_summary.pkl': [
        f'{DB_DOWNLOAD_LINK}8mffjyvintl757a/indicators_summary.pkl?dl=0',
        '280081912bee1676638572fe623954c2b42480e1616043fcb0f63f199f3b5244',
    ],
}
"""Dict[str, List[str]]: Contains file information for replication data.

The keys of the dictionary are the file names on the disk. The values are a
list containing urls in the first and file hashes in the second position.

The has can be computed in Powershell with ``Get-FileHash <file>``. Notice
that Powershell returns uppercase letters and Python lowercase.

"""


DOWNLOAD_FOLDER = Path('src', 'data', 'downloaded')
"""pathlib.Path: Points to the target directory of downloads."""
DATA_RAW_FOLDER = Path('src', 'data', 'raw')
"""pathlib.Path: Points to the target directory of raw files."""
DATA_PROCESSED_FOLDER = Path('src', 'data', 'processed')
"""pathlib.Path: Points to the target directory of processed files."""


PATENTSVIEW_MISSPELLINGS = {
    '\.degree\.': '°',
    '\.gt\.': '>',
    '\.lt\.': '<',
    '\.ltoreq\.': '≦',
    '\.gtoreq\.': '≧',
}


def check_for_existing_files_before_splitting(filename: str):
    # Detect if there are already files in the output folder
    out_files = DATA_RAW_FOLDER.glob(filename.split('.')[0] + '_*')
    num_out_files = len(list(out_files))

    if num_out_files > 0:
        if click.confirm(
            f'There are already {num_out_files} chunks of {filename} in '
            f'{DATA_RAW_FOLDER}. Do you want to overwrite them?',
            default=False,
        ):
            start_splitting = True
        else:
            start_splitting = False
    else:
        start_splitting = True

    return start_splitting


def downloader(file: Path, url: str, resume_byte_pos: int = None):
    """Download url in ``URLS[position]`` to disk with possible resumption.

    Parameters
    ----------
    file : str
        Path of file on disk
    url : str
        URL of file
    resume_byte_pos: int
        Position of byte from where to resume the download

    """
    # Get size of file
    r = requests.head(url)
    file_size = int(r.headers.get('content-length', 0))

    # Append information to resume download at specific byte position
    # to header
    resume_header = (
        {'Range': f'bytes={resume_byte_pos}-'} if resume_byte_pos else None
    )

    # Establish connection
    r = requests.get(url, stream=True, headers=resume_header)

    # Set configuration
    block_size = 1024
    initial_pos = resume_byte_pos if resume_byte_pos else 0
    mode = 'ab' if resume_byte_pos else 'wb'

    with open(file, mode) as f:
        with tqdm(
            total=file_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc=file.name,
            initial=initial_pos,
            ascii=True,
            miniters=1,
        ) as pbar:
            for chunk in r.iter_content(32 * block_size):
                f.write(chunk)
                pbar.update(len(chunk))


def download_file(filename: str, url: str):
    """Execute the correct download operation.

    Depending on the size of the file online and offline, resume the
    download if the file offline is smaller than online.

    Parameters
    ----------
    filename : str
        Name of file
    url : str
        URL of file

    """
    # Establish connection to header of file
    r = requests.head(url)

    # Get filesize of online and offline file
    file_size_online = int(r.headers.get('content-length', 0))
    # Set output path depending on raw or replication data
    file = (
        DOWNLOAD_FOLDER / filename
        if filename in FILES_RAW
        else DATA_PROCESSED_FOLDER / filename
    )

    if file.exists():
        file_size_offline = file.stat().st_size

        if file_size_online != file_size_offline:
            click.echo(f'File {file} is incomplete. Resume download.')
            downloader(file, url, file_size_offline)
        else:
            click.echo(f'File {file} is complete. Skip download.')
            pass
    else:
        click.echo(f'File {file} does not exist. Start download.')
        downloader(file, url)


def validate_file(filename: str, hash_value: str = None):
    """Validate a given file with its hash.

    The downloaded file is compared with a hash to validate the download
    procedure.

    Parameters
    ----------
    file_name : str
        Name of file
    hash_value : str
        Hash value of file

    """
    if not hash_value:
        click.echo(f'File {filename} has no hash.')
        return 0

    # Set output path depending on raw or replication data
    file = (
        DOWNLOAD_FOLDER / filename
        if filename in FILES_RAW
        else DATA_PROCESSED_FOLDER / filename
    )
    # Skip files which are not downloaded.
    if not file.exists():
        return 0

    sha = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            chunk = f.read(1000 * 1000)  # 1MB so that memory is not exhausted
            if not chunk:
                break
            sha.update(chunk)
    try:
        assert sha.hexdigest() == hash_value
    except AssertionError:
        click.echo(
            f'File {filename} is corrupt. '
            'Delete it manually and restart the program.'
        )
    else:
        click.echo(f'File {filename} is validated.')


def split_detail_desc_text(filename: str) -> None:
    """Split a given file in smaller chunks.

    Parameters
    ----------
    filename : str
        Name of file

    """
    start_splitting = check_for_existing_files_before_splitting(filename)

    if start_splitting:
        click.echo(f'Start splitting file {filename}')
        start = time()

        i = 1

        for chunk in pd.read_table(
            Path('src', 'data', 'downloaded', filename),
            sep='\t',
            chunksize=10000,
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
            chunk.ID = pd.to_numeric(
                chunk.ID, downcast='integer', errors='coerce'
            )
            chunk.dropna(inplace=True)
            chunk.ID = chunk.ID.astype('int64')

            chunk.to_parquet(
                DATA_RAW_FOLDER / (filename.split('.')[0] + f'_{i}.parquet')
            )

            temp = time()

            click.echo(
                f'Finished chunk {i} of file {filename} in '
                f'{temp - start_chunk} seconds.'
            )

            i += 1

        end = time()

        click.echo(f'Finished file {filename} in {end - start} seconds')
    else:
        click.echo(f'Skipped splitting of {filename}')


def split_patent(filename: str):
    """Split a given file in smaller chunks.

    Parameters
    ----------
    filename : str
        Name of file

    """
    start_splitting = check_for_existing_files_before_splitting(filename)

    if start_splitting:
        click.echo(f'Start splitting file {filename}')
        start = time()

        i = 1

        for chunk in pd.read_table(
            Path('src', 'data', 'downloaded', filename),
            sep='\t',
            chunksize=270000,
            usecols=[0, 1, 4, 5, 6, 7, 8],
            error_bad_lines=False,
            lineterminator='\n',
            encoding='ISO-8859-1',
            quoting=csv.QUOTE_NONE,
        ):
            start_chunk = time()

            # Only utility patents
            chunk = chunk.loc[chunk.type == 'utility'].copy()
            # Ensure that only patents are chosen
            chunk = chunk.loc[chunk.kind.isin(['A', 'B1', 'B2'])]

            # ID is numeric
            chunk['ID'] = pd.to_numeric(chunk.id, errors='coerce')
            # CLAIMS_NUMBER is numeric
            chunk['CLAIMS_NUMBER'] = pd.to_numeric(
                chunk.num_claims, errors='coerce'
            )
            # DATE is datetime
            chunk['DATE'] = pd.to_datetime(chunk.date)

            # Drop unnecessary columns
            chunk.drop(
                columns=['type', 'id', 'date', 'num_claims', 'kind'],
                inplace=True,
            )

            # Rename columns
            col_names = {'abstract': 'ABSTRACT', 'title': 'TITLE'}
            chunk = chunk.rename(columns=col_names)

            # Drop NaNs
            chunk.dropna(inplace=True)

            chunk.ID = chunk.ID.astype(int)

            if chunk.shape[0] == 0:
                continue

            # More efficient dtypes
            chunk.ID = pd.to_numeric(chunk.ID)
            chunk.CLAIMS_NUMBER = pd.to_numeric(chunk.CLAIMS_NUMBER)
            # Edits to text columns
            chunk.TITLE = chunk.TITLE.str.strip()
            chunk.ABSTRACT = chunk.ABSTRACT.str.strip()

            for column in ['TITLE', 'ABSTRACT']:
                for key, value in PATENTSVIEW_MISSPELLINGS.items():
                    chunk[column] = chunk[column].str.replace(key, value)

            chunk.to_parquet(
                DATA_RAW_FOLDER / (filename.split('.')[0] + f'_{i}.parquet')
            )

            temp = time()

            click.echo(
                f'Finished chunk {i} of file {filename} in '
                f'{temp - start_chunk} seconds.'
            )

            i += 1

        end = time()

        click.echo(f'Finished file {filename} in {end - start} seconds')
    else:
        click.echo(f'Skipped splitting of {filename}')


def split_brf_sum_text(filename: str):
    start_splitting = check_for_existing_files_before_splitting(filename)

    if start_splitting:
        click.echo(f'Start splitting file {filename}')
        start = time()

        i = 1

        for chunk in pd.read_table(
            Path('src', 'data', 'downloaded', filename),
            sep='\t',
            chunksize=30000,
            usecols=[1, 2],
            error_bad_lines=False,
            lineterminator='\n',
            encoding='ISO-8859-1',
            quoting=csv.QUOTE_NONE,
            header=0,
            names=['ID', 'SUMMARY'],
        ):
            start_chunk = time()
            # Drop all NaNs
            chunk.ID = pd.to_numeric(
                chunk.ID, downcast='integer', errors='coerce'
            )
            chunk.dropna(inplace=True)
            chunk.ID = chunk.ID.astype('int64')

            chunk.to_parquet(
                DATA_RAW_FOLDER / (filename.split('.')[0] + f'_{i}.parquet')
            )

            temp = time()

            click.echo(
                f'Finished chunk {i} of file {filename} in '
                f'{temp - start_chunk} seconds.'
            )

            i += 1

        end = time()

        click.echo(f'Finished file {filename} in {end - start} seconds')
    else:
        click.echo(f'Skipped splitting of {filename}')


@click.group(context_settings=CONTEXT_SETTINGS, chain=True)
def cli():
    """Program for preparing the data for the project.

    \b
    The program covers three steps:
    1. Downloading data.
    2. Validating the downloaded data with hash values.
    3. Splitting the data into reasonable chunks to meet machine requirements.

    To download and validate a file, add file name, url and hash to `FILES_RAW`
    or `FILES_REPLICATION`.

    """
    pass


@cli.command()
@click.option(
    '--subset',
    type=click.Choice(['all', 'replication', 'raw']),
    default='replication',
    help='Download raw data (~60GB), replication data (<750MB) or both.',
)
def download(subset):
    """Download files specified in ``URLS``."""
    if subset == 'raw':
        files = FILES_RAW
    elif subset == 'replication':
        files = FILES_REPLICATION
    else:
        files = {**FILES_RAW, **FILES_REPLICATION}

    click.echo('\n### Start downloading required files.\n')
    for filename, (url, _) in files.items():
        download_file(filename, url)
    click.echo('\n### End\n')


@cli.command()
def validate():
    """Validate downloads with hashes in ``HASHES``."""
    click.echo('### Start validating existing files.\n')
    files = {**FILES_RAW, **FILES_REPLICATION}
    for filename, (_, hash_value) in files.items():
        validate_file(filename, hash_value)
    click.echo('\n### End\n')


@cli.command()
def split():
    """Split downloaded files into smaller chunks.

    The chunk size is chosen so that files are about 100MB big.

    """
    click.echo('### Start splitting predefined files.\n')
    for filename in FILES_RAW.keys():
        if 'detail_desc_text' in filename:
            split_detail_desc_text(filename)
        elif 'patent.tsv.zip' in filename:
            split_patent(filename)
        elif 'brf_sum_text.tsv.zip' in filename:
            split_brf_sum_text(filename)
        else:
            click.echo(f'File {filename} will not be splitted.')
    click.echo('\n### End\n')


if __name__ == '__main__':
    cli()
