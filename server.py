from flask import Flask, render_template, redirect, session, request
import random

app = Flask(__name__)
app.secret_key = "Nope"


@app.route("/")
def root():
    if ("random" not in session or "try" not in session or "attemps" not in session or "done" not in session ):
        session["random"] = random.randint(1, 100)
        session["try"] = 0
        session["attemps"] = 0
        session["done"] =False
        print(session["random"])
        return render_template("index.html", show="none", text="Nothing",winList="none")

    elif (session["done"] ==True):
        session.clear()
        session["random"] = random.randint(1, 100)
        session["try"] = 0
        session["attemps"] = 0
        session["done"] =False
        return render_template("index.html", show="none", text="Nothing",winList="none")
    else:
        if(int(session["try"]) == 0):
            return render_template("index.html", show="none", text="Nothing",winList="none")
        elif(int(session["try"]) > session["random"]):
            return render_template("index.html", show="red", text="Too Hight!",winList="none")

        elif(int(session["try"]) < session["random"]):
            return render_template("index.html", show="red", text="Too LOW!",winList="none")

        else:
            session["done"] =True
            return render_template("index.html", show="green", text=str(session["try"])+" Was the number "+ str(session["attemps"])+" intentos" ,winList="show")


@app.route("/guess", methods=["POST"])
def guess():
    if(request.form["numero"] !=""):
        session["try"] = int(request.form["numero"])
    else:
        session["try"] = 0
    session["attemps"] += 1
    return redirect("/")


if(__name__ == "__main__"):
    app.run(debug=True)
