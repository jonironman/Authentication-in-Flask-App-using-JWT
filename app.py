from flask import Flask, request, jsonify, make_response, render_template, session
import config
import jwt
from datetime import datetime, timedelta
from functools import wraps



app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify( {'Alert' : 'Token is missing!'})
        try:
            data = jwt.decode( token, app.config['SECRET_KEY'] )
        except:
            return jsonify( {'Alert' : 'Invalid Token!'})
        return func(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'logged in currently!'

@app.route('/public')
def public():
    return 'For public'


@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard'



@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        
        # token = jwt.encode ({
        #         'user': request.form['username'],
        #         'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        #     },
        #     app.config['SECRET_KEY']
        # )
        # return jsonify( { 'toket' : token.decode('utf-8')})
        token = jwt.encode({
            'user': request.form['username'],
            # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token})

    else: 
        return make_response('unable to verify', 403, {'WWW-Authenticate' : 'Basic Autifiacation Falied!'})
 
 
if __name__ == "__main__":
    app.run(debug=True)
