# deploy_front/app.py
#

import os.path
from flask import Flask, request, render_template #
import os
import json
import run_backend
import ml_utils #
import codecs
import requests as rq
import youtube_dl as ytdl
import sqlite3 as sql  # 

import time

from form import PredictForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'felipeshiwu'


def get_predictions():

    videos = []

    with sql.connect(run_backend.db_name) as conn: # 
        c = conn.cursor() #
        for line in c.execute("SELECT * FROM videos"): #
            #(title, video_id, score, update_time)
            line_json = {"title": line[0], "video_id": line[1], "score": line[2], "update_time": line[3]} #
            videos.append(line_json)
			

    predictions = []
    for video in videos:
        predictions.append((video['video_id'], video['title'], float(video['score'])))

    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]


    predictions_formatted = []
    for e in predictions:
        #print(e)
        predictions_formatted.append("<tr><td><a class=\"video-row\" href=\"{link}\">{title}</a></td><td>{score}</th></td>".format(title=e[1], link=e[0], score=e[2]))
  
    return '\n'.join(predictions_formatted) #

@app.route('/')
def main_page():
    preds = get_predictions() #
    header_html = codecs.open("templates/header.html", "r", "utf-8").read()
    page = header_html + """
    
                <tbody>
                    {}
                </tbody>
            </table>
        </div>
        <div class="predict-button">
        <button type=submit class="waves-effect waves-light btn"><a href="/predict">PREDICT VIDEO</a></button>
        </div>
        <div class="made-with-love">
        Project made by <a target="_blank" href="https://thefelipes.site">Felipe Wu </a> <i><3</i> Visual design by
        <a target="_blank" href="https://codepen.io/nikhil8krishnan">Nikhil Krishnan</a><br>
        <a target="_blank" href="https://github.com/felipeshiwu/video-recommender">Access this project Github page</a>
        </div>
    </section>
    </body>
    """.format(preds) #

    view = open("templates/index.html", "w")
    view.write(page)
    view.close()

    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictForm()
    if form.is_submitted():
        result = request.form
        url = result['predict_url']

        try: 
            ydl = ytdl.YoutubeDL({"ignoreerrors": True})
            video_json_data = ydl.extract_info(url, download=False)
        except:
            return render_template('result.html', result={"title": "Not Found", "score": "0", "url": "/predict"})

        if video_json_data is None:
            return render_template('result.html', result={"title": "Not Found", "score": "0", "url": "/predict"})

        p = ml_utils.compute_prediction(video_json_data)
        output = {"title": video_json_data['title'], "score": p, "url": "{}".format(url)}
        return render_template('result.html', result=output)

    return render_template('predict.html', form=form)




if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0')
    app.run()
