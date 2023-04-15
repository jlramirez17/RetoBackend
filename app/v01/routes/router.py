"""
    Aplicación: Reto Backend Version v01
    Módulo: Configuración de rutas de la API
    Fecha Creación: 06-04-2023
    Programador: José Luis Ramirez - JLRAMIREZ
    Descripción: Definición de la configuración de las rutas de la API-RetoBackend
"""
import requests
import json
from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from app.v01.utils.settings import Settings
from app.v01.schema  import jokes_schema, numbers_schema
from app.v01.config.db import SessionLocal, engine, Base
from app.v01.model import jokes
from sqlalchemy.orm import Session


# librerías para el reto endpoint matemático
from math import lcm as mcm


settings = Settings()

joke = APIRouter()

#se crean las tablas de la bd
Base.metadata.create_all(bind=engine)


ver = settings.version
appname = settings.appname
appcode = settings.appcode

@joke.get("/")
def root():
    return {"message":"API-RetoBackend, Aquí se construye algo grande"}


#conexion a la bd
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



#consulta lista de todos los chistes
@joke.get("/api/"+appname+"/"+ver+"/joke/", status_code=HTTP_201_CREATED)
def get_jokes(p_jk: str | None = None):
    url = ""
    #verificamos si viene el parametro para buscar en la url indicada, vacío retornar mensaje de error
    
    if(p_jk == None):
        
        return {
                "status": 404,
                "message" : "Parámetro no válido, para buscar un chiste debe especificar uno de estos valores: Chuck ó Dad"
            }
    elif(p_jk == "Chuck"):  
        try:              
            url = 'https://api.chucknorris.io/jokes/random'
            #validar tiempo de respuesta, conexión
            res = requests.get(url, timeout=600)
            #si la respuesta es satisfactoria = 200                        
            if(res.status_code==200):
                data = json.loads(res.text)                
                return data['value']
            else:
                if(requests.exceptions.ConnectionError): 
                    return {"message":"Por favor revise su conexión a internet y vuelva a intentarlo"}                    
                elif(requests.exceptions.Timeout):
                    return {"message":"Tiempo de espera agotado, vuelva a intente más tarde "}
                else:
                    return {"message":"ha ocurrido un error "+str(res.status_code)+"en la llamada: "}
        except Exception as ex:             
            if(requests.exceptions.ConnectionError): 
                    return {"message":"Por favor revise su conexión a internet y vuelva a intentarlo"}                    
            elif(requests.exceptions.Timeout):
                return {"message":"Tiempo de espera agotado, vuelva a intente más tarde "}
            else:
                return {"message":"ha ocurrido un error en la llamada: "+str(ex)}
            
    elif(p_jk == "Dad"):  
        try:              
            url = 'https://icanhazdadjoke.com'
            cabeceras = {'cache-control': 'no-cache', 'Accept': 'application/json'}

            #validar tiempo de respuesta, conexión
            res = requests.get(url, headers=cabeceras, timeout=600)
            
            #si la respuesta es satisfactoria = 200                        
            if(res.status_code==200):
                data = json.loads(res.text)                
                return data['joke']
            else:
                if(requests.exceptions.ConnectionError): 
                    return {"message":"Por favor revise su conexión a internet y vuelva a intentarlo"}                    
                elif(requests.exceptions.Timeout):
                    return {"message":"Tiempo de espera agotado, vuelva a intente más tarde "}
                else:
                    return {"message":"ha ocurrido un error "+str(res.status_code)+"en la llamada: "}
            
        except Exception as ex:        
            if(requests.exceptions.ConnectionError): 
                    return {"message":"Por favor revise su conexión a internet y vuelva a intentarlo"}                    
            elif(requests.exceptions.Timeout):
                return {"message":"Tiempo de espera agotado, vuelva a intente más tarde "}
            else:
                return {"message":"ha ocurrido un error en la llamada: "+str(ex)}
    else:   
        return {
                "status": 404,
                "message" : "Parámetro no válido, para buscar un chiste debe especificar uno de estos valores: Chuck ó Dad"
            }

#sumar un 1 al número pasado por parámetro 
@joke.get("/api/"+appname+"/"+ver+"/suma/{number}", status_code=HTTP_201_CREATED)
def get_jokes(number: int):
    try:
        if(number):            
            return {
                "status": 200,                
                "message" : f"La suma de {number} + 1 = {(number+1)}"
            }
    except Exception as ex:        
        return {'message': str(ex)}


#obtener mcm de una lista de números 

@joke.post("/api/"+appname+"/"+ver+"/mcm/", status_code=HTTP_201_CREATED)
def get_mcm(entrada: numbers_schema.NumbersSchema):
    try:                
        if(entrada.numbers):   
            mcm = get_mcm(entrada.numbers) #llamada a la función que calcula el mcm
            if mcm > 0:      
                return {
                    "status": 200,                
                    "message" : f"El Mínimo Común M+ultiplo de la lista {entrada.numbers} {mcm}"
                }
            else:
                return {
                    "status": 400,                
                    "message" : f"Envíe una lista de valores válidos, número mayores a cero {entrada.numbers} {mcm}"
                }
    except Exception as ex:        
        return {'message': str(ex)}
    

#crear chiste 
@joke.post("/api/"+appname+"/"+ver+"/joke/",status_code=HTTP_201_CREATED)
def create_joke(entrada:jokes_schema.Jokes, db:Session=Depends(get_db)):
    joke=jokes.Jokes(id=entrada.id,value=entrada.value)
    db.add(joke)
    db.commit()
    db.refresh(joke)
    return {                
                "status": 200,
                "message" : "El chiste fue creado satisfactoriamente",
                "chiste_agregado": joke
           }   


#modificar chiste 
@joke.put("/api/"+appname+"/"+ver+"/joke/",status_code=HTTP_201_CREATED)
def update_joke(entrada:jokes_schema.JokeUpdate, db:Session=Depends(get_db)):
    joke=jokes.Jokes(id=entrada.id,value=entrada.value)
    joke=db.query(jokes.Jokes).filter_by(id=entrada.id).first()
    joke.value=entrada.value    
    db.commit()
    db.refresh(joke)    
    return {                
                "status": 200,
                "message" : "El chiste fue modificado satisfactoriamente",
                "chiste_modificado": joke
           }      

#eliminar chiste 
@joke.delete("/api/"+appname+"/"+ver+"/joke/",status_code=HTTP_201_CREATED)
def update_joke(entrada:jokes_schema.JokeDelete, db:Session=Depends(get_db)):
    
    joke=db.query(jokes.Jokes).filter_by(id=entrada.id).first()    
    db.delete(joke)
    db.commit()    
    return {                
                "status": 200,
                "message" : "El chiste fue eliminado satisfactoriamente",
                "chiste_eliminado": entrada.id
           }      


def get_mcm(numbers):
    if numbers:
        for num in numbers:
            resultado = mcm(*numbers) # pasamos cada item de la lista como argumento.
            print(str(numbers).replace('[', '').replace(']', ''))
            return resultado
    else:
        return 0



