from pony import orm

db = orm.Database()

class User(db.Entity):
    __table__ = "Users"
    public_id = orm.Required(str)
    name = orm.Required(str)
    password = orm.Required(str)
    is_admin = orm.Optional(bool)
    def __dict__(self):
        return {
            "public_id":self.public_id,
            "name":self.name,
            "password":self.password,
            "isAdmin":self.is_admin
        }

class Author(db.Entity):
    _table_ = "Authors"
    name = orm.Required(str)
    notes = orm.Set("Note")
    def __dict__(self):
        return {
            "id":self.id,
            "name":self.name,
        }

class Note(db.Entity):
    _table_ = "Notes"
    author = orm.Optional(Author)
    title = orm.Required(str)
    body = orm.Required(str)
    
    def __dict__(self):
        return {
            "id":self.id,
            "author":self.author.__dict__(),
            "title":self.title,
            "body":self.body,
        }


