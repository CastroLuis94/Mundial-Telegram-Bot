from sqlalchemy import create_engine, Column, Integer, String, Index, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta



engine = create_engine('sqlite:///base.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()



class Pais(Base):
    __tablename__ = 'paises'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    grupo = Column(String)
    en_juego = Column(Boolean)
    def __init__(self, nombre, grupo):
        self.nombre = nombre
        self.grupo = grupo.strip()
        self.en_juego = True

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String)
    nombre = Column(String)
    def __init__(self, chat_id, nombre):
        self.nombre = nombre
        self.chat_id = chat_id
    




class Partidos(Base):
    __tablename__ = 'partidos'
    id = Column(Integer, primary_key=True)
    equipo1 = Column(Integer)
    equipo2 = Column(Integer)
    horario = Column(String)
    resultado = Column(String)
    clase_de_partido = Column(String)
    ya_termino = Column(Boolean)
    def __init__(self,equipo1,equipo2,horario,clase_de_partido):
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.horario = horario
        self.resultado = '0-0'
        self.clase_de_partido = clase_de_partido.strip()
        self.ya_termino = False


Base.metadata.create_all(engine)



def levantar_partidos(nombre_archivo):
    archivo = open(nombre_archivo,"r")
    contenido = archivo.readlines()
    partidos = []
    for elem in contenido:
        datos_partido = elem.split(",")
        equipo1 = datos_partido[0]
        equipo2 = datos_partido[1]
        horario = datos_partido[2]
        resultado = datos_partido[3]
        clase_de_partido = datos_partido[4]
        partidos.append(Partidos(equipo1,equipo2,horario,clase_de_partido))
    return partidos

def levantar_paises(nombre_archivo):
    archivo = open(nombre_archivo,"r")
    contenido = archivo.readlines()
    paises = []
    for elem in contenido:
        datos_pais = elem.split(",")
        nombre = datos_pais[0]
        grupo = datos_pais[1] 
        paises.append(Pais(nombre,grupo))
    return paises


"""
def agregar_partidos(partidos):
    session = Session()
    print(partidos)
    for partido in partidos:
        aAgregar = {
        'equipo1' : partido.equipo1,
        'equipo2' : partido.equipo2,
        'horario' : partido.horario
        }
        ya_esta = session.query(Partidos).filter_by(**aAgregar).first()
        if ya_esta is None:
            session.add(partido)
    session.commit()
"""

def agregar_paises(paises):
    session = Session()
    for pais in paises:
        aAgregar = {
        'nombre' : pais.nombre,
        'grupo' : pais.grupo,
        }
        ya_esta = session.query(Pais).filter_by(**aAgregar).first()
        if ya_esta is None:
            session.add(pais)
    session.commit()


def agregar_partidos(partidos):
    session = Session()
    for partido in partidos:
        equipo1 = session.query(Pais).filter_by(nombre = partido.equipo1).first().id
        equipo2 = session.query(Pais).filter_by(nombre = partido.equipo2).first().id
        aAgregar = {
        'equipo1' : equipo1,
        'equipo2' : equipo2,
        'horario' : partido.horario
        }
        ya_esta = session.query(Partidos).filter_by(**aAgregar).first()
        if ya_esta is None:
            partido_ID = Partidos(equipo1, equipo2, partido.horario, partido.clase_de_partido)
            session.add(partido_ID)
    session.commit()


if __name__ == "__main__":
    paises = levantar_paises("paises.csv")
    agregar_paises(paises)
    partidos = levantar_partidos("partidos.csv")
    agregar_partidos(partidos)
    
    agregar_partidos(partidos)

    
