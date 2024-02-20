Mumbo-Jumbo: A Template-Based Project Generator 🚀
========================================================================================================================



🧐 About
------------------------------------------------------------------------------------------------------------------------


A template-based project generator that takes care of all the mumbo-jumbo.



🏁 Getting Started
------------------------------------------------------------------------------------------------------------------------


The repository uses [`just`](https://github.com/casey/just) (a build tool like `Makefile`) to automate common tasks such
as testing, building, etc.
To list all available recipes, run the following command in the project directory:

```bash
$ just -l
Available recipes:
    build-docs                 # Builds the documentation.
    build-library              # Builds the library.
    clean                      # Cleans up all generated files.
    mj-apply *args             # Runs the entry point mj-apply.
    publish-library            # Builds and publishes the library in the PyPI.
    publish-test-library       # Builds and publishes the library in the TestPyPI.
    test                       # Runs all unit tests in the test directory.
    test-with-coverage         # Runs all unit tests in the test directory with coverage.
    update-version-to-snapshot # Updates the current version of the library to a snapshot version.
```

Furthermore, [Poetry](https://python-poetry.org/) is used to manage dependencies, which provides a virtualenv
environment that readily contains all dependencies required for development, testing, and building.

> ☝️You have to run `poetry install` (in the project root) after cloning this repository for the environment to be
> created.

To use the environment from the shell, run either `poetry run ...` to execute a single command or `poetry shell` to
permanently activate the environment.



🏗 CI/CD
------------------------------------------------------------------------------------------------------------------------


This project makes use of a simple CI/CD pipeline that consists of the following steps:

1. On every push, all tests are executed.
2. If the tests finished successfully, then the library is published in the PyPI.
   To that end:
   1. If the push did **not** occur on the `main` branch, then a snapshot version is built and published.
      The version of the published library is the same as the project version (specified in
      [`pyproject.toml`](/pyproject.toml)) with `.dev` and a timestamp appended (e.g., `1.2.3.dev20220626103456`).
   2. If the push occurred on the `main` branch, then a release version is built and published. In addition
      to this, the commit is tagged with the version of the released artifacts with `v` prepended (e.g., `v1.2.3`).

For the CI/CD pipeline to work, the following secrets have to be in place:

| Secret       | Description                                                                          |
|--------------|--------------------------------------------------------------------------------------|
| `PYPI_TOKEN` | An API token that has permission to publish in the `mumbojumbo` project in the PYPI. |



✍️ Authors
------------------------------------------------------------------------------------------------------------------------


* Patrick Hohenecker ([patrick.hohenecker@gmx.at](mailto:patrick.hohenecker@gmx.at))
