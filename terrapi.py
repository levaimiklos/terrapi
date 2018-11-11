#! /usr/bin/env python3

from webapp import webapp, db, socketio
from webapp.models import User, Post


@webapp.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == "__main__":
    socketio.run(webapp, host='0.0.0.0', port=6969)
