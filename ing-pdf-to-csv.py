import logging
import os
import re
import sys
from re import Match
from subprocess import getstatusoutput

os.makedirs("log", exist_ok=True)
logging.basicConfig(filename=f"log/run.log",
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

date_pattern = r'\d\d\.\d\d\.\d\d\d\d'
first_line_pattern = r'\s+(%s)\s+(.*)\s+(-?[\d.]*\d{1,3},\d\d)' % date_pattern
sec_line_pattern = rf'\s+({date_pattern})(\s+(.*))?'


class Transaction:
    def __init__(self, first_line_match: Match):
        self.valuta = None
        self.text_lines = []
        self.second_line_index = -1
        self.has_second_line = False

        self.date = first_line_match.group(1)
        type_originator = first_line_match.group(2).rstrip()
        type_originator = type_originator.split(" ", 1)
        self.trans_type = type_originator[0]
        try:
            self.originator = type_originator[1]
        except IndexError:
            self.originator = self.trans_type
        self.value = first_line_match.group(3)

    def add_second_line(self, second_line_match: Match):
        self.valuta = second_line_match.group(1)
        second_line_text = second_line_match.group(3) if second_line_match.group(3) is not None else ''
        self.text_lines.append(second_line_text)
        self.second_line_index = second_line_match.span(3)[0] if second_line_match.group(3) else 0
        self.has_second_line = True

    def add_further_line(self, further_line_match: Match):
        self.text_lines.append(further_line_match.group(1))

    def build_csv_row(self):
        return ";".join([
            self.date,
            self.valuta,
            self.originator,
            self.trans_type,
            ' '.join(self.text_lines),
            self.value,
            "EUR",
            self.value,
            "EUR",
        ])

    def __str__(self):
        return self.build_csv_row()


# CSV header
print("Buchung;Valuta;Auftraggeber/Empfänger;Buchungstext;Verwendungszweck;Saldo;Währung;Betrag;Währung")

for fn in sys.argv[1:]:
    # we use iconv to ignore the encoding issues
    # TODO: better to use subprocess for this
    ret, output = getstatusoutput("pdftotext %s -layout -nopgbrk -| iconv --to-code utf-8//IGNORE" % fn)
    if ret != 0:
        print("Error while reading file %s:" % fn)
        raise Exception(output)

    logging.debug(output)

    transaction = None
    for line in output.split('\n'):
        match = re.match(first_line_pattern, line)
        if match:
            if transaction is None:
                # first match -> init transaction
                transaction = Transaction(match)
            elif transaction.has_second_line:
                # next match -> finish previous transaction and prepare new transaction
                print(transaction.build_csv_row())
                transaction = Transaction(match)

        else:
            if transaction is not None:
                match = re.match(sec_line_pattern, line)
                if match:
                    transaction.add_second_line(match)
                elif transaction.has_second_line and transaction.second_line_index > 0:
                    # match only lines, that start with correct number of spaces (aligned with second line <text>
                    # and do not end with value
                    match = re.match(r'^ {%d}(\w.*)' % transaction.second_line_index, line)  # (?!\s+-?\d+,\d\d$)
                    if match:
                        transaction.add_further_line(match)

    if transaction is not None and transaction.has_second_line:
        # finish last match -> print last transaction
        print(transaction.build_csv_row())
