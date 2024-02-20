import json
from pathlib import Path
import sys
import tempfile
from typing import Annotated
import requests
from tqdm import tqdm
import os
from loguru import logger
import diskcache
import docker
import typer

app = typer.Typer()


def get_uploaded_size(session_uri):
    """Check how much has been uploaded to resume correctly."""
    headers = {"Content-Range": "bytes */*"}  # Asking for the current status
    response = requests.put(session_uri, headers=headers)
    if response.status_code == 308:  # Resume Incomplete
        range_header = response.headers.get("Range")
        if range_header:
            bytes_uploaded = int(range_header.split("-")[1]) + 1
            return bytes_uploaded
    return 0


def upload_chunk(session_uri, file_path, start_position, chunk_size, total_size):
    """Upload a single chunk."""
    end_position = start_position + chunk_size - 1
    headers = {"Content-Range": f"bytes {start_position}-{end_position}/{total_size}"}

    with open(file_path, "rb") as f:
        f.seek(start_position)
        data = f.read(chunk_size)
        response = requests.put(session_uri, headers=headers, data=data)
        return response


def upload_file_in_chunks(session_uri, file_path, chunk_size=26214400):
    """Upload a file in chunks and resume if interrupted."""
    file_size = os.path.getsize(file_path)
    start_position = get_uploaded_size(session_uri)

    # Calculate the number of chunks
    total_chunks = (file_size - start_position + chunk_size - 1) // chunk_size
    logger.debug(f"Resuming at {start_position} bytes for {total_chunks} chunks")
    # Iterate over the file in chunks with a for loop
    for i in tqdm(range(total_chunks), desc="Uploading"):
        current_position = start_position + i * chunk_size
        current_chunk_size = min(chunk_size, file_size - current_position)

        response = upload_chunk(
            session_uri, file_path, current_position, current_chunk_size, file_size
        )
        response.raise_for_status()

        if response.status_code in (200, 201):
            logger.info(f"Upload complete after {total_chunks} chunks.")
            break
        elif response.status_code == 308:
            continue


def get_openapi_specs(path):
    client = docker.from_env()
    with open(path, "rb") as image_file:
        images = client.images.load(image_file)
    logger.debug("Image loaded successfully")
    assert len(images) == 1
    out = client.containers.run(
        images[0].tags[0],
        command="python openapi.py",
        remove=True,
        stdout=True,
        stderr=True,
    )
    openapi = out.decode().strip()
    logger.debug("Generated API specs")
    openapi = json.loads(openapi)
    logger.debug("API specs parsed successfully")
    return openapi


def get_session_uri(url):
    headers = {"x-goog-resumable": "start", "Content-Type": "application/octet-stream"}
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    session_uri = response.headers["Location"]
    return session_uri


@app.command()
def other():
    ...

@app.command()
def push(
    url: Annotated[str, typer.Option("--url", "-u")],
    path: Annotated[Path, typer.Option("--input", "-i")],
):
    cache = diskcache.Cache("/tmp/cache", timeout=3600 * 24)
    cache.clear()
    if url in cache:
        logger.info("Resuming upload.")
        session_uri = cache[url]
    else:
        logger.info("Starting new upload.")
        signed_urls_res = requests.get(url)
        signed_urls_res.raise_for_status()
        signed_urls = signed_urls_res.json()

        url_openapi = signed_urls["openapi"]

        openapi = get_openapi_specs(path)
        with tempfile.NamedTemporaryFile(mode="w") as f:
            json.dump(openapi, f)
            f.flush()
            openapi_path = f.name

            session_openapi_uri = get_session_uri(url_openapi)
            upload_file_in_chunks(session_openapi_uri, openapi_path)
        logger.info("API specs uploaded.")

        url_image = signed_urls["image"]
        session_uri = get_session_uri(url_image)

        cache[url] = session_uri
    upload_file_in_chunks(session_uri, path)


if __name__ == "__main__":
    app()
