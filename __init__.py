from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, join
import hashlib
import os

app = Flask(__name__)
app.secret_key = "oogabooga"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///characters.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Misc(db.Model):
    char = db.Column(db.String(20), primary_key=True)
    weight = db.Column(db.Integer())
    gravity = db.Column(db.Float())
    walk_speed = db.Column(db.Float())
    run_speed = db.Column(db.Float())
    wd_length = db.Column(db.Integer())
    wd_frames = db.Column(db.Integer())
    jump_squat = db.Column(db.Integer())
    wall_jump = db.Column(db.Boolean())
    notes = db.Column(db.String(200))

    def __init__(self, c, wght, gr, ws, rs, js, wj, n, wdl, wdf):
        self.char = c
        self.weight = wght
        self.gravity = gr
        self.walk_speed = ws
        self.run_speed = rs
        self.wd_length = wdl
        self.wd_frames = wdf
        self.jump_squat = js
        self.wall_jump = wj
        self.notes = n


class Attacks(db.Model):
    char = db.Column(db.String(20))
    move = db.Column(db.String(20))
    start = db.Column(db.Integer())
    end = db.Column(db.Integer())
    total = db.Column(db.Integer())
    iasa = db.Column(db.Integer())
    ld_fl_spec = db.Column(db.Integer())
    stun = db.Column(db.Integer())
    percent = db.Column(db.Float())
    percent_weak = db.Column(db.Float())
    notes = db.Column(db.String(200))

    auto_cancel_s = db.Column(db.Integer())
    auto_cancel_e = db.Column(db.Integer())
    land_lag = db.Column(db.Integer())  # aerials only
    cancel_lag = db.Column(db.Integer())  # derived from land_lag

    __table_args__ = (PrimaryKeyConstraint("char", "move"), {})

    def __init__(self, c, mv, st, ed, tot, per, n, isa, stn, w_per, aos=-1, aoe=-1, ll=-1, spec=-1):
        self.char = c
        self.move = mv
        self.start = st
        self.end = ed
        self.total = tot
        self.percent = per
        self.notes = n
        self.iasa = isa
        self.stun = stn
        self.ld_fl_spec = spec
        self.auto_cancel_s = aos
        self.auto_cancel_e = aoe

        if w_per != "":
            self.percent_weak = w_per

        if ll != "":
            self.land_lag = int(ll)
            if self.land_lag >= 0:
                self.cancel_lag = self.land_lag // 2
        else:
            self.cancel_lag = -1


class Grabs(db.Model):
    char = db.Column(db.String(20))
    type = db.Column(db.String(10))
    start = db.Column(db.Integer())
    total = db.Column(db.Integer())
    notes = db.Column(db.String(200))

    __table_args__ = (PrimaryKeyConstraint("char", "type"), {})

    def __init__(self, c, ty, st, tot, n):
        self.char = c
        self.type = ty
        self.start = st
        self.total = tot
        self.notes = n


class Throws(db.Model):
    char = db.Column(db.String(20))
    type = db.Column(db.String(10))
    start = db.Column(db.Integer())
    end = db.Column(db.Integer())
    total = db.Column(db.Integer())
    percent = db.Column(db.Float())
    notes = db.Column(db.String(200))

    __table_args__ = (PrimaryKeyConstraint("char", "type"), {})

    def __init__(self, c, ty, st, ed, tot, per, n):
        self.char = c
        self.type = ty
        self.start = st
        self.end = ed
        self.total = tot
        self.percent = per
        self.notes = n


