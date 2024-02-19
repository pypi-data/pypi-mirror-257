import time
import warnings
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Annotated, List, Optional

from dotenv import dotenv_values

# Suppress `NotOpenSSLWarning` warning on macOS
warnings.filterwarnings("ignore", message="urllib3 v2 only supports")

import arrow
import httpx
import questionary
import typer
from ray.job_submission import JobSubmissionClient
from rich import print
from yaspin import yaspin

from pflops import data
from pflops.api import (
    list_datasets,
    retrieve_dataset,
    retrieve_org,
    retrieve_token,
    retrieve_user,
)
from pflops.auth import get_local_token, save_local_token
from pflops.constant import CONSOLE_URL, LOGIN_TIMEOUT_SECONDS
from pflops.util import cuid_generator, format_size

app = typer.Typer()

app.add_typer(data.app, name="data")


@app.callback()
def callback():
    """
    Petaflops CLI
    """
    pass


@app.command()
def login():
    """
    Retrieve sign-in token from the Petaflops server and store it to the local machine.
    """
    cli_id = cuid_generator(prefix="cli")
    url = f"{CONSOLE_URL}/cli/auth?id={cli_id}"
    try:
        webbrowser.open(url)
    finally:
        print(
            "Please sign in using the following link:\n" f"[link={url}]{url}[/link]\n"
        )

    start_time = time.time()
    with yaspin(text="Waiting...") as spinner:
        while time.time() < start_time + LOGIN_TIMEOUT_SECONDS:
            token = retrieve_token(cli_id)
            if not token:
                time.sleep(3)
                continue
            save_local_token(token)
            spinner.ok("✅")
            print("[green]Successfully logged in.")
            return


@app.command()
def run(
    command: Annotated[
        str,
        typer.Argument(
            help="Command to run on the cluster (e.g. python main.py)",
        ),
    ],
    name: Annotated[
        Optional[str],
        typer.Option(help="Name of the job"),
    ] = None,
    dataset_name: Annotated[
        Optional[str],
        typer.Option(
            "--dataset",
            help="Name of the dataset uploaded to Petaflops storage",
        ),
    ] = None,
    num_cpus: Annotated[
        Optional[int],
        typer.Option(help="Number of CPU cores to request"),
    ] = None,
    num_gpus: Annotated[
        Optional[int],
        typer.Option(help="Number of GPUs to request"),
    ] = None,
):
    """
    Submit a job to your organization's cluster.
    """
    if not get_local_token():
        print("[red]You are not logged in. Please run `pflops login` first.")
        raise typer.Exit()

    if not name:
        name = questionary.text("Name of the job:").ask()

    if not dataset_name:
        if questionary.confirm(
            "Do you have a dataset to use in Petaflops storage?",
            default=False,
            auto_enter=False,
        ).ask():
            datasets: List = list_datasets()["datasets"]
            choices = list(
                map(
                    lambda d: questionary.Choice(
                        title=f"{d['name']} ({format_size(d['size'])}, {arrow.get(d['lastModifiedTime']).humanize()})",
                        value=d["name"],
                    ),
                    datasets,
                )
            )
            dataset_name = questionary.select(
                "Select dataset to use:",
                choices=choices,
            ).ask()

    if num_cpus is None:
        num_cpus = int(questionary.text("CPU cores to request:").ask())

    if num_gpus is None:
        num_gpus = int(questionary.text("GPUs to request:").ask())

    runtime_env: dict[str, str] = {"working_dir": "."}
    if Path(".env").exists():
        if questionary.confirm(
            ".env detected. Use it?",
            default=True,
            auto_enter=False,
        ).ask():
            runtime_env["env_vars"] = dotenv_values(".env")

    if Path("requirements.txt").exists():
        if questionary.confirm(
            "requirements.txt detected. Use it?",
            default=True,
            auto_enter=False,
        ).ask():
            runtime_env["pip"] = "./requirements.txt"

    if Path(".pfignore").exists():
        with open(".pfignore", "r") as f:
            runtime_env["excludes"] = f.read().splitlines()

    try:
        user = retrieve_user()
        org = retrieve_org()
        dataset_url = retrieve_dataset(dataset_name)["url"]
        ray_endpoint: str = org["rayEndpoint"]
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            print("[red]Your token is invalid. Please run `pflops login` again.")
            return
        if e.response.status_code == 404:
            print(
                "[red]Your organization is not found. Please contact your administrator."
            )
            return
        print(f"[red]An error occurred: {e}")
        return

    client = JobSubmissionClient(ray_endpoint)
    job_id = cuid_generator(prefix="job")
    # TODO: Add timestamp to each row (requires moreutils): ts '[%Y-%m-%d %H:%M:%S]'
    entrypoint = f'wget -O {dataset_name} "{dataset_url}" && {command}'

    client.submit_job(
        submission_id=job_id,
        entrypoint=entrypoint,
        entrypoint_num_cpus=num_cpus,
        entrypoint_num_gpus=num_gpus,
        runtime_env=runtime_env,
        metadata={
            "name": name,
            "author_id": user["id"],
            "submit_time": datetime.now().isoformat(),
        },
    )

    print(
        f'[green]Job "{name}" has been submitted. Check its progress on:\n {CONSOLE_URL}/jobs/{job_id}'
    )


if __name__ == "__main__":
    app()
