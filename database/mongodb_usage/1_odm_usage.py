from mongoengine import connect, Document, StringField
import logging
from pymongo import monitoring
from mongoengine import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} started on server "
                  "{0.connection_id}".format(event))

    def succeeded(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} on server {0.connection_id} "
                  "succeeded in {0.duration_micros} "
                  "microseconds".format(event))

    def failed(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} on server {0.connection_id} "
                  "failed in {0.duration_micros} "
                  "microseconds".format(event))


con = connect(
    db="test-repo"
)


class UserDocument(Document):
    user_id = StringField(primary_key=True)
    user_name = StringField()


import uuid

log.info('Querying through MongoEngine...')

users = UserDocument.objects.first()

# UserDocument.objects.insert(users)

con.close()
