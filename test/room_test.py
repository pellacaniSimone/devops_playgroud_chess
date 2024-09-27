#!/usr/local/bin/python3
import unittest

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
os.chdir('../')
# fix path

from chess_engine.room import Room

import re

class room_test(unittest.TestCase):

    def test_capacity(self):
        """Testa la dimensione delle stanze"""
        self.assertEqual(2, Room.ROOM_MAX_CAPACITY )  # add assertion here

    def test_uuid(self):
        """Testa il numeri di utenti in ogni stanza e se UUID funziona"""
        ro=Room()
        UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
        for _ in range(6):
            fu1 = ro.join_room()
            n1 = ro.utenti_in_stanza(fu1)
            self.assertEqual(1, n1) # socketio fa join a caso
            Actual = bool(UUID_PATTERN.match(fu1))
            self.assertEqual( True ,Actual )
            fu2 = ro.join_room()
            n2 = ro.utenti_in_stanza(fu2)
            self.assertEqual(2, n2)
            actual = bool(UUID_PATTERN.match(fu2))
            self.assertEqual( True ,actual )
            self.assertEqual( fu1 , fu2)

    def test_capacity(self):
        """Testa quando si lascia la stanza"""
        ro = Room()
        fu1 = ro.join_room()
        fu2 = ro.join_room()
        ro.ha_lasciato(fu1)
        ro.ha_lasciato(fu2)
        ro.ha_lasciato(fu2)
        self.assertEqual( 0 , ro.rooms_state[0][1]) # valore negativo, consiglio metere un controllo in ha lasciato



if __name__ == '__main__':
    unittest.main()