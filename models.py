

from peewee import *
import uuid
from datetime import datetime
import json

db = SqliteDatabase('users.db');

def init_tables():
     db.create_tables([OrgUser], safe=True)


def generate_users(num_users):
     for i in range(num_users):
         user_name = str(uuid.uuid4())[0:8]
         OrgUser(username=user_name).save()


class PeeweeConnectionMiddleware(object):
     def process_request(self, req, resp):
         db.connection()


class BaseModel(Model):
     class Meta:
         database = db


class OrgUser(BaseModel):
    username = CharField(unique=True)
    created = DateTimeField(default=datetime.now())

    def serialize(self):
        return {
                    "id": self.id,
                    "username": self.username,
                    "created": unicode(self.created)
                }

