import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(".") / "interfax.env")
login_prod = 'pgkweb_gate'
#login_test = os.getenv("INTERFAX_LOGIN")
password_prod = 'NYo2ld8'
#password_test = os.getenv("INTERFAX_PASSWORD")

ENDPOINT_prod = "https://api.spark-interfax.ru/IfaxWebService/"
#ENDPOINT_prod = "http://webservicefarm.interfax.ru/IfaxWebService/ifaxwebservice.asmx?WSDL"
ENDPOINT_test = "http://sparkgatetest.interfax.ru/iFaxWebService/iFaxWebService.asmx?WSDL"


def locate_schema_file(filename: str):
    return str(Path(".") / "schemas" / filename)


# INTERFAX_LOGIN=pgkwebGate
# INTERFAX_PASSWORD=hQb4nbV
# INTERFAX_LOGIN_prod=pgkweb_gate
# INTERFAX_PASSWORD_prod=NYo2ld8