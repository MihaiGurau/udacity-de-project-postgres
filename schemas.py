# define schemas and tables


from helpers import Table


class PGT:
    """Utility class for storing postgresql data types"""

    VARCHAR = "varchar"
    INTEGER = "integer"
    BIGINT = "bigint"
    CHARACTER = "character"
    DOUBLE_PRECISION = "double precision"


# FACT TABLES


SONG_PLAYS = {
    "songplay_id": PGT.VARCHAR,
    "start_time": PGT.BIGINT,
    "user_id": PGT.INTEGER,
    "level": PGT.VARCHAR,
    "song_id": PGT.VARCHAR,
    "artist_id": PGT.VARCHAR,
    "session_id": PGT.VARCHAR,
    "location": PGT.VARCHAR,
    "user_agent": PGT.VARCHAR,
}


# DIMENSION TABLES

USERS = {
    "user_id": PGT.INTEGER,
    "first_name": PGT.VARCHAR,
    "last_name": PGT.VARCHAR,
    "gender": PGT.CHARACTER,
    "level": PGT.VARCHAR,
}

SONGS = {
    "song_id": PGT.VARCHAR,
    "title": PGT.VARCHAR,
    "artist_id": PGT.VARCHAR,
    "year": PGT.INTEGER,
    "duration": PGT.DOUBLE_PRECISION,
}


ARTISTS = {
    "artist_id": PGT.VARCHAR,
    "name": PGT.VARCHAR,
    "location": PGT.VARCHAR,
    "latitude": PGT.DOUBLE_PRECISION,
    "longitude": PGT.DOUBLE_PRECISION,
}

TIME = {
    "start_time": PGT.BIGINT,
    "hour": PGT.INTEGER,
    "day": PGT.INTEGER,
    "week": PGT.INTEGER,
    "month": PGT.INTEGER,
    "year": PGT.INTEGER,
    "weekday": PGT.INTEGER,
}

# DATABASE TABLES


songplays_table = Table(
    name="songplays", schema=SONG_PLAYS, primary_key_column="songplay_id"
)
users_table = Table(name="users", schema=USERS, primary_key_column="user_id")
songs_table = Table(name="songs", schema=SONGS, primary_key_column="song_id")
artists_table = Table(name="artists", schema=ARTISTS, primary_key_column="artist_id")
time_table = Table(name="time", schema=TIME, primary_key_column="start_time")
