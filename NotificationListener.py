#!/usr/bin/env python

""" TODO make explanation here """

from infi.systray import SysTrayIcon
import webbrowser
from flask import Flask, request, Response, jsonify
from functools import wraps
from win10toast import ToastNotifier

__author__ = "Lukas Rønsholt"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Lukas Rønsholt"
__email__ = "lukasronsholt@gmail.com"
__status__ = "Development"


class ServerPrograms:
    ip = "http://192.168.0.72"
    torrent = ip + ":32400/web"
    plex = ip + ":8080"


class SystemTray(object):
    def __init__(self):
        self._hover_text = "Media Server Client"
        self._icon = "server.ico"
        self._options = (('Plex', None, self._openPlex),('Torrent', None, self._openTorrent))
        self._system_tray = SysTrayIcon(self._icon, self._hover_text, self._options)

    def _openPlex(self, icon: SysTrayIcon):
        webbrowser.open(ServerPrograms.plex)

    def _openTorrent(self, icon: SysTrayIcon):
        webbrowser.open(ServerPrograms.torrent)

    def run(self):
        self._system_tray.start()


def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate():
    message = {'message': "I'm sorry Dave, I'm afraid I can't do that"}
    resp = jsonify(message)

    resp.status_code = 401

    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def notification_body(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return Response(status=400)
        if "title" not in request.get_json() or "message" not in request.get_json():
            return Response(status=400)
        return f(*args, **kwargs)
    return decorated


def showNotification(title, message):
    toaster.show_toast(title, message,  icon_path="server_128.ico", duration=10,  threaded=True)


webServer = Flask(__name__)
toaster = ToastNotifier()


@webServer.route('/success', methods=["POST"])
@requires_auth
@notification_body
def successNotification():
    showNotification(request.get_json()["title"], request.get_json()["message"])
    return Response(status=200)


@webServer.route('/warning', methods=["POST"])
@requires_auth
@notification_body
def warningNotification():
    showNotification(request.get_json()["title"], request.get_json()["message"])
    return Response(status=200)


@webServer.route('/error', methods=["POST"])
@requires_auth
@notification_body
def errorNotification():
    showNotification(request.get_json()["title"], request.get_json()["message"])
    return Response(status=200)


SystemTray().run()
webServer.run()
