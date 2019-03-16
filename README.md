# all_reposts_by_the_schedule!

Проект предназначен для автоматизированного постинга 
по расписанию текста и изображений из Google Spreadsheets 
в группы социальных сетей - телеграм, фейсбук, вконтакте.

### Как установить

Программа рассчитана для установки на постоянно работающем сервере.

Скачиваем файлы в папку all_reposts_by_the_schedule. В этой же папке создаем .env файл. Ваш .env должен содержать строки:

```
SHEETS_LINK = url_google_spreadsheets 
SHEETS_RANGE = диапазон_данных_url_google_spreadsheets #например: Лист1!A3:H100000 
LOGIN_VK = ваш_логин_в_контакте
PASSWORD_VK = ваш_пароль_в_контакте
TOKEN_VK = токен_вашего приложения_в_контакте
GROUP_ID_VK = id_группы_в_контакте
GROUP_ID_ALBUM_VK = id_альбома_в_контакте
TOKEN_TG = токен_вашего_бота_телеграм
CHANNEL_TG = название_канала_телеграм
TOKEN_FB = токен_вашего_приложения_в_фейсбуке
GROUP_ID_FB = id_вашей_группы_в_фейсбуке
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Использование
1. Программа управляется через таблицу Google Spreadsheets. После постинга обновляется пометка **Опубликовано?**

Формат таблицы-

![](https://www.radikal.kz/images/2019/03/16/BEZYMYNNYI.png)

2. запуск программы - 

```
python3 main.py
```
Программа выводит в консоль лог своей работы. 

```
INFO:googleapiclient.discovery:URL being requested: GET https://www.googleapis.com/drive=json
INFO:root:It's not a good time - 2019-03-21 19:00:00
INFO:root:It's time to publish - 2019-03-16 12:00:00
INFO:root:download & saved content_folder/Темнота.txt
INFO:root:download & saved content_folder/9341396273_8237029_8110393.jpg
INFO:root: Success publish: facebook post was published
INFO:root:It's not a good time - 2019-03-19 16:00:00
INFO:root:It's not a good time - 2019-03-16 14:00:00
```


```

INFO:root: Success publish: facebook post was published

```
После этого сообщения пост размещен.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
