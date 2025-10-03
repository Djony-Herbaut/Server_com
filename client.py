import socket 
import threading
client_s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client_s.connect(("127.0.0.1",12345))

def chiffrer(message):
    resultat = ""
    for elmt in message:
        if 'A' <= elmt <= 'Z': 
           resultat += chr((ord(elmt) - ord("A") + 5) % 26 + ord("A"))
        elif 'a' <= elmt <= 'z':
            resultat += chr((ord(elmt) - ord("a") + 5) % 26 + ord("a"))
        else:
            resultat += elmt
    return resultat

def dechiffrer(message):
    resultat = ""
    for elmt in message:
        if 'A' <= elmt <= 'Z':
            resultat += chr((ord(elmt) - ord("A") - 5) % 26 + ord("A"))
        elif 'a' <= elmt <= 'z':
            resultat += chr((ord(elmt) - ord("a") - 5) % 26 + ord("a"))
        else:
            resultat += elmt
    return resultat

while True :
    pseudo = input("Veuillez entrez votre pseudo :")
    client_s.send(pseudo.encode())
    reponse = client_s.recv(1024).decode()

    if reponse == "Refusé" : 
        print("Pseudo déjà utilisé.")
    elif reponse == "Ok" :
        print("Vous êtes connecté !")
        break
def envoyer():
    while True : 
        msg = input(f"{pseudo} >>>")
        msg_list = msg.split(" ",2)
        if msg_list[0]=="/msg" and len(msg_list) >= 3:
            msg_final=msg_list[0]+" "+ msg_list[1]+" "+chiffrer(msg_list[2])
            client_s.send(msg_final.encode())
        elif msg == "/quit":
            client_s.close()
            break
        else:
            client_s.send(msg.encode())
def recevoir():
    while True :
        msg_recv = client_s.recv(1024).decode()
        if not msg_recv:
            print("Connexion fermée par le serveur")
            client_s.close()
            break
        msg_list = msg_recv.split(" ",2)
        if msg_list[0] == "/msg" and len(msg_list) >= 3:
            msg_recv = dechiffrer(msg_list[2])
            print(f"{msg_list[1]} vous a envoyé : {msg_recv}")
        else : 
            print(msg_recv)
threading.Thread(target=envoyer).start()
threading.Thread(target=recevoir).start()