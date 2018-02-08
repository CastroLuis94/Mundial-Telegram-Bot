
from sqlalchemy import create_engine, Column, Integer, String, Index, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base




engine = create_engine('sqlite:///base.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Pais(Base):
    __tablename__ = 'paises'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    grupo = Column(String)


class Partidos(Base):
    __tablename__ = 'partidos'

    id = Column(Integer, primary_key=True)
    equipo1 = Column(String)
    equipo2 = Column(String)
    horario = Column(String)
    resultado = Column(String)
    clase_de_partido = Column(String)
    def __init__(self,equipo1,equipo2,horario,resultado,clase_de_partido):
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.horario = horario
        self.resultado = resultado
        self.clase_de_partido = clase_de_partido
    

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
        partidos.append(Partidos(equipo1,equipo2,horario,resultado,clase_de_partido))
    return partidos


partidos = levantar_partidos("partidos.csv")


session = Session()
for partido in partidos:
    session.add(partido)
session.commit()