class Dodges(db.Model):
    char = db.Column(db.String(20))
    type = db.Column(db.String(20))
    start = db.Column(db.Integer())
    inv_end = db.Column(db.Integer())
    total = db.Column(db.Integer())
    notes = db.Column(db.String(200))

    __table_args__ = (PrimaryKeyConstraint("char", "type"), {})

    def __init__(self, c, ty, st, ed, tot, n):
        self.char = c
        self.type = ty
        self.start = st
        self.total = tot
        self.notes = n

        if ed != "":
            self.inv_end = ed

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home_page.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"].encode("utf8")
        pswd = request.form["pw"].encode("utf8")
        user = hashlib.sha1(user).hexdigest()
        pswd = hashlib.sha1(pswd).hexdigest()
        current_path = os.getcwd()
        #functionality disabled on server, need to find what path apache runs in
        f = open(current_path+"/static/keys.txt", "r")
        auth_user = (f.readline()).replace("\n", "")
        auth_pswd = (f.readline()).replace("\n", "")
        f.close()
        if user == auth_user and pswd == auth_pswd:
            return redirect(url_for("admin", usr=user, ps=pswd, a_usr=auth_user, a_ps=auth_pswd))
        else:
            flash("Incorrect Login Info")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "GET":
        n = request.args.get('usr')
        p = request.args.get('ps')
        a_n = request.args.get('a_usr')
        a_p = request.args.get('a_ps')
        if n != a_n or p != a_p or n == None:
            return redirect(url_for("home"))
        else:
            return render_template("admin.html")
    else:
        char = request.form["char"]
        char = char.lower()
        char = char.replace(" ", "_")  # format variety of inputs

        sub_type = request.form["sub"]

        m = "Misc"

        if m in sub_type:
            move = ""
            wght = request.form["wght"]
            gty = request.form["grav"]
            #need to change name in db class
            ws = request.form["dash_spd"]
            rs = request.form["run_spd"]
            js = request.form["jump_sqt"]
            wl = request.form["wd_length"]
            wf = request.form["wd_frames"]
            notes = request.form["notes"]

            if request.form["wall_jp"] == "y":
                wj = True
            else:
                wj = False

            fc = Misc.query.filter_by(char=char).first()
            if fc:
                fc.weight = wght
                fc.gravity = gty
                fc.walk_speed = ws
                fc.run_speed = rs
                fc.jump_squat = js
                fc.wd_length = wl
                fc.wd_frames = wf
                fc.notes = notes
                fc.wall_jump = wj
            else:
                model = Misc(char, wght, gty, ws, rs, js, wj, notes, wl, wf)

        else:
            move = request.form["move"]
            start = request.form["start"]
            total = request.form["total"]
            notes = request.form["notes"]

            g = "Grab"
            t = "Throw"
            d = "Dodge"
            n = "Normal"
            s = "Special"
            a = "Aerial"

            if g not in sub_type:
                end = request.form["active_end"]

            if s in sub_type:
                ld_fall = request.form["land_fall"]

            if d not in sub_type and g not in sub_type:
                percent = request.form["percent"]
                if t not in sub_type:
                    stun = request.form["stun"]
                    iasa = request.form["iasa"]
                    w_percent = request.form["w_per"]
                    if n not in sub_type:
                        lag = request.form["lag"]
                        if s not in sub_type:
                            aos = request.form["aos"]
                            aoe = request.form["aoe"]

            if g in sub_type:
                fc = Grabs.query.filter_by(char=char, type=move).first()
                if fc:
                    fc.start = start
                    fc.total = total
                    fc.notes = notes
                else:
                    model = Grabs(char, move, start, total, notes)
            elif t in sub_type:
                fc = Throws.query.filter_by(char=char, type=move).first()
                if fc:
                    fc.start = start
                    fc.end = end
                    fc.total = total
                    fc.percent = percent
                    fc.notes = notes
                else:
                    model = Throws(char, move, start, end, total, percent, notes)
            elif d in sub_type:
                fc = Dodges.query.filter_by(char=char, type=move).first()
                if fc:
                    fc.start = start
                    fc.inv_end = end
                    fc.total = total
                    fc.notes = notes
                else:
                    model = Dodges(char, move, start, end, total, notes)
            elif n in sub_type:
                fc = Attacks.query.filter_by(char=char, move=move).first()
                if fc:
                    fc.start = start
                    fc.end = end
                    fc.total = total
                    fc.iasa = iasa
                    fc.stun = stun
                    fc.percent = percent
                    fc.notes = notes
                    if w_percent != "":
                        fc.percent_weak = w_percent
                else:
                    model = Attacks(char, move, start, end, total, percent, notes, iasa, stun, w_percent)
            else:
                fc = Attacks.query.filter_by(char=char,move=move).first()
                if fc:
                    fc.start = start
                    fc.end = end
                    fc.total = total
                    fc.land_lag = lag
                    fc.cancel_lag = int(lag)//2
                    fc.percent = percent
                    fc.notes = notes
                    fc.iasa = iasa
                    fc.stun = stun

                    if w_percent != "":
                        fc.percent_weak = w_percent

                    if s in sub_type:
                        fc.ld_fl_spec = ld_fall
                    else:
                        fc.auto_cancel_s = aos
                        fc.auto_cancel_e = aoe
                else:
                    if s in sub_type:
                        model = Attacks(char, move, start, end, total, percent, notes, iasa, stun, w_percent, -1, -1, lag, ld_fall)
                    else:
                        model = Attacks(char, move, start, end, total, percent, notes, iasa, stun, w_percent, aos, aoe, lag)


        try:
            db.session.add(model)
            db.session.commit()
            #keep these lines commented, causes errors on deployment server
            #flash(f"Successfully submitted info for {char} {move}")
        except:
            db.session.commit()
            #flash(f"Successfully updated info for {char} {move}")

        return render_template("admin.html")


