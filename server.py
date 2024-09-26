import socket
from _thread import *
import sys

server = "192.168.86.72"
port = 25566
player_count = 0
spotsTaken = 0
freeze = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
users = []

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print("Waiting for a connection, Server Started")

coordinates = dict()
for i in range(0, 8):
    for k in range(0, 8):
        temp_coord = str(i) + ' ' + str(k)
        coordinates[temp_coord] = "empty"

def threaded_client(conn):
    global player_count
    global spotsTaken
    global freeze
    player_count += 1
    conn.send(str.encode("Connected as Player {}".format(player_count)))
    packet = 0
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if reply == "Q":
                users.remove(conn)
                print("Lost connection")
                player_count -= 1
                conn.close()
                break
            elif reply == "reset":
                #Does this even work properly?
                for i in range(0, 8):
                    for k in range(0, 8):
                        temp_coord = str(i) + ' ' + str(k)
                        coordinates[temp_coord] = "empty"
                for u in users:
                    u.send(str.encode(reply))
                freeze = True
                spotsTaken = 0

            elif reply == "start":
                for u in users:
                    u.send(str.encode(reply))
                freeze = False
            else:
                # print(reply)
                temp = reply.split()
                if temp[0] == "draw" and freeze == False:
                    coords = temp[1] + ' ' + temp[2]
                    color = temp[3]
                    if coordinates[coords] == "empty" or coordinates[coords] == color:
                        for u in users:
                            u.send(str.encode(reply))
                        coordinates[coords] = color
                elif temp[0] == "fill" and freeze == False:
                    coords = temp[2] + ' ' + temp[3]
                    color = temp[4]
                    if coordinates[coords] != "done":
                        if coordinates[coords] == color:
                            print("Sending")
                            for u in users:
                                u.send(str.encode(reply))
                            if temp[1] == "fail":
                                coordinates[coords] = "empty"
                            elif temp[1] == "pass":
                                coordinates[coords] = "done"
                                spotsTaken += 1
                                if spotsTaken >= 64:
                                    for u in users:
                                        u.send(str.encode("finish"))
                                    freeze = True


        except:
            pass


while True:
    conn, addr = s.accept()
    users.append(conn)
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))