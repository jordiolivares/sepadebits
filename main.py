import sys
import datetime
import argparse

import fintech
import pandas as pd
fintech.register()
from fintech.sepa import Account, SEPADirectDebit


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-t", "--destination-iban", type=str, required=True, help="IBAN to transfer the SEPA debits to")
arg_parser.add_argument("-i", "--creditor-id", type=str, required=True, help="Creditor ID")
arg_parser.add_argument("-n", "--creditor-name", type=str, required=True, help="Creditor name")
arg_parser.add_argument("--creditor-country", type=str, required=False, help="Creditor Country in ISO-3166 ALPHA 2 format")
arg_parser.add_argument("--creditor-city", type=str, required=False, help="Creditor city")
arg_parser.add_argument("-m", "--mandate", type=str, required=True, help="Mandate in Python {} string formatting style, supports the variables: 'id'")
arg_parser.add_argument("-c", "--concept", type=str, required=True, help="Concept in Python {} string formatting style, supports the variables: 'id'")
arg_parser.add_argument("-f", "--input-file", required=True, type=argparse.FileType('r'), help="CSV input file")
arg_parser.add_argument("-o", "--output-file", required=False, type=argparse.FileType('w'), default=sys.stdout)
arg_parser.add_argument("-d", "--due-date", required=True, type=datetime.date.fromisoformat, help="CSV input file")
arg_parser.add_argument("--iban-column", required=True, type=str)
arg_parser.add_argument("--name-column", required=True, type=str)
arg_parser.add_argument("--id-column", required=True, type=str)
arg_parser.add_argument("--amount-column", required=True, type=str)
args = arg_parser.parse_args()

IBAN = args.destination_iban
CREDITOR_ID = args.creditor_id
NAME = args.creditor_name
COUNTRY = args.creditor_country
CITY = args.creditor_city
CONCEPT = args.concept
MANDATE = args.mandate

creditor = Account(iban=IBAN, name=NAME, country=COUNTRY, city=CITY)
creditor.set_creditor_id(CREDITOR_ID)

sdd = SEPADirectDebit(creditor, 'CORE')

df = pd.read_csv(args.input_file, quotechar='"')
for _, row in df.iterrows():
    try:
        debtor = Account(iban=row[args.iban_column].replace(' ', ''), name=row[args.name_column])
        debtor.set_mandate(mref=MANDATE.format(id=row[args.id_column]), signed=datetime.date.today(), recurrent=False)
        sdd.add_transaction(account=debtor, amount=row[args.amount_column], purpose=CONCEPT.format(id=row[args.id_column]), due_date=args.due_date)
    except:
        _, exc_obj, _ = sys.exc_info()
        print("{} - {} / {}".format(row[args.id_column], row[args.iban_column], str(exc_obj)), file=sys.stderr)
args.out_file.write(sdd.render())

