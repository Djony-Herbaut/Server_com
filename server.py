import socket 
import threading

clients = {}
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) #Af_Inet = pour une connexion IPv4 / Sock_steam = connexion en TCP

s.bind(("127.0.0.1", 12345)) # on écoute bind("Ip",port)
s.listen(4) # nb utilisateur max dans la file d'attente

print("Serveur en écoute sur le port 12345...")

def gerer_client(conn,pseudo):
    """Fonction qui effecctue la gestion des messages envoyé par le client"""
    try:
        while True:
            try:
                msg = conn.recv(1024).decode()
            except ConnectionResetError or ConnectionAbortedError:
                break 
            if not msg:  # client se déconnecte
                break
            msg_list = msg.split(" ",2)
            match msg_list[0] :
                case "/users":
                    conn.send("Voici la liste des utilisateurs connectés :\n".encode())
                    for valeur in clients.items():
                        conn.send(f"{valeur[0]}\n".encode())
                case "/msg":
                    if len(msg_list) < 3:
                        conn.send("Vous devriez tapez: /msg <pseudo|all> <message>\n".encode())
                        continue
                    cible = msg_list[1]
                    contenu = msg_list[2]
                    if cible == "all":
                        for user, sock in clients.items():
                            if user != pseudo:
                                sock.send(f"/msg {pseudo} {contenu}\n".encode())
                    else:
                        if cible in clients:
                            cible_socket = clients[cible]
                            cible_socket.send(f"/msg {pseudo} {contenu}\n".encode())
                        else:
                            conn.send(f"Utilisateur {cible} introuvable.\n".encode())
    finally:
        print(f"{pseudo} déconnecté")
        if pseudo in clients:
            del clients[pseudo]
        conn.close()
    
while True:
    conn, addr = s.accept() # ici le serveur attend la connexion d'un client avec un connect(ip,port) et conn va être égal à un socket dédié au client et adrr un tuple contenant le port et l'ip du client
    print(f"Nouvelle connexion : {addr}")
    pseudo_valide = False
    while not pseudo_valide:
        pseudo = conn.recv(1024).decode() #on définit la taille d'un paquet à 1024octets max et on attribut la réponse de l'utilisateur à son pseudo
        if pseudo not in clients :
            conn.send("Ok".encode())
            pseudo_valide = True
            clients[pseudo] = conn
            print(f"{pseudo} est connecté")
            threading.Thread(target=gerer_client, args=(conn,pseudo)).start()
        else : 
            conn.send("Refusé".encode())