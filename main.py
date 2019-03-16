from __future__ import print_function
import pickle
import os.path
import logging
import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from services import get_file_metadata_from_gdrive
from services import save_file
from services import extract_google_spreadsheet_id
from services import extract_file_id



def get_spreadsheet(link, range_name):
    spreadsheet_id = extract_google_spreadsheet_id(link)
    creds = None
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(scopes=SCOPES,
                                    client_secrets_file='client_secrets.json')
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name,
                                valueRenderOption='FORMULA').execute()
    try:
        return result.get('values', [])
    except (ValueError, KeyError, ModuleNotFoundError):
        return None



def check_publish_moment(publish_day, publish_time):
    all_days = {'понедельник':0, 'вторник':1, 'среда':2, 'четверг':3,
                'пятница':4, 'суббота':5, 'воскресенье':6}
    now = datetime.datetime.now()
    future_day = datetime.date(now.year, now.month, now.day)
    while future_day.weekday() != all_days[publish_day.lower()]:
        future_day += datetime.timedelta(days=1)
    publish_moment = datetime.datetime.combine(future_day, datetime.time(publish_time))
    if (now.year == publish_moment.year) and \
            (now.month == publish_moment.month) and \
            (now.day == publish_moment.day) and \
            (now.hour == publish_moment.hour):
        logging.info('It\'s time to publish- '.format(publish_moment))
        print('start')
        return True
    else:
        logging.info('Still too early - '.format(publish_moment))
        return False


def check_spreadsheet(schedule_spreadsheet, non="нет"):
    for schedule_row in schedule_spreadsheet:
        if len(schedule_row) != 8:
            raise ValueError('Incorrect! Check the schedule spreadsheet!')
        flag_vk, flag_tg, flag_fb, publish_day, publish_time, txt_id, img_id, non_published_flag = schedule_row
        if non_published_flag.lower() != non:
            logging.info('Already published - '.format(non_published_flag))
            pass
        else:
            flags = {'vk': flag_vk, 'tg': flag_tg, 'fb': flag_fb}
            all_content = [x if extract_file_id(x) is None else extract_file_id(x) for x in [txt_id, img_id]]
            publish_moment = check_publish_moment(publish_day, publish_time)
            if publish_moment:
                content = list(map(get_file_metadata_from_gdrive, all_content))
                s = [save_file(x['file_link'], x['file_title']) for x in content]



if __name__ == '__main__':
    spreadsheet_link = 'https://docs.google.com/spreadsheets/d/10kRjz6TXNHtlEWaOTgMB0RZ_eLz8I6DZwEo78d9R9Bs/edit#gid=0'
    RANGE_NAME = 'Лист1!A3:H100000'
    spreadsheet = get_spreadsheet(spreadsheet_link, RANGE_NAME)
    #print(spreadsheet)
    check_spreadsheet(spreadsheet)

