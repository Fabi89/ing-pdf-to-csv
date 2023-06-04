# ing-pdf-to-csv.py

Transforms an ING DIBA PDF (Kontoauszug) into a CSV file.

Cite of https://github.com/mkoderer:
> Import works fine with [MoneyMoney](https://moneymoney-app.com/).

I can not confirm that, because I don't know or use it. Have a try.

# Installation

## Unix

Preferably set up your local virtual environment once (e.g. `python3 -m venv .venv`)
and enter virtual environment (`. .venv/bin/activate`).

Convert PDFs to CSV with
```bash
pip3 install pdftotext
python3 ing-pdf-to-csv.py *.pdf > result.csv
```

## Windows

Please install pdftotext and add it to your PATH.
