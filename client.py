import socket 
import threading
client_s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client_s.connect(("127.0.0.1",12345))

def chiffrer(message):
    """Fonction de chiffrage simple qui décale les lettres d'un 
    certains nombre en faisaant bien attention qu'une fois arrivé à la lettre z on renviens à la lettre a"""
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
    """Fonction de déchiffrage miroir de la fonction de chiffrage pour retourner au message d'origine"""
    resultat = ""
    for elmt in message:
        if 'A' <= elmt <= 'Z':
            resultat += chr((ord(elmt) - ord("A") - 5) % 26 + ord("A"))
        elif 'a' <= elmt <= 'z':
            resultat += chr((ord(elmt) - ord("a") - 5) % 26 + ord("a"))
        else:
            resultat += elmt
    return resultat
#Boucle d'envoie/approbation du serveur pour le pseudo
while True :
    pseudo = input("Veuillez entrez votre pseudo :")# On entre son pseudo
    client_s.send(pseudo.encode()) #Le client l'envoie au serveur qui vérifie 
    reponse = client_s.recv(1024).decode()# On stock la réponse server 

    if reponse == "Refusé" : # Si pseudo déjà utilisé on retourne au début de la boucle
        print("Pseudo déjà utilisé.")
    elif reponse == "Ok" :#sinon On est connecté et le serveur nous enregistre
        print("Vous êtes connecté !")
        break
def envoyer():
    """Fonction servant à traiter les envoies côté client"""
    while True : 
        msg = input(f"{pseudo} >>>")
        msg_list = msg.split(" ",2)
        if msg_list[0]=="/msg" and len(msg_list) >= 3:#Si l'utilisateur commence une commande par /msg on chiffre le coeur du msg
            msg_final=msg_list[0]+" "+ msg_list[1]+" "+chiffrer(msg_list[2])
            client_s.send(msg_final.encode())
        elif msg == "/quit": #La commande pour que l'utilisateur se déconnecte est gérer côté client
            client_s.close()
            break
        else:
            client_s.send(msg.encode())#si la commande est différente de /msg on ne chiffre pas
def recevoir():
    """Fonction servant à traiter les réceptions côté client"""
    while True :
        msg_recv = client_s.recv(1024).decode()
        if not msg_recv: # Si le client ne peut plus reçevoir de messages on stop la connexion
            print("Connexion fermée par le serveur")
            client_s.close()
            break
        msg_list = msg_recv.split(" ",2)
        if msg_list[0] == "/msg" and len(msg_list) >= 3: #Si l'utilisateur reçoit une commande commençant par /msg on déchiffre le coeur du message
            msg_recv = dechiffrer(msg_list[2]) 
            print(f"{msg_list[1]} vous a envoyé : {msg_recv}")
        else : 
            print(msg_recv) #sinon 
threading.Thread(target=envoyer).start() #On démarre le thread pour que le client puisse envoyer
threading.Thread(target=recevoir).start() #Un autre pour que l'utilisateur puisse reçevoir 
#Les deux threads tournent en parrallèle