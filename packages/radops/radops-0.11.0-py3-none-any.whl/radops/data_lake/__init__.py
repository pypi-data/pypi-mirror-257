import os
import shutil
from typing import List

import requests
from tqdm import tqdm

from radops.settings import settings

from ._file import (
    File,
    FileInfo,
    FunctionInfo,
    file_exists_in_data_lake,
    get_local_path,
)
from ._file_creator import file_creator
from .cloud_ops import file_exists_in_s3

__all__ = [
    "File",
    "FileInfo",
    "file_creator",
    "file_exists_in_data_lake",
    "get_local_path",
    "add_local_file",
    "FunctionInfo",
]


@file_creator
def add_local_file(path: str, output_uid: str, copy: bool) -> File:
    f = File(output_uid)
    os.makedirs(f.storage_path.parent, exist_ok=True)
    if copy:
        shutil.copy(path, f.storage_path)
    else:
        shutil.move(path, f.storage_path)
    return f


@file_creator
def add_from_url(url: str, output_uid: str) -> File:
    f = File(output_uid)
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    with f.open("wb") as fileobj, tqdm(
        total=total_size, unit="B", unit_scale=True, desc="Downloading"
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            fileobj.write(chunk)
            pbar.update(len(chunk))
    return f


def list_local_files() -> List[str]:
    return [
        os.path.relpath(os.path.join(root, f), settings.local_storage)
        for root, _, files in os.walk(settings.local_storage)
        for f in files
    ]


def get_unsynced_files() -> List[str]:
    return [f for f in list_local_files() if not file_exists_in_s3(f)]
