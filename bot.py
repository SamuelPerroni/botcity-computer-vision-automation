import pandas as pd

from config.const import *
from workflows.invoices_record import InvoiceRecord

invoices_df = pd.read_excel(PATH_INVOICES)


bot = InvoiceRecord(PATH_APP)

if bot.open_app():
    try:
        print("Successfully opened Contoso application.")
        print("\nStarting to process invoices...")

        # Writes each row of the DataFrame to the Contoso application
        for row in invoices_df.itertuples():
            invoice = bot.invoice_record(
                date=str(row[1]),
                account=str(row[2]),
                contact=str(row[3]),
                amount=int(row[4]),
                status=str(row[5]),
            )
            print(invoice)

    finally:
        bot.close_app()
        print("\n...Contoso application closed.")
        print("\nFinished processing invoices.")

else:
    print("\nFailed to open Contoso application.")
