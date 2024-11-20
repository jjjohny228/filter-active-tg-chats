import re
import requests

from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema


class ChatAnalyzer:
    def __init__(self, source_file, result_file):
        self.source_file = source_file
        self.result_file = result_file
        self.active_chats = []

    def read_all_channels(self):
        with open(self.source_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f.readlines()]
            return urls

    @staticmethod
    def is_chat_active(subs_text):
        matches = re.findall(r'\d+\s*\d*', subs_text)
        numbers = [int(match.replace(" ", "")) for match in matches]
        if len(numbers) < 2:
            return
        members, online_members = numbers
        active_users_percentage = (online_members * 100) // members

        if active_users_percentage > 15:
            return True

    def write_result(self):
        with open(self.result_file, 'w', encoding='utf-8') as f:
            for url in self.active_chats:
                f.write(url + '\n')

    def analyze(self):
        urls = self.read_all_channels()
        for url in urls:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                element = soup.find('div',
                                    class_='tgme_page_extra')  # написать правильный поиск элемент с подписотой и тд
                if element:
                    subs_text = element.text
                    if self.is_chat_active(subs_text):
                        self.active_chats.append(url)
                        print('Chat is active')
            except MissingSchema as e:
                print(e)

        self.write_result()


if __name__ == '__main__':
    analyzer = ChatAnalyzer('source.txt', 'result.txt')
    analyzer.analyze()