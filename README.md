# ING PDF to CSV Converter

Transforms an ING DiBa PDF (Kontoauszug) into a CSV file.

Cite of [original author](https://github.com/mkoderer):
> Import works fine with [MoneyMoney](https://moneymoney-app.com/).

I can not confirm that, because I don't know or use it. Have a try.

# Installation

## Unix

### Poetry Project

This project is powered by `poetry`.
All examples are based on `poetry` and an initial `poetry install` call.
You can enter `poetry`s virtual environment by `poetry shell`.
`poetry` manages your virtual environment itself, so if you prefix your project-specific commands with `poetry run`, you should not get into touch with environment handling.

### Install

Make sure your system has all prerequisites of `pdftotext` installed, see [PyPI package#OS Dependencies](https://pypi.org/project/pdftotext/).

Once, install `pdftotext` and other dependencies by `poetry` with

```bash
# poetry
poetry install
```

### Add Data

I keep my ING data out of the project, but want to have the used sources near the results, so I use the git ignored `data` and `output` directories.
This is not necessary and should be easy to skip by changing the `main.py` call described later to your needs.

```bash
ING_YEAR=2023
mkdir -p "./data/$ING_YEAR"
cp -t "./data/$ING_YEAR" "<path_to_pdfs>"/Girokonto_*_Kontoauszug_{$ING_YEAR*,$((ING_YEAR+1))01*}.pdf
```

### Run Converter

Convert PDFs to CSV with

```bash
mkdir -p output
poetry run python3 main.py ./data/"$ING_YEAR"/*.pdf > "output/${ING_YEAR}_result.csv"
```

### Run by Script

You can also use the simplified `run.sh` script, as follows: 

```bash
./run.sh "<PATH_TO_ING_RESOURCES>" "<YEAR>" "<PREFIX_FOR_DATA_DIR_AND_RESULTS_CSV>"
```

## Windows

Please install `pdftotext` and add it to your `PATH`.
