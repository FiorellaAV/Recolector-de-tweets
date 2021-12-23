import os
import json
from nltk.stem import SnowballStemmer #Stemmer
from nltk.corpus import stopwords #Stopwords
import string

class indice_invertido:

    def __init__(self, nombre):
        ''' Recibe una lista con los nombres de los documentos
        '''
        self.doc_de_tweets=nombre
        self.direct = os.path.dirname(__file__)
        self.ruta = os.path.join(self.direct)
        self.stop_words = frozenset(stopwords.words('spanish'))  # lista de stop words
        self._spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
        self.guardar_palabras()
        
    # CREA LOS INDICES CON CLAVE la palabra Y VALOR : los usuarios q la emplearon en sus tweets
    def guardar_palabras(self):
        ''' Asigna a cada palabra el usuario correspondiente y guarda en un diccionario'''
 
        self.indice_de_palabras={}
        lista_de_usuarios=set()
        with open(self.ruta+"/"+self.doc_de_tweets,"r")as archivo:
            informacion=json.load(archivo)

            #usuario {"@Luis" :{hora escrito: tweet}}
            #se ejecuta cantidad de usuarios veces
            for usuario in informacion:
                lista_de_usuarios=set()
                dic_aux=informacion[usuario]

                #tweet es el dia q fue escrito 
                for tweet in dic_aux:
                    texto_del_tweet=dic_aux[tweet]

                    #agarro palabra a palabra
                    #se ejecuta el alrgo del texto no mas de 140(max largo de tweet)
                    texto_splitiado=texto_del_tweet.split()
                    for  palabra in texto_splitiado:
                        if palabra not in self.stop_words:  
                            lem=self.__lematizar_palabra(palabra)
                            if lem in self.indice_de_palabras:
                                aux=self.indice_de_palabras.get(lem)                            
                                aux.add(usuario)       
                            else:        
                                lista_de_usuarios.add(usuario)
                                self.indice_de_palabras[lem]=lista_de_usuarios

    def __lematizar_palabra(self, palabra):
        ''' Usa el stemmer para lematizar o recortar la palabra, previamente elimina todos
        los signos de puntuación que pueden aparecer. El stemmer utilizado también se
        encarga de eliminar acentos y pasar todo a minúscula, sino habría que hacerlo
        a mano'''  
        palabra = palabra.strip(string.punctuation + "»" + "\x97" + "¿" + "¡")
        # "\x97" representa un guión
        palabra_lematizada = self._spanish_stemmer.stem(palabra)
        return palabra_lematizada

        #busca en el indice los usuarios q usaron esa palabra
    def buscar(self, palabra):
        if len(palabra)==1:
            palabra_lematizada=self.__lematizar_palabra(palabra[0])
            self.verificar_si_esta(palabra_lematizada)
            personas=self.indice_de_palabras[palabra_lematizada]
            return personas
        else:
            lista_de_conjuntos=[]
            for una_palabra in palabra:
                palabra_lematizada=self.__lematizar_palabra(una_palabra)
                self.verificar_si_esta(palabra_lematizada)

                #obtengo el conjunto set con los nombres de las personas y las guardo en una lista
                personas=self.indice_de_palabras[palabra_lematizada]
                lista_de_conjuntos.append(personas)
            return lista_de_conjuntos
    # verifica si la palabra esta en el indice para evitar key Error
    def verificar_si_esta(self,palabra):
        if palabra not in self.indice_de_palabras:
            raise ValueError("ATENCION: alguna de las  palabras ingresadas no fue encontrada en el indice.")    

