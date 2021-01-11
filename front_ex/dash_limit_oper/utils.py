import pyhdb
import datetime as dt
from datetime import datetime
import numpy as np 


def get_connection():
    connection_hana = pyhdb.connect(
            host = "sap-db-s4q.sap.tc",
            port = 30115,
            user = "PGKAUDIT",
            password = "Rfh,jyfhf20"
            )
    return connection_hana