import schemas

# DROP TABLES

songplay_table_drop = schemas.songplays_table.get_drop_table_query()
user_table_drop = schemas.users_table.get_drop_table_query()
song_table_drop = schemas.songs_table.get_drop_table_query()
artist_table_drop = schemas.artists_table.get_drop_table_query()
time_table_drop = schemas.time_table.get_drop_table_query()

# CREATE TABLES

songplay_table_create = schemas.songplays_table.get_create_table_query()
user_table_create = schemas.users_table.get_create_table_query()
song_table_create = schemas.songs_table.get_create_table_query()
artist_table_create = schemas.artists_table.get_create_table_query()
time_table_create = schemas.time_table.get_create_table_query()


# INSERT RECORDS

songplay_table_insert = schemas.songplays_table.get_insert_query()
user_table_insert = schemas.users_table.get_insert_query()
song_table_insert = schemas.songs_table.get_insert_query()
artist_table_insert = schemas.artists_table.get_insert_query()
time_table_insert = schemas.time_table.get_insert_query()

# FIND SONGS

SONG_SELECT = (
    "select s.song_id, s.artist_id "
    "from songs s "
    "join artists a "
    "on s.artist_id = a.artist_id "
    "where s.title = %s "
    "and a.name = %s "
    "and s.duration = %s"
)

# QUERY LISTS

create_table_queries = [
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]
drop_table_queries = [
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]
