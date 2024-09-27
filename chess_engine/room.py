

import uuid
from typing import Final

ROOM_MAX_CAPACITY: Final[int] = 2


class Room:
    def __init__(self):
        self.rooms_state =[]
        

    def join_room(self, capienza=ROOM_MAX_CAPACITY):
        print("sei entrato in una stanza")
        for room in self.rooms_state:
            if room[1] < capienza:
               room[1]+=1
               print("sono dentro l'if")
               return room[0]

        id= str(uuid.uuid4())
        users= 1
        new_room=[id, users]
        self.rooms_state.append(new_room)
        return id

    def utenti_in_stanza(self,id):
        for room in self.rooms_state:
            if room[0]==id:
                return room[1]
            
    def ha_lasciato(self,id):         
        for room in self.rooms_state:
            if room[0]==id:
                room[1]= 0 if room[1]==0 else room[1]-1
            