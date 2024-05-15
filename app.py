from flask import *
import hashlib

import content as contentManager
import users as Users

hash_object = hashlib.sha256()


app = Flask(__name__)

app.secret_key="BAS_SECRET_KEY"
moviesList={
    "dune_2021":["Dune part 1 (2021)", "Description for Dune part 1"],
    "dune_2024":["Dune part 2 (2024)", "Description for Dune part 2"],
    "jurassic_park":["Jurassic Park", "Description for Jurassic Park"]
    }
def returnMovieName(List):
    return List[0]
def returnContentDescription(List):
    return List[1]

def encrypt(password):# changed for encryption
    return password

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

    if movieList:
        #try:
        print("quiz Page")
        return render_template(f"quiz/{movie}_quiz.html.j2",link=f"{movie}",pageName='#quiz',movieName=f"{movieList[0][1]}", status=status)
        #except Exception as e:
        #    print(e)
        #    return render_template(f"quiz/Default_Quiz_Page.html.j2",link=f"{movie}",pageName='#quiz',movieName=f"{movieList[0][1]}", status=status)
    else:
        return redirect("/")

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

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)