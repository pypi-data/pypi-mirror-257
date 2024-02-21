import os
import json
import yaml
from ..models import Config
from rich import print
from typing import List


def validate_folder(dir, folder, typer):
    if not os.path.exists(dir / folder):
        raise typer.BadParameter(f"No {folder} directory found in '{dir}'.")


def validate_item(dir, folder, item, name, typer, file="main.py"):
    # check name
    if not item.name:
        raise typer.BadParameter(f"{name} '{item.name}' is missing 'name' attribute.")
    # check folder has folder with item name
    if not os.path.exists(dir / folder / item.name):
        raise typer.BadParameter(
            f"{name} '{item.name}' cannot be found in {dir}/{folder}."
        )
    # check folder has file
    if not file in os.listdir(dir / folder / item.name):
        raise typer.BadParameter(f"{name} '{item.name}' is missing file 'main.py'.")
    # TODO: check optionals: reqs, env...


def validate_storage(storage, typer, cloud):
    if storage.type == "local" and cloud:
        raise typer.BadParameter(
            f"Local storage not allowed in cloud deployment, please use S3 storage."
        )
    # if storage.type == "s3" and not storage.credentials:
    #     typer.echo(
    #         f"S3 storage credentials not provided, an S3 bucket will be created if it does not already exist."
    #     )


def load_and_validate_config(dir, typer, verbose=False, cloud=False):
    # check dir exists
    if not dir.exists():
        raise typer.BadParameter(f"Directory '{dir}' does not exist.")
    # check dir is a spai project
    if not "spai.config.yaml" in os.listdir(dir):
        raise typer.BadParameter(
            f"Directory '{dir}' is not a spai project. No spai.config.yaml file found."
        )
    # TODO: guardar todo lo que haga falta en variables de entorno

    # load config
    config = {}
    with open(dir / "spai.config.yaml", "r") as f:
        config = yaml.safe_load(f)
    if not config:
        raise typer.BadParameter(f"spai.config.yaml file is empty.")
    config.update(dir=dir)
    if verbose:
        print(config)
    config = Config(**config)
    # TODO: check if project name is already taken in cloud, locally is not a problem
    config.project = dir.name if not config.project else config.project
    # check storage
    if config.storage:
        names = []
        for storage in config.storage:
            if storage.name in names:
                raise typer.BadParameter(
                    f"Found multiple storages with name '{storage.name}', please use unique names for your storage."
                )
            validate_storage(storage, typer, cloud)
            names.append(storage.name)
    # check scripts
    if config.scripts:
        # check project has scripts folder
        validate_folder(dir, "scripts", typer)
        for script in config.scripts:
            validate_item(dir, "scripts", script, "script", typer)
    # check apis
    if config.apis:
        # check project has apis folder
        validate_folder(dir, "apis", typer)
        for api in config.apis:
            validate_item(dir, "apis", api, "api", typer)
    # check uis
    if config.uis:
        # check project has uis folder
        validate_folder(dir, "uis", typer)
        for ui in config.uis:
            validate_item(dir, "uis", ui, "ui", typer)
    # check notebooks
    if config.notebooks:
        # check project has notebooks folder
        validate_folder(dir, "notebooks", typer)
        for notebook in config.notebooks:
            validate_item(dir, "notebooks", notebook, "notebook", typer, "main.ipynb")
    return config


def validate_template_parameters(url: str, aoi: str, dates: List) -> bool:
    """
    Validate the parameters of the template command.

    Parameters
    ----------
    url : str
        URL of the template repository.
    aoi : str
        Path to the AOI GeoJSON file.
    dates : List
        Start and end dates of the time interval.

    Returns
    -------
    bool
        True if the parameters are valid, False otherwise.
    """
    if not url:
        raise BadParameter(f"Template URL must be provided")
    if not validators.url(url):
        raise BadParameter(f"Invalid url '{url}'")

    if not aoi:
        raise FileNotFoundError(f"AOI file must be provided")
    if not os.path.exists(aoi):
        raise FileNotFoundError(f"AOI file not found in {aoi}")

    if not dates:
        raise BadParameter(f"Dates must be provided")

    return True
