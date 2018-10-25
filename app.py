
import falcon
from models import *
from playhouse.shortcuts import model_to_dict
import json
import uuid
from g.auth import Auth

from falcon_auth import FalconAuthMiddleware, BasicAuthBackend

user_loader = lambda username, password: { 'username': username }
auth_backend = BasicAuthBackend(user_loader)
auth_middleware = FalconAuthMiddleware(auth_backend, exempt_routes=['/exempt','/jwt'], exempt_methods=['HEAD'])

class MAuth():
    auth = {
            'auth_disabled': False
        }
    def on_get(self, req, resp):
        if not 'user' in req.context:
            resp.status = falcon.HTTP_404
            return
        user = req.context['user']
        print(user)
        resp.body = "User Found: {}\n".format(user['username'])

    def on_head(self,req,resp):
        resp.body = '?'

class UserIdResource():
    def on_get(self, req, resp, user_id):
        try:
            user = OrgUser.get(OrgUser.id == user_id)
            resp.body = json.dumps(user.serialize())
        except OrgUser.DoesNotExist:
            resp.status = falcon.HTTP_404


class UserResource():
    def on_get(self, req, resp):
        users = OrgUser.select().order_by(OrgUser.id)
        resp.body = json.dumps([u.serialize() for u in users])

    def on_post(self, req, resp):
        user_name = str(uuid.uuid4())[0:8]
        user = OrgUser(username=user_name)
        user.save()
        resp.body = user.serialize()
        #json.dumps(model_to_dict(user))

#api = falcon.API(middleware=[auth_middleware,PeeweeConnectionMiddleware()])
api = falcon.API(middleware=[PeeweeConnectionMiddleware()])

users = UserResource()
users_id = UserIdResource()
auth = MAuth()

api.add_route('/jwt', Auth())
api.add_route('/auth/', auth)
api.add_route('/users/', users)
api.add_route('/users/{user_id}', users_id)
