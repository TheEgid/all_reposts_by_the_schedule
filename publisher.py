import logging
import requests
import vk_api
import telegram
import os


def get_content_from_file_system(content_number):
    dir_name = 'content_folder'
    if not os.path.exists(dir_name):
        logging.exception('folder error! check the content_folder')
        raise FileNotFoundError('folder error!')

    content_img_file_pathname = '{}/{}.jpg'.format(dir_name, content_number)
    content_text_file_pathname = '{}/{}.txt'.format(dir_name, content_number)

    if os.path.isfile(content_text_file_pathname):
        with open(content_text_file_pathname, 'r', encoding='utf-8') as imp_file:
            content_text = imp_file.read()
    else:
        content_text = None
    if not os.path.isfile(content_img_file_pathname):
        content_img_file_pathname = None
    return (content_text, content_img_file_pathname)


def post_facebook(token, fb_group, file_number):
    text, img_file_pathname = get_content_from_file_system(file_number)
    if text is None:
        text = file_number
    url = 'https://graph.facebook.com/{}/photos'.format(fb_group)
    params = {'access_token': token, 'message': text}
    if img_file_pathname is not None:
        with open(img_file_pathname, 'rb') as img_file:
            response = requests.post(url=url, params=params, files={'file': img_file})
            response.raise_for_status()
        logging.info(' Success publish: facebook post was published')


def post_telegram(token, tg_channel, file_number):
    text, img_file_pathname = get_content_from_file_system(file_number)
    if text is None:
        text = file_number
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=tg_channel, text=text)
    if img_file_pathname is not None:
        with open(img_file_pathname, 'rb') as img_file:
            bot.send_photo(chat_id=tg_channel, photo=img_file)
        logging.info(' Success publish: telegram post was published')


def post_vkontakte(login, password, token, vk_group, vk_group_album,
            file_number):
    text, img_file_pathname = get_content_from_file_system(file_number)
    if text is None:
        text = file_number
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth(token_only=True)
    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk_session)
    if img_file_pathname is not None:
        img = upload.photo(photos=img_file_pathname,
                       album_id=vk_group_album,
                       group_id=vk_group)
        attach = 'photo{}_{}'.format(img[0]['owner_id'], img[0]['id'])
        vk_group = int(vk_group) * -1  # with "-" (vk.com/dev/wall.post#owner_id)
        vk.wall.post(message=text,
                 access_token=token,
                 owner_id=vk_group,
                 attachments=attach)
        logging.info(' Success publish: vkontakte post was published')
