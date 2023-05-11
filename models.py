from pony import orm

db = orm.Database()

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


