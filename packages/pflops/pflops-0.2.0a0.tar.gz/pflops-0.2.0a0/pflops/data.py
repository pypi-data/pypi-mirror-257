import asyncio
import os
from operator import itemgetter
from typing import Annotated, Callable, List

import arrow
import httpx
import typer
from rich import print
from rich.progress import Progress
from rich.table import Table

from pflops.api import (
    create_dataset,
    delete_dataset,
    finish_upload_dataset,
    list_datasets,
    retrieve_dataset,
)
from pflops.util import chunks, format_size, get_file_size

app = typer.Typer()


@app.command()
def push(
    file: Annotated[typer.FileBinaryRead, typer.Argument()],
    name: Annotated[
        str,
        typer.Option(
            help="Name of the dataset",
            prompt="What is the name of the dataset?",
        ),
    ],
):
    """
    Push a dataset to Petaflops storage.
    """
    if "/" in name:
        print("[red]Dataset name cannot contain '/'")
        raise typer.Exit()

    size = get_file_size(file)
    try:
        res = create_dataset(name, size)
    except httpx.HTTPStatusError as e:
        print(f"[red]{e.response.text}")
        raise typer.Exit()

    chunk_size: int = res["chunkSize"]
    urls: List[str] = res["urls"]
    upload_id: str = res["uploadId"]
    e_tags: List[str] = [None] * len(urls)

    print(f"Pushing {name} ({format_size(size)}) to Petaflops storage...\n")

    async def upload_chunks():
        with Progress() as progress:
            task_id = progress.add_task("", total=len(urls))

            async def upload_chunk(url: str, data: bytes, index: int):
                async with httpx.AsyncClient() as client:
                    # TODO: retry on failure (e.g. using tenacity)
                    r = await client.put(url, data=data, timeout=None)
                    e_tags[index] = r.headers["etag"]
                    r.raise_for_status()
                    progress.advance(task_id)

            for chunk in chunks(list(enumerate(urls)), 5):
                tasks: List[asyncio.Task] = []
                for index, url in chunk:
                    data = file.read(chunk_size)
                    tasks.append(asyncio.create_task(upload_chunk(url, data, index)))
                await asyncio.gather(*tasks)

    asyncio.run(upload_chunks())
    finish_upload_dataset(name, upload_id, e_tags)
    print("[green]Successfully uploaded.")


@app.command()
def pull(name: Annotated[str, typer.Argument()]):
    try:
        url: str = retrieve_dataset(name)["url"]
    except httpx.HTTPStatusError as e:
        print(f"[red]{e.response.text}")
        raise typer.Exit()

    with httpx.stream("GET", url) as res, Progress() as progress, open(
        name, "wb"
    ) as file:
        size = int(res.headers["content-length"])
        print(f"Pulling {name} ({format_size(size)}) from Petaflops storage...\n")
        task_id = progress.add_task("", total=size)
        for chunk in res.iter_bytes():
            file.write(chunk)
            progress.advance(task_id, len(chunk))


@app.command(name="list")
def ls():
    try:
        datasets: List = list_datasets()["datasets"]
    except httpx.HTTPStatusError as e:
        print(f"[red]{e.response.text}")
        raise typer.Exit()

    if not datasets:
        print("No datasets found.")
        return

    table = Table("Name", "Size", "Created")
    for dataset in datasets:
        table.add_row(
            dataset["name"],
            format_size(dataset["size"]),
            arrow.get(dataset["lastModifiedTime"]).humanize(),
        )
    print(table)


@app.command()
def delete(name: Annotated[str, typer.Argument()]):
    try:
        delete_dataset(name)
    except httpx.HTTPStatusError as e:
        print(f"[red]{e.response.text}")
        raise typer.Exit()

    print(f"Deleted.")
