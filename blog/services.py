import re


class ReExpression:
    @staticmethod
    def get_video_id(video_url):
        """Получает video_id из ссылки"""

        video_id = re.findall(r'(?<==).{11}', video_url)
        return video_id[0]

    @staticmethod
    def check_url(context):
        """Проверка на начилие совпадения"""
        search_text = re.search(r'youtube.com', context)
        return bool(search_text)
