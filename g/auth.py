
import jwt
import datetime
import json

# Should be in config file :-)
secret = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmb3QubnUiLCJyb2xlIjoiYWRtaW4iLCJzdWIiOiJrYWxsZSIsImV4cCI6MTU0MDMyNjEwMn0.PJBrMWt8VqUOZLBWSKDp-2ZFO-PLO-gT2Gmjkeu_-e0"
alg = "HS256"
ttl = 30

class Auth():
    def on_post(self, req, resp):
        if req.content_length:
            doc = json.load(req.stream)

        # Do real stuff :-)
        if 'user' in doc and 'password' in doc and doc['password'] == 'secret':
            resp.body =  jwt.encode({
                                    'sub': doc['user'], 
                                    'iss': 'fot.nu', 
                                    'role':'admin',
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=ttl)
                                }, secret, algorithm=alg) + "\n"
        else:
            resp.body = json.dumps("BEeeep") + "\n"

    def on_get(self, req, resp):
        try:
            resp.body = json.dumps(jwt.decode(req.params['jwt'], secret, algorithms=[alg]))
        except Exception as e:
            resp.body = json.dumps(str(e))