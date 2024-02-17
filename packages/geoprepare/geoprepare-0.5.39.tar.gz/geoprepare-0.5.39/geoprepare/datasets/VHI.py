import os
import pdb

import wget
import requests
import tarfile
import multiprocessing
import numpy as np
from tqdm import tqdm
from pathlib import Path
from osgeo.gdalnumeric import *
import requests
from bs4 import BeautifulSoup


base_url_historic = 'https://www.star.nesdis.noaa.gov/data/pub0018/VHPdata4users/VHP_4km_GeoTiff/'
base_url_present = 'https://www.star.nesdis.noaa.gov/pub/corp/scsb/wguo/data/Blended_VH_4km/geo_TIFF/'


def download_VHI(all_params):
    """


    """
    params, year = all_params

    download_folder = params.dir_download / 'vhi'
    # Ensure download folder exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Get the webpage content
    response = requests.get(base_url_historic)
    response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all .tar.gz links
    tar_gz_links = [a['href'] for a in soup.find_all('a') if a['href'].endswith('.tar.gz')]

    for link in tar_gz_links:
        # Construct the full URL for the file
        file_url = base_url_historic + link

        # Download the .tar.gz file
        print(f"Downloading {file_url}")
        file_response = requests.get(file_url)
        file_path = os.path.join(download_folder, link)

        # Check if the file already exists
        if os.path.exists(file_path):
            continue

        with open(file_path, 'wb') as file:
            file.write(file_response.content)

        # Unzip the downloaded file
        print(f"Extracting {file_path}")
        interim_folder = params.dir_interim / 'vhi'
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=interim_folder)

        print(f"Completed {link}")


def run(params):
    import itertools

    all_params = []
    for year in range(params.start_year, params.end_year + 1):
        all_params.extend(list(itertools.product([params], [year])))

    # Download ESI data
    if params.parallel_process:
        with multiprocessing.Pool(int(multiprocessing.cpu_count() * 0.8)) as p:
            with tqdm(total=len(all_params), desc="Download VHI") as pbar:
                for i, _ in tqdm(enumerate(p.imap_unordered(download_VHI, all_params))):
                    pbar.update()
    else:
        for val in all_params:
            download_VHI(val)


if __name__ == "__main__":
    pass
