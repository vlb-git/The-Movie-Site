from flask import *
import hashlib
import sqlite3

import content as contentManager
import users as Users

hash_object = hashlib.sha256()


app = Flask(__name__)

app.secret_key="BAS_SECRET_KEY"

def executeSQL(sql, extraValues=(), fetch=False):
    conn=sqlite3.connect("data/data.db")
    rows=None
    if not fetch:
        if not extraValues:
            conn.execute(sql)
        else:
            conn.execute(sql,extraValues)
        conn.commit()
        
    else:
        cur = conn.cursor()
        if not extraValues:
            cur.execute(sql)
        else:
            cur.execute(sql,extraValues)
        rows = cur.fetchall()
    conn.close()
    return rows

def returnMovieName(List):
    return List[0]
def returnContentDescription(List):
    return List[1]

def encrypt(password):# changed for encryption
    return password
def questionsList(movieName):
    return executeSQL("SELECT * FROM quiz_questions WHERE movie_name=?",extraValues=(movieName,), fetch=True)


@app.route("/")
def index():
    status = {"Logged In":False}
    return render_template("home.html.j2",pageName='#home', status=status)

@app.route("/login/")
def login():
    status = {"Logged In":False}
    return render_template("login.html.j2",pageName='#login', status=status)

@app.route("/logout/")
def logout():
    session.pop('user')
    return redirect("/")

@app.route("/login/entry/", methods=["GET", "POST"])
def login_entry():
    status = {"Logged In":False}
    users = Users.Users()
    if (request.method=="POST"):
        username = request.form["username"]
        result = users.verifyUser(username, request.form["passwd"])
        if result:
            session["user"] = users.findUser(username)[0][:3] + users.findUser(username)[0][4:]
            return redirect("/dashboard/")
        else:
            return redirect("/login/")
    return "login entry"

@app.route("/signup/")
def signup():
    status = {"Logged In":False}
    return render_template("signup.html.j2",pageName='#signup', status=status)


@app.route("/signup/entry/", methods=["POST"])
def signup_entry():
    status = {"Logged In":False}
    users_object = Users.Users()
    if request.method=="POST":
        username = request.form["username"]
        email = request.form["email"]
        dob = request.form["dob"]

        users_object.createUser(username, email, request.form["passwd"], dob)

    return redirect("/login/")


@app.route("/dashboard/")
def dash():
    status = {"Logged In":False}
    return render_template("dashboard.html.j2",pageName='#profile', status=status)

@app.route("/list/")
def movie_list():
    status = {"Logged In":False}
    return "Movie List Page"

@app.route("/quiz/")
def quiz_home():
    # movieList
    status = {"Logged In":False}
    c = contentManager.Content()

    movieList = c.fetchAll()

    movieQuiz=[[row[1],row[2],row[0]] for row in movieList]

    return render_template("quiz_home.html.j2",pageName='#quiz',movieQuiz=movieQuiz, status=status)

@app.route("/quiz/<movie>/")
def quiz(movie):
    status = {"Logged In":False}
    #MOVIELIST SQL
    c = contentManager.Content()

    movieList = c.fetchContent(movie)

    questions = questionsList(movie)

    if movieList:
        if(len(questions)>0):
            print("quiz Page")
            return render_template(f"quiz/quiz_page.html.j2",link=f"{movie}",pageName='#quiz',movieName=f"{movieList[0][1]}", questions=questions, status=status)
        else:
            return render_template(f"quiz/Default_Quiz_Page.html.j2",link=f"{movie}",pageName='#quiz',movieName=f"{movieList[0][1]}", status=status)
    else:
        return redirect("/")

@app.route("/quiz/<movie>/submit/", methods=["POST"])
def quizEntry(movie):
    questions = questionsList(movie)
    answers=[]
    correctAnswers=[]
    score = 0
    if len(questions)==0:
        return "This movie does not exist"
    if request.method=="POST":
        print(request.form)
        for i in range(10):
            answer = request.form[f"q{i+1}"]
            answers.append(answer)
            correctAnswers.append(questions[i][5])
            if answer==questions[i][5]:
                score+=1

        
        return render_template("quiz/quiz_answers_page.html.j2", answers = answers, correctAnswers = correctAnswers, questions=questions, score=score) 


@app.route("/content/")
def content_home():
    status = {"Logged In":False}
    #movielist SQL
    c=contentManager.Content()
    movies = [[row[1], row[2], row[0]] for row in c.fetchAll()]
    #movies = [[returnMovieName(moviesList[movie]),returnContentDescription(moviesList[movie]),movie] for movie in moviesList]
    return render_template("content/content_home.html.j2", movies=movies, pageName="#navContent", status=status)

@app.route("/content/<movie>/")
def theContentPage(movie):
    status = {"Logged In":False}
    #MOVIELIST SQL
    c = contentManager.Content()

    movieList = c.fetchContent(movie)
    
    if movieList:
        try:
            return render_template(f"content/{movie}.html.j2",link=f"{movie}",pageName='#navContent',movieName=f"{movieList[0][1]}", status=status)
        except:
            return render_template(f"content/Default_Page.html.j2",link=f"{movie}",pageName='#navContent',movieName=f"{movieList[0][1]}", status=status)
    else:
        return redirect("/")
def test_page_function():
    print(render_template("home.html.j2"))
    return render_template("home.html.j2")
@app.route("/test/")
def testPage():
    return test_page_function()
if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)