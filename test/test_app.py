#!/usr/local/bin/python3
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
os.chdir('../')
# fix path


import urllib.request as urllib2 # In Python 3, urllib2 was replaced by two in-built  modules named urllib.request and  urllib.error
import unittest
from flask import Flask
from flask_testing import TestCase
import app as a
from flask_testing import LiveServerTestCase
import contextlib




class test_local_routes(TestCase):
    """Testa che le pagine restituiscano 200"""
    render_templates = True

    local_url = "http://localhost"
    local_port = "80"

    def __get_server_url(self):
        return self.__server_url

    def create_app(self):
        """crea una app di test client per il server attivo sulla porta 12100"""
        app = Flask(
            __name__,
            static_folder = 'static',
            template_folder = 'static',
            static_url_path=''
        )
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = int(self.local_port) # funziona solo in Sviluppo, ma per tutti la porta del sever è la 80
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app
    

    def test_index(self):
        """controlla che il server alla porta sia "Up and running" alla pagina di ingresso principale index """
        response = urllib2.urlopen(self.local_url+":"+self.local_port+"/index")
        self.assertEqual(response.code, 200)

    def test_gamepvp(self):
        """testa che gamepvp.html sia chiamato da /gamepvp"""
        response = urllib2.urlopen(self.local_url+":"+self.local_port+"/gamepvp")
        self.assertEqual(response.code, 200)

    def test_gamepixel(self):
        """testa che gamepvp.html sia chiamato da  /gamepixel"""
        response = urllib2.urlopen(self.local_url+":"+self.local_port+"/gamepixel")
        self.assertEqual(response.code, 200)

    def test_cypress_on(self):
        """testa che Vue sia chiamato da /cypress"""
        response = urllib2.urlopen(self.local_url+":"+self.local_port+"/cypress")
        self.assertEqual(response.code, 200)

    def test_loginForm(self):
        """testa che gamepvp.html sia chiamato da lla chiamata get /loginForm.html"""
        response = urllib2.urlopen(self.local_url+":"+self.local_port+"/loginForm.html")
        self.assertEqual(response.code, 200)

    def test_logout(self):
        """testa che gamepvp.html sia chiamato da lla chiamata get /logout"""
        response = urllib2.urlopen(self.local_url+":"+self.local_port+"/logout")
        self.assertEqual(response.code, 200)



if __name__ == '__main__':
    unittest.main()
