from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from cs50 import SQL

db = SQL("sqlite:///flaskbook.db")

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretKEY"


def validate_student(id_student, name_student):
    login_student = db.execute("SELECT id, name FROM students WHERE id = ? AND name = ?", id_student, name_student)
    if login_student:
        return login_student[0]
    
def get_name(id_student):
    name = db.execute("SELECT name FROM students WHERE id = ?", id_student)
    return name[0]["name"]

""" metodos sin sentido
get id or get name get sports
validate_student
get studen sports
get_unenrolled_sport (NO NESEITO ASI DIN AVALIABLE SPORT) lo pongo proerty porque cada tanto se necesita llamar actualziada cada vez qeu agrego un deporte ejectura para imprimri los que estan sina gregar
"""
class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
    def delete_student(self):
        return db.execute("DELETE FROM students WHERE id = ?", self.id)
    
    
    @property
    def get_enrolled_sports(self):
        return db.execute("""
            SELECT * FROM sports 
            JOIN registrations ON sports.id = registrations.sport_id 
            WHERE registrations.student_id = ?
            """, self.id)
    
    @property
    def get_unenrolled_sport(self):
        return db.execute("""
        SELECT * FROM sports WHERE id NOT IN (
            SELECT sport_id FROM registrations WHERE student_id = ?
        )
        """, self.id)
        
    def find_available_sports(self, q):
        return db.execute("""SELECT * FROM sports  WHERE sport LIKE ? AND id NOT IN (
                SELECT sport_id FROM registrations WHERE student_id = ?
            ) """, q + "%", self.id)
    
    def assign_sport(self, id_sport):
        return db.execute("INSERT INTO registrations (student_id, sport_id) VALUES (?,?)", self.id, id_sport)

    
    def unassign_sport(self, sport_id):
        db.execute("DELETE FROM registrations WHERE student_id = ? AND sport_id = ?", self.id, sport_id)
 
        
def create_student(name_student):
    return db.execute("INSERT INTO students (name) VALUES (?)", name_student)


        

# --------------------------------------------------------------------------
@app.route("/", methods=["GET","POST"])
def index():
    if session.get("user_id"):
        return redirect(url_for("home"))
    return render_template("index.html")
    
@app.route("/log_in", methods=["POST"])
def log_in():
    id = request.form.get("id")
    name = request.form.get("name")
    valid_student= validate_student(id, name)
    
    if valid_student is None:
        return render_template("error.html", message = "Invalid User")

    session["user_id"] = id
    return redirect(url_for("home"))
    
    
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        
        # if not valid name
        if not name:
            return render_template("error.html", message = "invalid name")
        
        # generate student and save id in session
        user_id = create_student(name)
        session["user_id"] = user_id
        
        return redirect(url_for("home"))
    
    return render_template("signup.html")
    
    
@app.route("/home", methods=["GET","POST"])
def home():
    
    # check log in
    if not session.get("user_id"):
        return redirect(url_for("index"))
    
    # session
    user_id = session.get("user_id")
    name = get_name(user_id)
    student = Student(user_id, name)
    
    # send sports
    student_enrolled_sports = student.get_enrolled_sports
    unenrolled_sports = student.get_unenrolled_sport
    
    return render_template("home.html", name = name, enrolled_sports = student_enrolled_sports, unenrolled_sports = unenrolled_sports, id = session.get("user_id"))

# HOME:
# log out
@app.route("/log_out", methods=["POST"])
def log_out():
    session.clear()
    return redirect(url_for("index"))

# remove sport
@app.route("/remove", methods=["POST"])
def remove_sport():
    id_sport = request.form.get("sport_id")
    student = Student(session.get("user_id"), get_name(session.get("user_id")))
    student.unassign_sport(id_sport)
    return redirect(url_for("home"))

# add sport
@app.route("/add", methods=["POST"])
def add_sport():
    id_sport = request.form.get("sport_id")
    student = Student(session.get("user_id"), get_name(session.get("user_id")))
    student.assign_sport(id_sport)
    return redirect(url_for("home"))

# search 
@app.route("/search")
def search():
    q = request.args.get("q")
    student = Student(session.get("user_id"), get_name(session.get("user_id")))
    founded_sports = student.find_available_sports(q)
    return jsonify(founded_sports)


