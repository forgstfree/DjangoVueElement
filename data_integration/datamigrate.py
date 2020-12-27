import pymysql
from pyetl import Task, DatabaseReader, DatabaseWriter, reader


class MyMigrationTest():
    src=None
    reader = None
    dst = None
    writer = None
    def __init__(self) -> None:
        super().__init__()
        self.src = pymysql.connect(host="localhost", port=13335, user="root",db="djangodb",passwd="123")
        self.reader = DatabaseReader(self.src,table_name="django_migrations")
        self.dst = pymysql.connect(host="localhost",user="root",db="test",passwd="123",port=13335)
        self.writer = DatabaseWriter(self.dst,table_name="django_migrations")


    def migrate(self):
        # columns = {'app': 'app', 'id': 'id', 'name': 'name'}
        # Task(reader,writer,columns=columns).start()
        Task(self.reader,self.writer).show()

# if __name__ == "__main__":
    # test = MyMigrationTest()
    # test.migrate()