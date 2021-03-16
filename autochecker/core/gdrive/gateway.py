from dataclasses import astuple
from importlib.resources import path

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from core.submittion import StudentSubmission


class GoogleSheetGateway:
    def __init__(self):
        self._sheet_url = "https://docs.google.com/spreadsheets/d/1xIcsnWsh-miT9AN86ujW_8cF2ixtyXWkEiwBlk_eMj4/edit#gid=0"

    def _get_creds(self):
        from core import gdrive

        creds_name = "azureml-autochecker-8825d6ffcb15.json"
        with path(gdrive, creds_name) as google_credentials_path:
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_path, scopes)
            return credentials

    def _google_client(self):
        return gspread.authorize(self._get_creds())

    def _get_sheet_by_url(self, url: str):
        google_client = self._google_client()
        sheet = google_client.open_by_url(url)
        return sheet

    def add_new_submission(self, student_submission: StudentSubmission) -> None:
        worksheet = self._get_sheet_by_url(self._sheet_url).worksheet("Results")
        row_values = astuple(student_submission)
        worksheet.append_row(row_values)
