from flask import Flask, render_template, redirect, session, request
import random

app = Flask(__name__)
app.secret_key = "Nope"

winnersList = []


@app.route("/")
def root():
    if ("random" not in session or "try" not in session or "attemps" not in session or "done" not in session):
        session["random"] = random.randint(1, 100)
        session["try"] = 0
        session["attemps"] = 0
        session["done"] = False
        print(session["random"])
        return render_template("index.html", show="none", text="Nothing", winList="none",gameover="show")

    elif (session["done"] == True):
        session.clear()
        session["random"] = random.randint(1, 100)
        session["try"] = 0
        session["attemps"] = 0
        session["done"] = False
        return render_template("index.html", show="none", text="Nothing", winList="none",gameover="show")

    elif (session["attemps"] >= 5):
        session.clear()
        session["random"] = random.randint(1, 100)
        session["try"] = 0
        session["attemps"] = 0
        session["done"] = False
        return render_template("index.html", show="red", text="Gastó sus 5 intentos", winList="none",gameover="none")

    else:
        if(int(session["try"]) == 0):
            return render_template("index.html", show="none", text="Nothing", winList="none",gameover="show")
        elif(int(session["try"]) > session["random"]):
            return render_template("index.html", show="red", text="Too Hight!", winList="none",gameover="show")

        elif(int(session["try"]) < session["random"]):
            return render_template("index.html", show="red", text="Too LOW!", winList="none",gameover="show")

        else:
            session["done"] = True
            return render_template("index.html", show="green", text=str(session["try"])+" Was the number " + str(session["attemps"])+" intentos", winList="show",gameover="none")


@app.route("/guess", methods=["POST"])
def guess():
    if(request.form["numero"] != ""):
        session["try"] = int(request.form["numero"])
    else:
        session["try"] = 0
    session["attemps"] += 1
    return redirect("/")


@app.route("/win", methods=["POST"])
def win():
    global winnersList

    intentos = session["attemps"]
    if(request.form["name"] == ""):
        winnersList.append(f"Player {intentos}")
    else:
        player = request.form["name"]
        winnersList.append(f"{player} | {intentos}")
    return redirect("/winners")


@app.route("/winners")
def winners():
    global winnersList
    return render_template("win.html", winners=winnersList)


if(__name__ == "__main__"):
    app.run(debug=True)
