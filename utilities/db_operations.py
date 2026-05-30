import pyodbc

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

    logger.info("Connected!")

    return db

def get_execution_dates(bkmcode, exccode, logger):
    db = None
    try:
        db = get_db_connection(
            DataServerName="160.30.125.196,10222",
            LoginName="ComtekAdmin",
            LoginPassword="ComTek@dm!n123", 
            logger=logger
        )

        cursor = db.cursor()
        cursor.execute(f"select distinct TrxDate,PTradeDate from SOSDevPmla..CalenderBE where trxdate='20260530' and BkmCode={bkmcode}")

        transaction_date, ptradedate = cursor.fetchall()[0]
        return transaction_date, ptradedate

    except Exception as e:
        print("Full error:")
        print(repr(e))

    finally:
        try:
            if db and db.connected != 0:
                db.close()
                logger.info("Connection closed.")
        except Exception:
            pass