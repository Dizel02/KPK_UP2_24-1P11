from peewee import *

# Подключение к локальной базе данных SQLite
db = SqliteDatabase('group_service_s7.db')

class BaseModel(Model):
    class Meta:
        database = db

class Curator(BaseModel):
    """Справочник кураторов (3НФ)"""
    full_name = CharField(unique=True, null=False)

class GroupStatus(BaseModel):
    """Справочник статусов (3НФ)"""
    title = CharField(unique=True, null=False)

class Group(BaseModel):
    """Таблица учебных групп"""
    name = CharField(unique=True, null=False)
    formation_year = IntegerField(null=False)
    # Внешние ключи для связи таблиц
    status = ForeignKeyField(GroupStatus, backref='groups', null=False)
    curator = ForeignKeyField(Curator, backref='groups', null=False)

def init_db():
    """Создание таблиц и заполнение начальными данными"""
    db.connect()
    db.create_tables([Curator, GroupStatus, Group], safe=True)
    
    # Наполнение справочников, если они пусты
    if GroupStatus.select().count() == 0:
        GroupStatus.create(title="Активна")
        GroupStatus.create(title="Выпустилась")
    
    if Curator.select().count() == 0:
        Curator.create(full_name="Столяров А.С.")

if __name__ == "__main__":
    init_db()
    print("Группа №7: База данных успешно инициализирована.")
