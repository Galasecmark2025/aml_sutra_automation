import pymssql
from datetime import datetime

def get_db_connection(DataServerName, LoginName, LoginPassword, logger=None):
    try:
        if logger:
            logger.info(f"Connecting to SQL Server: {DataServerName}")

        # If DataServerName is like "111.11.111.111,11111"
        if "," in DataServerName:
            server, port = DataServerName.split(",", 1)
            conn = pymssql.connect(
                server=server.strip(),
                port=int(port.strip()),
                user=LoginName.strip(),
                password=LoginPassword.strip(),
                timeout=15,
                login_timeout=15
            )
        else:
            conn = pymssql.connect(
                server=DataServerName.strip(),
                user=LoginName.strip(),
                password=LoginPassword.strip(),
                timeout=15,
                login_timeout=15
            )

        if logger:
            logger.info("Database connection established successfully")

        return conn

    except Exception as e:
        if logger:
            logger.exception(f"Database connection failed: {e}")
        raise

def get_execution_dates(config, bkmcode, exccode=None, database_name=None, range_required=False, from_date=None, to_date=None, logger=None):
    db = None
    data_server_name = config.get("data_server_name", "")
    server_username = config.get("server_username", "")
    server_password = config.get("server_password", "")
    try:
        db = get_db_connection(
            DataServerName=data_server_name,
            LoginName=server_username,
            LoginPassword=server_password, 
            logger=logger
        )
        cursor = db.cursor()
        if range_required:
            from_date_sql = datetime.strptime(from_date, "%d/%m/%Y").strftime("%Y%m%d")
            to_date_sql = datetime.strptime(to_date, "%d/%m/%Y").strftime("%Y%m%d")
            date_range_query = f"select distinct trxdate from {database_name}..Calenderbe where htradetype=0 and trxdate between '{from_date_sql}' and '{to_date_sql}'"
            logger.info(f"Query for fetching date range: {date_range_query}")
            cursor.execute(date_range_query)
            rows = cursor.fetchall()
            execution_dates = [row[0].strftime("%d/%m/%Y") for row in rows if row and row[0]]
            return execution_dates
        else:
            exccode_cond = f"and exccode = {exccode}" if exccode else ""
            curr_date = datetime.today().strftime("%Y%m%d")
            logger.info(f"Current date: {curr_date}")
            logger.info(f"Query for fetching date: select distinct PTradeDate from {database_name}..CalenderBE where trxdate='{curr_date}' and BkmCode={bkmcode} {exccode_cond}")
            cursor.execute(f"select distinct PTradeDate from {database_name}..CalenderBE where trxdate='{curr_date}' and BkmCode={bkmcode} {exccode_cond}")

            row = cursor.fetchone()
            ptradedate = row[0].strftime("%d/%m/%Y") if row and row[0] else None
            return ptradedate

    except Exception as e:
        logger.error("Full error:")
        logger.error(repr(e))
        if range_required:
            return []
        return None

    finally:
        try:
            if db and db.connected != 0:
                db.close()
                if logger: logger.info("Connection closed.")
        except Exception:
            pass
