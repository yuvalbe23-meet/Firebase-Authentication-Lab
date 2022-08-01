
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyA6bm8pnGzHj6pBaN-7mLQpnOAxPEGgpTI",
  "authDomain": "test-882ae.firebaseapp.com",
  "projectId": "test-882ae",
  "storageBucket": "test-882ae.appspot.com",
  "messagingSenderId": "559871725242",
  "appId": "1:559871725242:web:c1339d21b4f0f739e1bc83",
  "measurementId": "G-NX9GJB39PJ",
  "databaseURL": "https://test-882ae-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
db= firebase.database()


@app.route('/', methods=['GET', 'POST'])
def signin():
    eror=""
    if request.method == 'POST':
        email= request.form['email']
        password= request.form['password']

        try: 
            login_session['user']= auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except:
            eror="Not Working"
    return render_template("signin.html")
   


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    eror=""

    if request.method == 'POST':
        email= request.form['email']
        password= request.form['password']

        user={"email": request.form['email'],"password": request.form['password'],"full_name": request.form['full_name'],"username": request.form['username'] }
        try: 
            login_session['user']= auth.create_user_with_email_and_password(email,password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
            eror="Not Working"
    return render_template("signup.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    eror=""
    if request.method== 'POST':
        tweet={"title": request.form['title'],"text":request.form['text'],"uid":login_session['user']['localId']}
        try:
            db.child("Users").child(login_session['user']['localId']).child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            eror="Eror"
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    return render_template("all_tweets.html",all_tweets= db.child("Users").child(login_session['user']['localId']).child("Tweets").get().val())
if __name__ == '__main__':
    app.run(debug=True)