def char(c, hits):
    i = c.lower()
    boxes = "N"
    if hits:
        boxes = "Y"
    img = "static/images/profImgs/" + i + ".png"
    gif = "static/gifs/" + i + "/"
    data = format(i)
    i = i.upper()
    i = i.replace("_", " ")
    return render_template("char.html", data=data, name=i, img=img, style=boxes, gif=gif, box=boxes, path=c)


@app.route("/<c>", methods=["POST", "GET"])
def char_desk(c):
    hits = True
    if request.method == "POST":
        if request.form["submit_button"] == " Select Another Character ":
            return(redirect(url_for("home")))
        elif request.form["submit_button"] == "      Toggle Hitboxes Off      ":
           hits = False
    return char(c, hits)


@app.route("/template")
def template():
    return render_template("char.html")


@app.route("/test")
def test():
    return render_template("test_char.html")


# format in a way data can be displayed easily
def format(name):
    arr = ["jab1", "ftilt", "utilt", "dtilt", "dattack", "fsmash",
           "usmash", "dsmash", "nair", "fair", "bair", "uair",
           "dair", "neutral_b", "up_b", "side_b", "down_b",
           "standing_grab", "dash_grab", "pivot_grab", "forward_throw",
           "back_throw", "down_throw", "up_throw", "spot_dodge",
           "back_roll", "forward_roll", "air_dodge", "jab2",
           "jab3", "rjab", "aneutral_b", "aside_b", "aup_b", "adown_b"]
    data = []

    # Sloppy but effective :)
    for i in range(17):
        data.append(Attacks.query.filter_by(char=name, move=arr[i]).first())
    for i in range(17, 20):
        data.append(Grabs.query.filter_by(char=name, type=arr[i]).first())
    for i in range(20, 24):
        data.append(Throws.query.filter_by(char=name, type=arr[i]).first())
    for i in range(24, 28):
        data.append(Dodges.query.filter_by(char=name, type=arr[i]).first())

    #data added in ver2
    for i in range(28, 35):
        data.append(Attacks.query.filter_by(char=name, move=arr[i]).first())

    data.append(Misc.query.filter_by(char=name).first())


    return data


if __name__ == "__main__":
    db.create_all()

    #change to commented line if debugging
    #app.run(host='0.0.0.0', debug=True)
    app.run(host='0.0.0.0')

