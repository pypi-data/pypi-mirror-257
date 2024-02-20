# PyEnvSync
PyEnvSync assists with synchronizing and validating Python workspaces across users and devices, ensuring seamless collaboration and consistent setups.

## Key Features

- Verifies Your Python Version
- Ensures the Correct Dependencies Exist in Your Environment
- Validates that the Required Environment Variables Exist on Your System

## Installation
`pip install pyenvsync`

## Creating the Configuration File
This packages utilizes a configuration file named `pyenvsync.ini`. This file contains the following 3 sections:

1. **version**
    
    - Set `python` equal to the version of Python required.

2. **requirements**

    - Set paths to your requirements file(s). Typically there is only one but sometimes projects have multiple.
    - NOTE: For this section, the name of each entry does not matter. I often use `main` and `dev` but you can use whatever makes sense.

3. **variables**

    - Set each environment variable equal to a description explaining what that variable is.
    - NOTE: Capitalization matters for environment variables.

Example `pyenvsync.ini` configuration file:
```ini
[version]
python = 0.0.0

[requirements]
main = requirements.txt
dev = requirements-dev.txt

[variables]
VAR_NAME_1 = Variable Description
VAR_NAME_2 = Variable Description
```

## Example Usage
In terminal from the directory containing the `pyenvsync.ini` file, run the following command and view the results:

`pyenvsync` OR `python -m pyenvsync`

### Example Success
![Successful Output](https://raw.githubusercontent.com/mitchell-gottlieb/pyenvsync/master/assets/success.png)

### Example with Warnings
![Warnings](https://raw.githubusercontent.com/mitchell-gottlieb/pyenvsync/master/assets/warnings.png)

## Community
All future work items are tracked in the "PyEnvSync To-Do" Project. Please submit requests, create issues, or utilize discussions.
