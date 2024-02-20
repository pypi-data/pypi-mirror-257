from ._ouput import warning, step, success, error
from ._config import Config
from ._version import version, compare_versions
from ._requirements import compare_requirements
from ._variables import compare_variables


def main():
    # Any Critical Error is Caught and Analysis is Stopped
    try:
        # Load Configuration File
        step("Read Configuration File", linebreak=False)
        config = Config()

        # If No Warnings, Configuration File Loaded Successfully
        if not config.warnings:
            success("Configuration File Loaded.")

        # Check Python Version
        step("Check Python Version")

        # If No Python Version Specified, Skip Check
        if config.version is None:
            warning("No Python version specified. Nothing to check.")

        # If Python Version Specified, Check
        else:
            sys_version = version()
            matching_versions = compare_versions(sys_version, config.version)

            # If Python Version Matches, Success
            if matching_versions:
                success(f"Python Version '{sys_version}' matches.")

            # If Python Version Does Not Match, Warning
            else:
                warning(f"Local Python Version '{sys_version}' does not match '{config.version}'.")

        # Check Package Requirements
        # If No Package Requirements Specified, Skip Check
        if config.requirements is None:
            step("Check Package Requirements")
            warning("No package requirements specified. Nothing to check.")

        # If Package Requirements Specified, Check
        else:
            step(f"Check Package Requirements ({len(config.requirements)} Total)")
            matching_requirements = compare_requirements(config.requirements)

            # If All Package Requirements Match, Success
            if matching_requirements:
                success("All package requirements match.")

        # Check Environment Variables
        # If No Environment Variables Specified, Skip Check
        if config.variables is None:
            step("Check Environment Variables")
            warning("No environment variables specified. Nothing to check.")

        # If Environment Variables Specified, Check
        else:
            step(f"Check Environment Variables ({len(config.variables)} Total)")
            matching_variables = compare_variables(config.variables)

            # If All Environment Variables Match, Success
            if matching_variables:
                success("All environment variables match.")

        step("All Checks Complete. Please see above for details.")

    # Alert Any Critical Error and Stop Check
    except Exception as excp:
        error(message=str(excp))
