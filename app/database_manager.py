from pony.orm import *

class DatabaseManager:

    def define_entities(self, db):

        class Person(db.Entity):
            first_name = Required(str)
            last_name = Required(str)
            profile_picture_url = Optional(str)

    def initialize_database(self):
        db = Database()
        db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
        self.define_entities(db)
        db.generate_mapping(create_tables=True)
        return db
