import click
import hashlib
import requests

from pathlib import Path
from tqdm import tqdm


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

URL_BASE = 'http://www.patentsview.org/data'
"""str: Base url for PatentsView."""

URLS = [
    f'{URL_BASE}/20171226/patent.tsv.zip',
    f'{URL_BASE}/detail-desc-text/detail_desc_text_1.tsv.zip',
    f'{URL_BASE}/detail-desc-text/detail_desc_text_2.tsv.zip',
    f'{URL_BASE}/detail-desc-text/detail_desc_text_3.tsv.zip',
    f'{URL_BASE}/detail-desc-text/detail_desc_text_4.tsv.zip',
    f'{URL_BASE}/detail-desc-text/detail_desc_text_5.tsv.zip',
]
"""List: Contains urls of files which need to be downloaded.

Make sure that you add a hash in the same position in ``HASHES`` so that the
integrity of the file can be verified. The hash has to be a lowercase sha265.

The has can be computed in Powershell with ``Get-FileHash <file>``. Notice
that Powershell returns uppercase letters and Python lowercase."""

HASHES = [
    '43f53554bae2c572c97aaaa2189e4ff22e1197aeaa7af6478bc5fa975b2855cd',
    'a852b223ff64eda89f71c809f59f4b287efe70614d4cfc4cda99a9fa77e03f8e',
    '7ecdc08e4c9e13eda06cf3b01b8bf7299b04b1e7d8cb195ec4f779806dd64988',
    '7e43bf52349ad956d2f0d6c43a2cb36372ee6900fb214ec28b2e549aeed68694',
    'af0234a963a228b43cfcdf827ffc543608c9eb992596631b24d157e1388b34db',
    'fc918871d3af99b1de1dfa2dd130092cef982d99f8e933d1f90430db1c9d6f67',
]
"""List: Contains sha265 hashes calculated for the files in ``URLS``."""

DOWNLOAD_FOLDER = Path('src', 'data', 'downloaded')
"""pathlib.Path: Points to the target directory of downloads."""


def downloader(position: int, resume_byte_pos: int = None):
    """Download url in ``URLS[position]`` to disk with possible resumption.

    Parameters
    ----------
    position: int
        Position of url.
    resume_byte_pos: int
        Position of byte from where to resume the download

    """
    # Get size of file
    url = URLS[position]
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
    file = DOWNLOAD_FOLDER / url.split('/')[-1]

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


def download_file(position: int):
    """Execute the correct download operation.

    Depending on the size of the file online and offline, resume the
    download if the file offline is smaller than online.

    Parameters
    ----------
    position: int
        Position of url.

    """
    # Establish connection to header of file
    url = URLS[position]
    r = requests.head(url)

    # Get filesize of online and offline file
    file_size_online = int(r.headers.get('content-length', 0))
    file = DOWNLOAD_FOLDER / url.split('/')[-1]

    if file.exists():
        file_size_offline = file.stat().st_size

        if file_size_online != file_size_offline:
            click.echo(f'File {file} is incomplete. Resume download.')
            downloader(position, file_size_offline)
        else:
            click.echo(f'File {file} is complete. Skip download.')
            pass
    else:
        click.echo(f'File {file} does not exist. Start download.')
        downloader(position)


def validate_file(position: int):
    """Validate a given file with its hash.

    The downloaded file is compared with a hash to validate the download
    procedure.

    Parameters
    ----------
    position: int
        Position of url and hash.

    """
    file = DOWNLOAD_FOLDER / URLS[position].split('/')[-1]
    try:
        hash = HASHES[position]
    except IndexError:
        click.echo(f'File {file.name} has no hash.')
        return 0

    sha = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            chunk = f.read(1000 * 1000)  # 1MB so that memory is not exhausted
            if not chunk:
                break
            sha.update(chunk)
    try:
        assert sha.hexdigest() == hash
    except AssertionError:
        file = URLS[position].split("/")[-1]
        print(
            f'File {file} is corrupt. '
            'Delete it manually and restart the program.'
        )
    else:
        print(f'File {file} is validated.')


@click.group(context_settings=CONTEXT_SETTINGS, chain=True)
def cli():
    """Program for downloading files.

    To download a file, add the link to ``URLS`` and its hash to ``HASHES`` if
    you want to validate downloaded files.
    """
    pass


@cli.command()
def download():
    """Download files specified in ``URLS``."""
    click.echo('\n### Start downloading required files.\n')
    for position in range(len(URLS)):
        download_file(position)
    click.echo('\n### End\n')


@cli.command()
def validate():
    """Validate downloads with hashes in ``HASHES``."""
    click.echo('### Start validating required files.\n')
    for position in range(len(URLS)):
        validate_file(position)
    click.echo('\n### End\n')


if __name__ == '__main__':
    cli()
