[['нет', 'да', 'нет', 'вторник', 10, '=HYPERLINK("https://drive.google.com/open?id=1Wthk5k2ucVXpsa_J2F9TTflA2ztjcarLu81Rtb05ps8";"Лапы")', '=HYPERLINK("https://drive.google.com/open?id=1zljULNgX1h1sS9x4iWLaDZQEVEMNf5PH";"Лапы")', 'да'], ['да', 'да', 'да', 'суббота', 15, '=HYPERLINK("https://drive.google.com/open?id=1kBFAOegBzmoC7I9ufv8rmFFqcSGqwA90ClE8hJ9cGFE";"Обоняние")', '=HYPERLINK("https://drive.google.com/open?id=1LEltAYogLBboyXgdyVH_1rW6Flr3zzjm";"Обоняние")', 'нет'], ['нет', 'да', 'да', 'четверг', 19, '=HYPERLINK("https://drive.google.com/open?id=1mS2RZO-TvhXZXqWQKx5AiWtCF-gkJHGAqtk59pAsHqA";"Усы")', '=HYPERLINK("https://drive.google.com/open?id=12V8spqPdepdMVflmcIoXMNb2SHlc7zdS";"Усы")', 'нет'], ['нет', 'нет', 'да', 'вторник', 19, '=HYPERLINK("https://drive.google.com/open?id=18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ";"Одиночество")', '=HYPERLINK("https://drive.google.com/open?id=1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i";"Одиночество")', 'да'], ['да', 'нет', 'нет', 'суббота', 15, '=HYPERLINK("https://drive.google.com/open?id=1iRiqwfofCqNRrsVVP0Sv6Tk5CkWfVztk2hJRzySNQlo";"Темнота")', '=HYPERLINK("https://drive.google.com/open?id=1eIzluX3xvZRiALjX-PQZeHNrHHHMjRJ1";"Темнота")', 'да'], ['да', 'да', 'нет', 'понедельник', 13, '=HYPERLINK("https://drive.google.com/open?id=1-gnx8kZnS8FZUd4DaoShb4RPD7D3n8wQxhVMRmUN7BI";"Про кошек")', '=HYPERLINK("https://drive.google.com/open?id=1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB";"Кошки")', 'нет'], ['нет', 'нет', 'да', 'четверг', 12, '=HYPERLINK("https://drive.google.com/open?id=1Wthk5k2ucVXpsa_J2F9TTflA2ztjcarLu81Rtb05ps8";"Лапы")', '=HYPERLINK("https://drive.google.com/open?id=1zljULNgX1h1sS9x4iWLaDZQEVEMNf5PH";"Лапы")', 'да'], ['да', 'нет', 'нет', 'вторник', 16, '=HYPERLINK("https://drive.google.com/open?id=1mS2RZO-TvhXZXqWQKx5AiWtCF-gkJHGAqtk59pAsHqA";"Усы")', '=HYPERLINK("https://drive.google.com/open?id=12V8spqPdepdMVflmcIoXMNb2SHlc7zdS";"Усы")', 'нет'], ['нет', 'да', 'нет', 'суббота', 14, '=HYPERLINK("https://drive.google.com/open?id=18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ";"Одиночество")', '=HYPERLINK("https://drive.google.com/open?id=1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i";"Одиночество")', 'нет'], ['да', 'нет', 'нет', 'понедельник', 16, '=HYPERLINK("https://drive.google.com/open?id=18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ";"Одиночество")', '=HYPERLINK("https://drive.google.com/open?id=1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i";"Одиночество")', 'да'], ['нет', 'да', 'да', 'четверг', 21, '=HYPERLINK("https://drive.google.com/open?id=1iRiqwfofCqNRrsVVP0Sv6Tk5CkWfVztk2hJRzySNQlo";"Темнота")', '=HYPERLINK("https://drive.google.com/open?id=1eIzluX3xvZRiALjX-PQZeHNrHHHMjRJ1";"Темнота")', 'да'], ['нет', 'нет', 'да', 'вторник', 10, '=HYPERLINK("https://drive.google.com/open?id=1-gnx8kZnS8FZUd4DaoShb4RPD7D3n8wQxhVMRmUN7BI";"Про кошек")', '=HYPERLINK("https://drive.google.com/open?id=1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB";"Кошки")', 'нет']]

from urllib.parse import parse_qsl
from urlextract import URLExtract

				
def extract_file_id(text):
  text= str(text)
  try:
      _text = URLExtract().find_urls(text)[0]
      return parse_qsl(_text)[0][1]
  except IndexError:
      return None
	 
	 
for schedule_row in schedule_spreadsheet:
	schedule_row = [x if extract_file_id(x) is None else extract_file_id(x) for x in schedule_row]
	print(schedule_row)