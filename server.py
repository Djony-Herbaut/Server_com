import socket 
import threading

clients = {}
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) #Af_Inet = pour une connexion IPv4 / Sock_steam = connexion en TCP

s.bind(("127.0.0.1", 12345)) # on écoute bind("Ip",port)
s.listen(4) # nb utilisateur max dans la file d'attente

print("Serveur en écoute sur le port 12345...")

def gerer_client(conn,pseudo): #
    """Fonction qui effecctue la gestion des messages envoyés/reçus par le client et qui prend en argument les infos de connexions et le pseudo"""
    try:
        while True: # Boucle principal de la fonction qui attends les commandes du client
            try: # Le try ici va attribuer à la variable msg tous ce qui est reçus dans la limite de 1024octets
                msg = conn.recv(1024).decode() 
            except ConnectionResetError or ConnectionAbortedError:
                break
            if not msg:  # client se déconnecte avec /quit ou en fermant le terminal
                break
            msg_list = msg.split(" ",2) #On fait une liste pour traiter les commandes de l'utilisateur 
            match msg_list[0] :
                #Si le client entre un /users on lui renvoie la liste des clients connectés en parcourant le dictionnaire 
                case "/users":
                    conn.send("Voici la liste des utilisateurs connectés :\n".encode())
                    for valeur in clients.items():
                        conn.send(f"{valeur[0]}\n".encode()) # À chaque fois que l'on envoie quelque chose à un client on fait .encode() pour que le socket puisse comprendre et faire la passerelle.
                case "/msg":
                    # Si le client entre un /msg on va traiter le cas all ou pseudo de manière à envoyer à tous 
                    # les clients présent sur le server ou à un client en particulier. 

                    if len(msg_list) < 3: # On informe au client de la convention attendu pour pouvoir traiter cette commande
                        conn.send("Vous devriez tapez: /msg <pseudo|all> <message>\n".encode())
                        continue
                    cible = msg_list[1]
                    contenu = msg_list[2]
                    if cible == "all":
                        # Pour le cas ou un client souhaiterait envoyer un message à tous,
                        # on parcours notre dictionnaire et on envoie le message voulu à tous ceux connecté en récupérant leur pseudo et
                        # leur socket.
                        for user, sock in clients.items():
                            if user != pseudo:
                                sock.send(f"/msg {pseudo} {contenu}\n".encode())
                    else:
                        #Ici on regarde si le destinataire existe dans notre dictionnaire et on envoie le message 
                        # sinon on informe l'expédditeur que le destinataire n'existe pas ou est introuvable
                        if cible in clients:
                            cible_socket = clients[cible]
                            cible_socket.send(f"/msg {pseudo} {contenu}\n".encode())
                        else:
                            conn.send(f"Utilisateur {cible} introuvable.\n".encode())
    finally: # Afiichage de déconnexion et suppressions du dictionnaire si le client quitte brutalement ou avec /quit et on clos les threads qui lui appartient
        print(f"{pseudo} déconnecté")
        if pseudo in clients:
            del clients[pseudo]
        conn.close()
    
while True:
    conn, addr = s.accept() # ici le serveur attend la connexion d'un client avec un connect(ip,port) et conn va être égal à un socket dédié au client et adrr un tuple contenant le port et l'ip du client
    print(f"Nouvelle connexion : {addr}")
    pseudo_valide = False
    while not pseudo_valide: # Boucle pour demander un pseudo non utilisé
        pseudo = conn.recv(1024).decode() #on définit la taille d'un paquet à 1024octets max et on attribut la réponse de l'utilisateur à son pseudo
        if pseudo not in clients : # Si le client n'existe pas pour le serveur 
            conn.send("Ok".encode()) # On envoie "Ok" en faisant .send("xxxx".encode())
            pseudo_valide = True # on met pseudo_valide à True pour sortir de la condition
            clients[pseudo] = conn # on ajoute le pseudo du client dans le dictionnaire clients{}
            print(f"{pseudo} est connecté")
            threading.Thread(target=gerer_client, args=(conn,pseudo)).start() #on démarre avec .start() 
            #le thread avec comme target la fonction qui va gérer les clients qui se connecte et on passe les arguments à donner à notre fonction target
        else : 
            conn.send("Refusé".encode()) # On refuse le la connexion et on refais un tour de boucle 