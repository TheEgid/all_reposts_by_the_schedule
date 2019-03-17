from __future__ import print_function
import pickle
import os.path
import logging
import datetime
import threading
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv
from flask import Flask
from services import get_file_metadata_from_gdrive
from services import save_files
from services import extract_google_spreadsheet_id
from services import extract_file_id
from services import create_google_color


logging.basicConfig(level=logging.INFO)
load_dotenv()
SHEETS_LINK = os.getenv("SHEETS_LINK")
SHEETS_RANGE = os.getenv("SHEETS_RANGE")
LOGIN_VK = os.getenv("LOGIN_VK")
PASSWORD_VK = os.getenv("PASSWORD_VK")
TOKEN_VK = os.getenv("TOKEN_VK")
GROUP_ID_VK = os.getenv("GROUP_ID_VK")
GROUP_ID_ALBUM_VK = os.getenv("GROUP_ID_ALBUM_VK")
TOKEN_TG = os.getenv("TOKEN_TG")
CHANNEL_TG = os.getenv("CHANNEL_TG")
TOKEN_FB = os.getenv("TOKEN_FB")
GROUP_ID_FB = os.getenv("GROUP_ID_FB")
activate_job = Flask(__name__)


def interact_spreadsheet(link, range, mode='read', cell_address=None):
    spreadsheet_id = extract_google_spreadsheet_id(link)
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
                client_secrets_file='client_secrets.json')
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
    if mode == 'read':
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range,
                                    valueRenderOption='FORMULA').execute()
        return result.get('values', [])

    if mode == 'write':
        row, column = cell_address
        service = build('sheets', 'v4', credentials=creds)
        requests = [{'repeatCell': {
            'range': {'sheetId': 0, 'startRowIndex': row-1, 'endRowIndex': row,
                      'startColumnIndex': column-1, 'endColumnIndex': column},
            'cell': {'userEnteredValue': {'stringValue': 'да'},
                     'userEnteredFormat': {
                         'backgroundColor': create_google_color(217, 234, 211)}},
            'fields': 'userEnteredValue,userEnteredFormat(backgroundColor)'}}]
        body = {'requests': requests}
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,body=body).execute()


def check_publish_moment(publish_day, publish_time):
    all_days = {'понедельник': 0, 'вторник': 1, 'среда': 2, 'четверг': 3,
                'пятница': 4, 'суббота': 5, 'воскресенье': 6}
    now = datetime.datetime.now()
    future_day = datetime.date(now.year, now.month, now.day)
    while future_day.weekday() != all_days[publish_day.lower()]:
        future_day += datetime.timedelta(days=1)
    publish_moment = datetime.datetime.combine(future_day, datetime.time(publish_time))
    if (now.year == publish_moment.year) and \
            (now.month == publish_moment.month) and \
            (now.day == publish_moment.day) and \
            (now.hour == publish_moment.hour):
        logging.info('It\'s date & time to publish - {}'.format(publish_moment))
        return True
    else:
        logging.info('It\'s not a good date & time - {}'.format(publish_moment))
        return False


def check_spreadsheet():
    schedule_spreadsheet = interact_spreadsheet(SHEETS_LINK, SHEETS_RANGE,
                                                mode='read', cell_address=None)
    row_counter = 2
    last_column = 8
    for schedule_row in schedule_spreadsheet:
        if len(schedule_row) != last_column:
             raise ValueError('Incorrect! Check the schedule spreadsheet!')
        flag_vk, flag_tg, flag_fb, publish_day, publish_time, txt_id, img_id, \
                                            non_published_flag = schedule_row
        row_counter += 1
        if non_published_flag.lower() != "нет":
            pass
        else:
            flags = {'vk': flag_vk, 'tg': flag_tg, 'fb': flag_fb}
            all_content = [x if extract_file_id(x) is None else extract_file_id(x)
                           for x in [txt_id, img_id]]
            publish_moment = check_publish_moment(publish_day, publish_time)
            if publish_moment:
                content_list = list(map(get_file_metadata_from_gdrive, all_content))
                for x in content_list:
                    save_files(x['file_link'], x['file_title'])

                cell_address = (row_counter, last_column)
                interact_spreadsheet(SHEETS_LINK, SHEETS_RANGE,
                                     mode='write', cell_address=cell_address)
                logging.info('Update sheets in cell {}'.format(cell_address))
    return 'OK'


@activate_job.before_first_request
def main():
    def run_job():
        while True:
                logging.info('Server is woken by command')
                check_spreadsheet()
                logging.info('Server went to sleep')
                time.sleep(300)
    try:
        thread = threading.Thread(target=run_job)
        thread.start()
    except KeyboardInterrupt:
        exit(1)


if __name__ == '__main__':
    main()


    #check_spreadsheet()

    #print('https://docs.google.com/spreadsheets/d/1vX-iA5gAls4K1gYOCYasKXidAQ7vcCgkpgKbZi9OUk0/edit#gid=0')

