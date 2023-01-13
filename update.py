#!/usr/bin/env python3
import platform
import typing
from urllib.request import urlretrieve
from tempfile import NamedTemporaryFile, TemporaryDirectory
import subprocess
import shutil
from hashlib import sha256

from config import SERVER_URL, APP_FOLDER


def get_platform_identifier() -> str:
    system = platform.system()
    if system == "Darwin":
        return "mac"
    elif system == "Windows":
        return "win"
    elif system == "Linux":
        return "linux"
    else:
        raise Exception("Unsupported platform")


def fetch_current_version() -> str:
    with NamedTemporaryFile("r") as f:
        urlretrieve(f"{SERVER_URL}/version", f.name)
        version = f.read().strip()
    return version


def retrieve_installed_version() -> typing.Union[str, None]:
    try:
        with open("VERSION", "r") as f:
            version = f.readline().strip()
    except:
        version = None

    if version == "":
        version = None

    return version


def launch_app() -> None:
    subprocess.Popen(["./application"], close_fds=True)


def retrieve_checksum(platform_identifier: str, version: str) -> str:
    with NamedTemporaryFile("r") as f:
        urlretrieve(f"{SERVER_URL}/{version}/checksums.txt", f.name)

        line = f.readline()

        checksum_spec = line.split("  ")
        if checksum_spec[1].strip().replace(".zip", "") == platform_identifier:
            return checksum_spec[0]

    raise Exception("Checksum for platform not found")


def sha256_file_checksum(file_path: str) -> str:
    sha256_hash = sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def update_app(new_version: str) -> None:
    platform_identifier = get_platform_identifier()
    checksum = retrieve_checksum(platform_identifier, new_version)

    with TemporaryDirectory() as tmpdir:
        filename, _ = urlretrieve(f"{SERVER_URL}/{new_version}/{platform_identifier}.zip",
                                  tmpdir + "/application.zip")

        if sha256_file_checksum(filename) != checksum:
            raise Exception("Invalid checksum")

        shutil.unpack_archive(filename, APP_FOLDER)


def update_and_launch():
    current_version = fetch_current_version()
    print("Current version", current_version)
    installed_version = retrieve_installed_version()

    if installed_version != current_version:
        print("Update version to ", current_version)
        update_app(current_version)

    launch_app()
