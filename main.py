
from __future__ import print_function
import pickle
import os.path
import logging
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv
from services import get_file_metadata_from_gdrive
from services import save_files
from services import extract_google_spreadsheet_id
from services import extract_file_id



def interact_spreadsheet(link, range, mode='read', updatedcell=None):
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

    elif mode == 'write':
        body = {'values': [['да']]}
        service = build('sheets', 'v4', credentials=creds)
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=updatedcell,
            valueInputOption='USER_ENTERED', body=body).execute()

        # requests = [{
        #     "repeatCell": {
        #         "range": {
        #             "sheetId": 0,
        #             "startRowIndex": 0,
        #             "endRowIndex": 1
        #         },
        #         "cell": {
        #             "userEnteredValue": {
        #                 "stringValue": 'string'
        #             },
        #             "userEnteredFormat": {
        #                 "backgroundColor": {
        #                     "red": 0.0,
        #                     "green": 0.0,
        #                     "blue": 0.0
        #                 },
        #                 "horizontalAlignment": "CENTER",
        #                 "textFormat": {
        #                     "foregroundColor": {
        #                         "red": 1.0,
        #                         "green": 1.0,
        #                         "blue": 1.0
        #                     },
        #                     "fontSize": 12,
        #                     "bold": True
        #                 }
        #             }
        #         },
        #         "fields": "userEnteredValue,userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
        #     }
        # }, {
        #     "updateSheetProperties": {
        #         "properties": {
        #             "sheetId": 0
        #         },
        #         "fields": "gridProperties.frozenRowCount"
        #     }
        # }]
        #
        # body = {
        #     'requests': requests
        # }
        #
        # response = service.spreadsheets().batchUpdate(
        #     spreadsheetId=spreadsheet_id,
        #     body=body).execute()

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
        logging.info('It\'s time to publish - {}'.format(publish_moment))
        return True
    else:
        logging.info('It\'s not a good time - {}'.format(publish_moment))
        return False


def check_spreadsheet():
    schedule_spreadsheet = interact_spreadsheet(SHEETS_LINK, SHEETS_RANGE,
                                                mode='read', updatedcell=None)
    start_row_counter = 2
    sheet_columns_amount = 8
    sheet_columns_amount_letter = 'H'
    sheets_name = SHEETS_RANGE.split('!')[0]
    for schedule_row in schedule_spreadsheet:
        if len(schedule_row) != sheet_columns_amount:
             raise ValueError('Incorrect! Check the schedule spreadsheet!')
        flag_vk, flag_tg, flag_fb, publish_day, publish_time, txt_id, img_id, \
                                            non_published_flag = schedule_row
        start_row_counter += 1
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

                updatedcell = ''.join((sheets_name, "!",
                                       sheet_columns_amount_letter,
                                       str(start_row_counter)))
                interact_spreadsheet(SHEETS_LINK, SHEETS_RANGE,
                                     mode='write', updatedcell=updatedcell)
                logging.info('update spreadsheet in cell {}'.format(updatedcell))



if __name__ == '__main__':
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

    check_spreadsheet()


    print('https://docs.google.com/spreadsheets/d/1vX-iA5gAls4K1gYOCYasKXidAQ7vcCgkpgKbZi9OUk0/edit#gid=0')

