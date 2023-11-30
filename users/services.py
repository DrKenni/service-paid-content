import requests

from config import settings


def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


def send_code(numb, code):
    responce = requests.get(
        f'https://sms.ru/sms/send?api_id={settings.SMS_API_ID}&to=+7{numb}&msg={code}&json=1'
    )
