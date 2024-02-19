from setuptools import setup, find_packages # pip install setuptools
from io import open


def read(filename):
   """Прочитаем наш README.md для того, чтобы установить большое описание."""
   with open(filename, "r", encoding="utf-8") as file:
      return file.read()


setup(name="verysimplesqlite3",
   version="0.1", 
   description="Удобная версия sqlite3",
   long_description=read("README.MD"), # Здесь можно прописать README файл с длинным описанием
   long_description_content_type="text/markdown", # Тип контента, в нашем случае text/markdown
   author="ngen",
   author_email="dontwriteme@gmail.com",
   url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", # Страница проекта
   keywords="sqlite3, sqlite, sqlitesimple", # Ключевые слова для упрощеннего поиска пакета на PyPi
   packages=find_packages() # Ищем пакеты, или можно передать название списком: ["package_name"]
)