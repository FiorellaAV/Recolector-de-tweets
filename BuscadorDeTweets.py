from logging import exception
from datetime import datetime
import json
import time
import tweepy 
import os
#busca tweets en vivo de usuario
#el usuario debe tener un minimo de 1 tweet
class TrabajoPracticoTwitter:
    def __init__(self):
        
        '''Obtengo la ruta del archivo'''
        self.direct = os.path.dirname(__file__)
        self.ruta = os.path.join(self.direct)
        self.listar_archivos()

        """Obtengo las credenciales"""
        self.obtener_credenciales()
    
    def buscar_tweets(self,query): 
        self.query=query
        self.inicio_busqueda = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        try:
            # Configuracion de acceso con las credenciales
            auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
            auth.set_access_token(self.access_token_key,self.access_token_secret)
            api = tweepy.API(auth,wait_on_rate_limit=True,)

            #algunas variables
            tweet_ID=0
            self.contador_de_tweets_totales=0
            self.dic_de_tweets={}

            #obtengo el primer id
            if tweet_ID==0:
                for ultimo_tweet in tweepy.Cursor(api.search_tweets,q=query,tweet_mode="extended",result_type="recent").items(1): #since_id(desde este id para arriba ,mas recientes)
                    tweet_ID=(ultimo_tweet._json["id"]) 
            
            #cuerpo del tp donde busca los tw y los guarda en json(autor,tweet,fecha en que se escribio)
            while True:
                for nuevo_tweet in tweepy.Cursor(api.search_tweets,q=query,tweet_mode="extended",result_type="recent",since_id=tweet_ID,count=100).items(): #since_id(desde este id para arriba ,mas recientes)
                        #actualizo el id para q el cursor busque por encima de este id
                        tweet_ID=(nuevo_tweet._json["id"])
        
                        nombre="@"+nuevo_tweet._json["user"]["screen_name"]
                        fecha=nuevo_tweet._json["created_at"]
                        tweet=nuevo_tweet._json["full_text"]
                   
                        if nombre in self.dic_de_tweets:
                            aux=self.dic_de_tweets.get(nombre)            
                            if fecha not in aux:                      
                                aux[fecha]=tweet       
                        else:        
                            self.dic_de_tweets[nombre]={fecha:tweet}
                        self.contador_de_tweets_totales+=1
                        print("Encontre "+str(self.contador_de_tweets_totales)+" tweets")
                                     
        except KeyboardInterrupt as e:
            #Colocamos un almacenar tweets para poder guardar los tweets remanentes
            self.almacenar_tweets()
            self.mostrar_info()
        except Exception as e:
            print(e)

    '''Funcion que guarda en disco el texto de cada tweet encontrado que coincida con la query'''
    # Cada vez que se ejecute el programa se creara un archivo nuevo de busqueda
    def almacenar_tweets(self):
        with open(self.ruta+"/"+time.strftime('%Y-%m-%d', time.localtime())+".j","a") as archivo:
            json.dump(self.dic_de_tweets, archivo)
            self.dic_de_tweets.clear()

    def obtener_credenciales(self):
        with open(self.ruta+"/"+"credenciales.json","r")as archivo:
            dict_leer=json.load(archivo)
            self.consumer_key=dict_leer["consumer_key"]
            self.consumer_secret=dict_leer["consumer_secret"]
            self.access_token_key=dict_leer["access_token_key"]
            self.access_token_secret=dict_leer["access_token_secret"]

    #obtengo una lista con los archivos.json del proyecto
    def listar_archivos(self):
        self.archivos=os.listdir(self.direct)
        self.archivos_json=[]
        for fichero in self.archivos:
            if os.path.isfile(os.path.join(self.ruta, fichero)) and fichero.endswith('.j'):
                self.archivos_json.append(fichero)

    #muestra la informacion de la recolecion de tweets de ese dia
    def mostrar_info(self):
        print('Fecha y hora de inicio: ' + str(self.inicio_busqueda) + '\n' + 'Cantidad de tweets recolectados: ' +
        str(self.contador_de_tweets_totales)+'\n'+'Cantidad de bytes: '+str(os.path.getsize(self.ruta+"/"+time.strftime('%Y-%m-%d', time.localtime())+".j")))
    
if __name__ == "__main__":
    #Todas las palabras separadas por espacios 
    query="COVID-19"
    date= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    r=TrabajoPracticoTwitter()
    aux=r.buscar_tweets(query)