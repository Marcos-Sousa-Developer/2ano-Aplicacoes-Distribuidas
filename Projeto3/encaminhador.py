import requests

class Encaminhador: 
    """Encaminhador dos pedidos para a API
    """

    def __init__(self):

        self.operacoes = {'CREATE':'POST','READ':'GET','DELETE':'DELETE','UPDATE':'PUT'} #dicionário de operacoes

    def __utilizador__(self,request,method):
        """Encaminha pedidos de parametro utilizador
        Args:
            request(list): comando feito pelo utilizador em formato de lista
            method(str): metodo in [POST,'GET',DELETE,PUT]
        Returns:
            r(requests): retorna uma resposta
        """

        r = None

        if method in ['POST','PUT']:
            nome_or_id = request[2] #nome do utilizador ou id_user
            senha = request[3] #senha do utilizador

            if method == 'POST': #CREATE
                if "UTILIZADOR" in request: #CREATE UTILIZADOR <nome> <senha>
                    r = requests.post('http://localhost:5000/utilizadores',json = (nome_or_id,senha))
                
                else: #CREATE <id_user> <id_musica> <avaliacao>
                    id_user = request[1]  
                    id_musica = request[2] 
                    avaliacao = request[3] 
                    r = requests.post('http://localhost:5000/utilizadores', json = (id_user,id_musica,avaliacao))
            
            else: #UPDATE UTILIZADOR <id_user> <password>
                r = requests.put('http://localhost:5000/utilizadores',json = (nome_or_id,senha)) 

        elif method in ["GET","DELETE"]:
            id_user = request[2] #id o utilizador 
            if method == "GET": #READ UTILIZADOR <id_user>
                r = requests.get('http://localhost:5000/utilizadores/'+ id_user) 
            
            else: #DELETE UTILIZADOR <id_user>
                r = requests.delete('http://localhost:5000/utilizadores/'+ id_user) 
        
        return r

    def __artista__(self,request,method):
        """Encaminha pedidos de parametro artista
        Args:
            request(list): comando feito pelo utilizador em formato de lista
            method(str): metodo in [POST,'GET',DELETE,PUT]
        Returns:
            r(requests): retorna uma resposta
        """
        r = None

        id = request[2] #id_spotify_artista ou id_artista

        if method == 'POST': #CREATE ARTISTA <id_spotify>
            r = requests.post('http://localhost:5000/artistas/' + id) 

        elif method  == 'GET': #READ ARTISTA <id_artista>
            r = requests.get('http://localhost:5000/artistas/' + id) 

        elif method == 'DELETE': #DELETE ARTISTA <id_artista>
            r = requests.delete('http://localhost:5000/artistas/' + id) 
        
        return r

    def __musica__(self,request,method):
        """Encaminha pedidos de parametro musica
        Args:
            request(list): comando feito pelo utilizador em formato de lista
            method(str): metodo in [POST,'GET',DELETE,PUT]
        Returns:
            r(requests): retorna uma resposta
        """
        
        id = request[2] #id_spotify_musica ou id_musica

        if method == 'POST': #CREATE MUSICA <id_spotify>
            r = requests.post('http://localhost:5000/musicas/' + id) 

        elif method  == 'GET': #READ MUSICA <id_musica>
            r = requests.get('http://localhost:5000/musicas/' + id) 

        elif method == 'DELETE': #DELETE MUSICA <id_musica> 
            r = requests.delete('http://localhost:5000/musicas/' + id) 
        
        elif method == 'PUT': #UPDATE MUSICA <id_musica> <avaliacao> <id_user>
            avaliacao = request[3]
            id_user = request[4]
            r = requests.put('http://localhost:5000/musicas', json = (id,avaliacao,id_user)) 
        
        return r
    
    def __all__(self,request,method):
        """Encaminha pedidos de parametro all
        Args:
            request(list): comando feito pelo utilizador em formato de lista
            method(str): metodo in [POST,'GET',DELETE,PUT]
        Returns:
            r(requests): retorna uma resposta
        """
        r = None
        parametro = request[2] #parametro in [UTILIZADORES, ARTISTAS, MUSICAS, MUSICAS_A, MUSICAS_U, MUSICAS]

        if method == 'GET': #READ
            
            if parametro == "UTILIZADORES": #READ ALL UTILIZADORES
                r = requests.get('http://localhost:5000/utilizadores') 

            elif parametro == "ARTISTAS": #READ ALL ARTISTAS 
                r = requests.get('http://localhost:5000/artistas') 

            elif parametro == "MUSICAS": #READ

                if len(request) == 3: #READ ALL MUSICAS
                    r = requests.get('http://localhost:5000/musicas')
                
                else: #READ ALL MUSICAS <avaliacao>
                    avaliacao = request[3]
                    r = requests.get('http://localhost:5000/musicas/all/'+avaliacao) 

            elif parametro == "MUSICAS_A": #READ ALL MUSICAS_A <id_artista>
                id_artistas = request[3]
                r = requests.get('http://localhost:5000/artistas/all/'+id_artistas) 

            elif parametro == "MUSICAS_U": #READ ALL MUSICAS_U <id_user>
                id_user = request[3]
                r = requests.get('http://localhost:5000/utilizadores/all/' + id_user) 

        else: #DELETE

            if parametro == "UTILIZADORES": #DELETE ALL UTILIZADORES
                r = requests.delete('http://localhost:5000/utilizadores') 

            elif parametro == "ARTISTAS": #DELETE ALL ARTISTA
                r = requests.delete('http://localhost:5000/artistas') 

            elif parametro == "MUSICAS": #DELETE MUSICAS

                if len(request) == 3: #DELETE ALL MUSICAS
                    r = requests.delete('http://localhost:5000/musicas') 
                
                else: #DELETE ALL MUSICAS <avaliacao>
                    avaliacao = request[3] 
                    r = requests.delete('http://localhost:5000/musicas/all/'+avaliacao) 

            elif parametro == "MUSICAS_A": #DELETE ALL MUSICAS_A <id_artista>
                id_artistas = request[3]
                r = requests.delete('http://localhost:5000/artistas/all/'+id_artistas) 

            elif parametro == "MUSICAS_U": #DELETE ALL MUSICAS_U <id_user>
                id_user = request[3]
                r = requests.delete('http://localhost:5000/utilizadores/all/'+id_user) 

        return r

    def encaminha(self,comando): 
        """Distribui cada comando para o encaminhador correspondente
        Args:
            comando(str): comando feito pelo utilizador
        Returns:
            r(requests): retorna uma resposta
        """
        
        req = comando.split() #separa o comando para lista 
        operacao = req[0] #operacao in [CREATE, READ, DELETE, UPDATE]
        parametro = req[1] #parametro in [UTILIZADOR, ARTISTA, MUSICA, ALL, <other>]
        method = self.operacoes[operacao] #method in [POST,'GET',DELETE,PUT]
            
        if parametro == "UTILIZADOR": #CREATE, READ, DELETE, UPDATE um utilizador
            return self.__utilizador__(req,method)

        elif parametro == "ARTISTA": #CREATE, READ ou DELETE um artista
            return self.__artista__(req,method)
            
        elif parametro == "MUSICA": #CREATE, READ, DELETE, UPDATE uma musica
            return self.__musica__(req,method)
        
        elif parametro == "ALL": #READ OU DELETE ALL 
             return self.__all__(req,method)
            
        else: #AVALIAR UMA MUSICA
            return self.__utilizador__(req,method)