from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_clean_code", methods=["GET","POST"])
def add_one_clean_code():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into clean_code (name,description) values (:name,:description)",hey)
        user = query_db('select * from clean_code')

        return render_template("clean_codeform.html", clean_codes=user, one_user=one_user, the_title="add new clean_code")


    user = query_db('select * from clean_code')
    one_user = query_db("select * from clean_code limit 1", one=True)
    return render_template("clean_codeform.html", clean_codes=user, one_user=one_user, the_title="add new clean_code")

@app.route("/add_one_traveler_status", methods=["GET","POST"])
def add_one_traveler_status():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into traveler_status (status,description,date) values (:status,:description,:date)",hey)
        user = query_db('select * from traveler_status')

        return render_template("traveler_statusform.html", traveler_statuss=user, one_user=one_user, the_title="add new traveler_status")


    user = query_db('select * from traveler_status')
    one_user = query_db("select * from traveler_status limit 1", one=True)
    return render_template("traveler_statusform.html", traveler_statuss=user, one_user=one_user, the_title="add new traveler_status")

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,email,password,phone,country_id) values (:username,:email,:password,:phone,:country_id)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','email','password','phone','country_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','email','password','phone','country_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','email','password','phone','country_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_user_traveler", methods=["GET","POST"])
def add_one_user_traveler():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        touslestraveler_status= query_db("select * from traveler_status")

        one_user = query_db("insert into user_traveler (user_id,traveler_status_id) values (:user_id,:traveler_status_id)",hey)
        user = query_db('select * from user_traveler')

        return render_template("user_travelerform.html", user_travelers=user, one_user=one_user, the_title="add new user_traveler", touslesuser=touslesuser, touslestraveler_status=touslestraveler_status)


    touslesuser= query_db("select * from user")

    touslestraveler_status= query_db("select * from traveler_status")

    user = query_db('select * from user_traveler')
    one_user = query_db("select * from user_traveler limit 1", one=True)
    return render_template("user_travelerform.html", user_travelers=user, one_user=one_user, the_title="add new user_traveler", touslesuser=touslesuser, touslestraveler_status=touslestraveler_status)

@app.route("/add_one_product", methods=["GET","POST"])
def add_one_product():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into product (description,user_id,date) values (:description,:user_id,:date)",hey)
        user = query_db('select * from product')

        return render_template("productform.html", products=user, one_user=one_user, the_title="add new product", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from product')
    one_user = query_db("select * from product limit 1", one=True)
    return render_template("productform.html", products=user, one_user=one_user, the_title="add new product", touslesuser=touslesuser)

@app.route("/add_one_rspectdd", methods=["GET","POST"])
def add_one_rspectdd():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into rspectdd (name) values (:name)",hey)
        user = query_db('select * from rspectdd')

        return render_template("rspectddform.html", rspectdds=user, one_user=one_user, the_title="add new rspectdd")


    user = query_db('select * from rspectdd')
    one_user = query_db("select * from rspectdd limit 1", one=True)
    return render_template("rspectddform.html", rspectdds=user, one_user=one_user, the_title="add new rspectdd")

@app.route("/add_one_producthascleancode", methods=["GET","POST"])
def add_one_producthascleancode():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesproduct= query_db("select * from product")

        touslesclean_code= query_db("select * from clean_code")

        one_user = query_db("insert into producthascleancode (product_id,clean_code_id) values (:product_id,:clean_code_id)",hey)
        user = query_db('select * from producthascleancode')

        return render_template("producthascleancodeform.html", producthascleancodes=user, one_user=one_user, the_title="add new producthascleancode", touslesproduct=touslesproduct, touslesclean_code=touslesclean_code)


    touslesproduct= query_db("select * from product")

    touslesclean_code= query_db("select * from clean_code")

    user = query_db('select * from producthascleancode')
    one_user = query_db("select * from producthascleancode limit 1", one=True)
    return render_template("producthascleancodeform.html", producthascleancodes=user, one_user=one_user, the_title="add new producthascleancode", touslesproduct=touslesproduct, touslesclean_code=touslesclean_code)

@app.route("/add_one_producthasrspectdd", methods=["GET","POST"])
def add_one_producthasrspectdd():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesproduct= query_db("select * from product")

        touslesrspectdd= query_db("select * from rspectdd")

        one_user = query_db("insert into producthasrspectdd (product_id,rspectdd_id) values (:product_id,:rspectdd_id)",hey)
        user = query_db('select * from producthasrspectdd')

        return render_template("producthasrspectddform.html", producthasrspectdds=user, one_user=one_user, the_title="add new producthasrspectdd", touslesproduct=touslesproduct, touslesrspectdd=touslesrspectdd)


    touslesproduct= query_db("select * from product")

    touslesrspectdd= query_db("select * from rspectdd")

    user = query_db('select * from producthasrspectdd')
    one_user = query_db("select * from producthasrspectdd limit 1", one=True)
    return render_template("producthasrspectddform.html", producthasrspectdds=user, one_user=one_user, the_title="add new producthasrspectdd", touslesproduct=touslesproduct, touslesrspectdd=touslesrspectdd)

