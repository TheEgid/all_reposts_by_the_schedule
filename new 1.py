import datetime
from urllib.parse import parse_qsl
from urlextract import URLExtract

schedule_spreadsheet = [['нет', 'да', 'нет', 'пятница', 14, '=HYPERLINK("https://drive.google.com/open?id=1Wthk5k2ucVXpsa_J2F9TTflA2ztjcarLu81Rtb05ps8";"Лапы")', '=HYPERLINK("https://drive.google.com/open?id=1zljULNgX1h1sS9x4iWLaDZQEVEMNf5PH";"Лапы")', 'нет'], ['да', 'да', 'да', 'суббота', 15, '=HYPERLINK("https://drive.google.com/open?id=1kBFAOegBzmoC7I9ufv8rmFFqcSGqwA90ClE8hJ9cGFE";"Обоняние")', '=HYPERLINK("https://drive.google.com/open?id=1LEltAYogLBboyXgdyVH_1rW6Flr3zzjm";"Обоняние")', 'нет'], ['нет', 'да', 'да', 'четверг', 19, '=HYPERLINK("https://drive.google.com/open?id=1mS2RZO-TvhXZXqWQKx5AiWtCF-gkJHGAqtk59pAsHqA";"Усы")', '=HYPERLINK("https://drive.google.com/open?id=12V8spqPdepdMVflmcIoXMNb2SHlc7zdS";"Усы")', 'нет'], ['нет', 'нет', 'да', 'вторник', 19, '=HYPERLINK("https://drive.google.com/open?id=18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ";"Одиночество")', '=HYPERLINK("https://drive.google.com/open?id=1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i";"Одиночество")', 'да'], ['да', 'нет', 'нет', 'суббота', 15, '=HYPERLINK("https://drive.google.com/open?id=1iRiqwfofCqNRrsVVP0Sv6Tk5CkWfVztk2hJRzySNQlo";"Темнота")', '=HYPERLINK("https://drive.google.com/open?id=1eIzluX3xvZRiALjX-PQZeHNrHHHMjRJ1";"Темнота")', 'да'], ['да', 'да', 'нет', 'понедельник', 13, '=HYPERLINK("https://drive.google.com/open?id=1-gnx8kZnS8FZUd4DaoShb4RPD7D3n8wQxhVMRmUN7BI";"Про кошек")', '=HYPERLINK("https://drive.google.com/open?id=1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB";"Кошки")', 'нет'], ['нет', 'нет', 'да', 'четверг', 12, '=HYPERLINK("https://drive.google.com/open?id=1Wthk5k2ucVXpsa_J2F9TTflA2ztjcarLu81Rtb05ps8";"Лапы")', '=HYPERLINK("https://drive.google.com/open?id=1zljULNgX1h1sS9x4iWLaDZQEVEMNf5PH";"Лапы")', 'да'], ['да', 'нет', 'нет', 'пятница', 10, '=HYPERLINK("https://drive.google.com/open?id=1mS2RZO-TvhXZXqWQKx5AiWtCF-gkJHGAqtk59pAsHqA";"Усы")', '=HYPERLINK("https://drive.google.com/open?id=12V8spqPdepdMVflmcIoXMNb2SHlc7zdS";"Усы")', 'нет'], ['нет', 'да', 'нет', 'суббота', 14, '=HYPERLINK("https://drive.google.com/open?id=18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ";"Одиночество")', '=HYPERLINK("https://drive.google.com/open?id=1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i";"Одиночество")', 'нет'], ['да', 'нет', 'нет', 'понедельник', 16, '=HYPERLINK("https://drive.google.com/open?id=18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ";"Одиночество")', '=HYPERLINK("https://drive.google.com/open?id=1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i";"Одиночество")', 'да'], ['нет', 'да', 'да', 'четверг', 21, '=HYPERLINK("https://drive.google.com/open?id=1iRiqwfofCqNRrsVVP0Sv6Tk5CkWfVztk2hJRzySNQlo";"Темнота")', '=HYPERLINK("https://drive.google.com/open?id=1eIzluX3xvZRiALjX-PQZeHNrHHHMjRJ1";"Темнота")', 'да'], ['нет', 'нет', 'да', 'вторник', 10, '=HYPERLINK("https://drive.google.com/open?id=1-gnx8kZnS8FZUd4DaoShb4RPD7D3n8wQxhVMRmUN7BI";"Про кошек")', '=HYPERLINK("https://drive.google.com/open?id=1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB";"Кошки")', 'нет']]
#schedule_row = ['нет', 'нет', 'да', 'вторник', 10, '=HYPERLINK("https://drive.google.com/open?id=1-gnx8kZnS8FZUd4DaoShb4RPD7D3n8wQxhVMRmUN7BI";"Про кошек")', '=HYPERLINK("https://drive.google.com/open?id=1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB";"Кошки")', 'нет']


def extract_file_id(text):
  text= str(text)
  try:
      _text = URLExtract().find_urls(text)[0]
      return parse_qsl(_text)[0][1]
  except IndexError:
      return None

def check_publish_moment(publish_day, publish_time):
	all_days = {'понедельник':0, 'вторник':1, 'среда':2, 'четверг':3, 'пятница':4, 'суббота':5, 'воскресенье':6}
	now = datetime.datetime.now()
	future_day = datetime.date(now.year, now.month, now.day)
	while future_day.weekday() != all_days[publish_day.lower()]: 
		future_day += datetime.timedelta(days=1)
	publish_moment = datetime.datetime.combine(future_day, datetime.time(publish_time))
	if (now.year == publish_moment.year) and (now.month == publish_moment.month) and (now.day == publish_moment.day) and (now.hour == publish_moment.hour):
		print('start')
		return True
	else:
		print('рано! '+str(publish_moment)+' '+str(now))
		return False

		
def check_spreadsheet(schedule_spreadsheet, non ="нет"):
	for schedule_row in schedule_spreadsheet:
		if len(schedule_row) != 8:
			raise ValueError('Incorrect! Check the schedule spreadsheet!')
		flag_vk, flag_tg, flag_fb, publish_day, publish_time, txt_id, img_id, non_published_flag = schedule_row
		if non_published_flag.lower() != non:
			print('уже',non_published_flag)
			pass
		else:
			flags = {'vk':flag_vk, 'tg': flag_tg, 'fb': flag_fb}
			content = [x if extract_file_id(x) is None else extract_file_id(x) for x in [txt_id, img_id]]
			publish_moment = check_publish_moment(publish_day, publish_time)
			if publish_moment:
				print('gogogo')
				print(content)
				print(flags, flags['vk'])

			
check_spreadsheet(schedule_spreadsheet)
