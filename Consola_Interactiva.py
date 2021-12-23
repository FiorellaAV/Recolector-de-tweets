import re,os,json
from generar_indice import indice_invertido

class BuscadorDeTweets:

    def __init__(self):
        self.direct = os.path.dirname(__file__)
        self.ruta = os.path.join(self.direct)
        self.encendido=True
        self.nombre_de_archivo="2021-11-06.j"
        self.seleccionar_archivo()
        self.leer_json()
        self.buscador()
    
    def seleccionar_archivo(self):
        self.validando=True
        self.archivos=os.listdir(self.direct)
        self.lista_archivos_json=[]
        for fichero in self.archivos:
            if os.path.isfile(os.path.join(self.ruta, fichero)) and fichero.endswith('.j'):
                self.lista_archivos_json.append(fichero)
        print("------------------------------------------------------------------------\n")

        while self.validando:
            print("Bienvenidos a nuestro trabajo practico de recopilacion y manejo de tweets.")
            print("A continuacion se mostraran los archivos disponibles. Por favor escriba textualmente el archivo con el que desea trabajar:\n")
            print(str(self.lista_archivos_json)+"\n")
            archivo_seleccionado=input("Archivo seleccionado: ")
            self.validar_archivo(archivo_seleccionado)
       
    def leer_json(self):
        with open(self.ruta+"/"+self.nombre_de_archivo,"r") as archivo:
            for lista in archivo:
               self.una_lista=json.loads(lista)
                
    def buscador(self):
        while self.encendido:
            opcion_seleccionada=input("\nPor favor seleccione a continuacion la accion que desea realizar :\n"+
            "1) Realizar una busqueda por Fecha y hora\n2) Realizar una busqueda por una o mas  palabras\n"+
            "3) Para cerrar la aplicacion precione cualquier tecla\n\nOpcion seleccionada: ")

            #opciones de accion
            if opcion_seleccionada=="1":
                self.buscar_por_hora()
            elif opcion_seleccionada=="2":
                self.buscar_por_palabras()
            else: self.encendido=False

    # la hora de busqueda debe estar separada por dos puntos (:)
    #ejemplo de como introducir la hora  15:30:05 
    def buscar_por_hora(self):
        try:
            #Hora Inicio
            print("\nPor favor a continuacion ingrese la hora de inicio de busqueda")
            print("La fecha debe respetar el formato: Hora: Minutos: Segundos (Ejemplo: 23:59:59)")
            hora_inicial=input("Horario Inicio: ")
            self.validar_hora(hora_inicial)

            #Hora fin
            print("\nPor favor a continuacion ingrese la hora de inicio de busqueda")
            print("La fecha debe respetar el formato: Hora: Minutos: Segundos (Ejemplo: 23:59:59)")
            hora_fin=input("Horario Fin: ")
            self.validar_hora(hora_fin)

            #Rango horario
            self.rango_horario(hora_inicial,hora_fin)

            #Usuario
            print ("\nSi desea recopilar tweets de un usuario en especifico escribalo a continuacion ('Ejemplo: @Twitter') de lo contrario oprima cualquier tecla")
            usuario=input("Usuario: ")
            if(usuario!=""):
                self.validar_usuario(usuario)

            #Cantidad de Tweets
            print("\nIngrese el numero de tweets que desea buscar (del 1 al 999)")
            cantidad_de_tweets=input("Cantidad De Tweets: ")
            self.validar_cantidad_de_tweets(cantidad_de_tweets)
            if(usuario!=""):
                self.comenzar_busqueda(usuario,cantidad_de_tweets)
            else:
                self.comenzar_busqueda_sin_usuario(cantidad_de_tweets)
        except ValueError as e:
            print(e)

    def buscar_por_palabras(self):
        indice=indice_invertido(self.nombre_de_archivo)

        try:
            opcion=input("\nAntes de comenzar indica la cantidad de tweets que desea buscar (entre 1 y 999).\nCantidad de tweets: ")
            self.validar_cantidad_de_tweets(opcion)
            cantidad_de_tweets=int(opcion)
            print("\nA continuacion seleccione que operacion desea realizar:")
            print("1)Buscar una palabra(ejemplo COVID-19)\n2)Buscar palabras con operador AND (minimo 2 palabras)\n3)Buscar palabras con operador OR (minimo 2 palabras)\n4)Buscar palabras con el operador AND y NOT")
            print("5)Para salir toque cualquier tecla\n")
            opcion_seleccionada=input("Operacion seleccionada: ")


            #busqueda normal
            if opcion_seleccionada=="1":
                tweets=[]
                palabra=input("Ingrese la palabra que desea buscar.\nPalabra: ")
                print()
                palabra_spl=palabra.split(" ")

                if len(palabra_spl)==1:
                   personas=indice.buscar(palabra_spl)
                   for  usuario in personas: 
                        if cantidad_de_tweets!=0:
                            fecha_del_tweet=self.una_lista[usuario]
                            for tweet in fecha_del_tweet:
                                tweets.append(fecha_del_tweet[tweet])
                                cantidad_de_tweets-=1
                    #imprimo los tweets
                   print("RESULTADOS: ")
                   for a in tweets:
                        print("\n"+a)               
                else: raise ValueError("\nERROR: Esta opcion acepta unicamente 1 palabra\n----------------------------")    

            #AND
            elif opcion_seleccionada=="2":
                contador=0
                otra=True
                lista_de_imput=[]
                tweets=[]
                while otra:
                    palabra=input("\nIngrese las palabras de una en una.\nPalabra: ")
                    print("\n----------------------------")
                    lista_de_imput.append(palabra)
                    una_mas=input("Seleccione: \n1)Si quiere ingresar otra palabra\n2)Cualquier caracter para finalizar.\nOpcion seleccionada: ")
                    if una_mas!="1":
                        otra=False

                if len(lista_de_imput)>=2:
                    lista_de_conjuntos=indice.buscar(lista_de_imput)
                    while contador!= len(lista_de_imput):
                        if contador==0:  
                            resultado=lista_de_conjuntos[0]&lista_de_conjuntos[1]
                            contador=2
                        else:
                            resultado=resultado&lista_de_conjuntos[contador]
                            contador+=1
                    lista_de_resultados=list(resultado)
                    if len(lista_de_resultados)==0:
                        print("No se encontraron tweets  que cumplan con las condiciones especificadas.")
                        print("\n----------------------------------")
                    else:
                        for  usuario in lista_de_resultados: 
                            if cantidad_de_tweets!=0:
                                fecha_del_tweet=self.una_lista[usuario]
                                for tweet in fecha_del_tweet:
                                    tweets.append(fecha_del_tweet[tweet])
                                    cantidad_de_tweets-=1
                        #imprimo los tweets
                    print("RESULTADOS:")   
                    for a in tweets:
                        print("\n"+a)
                else: raise ValueError("\nERROR: Esta opcion debe recivir  mas de una palabra\n----------------------------")
            
            #OR
            elif opcion_seleccionada=="3":
                contador=0
                otra=True
                lista_de_imput=[]
                tweets=[]
                while otra:
                    palabra=input("\nIngrese las palabras de una en una.\nPalabra: ")
                    print("\n----------------------------")
                    lista_de_imput.append(palabra)
                    una_mas=input("Seleccione: \n1)Si quiere ingresar otra palabra\n2)Cualquier caracter para finalizar.\nOpcion seleccionada: ")
                    if una_mas!="1":
                        otra=False

                if len(lista_de_imput)>=2:
                    lista_de_conjuntos=indice.buscar(lista_de_imput)
                    while contador!= len(lista_de_imput):
                        if contador==0:  
                            resultado=lista_de_conjuntos[0]|lista_de_conjuntos[1]
                            contador=2
                        else:
                            resultado=resultado|lista_de_conjuntos[contador]
                            contador+=1
                    lista_de_resultados=list(resultado)
                    if len(lista_de_resultados)==0:
                        print("No se encontraron tweets  que cumplan con las condiciones especificadas.")
                        print("\n----------------------------------")
                    else:
                        for  usuario in lista_de_resultados: 
                            if cantidad_de_tweets!=0:
                                fecha_del_tweet=self.una_lista[usuario]
                                for tweet in fecha_del_tweet:
                                    tweets.append(fecha_del_tweet[tweet])
                                    cantidad_de_tweets-=1
                        #imprimo los tweets
                    print("RESULTADOS:")   
                    for a in tweets:
                        print("\n"+a)
                else: raise ValueError("\nERROR: Esta opcion debe recivir  mas de una palabra\n----------------------------")

            #AND NOT
            elif opcion_seleccionada=="4":
                contador=0
                otra=True
                lista_de_imput=[]
                tweets=[]
                nots=0
                resultado=0
                while otra:
                    palabras_AND=input("\nIngrese las palabras AND de una en una.Minimo 2.\nPalabra: ")
                    print("\n----------------------------")
                    lista_de_imput.append(palabras_AND)
                    una_mas_AND=input("Seleccione: \n1)Si quiere ingresar otra palabra\n2)Cualquier caracter para finalizar.\nOpcion seleccionada: ")
                    if una_mas_AND!="1":
                        palabras_NOT=input("\nIngrese las palabras NOT de una en una.\nPalabra: ")
                        print("\n----------------------------")
                        nots+=1
                        lista_de_imput.append(palabras_NOT)
                        una_mas_NOT=input("Seleccione: \n1)Si quiere ingresar otra palabra\n2)Cualquier caracter para finalizar.\nOpcion seleccionada: ")
                        if una_mas_NOT!="1":
                            otra=False
                       
                if len(lista_de_imput)-nots>=2:
                    lista_de_conjuntos=indice.buscar(lista_de_imput)
                    while contador!= len(lista_de_imput)-nots:
                        if contador==0:  
                            resultado=lista_de_conjuntos[0]&lista_de_conjuntos[1]
                            contador=2
                        else:
                            resultado=resultado&lista_de_conjuntos[contador]
                            contador+=1
                    
                    while contador!=len(lista_de_conjuntos):
                        resultado=resultado-lista_de_conjuntos[contador]
                        contador+=1
                    lista_de_resultados=list(resultado)
                    if len(lista_de_resultados)==0:
                        print("No se encontraron tweets  que cumplan con las condiciones especificadas.")
                        print("\n----------------------------------")
                    else:
                        for  usuario in lista_de_resultados: 
                            if cantidad_de_tweets!=0:
                                fecha_del_tweet=self.una_lista[usuario]
                                for tweet in fecha_del_tweet:
                                    tweets.append(fecha_del_tweet[tweet])
                                    cantidad_de_tweets-=1
                        #imprimo los tweets
                    print("RESULTADOS:")   
                    for a in tweets:
                        print("\n"+a)
                else: raise ValueError("\nERROR: Esta opcion debe recivir  mas de una palabra AND\n----------------------------")  
            else: mas_palabras=False
        except ValueError as e:
            print(e)

    #Busqueda por fechas
    def comenzar_busqueda(self,usuario,cantidad_de_tweets):
        cantidad_encontrada = 0
        for persona in self.una_lista:
            if persona==usuario:
                dic_aux=self.una_lista[usuario]       
            
                if(cantidad_encontrada < int(cantidad_de_tweets)):
                
                    for hora in dic_aux:
                        patron=re.compile(r'((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d)')
                        m=patron.search(hora)

                        agrupado=m.group()
                        agrupado_spl=agrupado.split(":")
                        hora_limpia=int(agrupado_spl[0]+agrupado_spl[1]+agrupado_spl[2])

                        if hora_limpia >=self.hora_in and hora_limpia<=self.hora_fn:
                            print("\n"+ usuario)
                            print(dic_aux[hora])
                            cantidad_encontrada+=1


    #Busqueda por fecha y hora, sin usuario especificado
    def comenzar_busqueda_sin_usuario(self,cantidad_de_tweets):
        cantidad_encontrada = 0
        for usuario in self.una_lista:
            dic_aux=self.una_lista[usuario]       
            
            if(cantidad_encontrada < int(cantidad_de_tweets)):
               
                for hora in dic_aux:
                    #Utilice este regex para que devuelva solo la hora de la fecha del tweet
                    patron=re.compile(r'((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d)')
                    m=patron.search(hora)

                    agrupado=m.group()
                    agrupado_spl=agrupado.split(":")
                    hora_limpia=int(agrupado_spl[0]+agrupado_spl[1]+agrupado_spl[2])

                    if hora_limpia >=self.hora_in and hora_limpia<=self.hora_fn:
                        print("\n"+ usuario)
                        print(dic_aux[hora])
                        cantidad_encontrada+=1

    def validar_hora(self,hora):
        hora_valida=re.compile(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)')
        if hora_valida.match(hora):
            print ("hora valida")
        else: raise ValueError("\nERROR: Hora o Formato de Hora invalido.\n----------------------------")

    #hora inicial no puede ser mayor a hora  final ya que cada archivo es un dia
    def rango_horario(self,horaInicial,horaFin):
        r_inicial=horaInicial.split(":")
        self.hora_in=int(r_inicial[0]+r_inicial[1]+r_inicial[2])
        r_final=horaFin.split(":")
        self.hora_fn=int(r_final[0]+r_final[1]+r_final[2])
        if self.hora_in>self.hora_fn:
            raise  ValueError("\nERROR:  Hora Inicial no puede ser mayor a Hora Final.\n----------------------------")
        else:print("\nRango horario validado")

    def validar_cantidad_de_tweets(self,cantidad_de_tweets):
        cantidad=re.compile(r'^\d\d?\d?$')
        if cantidad.match(cantidad_de_tweets) and int(cantidad_de_tweets)<=999:
            print("Numero valido")
        else:  raise  ValueError("\nERROR: Formato incorrecto / Numero no soportado.\n----------------------------")

    def validar_usuario(self,usuario):
        us=re.compile(r'^@[a-zA-Z_\d]+$')
        if us.match(usuario):
            print("Usuario Valido")
        else: raise ValueError("\nERROR: Formato  o Usuario invalido.\n----------------------------")


    def validar_archivo(self,ArchivoSeleccionado):
        try:
            #el contador esta para comprobar  si el archivo existe
            contador=1
            for documento in self.lista_archivos_json:
                if documento== ArchivoSeleccionado:
                    print("Archivo Validado")
                    self.nombre_de_archivo=ArchivoSeleccionado
                    self.validando=False

                    #le asigno 0 para que no se ejecute el elif
                    contador=0
                elif contador==len(self.lista_archivos_json):
                    raise ValueError("\nERROR: El archivo seleccionado no existe.\n-----------------------------------------")
                contador+=1
        except ValueError as e:
            print(e)
            
  
    


if __name__== "__main__":
    prueba=BuscadorDeTweets()