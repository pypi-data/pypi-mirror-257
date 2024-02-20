import os
import configparser
from typing import List, Optional
from ._ouput import warning


class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


class Config(object):

    requirements_file: Optional[List[str]]
    requirements: Optional[dict]
    version: Optional[str]
    variables: Optional[dict]
    warnings: bool = False

    def __init__(self) -> None:
        # Verify Config File Exists
        if not os.path.exists("pyenvsync.ini"):
            raise FileNotFoundError("The pyenvsync.ini configuration file was not found.")

        # Config Parser
        self.config = CaseSensitiveConfigParser()
        self.config.read("pyenvsync.ini")

        # Load Values
        self.load_python_version()
        self.load_requirements()
        self.load_environment_variables()

    @staticmethod
    def _higher_version(version1: Optional[str], version2: Optional[str]) -> Optional[str]:
        # If One is None, Return the Other
        if version1 is None and version2 is not None:
            return version2

        # If One is None, Return the Other
        if version1 is not None and version2 is None:
            return version1

        # If Both are None, Return None
        if version1 is None and version2 is None:
            return None

        # Split Versions
        v1_parts = list(map(int, version1.split('.')))
        v2_parts = list(map(int, version2.split('.')))

        # Check For Higher Version
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1 = v1_parts[i] if i < len(v1_parts) else 0
            v2 = v2_parts[i] if i < len(v2_parts) else 0

            if v1 < v2:
                return version2
            elif v1 > v2:
                return version1

        return version1

    def _verify_requirement(self, requirement: str, version: Optional[str]) -> str:
        # If Requirement Already Exists, Use Higher Version
        if requirement in self.requirements.keys():
            return self._higher_version(self.requirements[requirement], version)

        return version

    def load_requirements(self) -> None:
        # Retrieve Requirements File(s)
        try:
            self.requirements_file = list(dict(self.config.items("requirements")).values())

        except configparser.NoSectionError:
            self.success = False
            self.requirements_file = None
            self.requirements = None
            self.warnings = True
            warning("No requirements section was found in the configuration file.")
            return

        # Verify Each Requirements File Exists
        for file in self.requirements_file:
            if not os.path.exists(file):
                raise FileNotFoundError(f"The requirements file {file} was not found.")

        # Consolidate Requirements
        self.requirements = {}
        try:
            for file in self.requirements_file:
                with open(file, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        package_name, *version = line.strip().split("==", 1)
                        version = version[0] if version else None
                        version = self._verify_requirement(package_name, version)
                        self.requirements[package_name] = version

        # Unable to Parse Requirements File
        except Exception:
            raise ValueError("Unable to process requirements file(s). Please ensure they are formatted correctly.")

    def load_python_version(self) -> None:
        # Retrieve Python Version
        try:
            self.version = self.config.get("version", "python")

        # No Python Version Specified
        except configparser.NoSectionError:
            self.version = None
            self.warnings = True
            warning("No version section was found in the configuration file.")

    def load_environment_variables(self) -> None:
        # Retrieve Environment Variables
        try:
            self.variables = dict(self.config.items("variables"))

        # No Environment Variables Specified
        except configparser.NoSectionError:
            self.variables = None
            self.warnings = True
            warning("No variables section was found in the configuration file.")
