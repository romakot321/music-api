from app.db.tables import Song
from sqladmin import ModelView


class SongView(ModelView, model=Song):
    column_list = "__all__"
    column_searchable_list = [Song.status, Song.user_id, Song.id]
    column_sortable_list = [Song.created_at, Song.updated_at]
    column_default_sort = [(Song.created_at, True)]

