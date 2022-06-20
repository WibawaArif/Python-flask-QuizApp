from flask import Flask, render_template, request, redirect
import os
import random
from pymongo import MongoClient

template_dir = os.path.abspath('template_fs')

app = Flask(__name__, template_folder=template_dir)
client = MongoClient(os.environ.get("MONGODB_URI"))
app.db = client.faq


@app.route('/', methods=['POST', 'GET'])        
def index():
        user_answer = request.form.get('answer__input')
        true_answer = request.form.get('true__answer')
        db_collection = app.db.questions.find()
        ul_quiz = []    
        for g in db_collection:
                ul_quiz.append((list(g.keys())[1], list(g.values())[1]))
        random_question = random.sample(ul_quiz, k=1)
        
        try:
                final_score = False
                with open("score.txt", "r") as r:
                        score = r.readline()
                        last_score = int(score) + 1
                        if score == '':
                                raise Exception('Data Kosong!')
                with open("score.txt", "w") as s:
                        if user_answer == true_answer and user_answer != None and true_answer != None:
                                to_int = int(score)
                                to_int += 1
                                s.write(f"{to_int}")
                                score = to_int
                        else:
                                s.write(score)
                        if score == '5':
                                final_score = True
                                raise Exception("Score Has Reach Maximum!")
                with open("game_over.txt", "r") as a:
                        game_over = int(a.readline())
                        if user_answer != None and true_answer != None:
                                game_over += 1
                with open("game_over.txt", "w") as d:
                        d.write(f"{game_over}")
                        if game_over == 5:
                                final_score = True
                                raise Exception("Score Has Reach Maximum!")   
                        
        except:
                with open("score.txt", "w") as f:
                        f.write("0")
                with open("game_over.txt", "w") as g:
                        g.write("0")
                with open("score.txt", "r") as t:
                        score = t.readline()
        return render_template("index.html", 
                                game_over=game_over, 
                                last_score=last_score, 
                                final_score=final_score, 
                                score_game=score, 
                                quiz=random_question[0], 
                                true_answer=true_answer , 
                                user_answer=user_answer)