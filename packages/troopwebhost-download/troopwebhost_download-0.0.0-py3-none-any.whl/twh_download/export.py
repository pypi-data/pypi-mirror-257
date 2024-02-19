import requests
from pathlib import Path
import toml
from dotenv import dotenv_values

__version__ = "0.0.0"

CONFIG = toml.load("config.toml")
CONFIG |= dotenv_values(".env")

def login(session, username, password):
    payload = {
            'Selected_Action': 'login',
            'Menu_Item_ID': 49792,
            'Form_ID': 7323,
            'Pass': 1,
            'Current_URL': 'https://www.troopwebhost.org/formCustom.aspx',
            'User_Login': username,
            'User_Password': password,
            }
    p = session.post("https://www.troopwebhost.org/formCustom.aspx",
                     data=payload)
    return "Log Off" in p.text


def get_logged_in_session(username=CONFIG['username'], password=CONFIG['password']):
    with requests.Session() as session:
        session.cookies.set('Application_ID', str(CONFIG['troop_id']))
        if login(session, username, password):
            return session
        return None


def get_report(session, report_number):
    return session.get(f"https://www.troopwebhost.org/FormReport.aspx?Menu_Item_ID={report_number}&Stack=1&ReportFormat=XLS")


def main():
    if session := get_logged_in_session():
        for name, report_number in CONFIG["REPORTS"].items():
            with open(Path("output") / f"{CONFIG['troop_prefix']}{name}.csv", "wb") as f:
                f.write(get_report(session, report_number).content)


if __name__ == "__main__":
    main()

