from setuptools import setup, find_packages

setup(
    name="pyenvsync",
    version="0.0.2",
    description=("PySyncEnv assists with synchronizing and validating Python workspaces "
                 "across users and devices, ensuring seamless collaboration and consistent setups."),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mitchell Gottlieb",
    url="https://github.com/mitchell-gottlieb/pyenvsync",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
    ],
    entry_points={
        "console_scripts": [
            "pyenvsync = pyenvsync.main:main",
        ],
    },
)
