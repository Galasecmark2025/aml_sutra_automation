import pyodbc
from datetime import datetime

def get_db_connection(DataServerName, LoginName, LoginPassword, logger):
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={DataServerName};"
        f"UID={LoginName.strip()};"
        f"PWD={LoginPassword.strip()};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    print("Trying to connect...")

    db = pyodbc.connect(conn_str,timeout=15)

    if logger: logger.info("Connected!")

    return db

def get_execution_dates(bkmcode, exccode=None, database_name=None, logger=None):
    db = None
    try:
        db = get_db_connection(
            DataServerName="160.30.125.196,10222",
            LoginName="ComtekAdmin",
            LoginPassword="ComTek@dm!n123", 
            logger=logger
        )
        curr_date = datetime.today().strftime("%Y%m%d")
        print(curr_date)
        cursor = db.cursor()
        exccode_cond = f"and exccode = {exccode}" if exccode else ""
        cursor.execute(f"select distinct PTradeDate from {database_name}..CalenderBE where trxdate='{curr_date}' and BkmCode={bkmcode} {exccode_cond}")

        row = cursor.fetchone()
        ptradedate = row[0].strftime("%d/%m/%Y") if row and row[0] else None
        # required date format: DD/MM/YYYY
        return ptradedate

    except Exception as e:
        print("Full error:")
        print(repr(e))
        return None, None

    finally:
        try:
            if db and db.connected != 0:
                db.close()
                if logger: logger.info("Connection closed.")
        except Exception:
            pass
        
if __name__ == "__main__":
    print(get_execution_dates("11"))