from pony import orm

db = orm.Database()

class Note(db.Entity):
    _table_ = "Notes"
    author = orm.Required(str)
    title = orm.Required(str)
    body = orm.Required(str)

# class Author(db.Entity):
#     _table_ = "Authors"
#     name = orm.Required(str)
#     notes = orm.Set("Note")
