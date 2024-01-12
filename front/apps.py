from django.apps import AppConfig
import os
from django.db import connection

class FrontConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'front'

    def ready(self):
      if os.environ.get('RUN_MAIN'):
        cursor = connection.cursor()
        cursor.execute("""DROP TABLE cart;""")
        cursor.execute("""CREATE TABLE cart (uuid char(32));""");

        cursor.execute("""DROP TABLE history;""")
        cursor.execute("""CREATE TABLE history (visited char(100));""");
