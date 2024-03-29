from ml_utils import *
import time
import sqlite3 as sql #
import youtube_dl

queries = ["machine+learning", "data+science", "kaggle", "aprendizado+de+maquina", "statistic", "ciencia+de+dados"]
db_name = 'videos.db' #

def update_db():
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True}) 
    with sql.connect(db_name) as conn: #
        for query in queries:
            r = ydl.extract_info("ytsearchdate20:{}".format(query), download=False)
            video_list = r['entries']
            for video in video_list:
                if video is None:
                    continue

                p = compute_prediction(video)

                video_id = video['webpage_url']
                watch_title = video['title'].replace("'", "") #
                data_front = {"title": watch_title, "score": float(p), "video_id": video_id} #
                data_front['update_time'] = time.time()

                print(video_id, json.dumps(data_front))
                c = conn.cursor() #
                c.execute("INSERT INTO videos VALUES ('{title}', '{video_id}', {score}, {update_time})".format(**data_front)) #
                conn.commit() #
    return True

