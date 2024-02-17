import os
import shutil
import time

import rich
import typer
from rich.table import Table

from radops import env_prefix, settings

from .common import _y_n_prompt_loop

app = typer.Typer()


@app.command(name="get-contexts")
def get_contexts():
    rich.print(
        [
            f[5:]
            for f in os.listdir(settings.model_config["env_file"].parent)
            if f.startswith(".env-")
        ]
    )


@app.command(name="view")
def view():
    """Displays current `radops` configuration"""
    table = Table("setting", "value")
    for k, v in settings.model_dump().items():
        table.add_row(k, str(v))
    rich.print(table)


def env_path_from_context(context: str):
    return str(settings.model_config["env_file"]) + "-" + context


CURRENT_CONTEXT_FILE = (
    settings.model_config["env_file"].parent / ".current_context"
)


@app.command(name="use-context")
def use_context(context: str):
    env_path = env_path_from_context(context)
    if not os.path.exists(env_path):
        rich.print(f"Context {context} does not exist")
        return

    shutil.copy(env_path, settings.model_config["env_file"])
    with open(CURRENT_CONTEXT_FILE, "w") as f:
        f.write(context)


@app.command(name="create-context")
def create_context(context: str):
    env_path = env_path_from_context(context)
    backup_path = None
    if os.path.exists(env_path):
        _y_n_prompt_loop(f"context {context} already exists, overwrite?")
        backup_path = str(env_path) + time.strftime("%Y%m%d-%H%M%S")
        rich.print(f"Backing up existing config to {backup_path}")
        shutil.move(env_path, backup_path)
    try:
        settings_dict = {}
        settings_dict[f"{env_prefix}email"] = typer.prompt(
            "Your e-mail address"
        )
        settings_dict[f"{env_prefix}s3_endpoint_url"] = typer.prompt("S3 URL")
        settings_dict[f"{env_prefix}aws_access_key_id"] = typer.prompt(
            "Access key"
        )
        settings_dict[f"{env_prefix}aws_secret_access_key"] = typer.prompt(
            "Secret access key", hide_input=True
        )
        settings_dict[f"{env_prefix}gcp_project_id"] = typer.prompt(
            "GCP project ID"
        )
        settings_dict[f"{env_prefix}mlflow_url"] = typer.prompt("MLFlow URL")
        settings_dict[f"{env_prefix}mlflow_username"] = typer.prompt(
            "MLFlow username"
        )
        settings_dict[f"{env_prefix}mlflow_password"] = typer.prompt(
            "MLFlow password", hide_input=True
        )
    except Exception as e:
        if backup_path is not None:
            rich.print("[yellow]Restoring configuration")
            shutil.move(backup_path, env_path)

        if not isinstance(e, KeyboardInterrupt):
            raise e

    with open(env_path, "w") as f:
        for k, v in settings_dict.items():
            f.write(f"{k}={v}\n")

    use_context(context)


@app.command(name="current-context")
def current_context():
    with open(CURRENT_CONTEXT_FILE) as f:
        rich.print(f.read())


@app.command(name="setup")
def setup():
    """Sets up `radops` configuration"""
    create_context("default")

    rich.print(
        f"For connecting to GCP, you will need to download a JSON key to {settings.gcp_key}."
    )
