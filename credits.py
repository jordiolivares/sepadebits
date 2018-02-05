import sys
import datetime

import fintech
import pandas as pd
fintech.register()

from fintech.sepa import SEPACreditTransfer, Account

IBAN_DEBTOR = "ES9121000418450200051332"
NAME = "NOM DE L'EMPRESA"
COUNTRY = "ES" # O qualsevol altre pais
CITY = "CIUTAT"

CREDITOR_ID = "A MIRAR-HO EN EL BANC, ALLÀ HI SURT"

deutor = Account(iban=IBAN_DEBTOR, name=NAME, country=COUNTRY, city=CITY)
deutor.set_creditor_id(CREDITOR_ID)

sct = SEPACreditTransfer(deutor, cutoff=20, cat_purpose="SALA") # SALA is the category code for Salary

# Accepta d'entrada un arxiu CSV separat per comes amb delimitador de text "
# Les columnes son IBAN, NOM, NOMINA

df = pd.read_csv(sys.argv[1], quotechar='"')
for _, row in df.iterrows():
    try:
        creditor = Account(iban=row['IBAN'].replace(' ', ''), name=row['NOM'])
        sct.add_transaction(creditor, row['NOMINA'], "Sou mes de Gener 2018")
    except ValueError as ex:
        print("IBAN malformat: {} / {}. Traceback: {}".format(row['IBAN'], row['NOM'], str(ex)))
with open(sys.argv[2], mode='wb') as f:
    f.write(sct.render())
