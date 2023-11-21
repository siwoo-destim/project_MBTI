"""
 the first alphabet of the roomname must be "@".
 ex) @myroom

 this function query database by its "room" param to let api know this room with supplied "roomname" param exist.
 after checking that, it returns what it received at first
"""

from fastapi import HTTPException, status
from BACK.models.rooms import Room


async def verify_room(roomname: str):
    if not roomname[0] == "@":
        print("1")
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="First alphabet of the roomname must be '@'"
        )

    room = await Room.find_one(Room.roomname == roomname)

    if not room:
        print("2")
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room with supplied roomname does not exist"
        )

    return room.roomname
