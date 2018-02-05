import sys
import datetime

import fintech
import pandas as pd
fintech.register()
from fintech.sepa import Account, SEPADirectDebit

IBAN_ACP = "XXXXXX"
CREDITOR_ID_ACP = "XXXXXX"
NAME = "Associació Catalana de Puntaires"
COUNTRY = "ES"
CITY = "Barcelona"

CONCEPT = "Cuota anual Associació Catalana de Puntaires - Sòci/a {}"
MANDATE = "ACP-2018-{}"
REFERENCE = "ACP-2018-{}-1"

creditor = Account(iban=IBAN_ACP, name=NAME, country=COUNTRY, city=CITY)
creditor.set_creditor_id(CREDITOR_ID_ACP)

sdd = SEPADirectDebit(creditor, 'CORE')

df = pd.read_csv(sys.argv[1], quotechar='"')
for _, row in df.iterrows():
    try:
        debtor = Account(iban=row['IBAN'].replace(' ', ''), name=row['NOM'])
        debtor.set_mandate(mref=MANDATE.format(row['SECCIO']), signed=datetime.date.today(), recurrent=False)
        sdd.add_transaction(debtor, row['CUOTA'], CONCEPT.format(row['SECCIO']), due_date=datetime.date(2018, 1, 26))
    except ValueError as ex:
        print("{} / {} - {}".format(str(ex), row['SECCIO'], row['IBAN']))
with open(sys.argv[2], mode='wb') as f:
    f.write(sdd.render())

