from config.setting import DBProvider, Setting
from agno.db.mongo import MongoDb
from agno.db.sqlite import SqliteDb
from agno.db.json import JsonDb
from agno.db.in_memory import InMemoryDb


class DbManager:
    def __init__(self, setting: Setting):
        self.setting = setting
        self.db = self._initialize_db()

    def _initialize_db(self):
        provider = self.setting.DB_PROVIDER

        if provider == DBProvider.MONGODB:

            return MongoDb(
                db_url=self.setting.MONGODB_URI,
                db_name=self.setting.MONGODB_DB,
            )

        if provider == DBProvider.SQLITE:

            return SqliteDb(db_file=self.setting.SQLITE_FILE)

        if provider == DBProvider.JSON:

            return JsonDb(db_path=self.setting.JSON_FILE)

        if provider == DBProvider.INMEMORY:

            return InMemoryDb()

        raise ValueError(f"Unsupported database type: {provider}")

    def get_db(self):
        return self.db
