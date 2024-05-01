# ING PDF to CSV Converter

Transforms an ING DiBa PDF (Kontoauszug) into a CSV file.

Cite of [original author](https://github.com/mkoderer):
> Import works fine with [MoneyMoney](https://moneymoney-app.com/).

I can not confirm that, because I don't know or use it. Have a try.

# Installation

## Unix

### Install

Preferably run with `poetry` (all examples are based on this) or set up your local virtual environment (once do e.g. `python3 -m venv .venv`) and enter virtual environment (`. .venv/bin/activate`).

If not already done, install `pdftotext` like

```bash
poetry add pdftotext
# or in virtual env
pip install pdftotext
```

### Add Data

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
