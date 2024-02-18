#! /usr/bin/env python
"""Manages environment registry, services, and stauts"""
from __future__ import annotations

import json
import typing
from pathlib import Path
from typing import Optional

import docker
import git
import pandas as pd
import yaml
from docker.errors import DockerException
from git.exc import InvalidGitRepositoryError
from yaml import safe_load

import colrev.exceptions as colrev_exceptions
import colrev.operation
import colrev.record
from colrev.constants import Colors
from colrev.constants import Fields
from colrev.constants import FieldValues
from colrev.env.utils import dict_keys_exists
from colrev.env.utils import dict_set_nested
from colrev.env.utils import get_by_path


class EnvironmentManager:
    """The EnvironmentManager manages environment resources and services"""

    colrev_path = Path.home().joinpath("colrev")
    cache_path = colrev_path / Path("prep_requests_cache")
    REGISTRY_RELATIVE = Path("registry.json")
    registry = colrev_path.joinpath(REGISTRY_RELATIVE)
    REGISTRY_RELATIVE_YAML = Path("registry.yaml")
    registry_yaml = colrev_path.joinpath(REGISTRY_RELATIVE_YAML)
    load_yaml = False

    def __init__(self) -> None:
        self.environment_registry = self.load_environment_registry()
        self.__registered_ports: typing.List[str] = []

    def register_ports(self, *, ports: typing.List[str]) -> None:
        """Register a localhost port to avoid conflicts"""
        for port_to_register in ports:
            if port_to_register in self.__registered_ports:
                raise colrev_exceptions.PortAlreadyRegisteredException(
                    f"Port {port_to_register} already registered"
                )
            self.__registered_ports.append(port_to_register)

    def load_environment_registry(self) -> dict:
        """Load the local registry"""
        environment_registry_path = self.registry
        environment_registry_path_yaml = self.registry_yaml
        environment_registry = {}
        if environment_registry_path.is_file():
            self.load_yaml = False
            with open(environment_registry_path, encoding="utf8") as file:
                environment_registry = json.load(fp=file)
            # assert "local_index" in environment_registry
            # assert "packages" in environment_registry
        elif environment_registry_path_yaml.is_file():
            self.load_yaml = True
            backup_file = Path(str(environment_registry_path_yaml) + ".bk")
            print(
                f"Found a yaml file, converting to json, it will be backed up as {backup_file}"
            )
            with open(environment_registry_path_yaml, encoding="utf8") as file:
                environment_registry_df = pd.json_normalize(safe_load(file))
                repos = environment_registry_df.to_dict("records")
                environment_registry = {
                    "local_index": {
                        "repos": repos,
                    },
                    "packages": {},
                }
                self.save_environment_registry(updated_registry=environment_registry)
                environment_registry_path_yaml.rename(backup_file)
        return environment_registry

    def local_repos(self) -> list:
        """gets local repos from local index"""
        self.environment_registry = self.load_environment_registry()
        if "local_index" not in self.environment_registry:
            return []
        if "repos" not in self.environment_registry["local_index"]:
            return []
        return self.environment_registry["local_index"]["repos"]

    def __cast_values_to_str(self, data) -> dict:  # type: ignore
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                result[key] = self.__cast_values_to_str(value)
            elif isinstance(value, list):
                result[key] = [self.__cast_values_to_str(v) for v in value]  # type: ignore
            else:
                result[key] = str(value)  # type: ignore
        return result

    def save_environment_registry(self, *, updated_registry: dict) -> None:
        """Save the local registry"""
        self.registry.parents[0].mkdir(parents=True, exist_ok=True)
        with open(self.registry, "w", encoding="utf8") as file:
            json.dump(
                dict(self.__cast_values_to_str(updated_registry)), indent=4, fp=file
            )

    def register_repo(self, *, path_to_register: Path) -> None:
        """Register a repository"""
        self.environment_registry = self.load_environment_registry()

        if "local_index" not in self.environment_registry:
            self.environment_registry["local_index"] = {"repos": []}
        registered_paths = [
            x["repo_source_path"]
            for x in self.environment_registry["local_index"]["repos"]
        ]

        if registered_paths:
            if str(path_to_register) in registered_paths:
                # print(f"Warning: Path already registered: {path_to_register}")
                return
        else:
            print(f"Creating {self.registry}")

        new_record = {
            "repo_name": path_to_register.stem,
            "repo_source_path": path_to_register,
        }
        git_repo = git.Repo(path_to_register)
        try:
            remote_urls = list(git_repo.remote("origin").urls)
            new_record["repo_source_url"] = remote_urls[0]
        except (ValueError, IndexError):
            for remote in git_repo.remotes:
                if remote.url:
                    new_record["repo_source_url"] = remote.url
                    break
        self.environment_registry["local_index"]["repos"].append(new_record)
        self.save_environment_registry(updated_registry=self.environment_registry)
        print(f"Registered path ({path_to_register})")

    def get_name_mail_from_git(self) -> typing.Tuple[str, str]:  # pragma: no cover
        """Get the committer name and email from git (globals)"""
        global_conf_details = ("NA", "NA")
        try:
            username = git.config.GitConfigParser().get_value("user", "name")
            email = git.config.GitConfigParser().get_value("user", "email")
            global_conf_details = (username, email)
        except (git.config.cp.NoSectionError, git.config.cp.NoOptionError) as exc:
            raise colrev_exceptions.CoLRevException(
                "Global git variables (user name and email) not available."
            ) from exc
        return global_conf_details

    @classmethod
    def build_docker_image(
        cls, *, imagename: str, image_path: Optional[Path] = None
    ) -> None:
        """Build a docker image"""

        try:
            client = docker.from_env()
            repo_tags = [t for image in client.images.list() for t in image.tags]

            if imagename not in repo_tags:
                if image_path:
                    assert colrev.review_manager.__file__
                    colrev_path = Path("")
                    if colrev.review_manager.__file__:
                        colrev_path = Path(colrev.review_manager.__file__).parents[0]
                    print(f"Building {imagename} Docker image ...")
                    context_path = colrev_path / image_path
                    client.images.build(
                        path=str(context_path), tag=f"{imagename}:latest"
                    )

                else:
                    print(f"Pulling {imagename} Docker image...")
                    client.images.pull(imagename)
        except DockerException as exc:
            raise colrev_exceptions.ServiceNotAvailableException(
                dep="docker",
                detailed_trace=f"Docker service not available ({exc}). "
                + "Please install/start Docker.",
            ) from exc

    def check_git_installed(self) -> None:
        """Check whether git is installed"""

        try:
            git_instance = git.Git()
            _ = git_instance.version()
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
            # raise colrev_exceptions.MissingDependencyError("git") from exc

    def check_docker_installed(self) -> None:
        """Check whether Docker is installed"""

        try:
            client = docker.from_env()
            _ = client.version()
        except docker.errors.DockerException as exc:
            if "PermissionError" in exc.args[0]:
                raise colrev_exceptions.DependencyConfigurationError(
                    "Docker: Permission error. Run "
                    f"{Colors.ORANGE}sudo gpasswd -a $USER docker && "
                    f"newgrp docker{Colors.END}"
                )
            raise colrev_exceptions.MissingDependencyError("Docker")

    def _get_status(
        self, *, review_manager: colrev.review_manager.ReviewManager
    ) -> dict:
        status_dict = {}
        with open(review_manager.status, encoding="utf8") as stream:
            try:
                status_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return status_dict

    def get_environment_details(self) -> dict:
        """Get the environment details"""

        # def get_last_modified() -> str:

        #     list_of_files = local_index.opensearch_index.glob(
        #         "**/*"
        #     )  # * means all if need specific format then *.csv
        #     latest_file = max(list_of_files, key=os.path.getmtime)
        #     last_mod = datetime.fromtimestamp(latest_file.lstat().st_mtime)
        #     return last_mod.strftime("%Y-%m-%d %H:%M")

        local_index = colrev.env.local_index.LocalIndex(
            index_tei=True, verbose_mode=True
        )

        environment_details = {}
        size = 0
        last_modified = "NOT_INITIATED"
        status = "TODO"

        size = 0
        # try:
        #     size = local_index.open_search.cat.count(
        #         index=local_index.RECORD_INDEX, params={"format": "json"}
        #     )[0]["count"]
        #     last_modified = get_last_modified()
        #     status = "up"
        # except (NotFoundError, IndexError):
        #     status = "down"

        environment_details["index"] = {
            "size": size,
            "last_modified": last_modified,
            "path": str(local_index.local_environment_path),
            "status": status,
        }

        environment_stats = self.get_environment_stats()

        environment_details["local_repos"] = {
            "repos": environment_stats["repos"],
            "broken_links": environment_stats["broken_links"],
        }
        return environment_details

    def get_environment_stats(self) -> dict:
        """Get the environment stats"""

        local_repos = self.local_repos()
        repos = []
        broken_links = []
        for repo in local_repos:
            try:
                cp_review_manager = colrev.review_manager.ReviewManager(
                    path_str=repo["repo_source_path"]
                )
                check_operation = colrev.operation.CheckOperation(
                    review_manager=cp_review_manager
                )
                repo_stat = self._get_status(review_manager=cp_review_manager)
                repo["size"] = repo_stat["overall"]["md_processed"]
                if repo_stat["atomic_steps"] != 0:
                    repo["progress"] = round(
                        repo_stat["completed_atomic_steps"] / repo_stat["atomic_steps"],
                        2,
                    )
                else:
                    repo["progress"] = -1

                git_repo = check_operation.review_manager.dataset.get_repo()
                repo["remote"] = any(
                    "remote" in x and x["remote"] for x in git_repo.remotes
                )
                repo["behind_remote"] = (
                    check_operation.review_manager.dataset.behind_remote()
                )

                repos.append(repo)
            except (
                colrev_exceptions.CoLRevException,
                InvalidGitRepositoryError,
            ):
                broken_links.append(repo)
        return {"repos": repos, "broken_links": broken_links}

    def get_curated_outlets(self) -> list:
        """Get the curated outlets"""
        curated_outlets: typing.List[str] = []
        for repo_source_path in [
            x["repo_source_path"]
            for x in self.local_repos()
            if "colrev/curated_metadata/" in x["repo_source_path"]
        ]:
            try:
                with open(f"{repo_source_path}/readme.md", encoding="utf-8") as file:
                    first_line = file.readline()
                curated_outlets.append(first_line.lstrip("# ").replace("\n", ""))

                with open(
                    f"{repo_source_path}/data/records.bib", encoding="utf-8"
                ) as file:
                    outlets = []
                    for line in file.readlines():
                        # Note : the second part ("journal:"/"booktitle:")
                        # ensures that data provenance fields are skipped
                        if (
                            Fields.JOURNAL == line.lstrip()[:7]
                            and "journal:" != line.lstrip()[:8]
                        ):
                            journal = line[line.find("{") + 1 : line.rfind("}")]
                            if journal != FieldValues.UNKNOWN:
                                outlets.append(journal)
                        if (
                            line.lstrip()[:9] == Fields.BOOKTITLE
                            and line.lstrip()[:10] != "booktitle:"
                        ):
                            booktitle = line[line.find("{") + 1 : line.rfind("}")]
                            if booktitle != FieldValues.UNKNOWN:
                                outlets.append(booktitle)

                    if len(set(outlets)) > 1:
                        raise colrev_exceptions.CuratedOutletNotUnique(
                            "Error: Duplicate outlets in curated_metadata of "
                            f"{repo_source_path} : {','.join(list(set(outlets)))}"
                        )
            except FileNotFoundError as exc:
                print(exc)

        return curated_outlets

    def get_settings_by_key(self, key: str) -> str | None:
        """Loads setting by the given key"""
        environment_registry = self.load_environment_registry()
        keys = key.split(".")
        if dict_keys_exists(environment_registry, *keys):
            return get_by_path(environment_registry, keys)
        return None

    def update_registry(self, key: str, value: str) -> None:
        """updates given key in the registry with new value"""

        keys = key.split(".")
        # We don't want to allow user to replace any core settings, so check for packages key
        if keys[0] != "packages" or len(keys) < 2:
            raise colrev_exceptions.PackageSettingMustStartWithPackagesException(key)
        self.environment_registry = self.load_environment_registry()
        dict_set_nested(self.environment_registry, keys, value)
        self.save_environment_registry(updated_registry=self.environment_registry)
