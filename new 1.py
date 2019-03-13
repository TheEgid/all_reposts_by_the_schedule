schedule_spreadsheet = [['нет', 'да', 'нет', 'вторник', 10, '=HYPERLINK("https://drive.google.com/open?id=1Wthk5k2ucVXpsa_J2F9TTflA2ztjcarLu81Rtb05ps8";"Лапы")', '=HYPERLINK("https://drive.google.com/open?id=1zljULNgX1h1sS9x4iWLaDZQEVEMNf5PH";"Лапы")', 'да'], ['да', 'да', 'да', 'суббота', 15, '=HYPERLINK("https://drive.google.com/open?id=1kBFAOegBzmoC7I9ufv8rmFFqcSGqwA90ClE8hJ9cGFE";"Обоняние")', '=HYPERLINK("https://drive.google.com/open?id=1LEltAYogLBboyXgdyVH_1rW6Flr3zzjm";"Обоняние")', 'нет'], ['нет', 'да', 'да', 'четверг', 19, '=HYPERLINK("https://drive.google.com/open?id=1mS2RZO-TvhXZXqWQKx5AiWtCF-gkJHGAqtk59pAsHqA";"Усы")', '=HYPERLINK("https://drive.google.com/open?id=12V8spqPdepdMVflmcIoXMNb2SHlc7zdS";"Усы")', 'нет'], ['нет', 'нет', 'да', 'вторник', 19, '=HYPERLINK("https://drive.google.com/open?id=18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ";"Одиночество")', '=HYPERLINK("https://drive.google.com/open?id=1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i";"Одиночество")', 'да'], ['да', 'нет', 'нет', 'суббота', 15, '=HYPERLINK("https://drive.google.com/open?id=1iRiqwfofCqNRrsVVP0Sv6Tk5CkWfVztk2hJRzySNQlo";"Темнота")', '=HYPERLINK("https://drive.google.com/open?id=1eIzluX3xvZRiALjX-PQZeHNrHHHMjRJ1";"Темнота")', 'да'], ['да', 'да', 'нет', 'понедельник', 13, '=HYPERLINK("https://drive.google.com/open?id=1-gnx8kZnS8FZUd4DaoShb4RPD7D3n8wQxhVMRmUN7BI";"Про кошек")', '=HYPERLINK("https://drive.google.com/open?id=1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB";"Кошки")', 'нет'], ['нет', 'нет', 'да', 'четверг', 12, '=HYPERLINK("https://drive.google.com/open?id=1Wthk5k2ucVXpsa_J2F9TTflA2ztjcarLu81Rtb05ps8";"Лапы")', '=HYPERLINK("https://drive.google.com/open?id=1zljULNgX1h1sS9x4iWLaDZQEVEMNf5PH";"Лапы")', 'да'], ['да', 'нет', 'нет', 'вторник', 16, '=HYPERLINK("https://drive.google.com/open?id=1mS2RZO-TvhXZXqWQKx5AiWtCF-gkJHGAqtk59pAsHqA";"Усы")', '=HYPERLINK("https://drive.google.com/open?id=12V8spqPdepdMVflmcIoXMNb2SHlc7zdS";"Усы")', 'нет'], ['нет', 'да', 'нет', 'суббота', 14, '=HYPERLINK("https://drive.google.com/open?id=18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ";"Одиночество")', '=HYPERLINK("https://drive.google.com/open?id=1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i";"Одиночество")', 'нет'], ['да', 'нет', 'нет', 'понедельник', 16, '=HYPERLINK("https://drive.google.com/open?id=18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ";"Одиночество")', '=HYPERLINK("https://drive.google.com/open?id=1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i";"Одиночество")', 'да'], ['нет', 'да', 'да', 'четверг', 21, '=HYPERLINK("https://drive.google.com/open?id=1iRiqwfofCqNRrsVVP0Sv6Tk5CkWfVztk2hJRzySNQlo";"Темнота")', '=HYPERLINK("https://drive.google.com/open?id=1eIzluX3xvZRiALjX-PQZeHNrHHHMjRJ1";"Темнота")', 'да'], ['нет', 'нет', 'да', 'вторник', 10, '=HYPERLINK("https://drive.google.com/open?id=1-gnx8kZnS8FZUd4DaoShb4RPD7D3n8wQxhVMRmUN7BI";"Про кошек")', '=HYPERLINK("https://drive.google.com/open?id=1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB";"Кошки")', 'нет']]

#schedule_row = ['нет', 'нет', 'да', 'вторник', 10, '=HYPERLINK("https://drive.google.com/open?id=1-gnx8kZnS8FZUd4DaoShb4RPD7D3n8wQxhVMRmUN7BI";"Про кошек")', '=HYPERLINK("https://drive.google.com/open?id=1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB";"Кошки")', 'нет']

from urllib.parse import parse_qsl
from urlextract import URLExtract

				
def extract_file_id(text):
  text= str(text)
  try:
      _text = URLExtract().find_urls(text)[0]
      return parse_qsl(_text)[0][1]
  except IndexError:
      return None

	  
def filter_schedule_row_to_publish(schedule_row, posting_day, non ="нет"):
	non_published_flag = schedule_row[7]
	if posting_day in schedule_row and non_published_flag == non:
		return schedule_row
	else:
		return None


def choice_schedule_row_to_publish(schedule_spreadsheet, posting_day):
	new_schedule_spreadsheet = []
	for schedule_row in schedule_spreadsheet:
	  new_schedule_row = filter_schedule_row_to_publish(schedule_row, posting_day)
	  if new_schedule_row is not None:
		  new_schedule_row = [x if extract_file_id(x) is None else extract_file_id(x) for x in new_schedule_row]
		  new_schedule_spreadsheet.append(new_schedule_row)
	return new_schedule_spreadsheet

	
def check_spreadsheet():
	pass

new_schedule_spreadsheet = choice_schedule_row_to_publish(schedule_spreadsheet, posting_day='суббота')
for row in new_schedule_spreadsheet:
	print(row)
	


###

s1 = ['нет', 'нет', 'да', 'вторник', 10, '1-gnx8kZnS8FZUd4DaoShb4RPD7D3n8wQxhVMRmUN7BI', '1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB', 'нет']	
	
def procss(schedule_row):
	if len(schedule_row) != 8:
		 return None
	flag_vk, flag_tg, flag_fb, publish_day, publish_time, txt_id, img_id, flag_published = schedule_row
	moment = [publish_day, publish_time]
	content = [txt_id, img_id]
	flags = [flag_vk, flag_tg, flag_fb]
	return moment, content, flags

print(procss(s1))		
		
mm = ['вторник', 10]


days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
print (days[datetime.date.today().weekday()])
