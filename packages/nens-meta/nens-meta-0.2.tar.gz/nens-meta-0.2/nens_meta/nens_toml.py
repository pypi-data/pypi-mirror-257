"""Purpose: read and manage the .nens.toml config file
"""
import copy
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomlkit
from tomlkit.items import Table

from nens_meta import __version__, utils


@dataclass
class Option:
    key: str
    description: str
    value_type: type = str
    default: Any = ""
    default_if_python: Any = ""


META_FILENAME = ".nens.toml"
KNOWN_SECTIONS: dict[str, list[Option]] = {}
# First key is the section name, the second key/value pair is the variable name and the
# explanation. If the second key ends with "_TRUE"/"_FALSE", this is stripped and will
# be used to treat the value as a boolean with the indicated default.
KNOWN_SECTIONS["meta"] = [
    Option(key="meta_version", description="Version used to generate the config"),
    Option(
        key="project_name",
        description="Project name (normally the name of the directory)",
    ),
    Option(
        key="is_python_project",
        description="Whether we are a python project",
        default=False,
        value_type=bool,
    ),
    Option(key="package_name", description="Name of the main python package"),
]
KNOWN_SECTIONS["pyprojecttoml"] = []
KNOWN_SECTIONS["tox"] = [
    Option(key="minimum_coverage", description="Minimum code coverage percentage"),
    Option(
        key="default_environments",
        description="List of envs to run when you call 'tox'",
        value_type=list,
        default=["lint"],
        default_if_python=[
            "lint",
            "py310",
            "py311",
            "py312",
            "coverage",
        ],
    ),
]
KNOWN_SECTIONS["meta_workflow"] = [
    Option(
        key="environments",
        description="Tox environments that should be called, 'TEST' means 'py*'",
        value_type=list,
        default=["format", "lint"],
        default_if_python=[
            "lint",
            "coverage",
            "dependencies",
            "dependencies-graph",
            "TEST",
        ],
    ),
    Option(
        key="main_python_version",
        description="Python version to use for linting and so",
        default="3.11",
    ),
    Option(
        key="python_versions",
        description="Python version(s) to run tests as",
        value_type=list,
        default=["3.11"],
        default_if_python=["3.10", "3.11", "3.12"],
    ),
]

logger = logging.getLogger(__name__)


def write_documentation():
    target = Path(__file__).parent.parent / "doc" / "nens_toml_example.toml"
    lines = []
    for section in KNOWN_SECTIONS:
        lines.append(f"[{section}]")
        for option in KNOWN_SECTIONS[section]:
            lines.append(f"# {option.description}")
            lines.append(f"{option.key} = {repr(option.default)}")
            if option.default_if_python:
                lines.append("# In case of a python project:")
                lines.append(f"# {option.key} = {option.default_if_python}")
        lines.append("")

    content = "\n".join(lines)
    content = content.replace(" False", " false")  # Toml syntax hack
    target.write_text(content)


def nens_toml_file(project: Path) -> Path:
    return project / META_FILENAME


def create_if_missing(project: Path):
    if not nens_toml_file(project).exists():
        nens_toml_file(project).write_text("")
    our_config = OurConfig(project)
    our_config.read()
    our_config.update_meta_options()
    our_config.write()


def _default_for_key(key: str) -> str | bool | list:
    """Return default (''), but handle the _TRUE/_FALSE postfix tricks"""
    if "_TRUE" in key:
        return True
    if "_FALSE" in key:
        return False
    if "_LIST" in key:
        return []
    return ""


def detected_meta_values(project: Path) -> dict[str, str | bool | list]:
    """Return values we can detect about the project, normally set in [meta]"""
    detected: dict[str, str | bool | list] = {}
    detected["is_python_project"] = utils.is_python_project(project)
    detected["meta_version"] = __version__
    name = project.resolve().name
    detected["project_name"] = name
    if detected["is_python_project"]:
        detected["package_name"] = name.replace("-", "_")
    return detected


class MissingDocumentationError(Exception):
    pass


class OurConfig:
    """Wrapper around a project's .nens.toml

    See https://tomlkit.readthedocs.io/en/latest/quickstart/
    """

    _config_file: Path
    _contents: tomlkit.TOMLDocument
    _project: Path

    def __init__(self, project: Path):
        self._project = project
        self._config_file = nens_toml_file(project)
        self._contents = self.read()
        self.update_meta_options()

    def read(self) -> tomlkit.TOMLDocument:
        return tomlkit.parse(self._config_file.read_text())

    def write(self):
        utils.write_if_changed(
            self._config_file, tomlkit.dumps(self._contents), handle_extra_lines=False
        )

    def update_meta_options(self):
        """Detect meta options"""
        if "meta" not in self._contents:
            self._contents.append("meta", tomlkit.table())
        current: Table = self._contents["meta"]  # type: ignore
        detected = detected_meta_values(self._project)
        for key, value in detected.items():
            if key not in current:
                current[key] = value
                if not isinstance(value, bool):
                    # TODO: .comment doesn't work for boolean values, strangely enough.
                    current[key].comment("Suggested by nens-meta")
        # Make sure our version is correctly recorded
        current["meta_version"] = detected["meta_version"]
        current["meta_version"].comment("Set by nens-meta")

    def has_section_for(self, section_name: str) -> bool:
        return section_name in KNOWN_SECTIONS

    def section_options(self, section_name: str) -> dict:
        """Return all options configured in a given section, if available."""
        if section_name not in KNOWN_SECTIONS:
            # Force ourselves to document our stuff!
            raise MissingDocumentationError(
                f"Section {section_name} not documented in nens-meta"
            )
        section = self._contents.get(section_name)
        if section is None:
            section = {}
        options: dict[str, str | bool | list] = {}
        for option in KNOWN_SECTIONS[section_name]:
            if (
                self._contents.get("meta")
                and self._contents.get("meta")["is_python_project"]
            ):
                default = option.default_if_python or option.default
            else:
                default = option.default
            value = section.get(option.key, copy.deepcopy(default))
            if not isinstance(value, option.value_type):
                raise ValueError(
                    f"{option.key} should be of type {option.value_type}, not {type(value)}"
                )
            options[option.key] = value
        logger.debug(f"Contents of section {section_name}: {options}")
        return options


if __name__ == "__main__":
    # Only called to write the documentation file.
    write_documentation()
