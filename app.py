from flask import Flask, session, request, Blueprint, redirect, url_for
from flask_restful import Api, Resource
import os, random, string

app = Flask(__name__)
n = 5
app.secret_key = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])
api_bp = Blueprint('api', "flask-restful with blueprint", url_prefix="/api",)
api = Api(api_bp)

CRYPT_PHRASE = dict()
SESSIONS = dict()

@app.before_request
def _before_request():
    print("やっほー")
    if 'auth' in session:
        print("sessionあるよ")
        return 'Hello ' + str(session['auth'])
    # return 'You are not logged in'
    print("sessionないよ")
    print("url_for api.login is %s" % url_for('api.login'))
    redirect(url_for('api.login'), code=302)

class Login(Resource):
    def get(self):
        return self._create_passphrase()

    def post(self):
        res = self._request_phrase_verification(request.json)
        if res:
            session['auth'] = True
            return {"message": "login succeded!!!"}, 200
        else:
            return {"message": "login failed, request passphrase not matchd."}, 503

    def put(self):
        return {"login": "put"}

    def _create_passphrase(self):
        n = 5
        base_phrase = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])
        phrase_data = { base_phrase: base_phrase }
        CRYPT_PHRASE.update(phrase_data)
        print("CRYPT_PHRASE is %s" % CRYPT_PHRASE)
        return { "phrase": base_phrase }

    def _request_phrase_verification(self, jsondata):
        if not jsondata['pass_phrase'] in CRYPT_PHRASE:
            print("key not found")
            return False
        verification_data = jsondata['pass_phrase']
        if CRYPT_PHRASE[verification_data]:
            return True
        else:
            return False
    

api.add_resource(Login, '/login')
app.register_blueprint(api_bp)

class License(Resource):
    def get(self):
        #return redirect(url_for('api.login'), code=302)
        return {"license": "get"}

    def post(self):
        return {"license": "post"}

    def put(self):
        return {"license": "put"}

    def delete(self):
        return {"license": "delete"}

api.add_resource(License, '/license')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

