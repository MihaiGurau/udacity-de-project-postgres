import glob
import os

import pandas as pd
import psycopg2
from tqdm import tqdm

import sql_queries


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = (
        df[["song_id", "title", "artist_id", "year", "duration"]].values[0].tolist()
    )
    cur.execute(sql_queries.song_table_insert, song_data)

    # insert artist record
    artist_data = (
        df[
            [
                "artist_id",
                "artist_name",
                "artist_location",
                "artist_latitude",
                "artist_longitude",
            ]
        ]
        .values[0]
        .tolist()
    )
    cur.execute(sql_queries.artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    timestamps = pd.to_datetime(df["ts"], unit="ms")

    # insert time data records
    # time_data =
    # column_labels =
    time_df = timestamps.to_frame(name="ts")
    time_df["start_time"] = time_df["ts"].view(int) / 1e6  # transform from ns to ms
    time_df["hour"] = time_df["ts"].dt.hour
    time_df["day"] = time_df["ts"].dt.day
    time_df["month"] = time_df["ts"].dt.month
    time_df["week"] = time_df["ts"].dt.isocalendar().week
    time_df["year"] = time_df["ts"].dt.year
    time_df["weekday"] = time_df["ts"].dt.weekday
    del time_df["ts"]

    for _, row in time_df.iterrows():
        cur.execute(sql_queries.time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for _, row in user_df.iterrows():
        cur.execute(sql_queries.user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(sql_queries.SONG_SELECT, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            index,
            row.ts,
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent,
        )
        cur.execute(sql_queries.songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func) -> None:
    # get all files matching extension from directory
    all_files = []
    for root, _, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for file in files:
            all_files.append(os.path.abspath(file))

    # get total number of files found
    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    # iterate over files and process
    for _, datafile in tqdm(enumerate(all_files), total=num_files):
        func(cur, datafile)
        conn.commit()


def main() -> None:
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student"
    )
    cur = conn.cursor()

    process_data(cur, conn, filepath="data/song_data", func=process_song_file)
    process_data(cur, conn, filepath="data/log_data", func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
