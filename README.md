# obelisk

A lightwight command line application for data transformations and interfacing
for reflectance calculations

## Installation

### Obelisk

Clone or download a `.zip` of the repository via github and
navigate to the repository directory.

### Poetry

[Install Poetry by following the directions here](https://python-poetry.org/docs/#installation)

### Install Dependencies

From the main `poetry` directory, issue the following on the command line:

`poetry install`

## Usage

Obelisk is a command-line application. You will usually want to navigate to the top-level obelisk directory (where this README is) in oder to use it. Here is a list of command line arguments:

`-c --convert`: convert file. (Currently the only mode of operation)

`-i --input-file`: an input file for conversion. Will prompt the user for input if not given.

`-d --destination`: a destination filepath for converted files. Will prompt the user for input if not given.

Since obelisk runs on poetry, it requires a `poetry run` command with command line arguments. For an example usage for conversion:

`poetry run python -m obelisk -c -i 'examples/input/p5Sample_MHDRS.tsv' -d 'examples/output/test'`

If relative filepaths are not working on your system, try absolute filepaths.

Additionally, a batchfile and Makefile command is available which will run in interactive mode, prompting the user for input and output filepath information. To use these, either run the batch file or (on UNIX systems equipped with the Make utility), `make convert`
