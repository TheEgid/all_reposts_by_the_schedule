from __future__ import print_function
import glob
import os.path
import logging
import datetime
import threading
import time
from dotenv import load_dotenv
from flask import Flask
from services import get_file_metadata_from_gdrive
from services import authorize_google_drive
from services import download_and_save_file
from services import extract_file_id
from services import read_spreadsheet_range
from services import write_spreadsheet_cell
from services import authorize_google_spreadsheets
from publisher import post_telegram
from publisher import post_facebook
from publisher import post_vkontakte


def post_all(file_number, flags):
    if flags['vk'] == 'да':
        post_vkontakte(login=LOGIN_VK,
                       password=PASSWORD_VK,
                       token=TOKEN_VK,
                       vk_group=GROUP_ID_VK,
                       vk_group_album=GROUP_ID_ALBUM_VK,
                       file_number=file_number)
    if flags['tg'] == 'да':
        post_telegram(token=TOKEN_TG,
                      tg_channel=CHANNEL_TG,
                      file_number=file_number)
    if flags['fb'] == 'да':
        post_facebook(token=TOKEN_FB,
                      fb_group=GROUP_ID_FB,
                      file_number=file_number)


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
        logging.info(' It\'s date & time to publish - {}'.format(publish_moment))
        return True
    else:
        logging.info(' It\'s not a good date & time - {}'.format(publish_moment))
        return False


def select_already_published_flag(in_flag):
    out_flag = False
    if in_flag.lower() == "да":
        out_flag = True
    return out_flag


def check_spreadsheet(spreadsheets_service, drive_service, start_row=3):
    schedule_spreadsheet = read_spreadsheet_range(spreadsheets_service,
                                                  SHEETS_LINK, SHEETS_RANGE)
    last_column = len(schedule_spreadsheet[0])
    for row_counter, schedule_row in enumerate(schedule_spreadsheet,
                                               start=start_row):
        flag_vk, flag_tg, flag_fb, publish_day, publish_time, txt_id, img_id, \
        published_flag = schedule_row
        if select_already_published_flag(published_flag) is True:
            continue

        flags = {'vk': flag_vk, 'tg': flag_tg, 'fb': flag_fb}
        all_content = [x if extract_file_id(x) is None else extract_file_id(x)
                       for x in [txt_id, img_id]]

        publish_moment = check_publish_moment(publish_day, publish_time)
        if publish_moment:
            content_list = [get_file_metadata_from_gdrive(drive_service, x)
                            for x in all_content]

            [download_and_save_file(x['file_link'], x['file_title'],
                                    row_counter) for x in content_list if x is not None]

            post_all(row_counter, flags)
            cell_address = (row_counter, last_column)
            write_spreadsheet_cell(spreadsheets_service, SHEETS_LINK,
                                   cell_address)
            for new_file in glob.glob('content_folder/*'):
                os.remove(new_file)
            logging.info(' Update sheets in cell {}'.format(cell_address))


activate_job = Flask(__name__)
@activate_job.before_first_request
def start_flask_server(time_sleep):
    def run_job():
        # authorization at the time of server startup. Cycle authorization better??
        spreadsheets_service = authorize_google_spreadsheets()
        drive_service = authorize_google_drive()
        while True:
            logging.info(' Server is woken by command')
            check_spreadsheet(spreadsheets_service, drive_service)
            logging.info(' Server went to sleep')
            time.sleep(time_sleep)
    try:
        thread = threading.Thread(target=run_job)
        thread.start()
    except KeyboardInterrupt:
        exit(1)


if __name__ == '__main__':
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

    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
    logging.basicConfig(level=logging.INFO)
    start_flask_server(time_sleep=300)


