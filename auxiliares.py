from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, relationship
from crearBase import Session, Pais, Partidos, Usuario




def restar_hora(hora1,hora2):
        formato = "%m:%d:%H:%M"
        h1 = datetime.strptime(hora1, formato)
        h2 = datetime.strptime(hora2, formato)
        resultado = h1 - h2
        return "En {0} dias, {1} horas y {2} minutos".format(resultado.days, resultado.seconds // 3600 , resultado.seconds // 60 % 60)

sinonimos = {
    'argentina' : []
    ,'rusia' : ['russia','pоссия']
    ,'arabia saudita' : ['arabia','saudita','saudi arabia','العربية السعودية']
    ,'egipto' : ['egypt','مصر']
    ,'portugal' : []
    ,'españa' : ['spain']
    ,'marruecos' : ['morocco','المغرب']
    ,'iran' : ['irán','ایران']
    ,'francia' : ['france']
    ,'australia' : []
    ,'peru' : ['perú']
    ,'dinamarca' : ['denmark','danmark']
    ,'islandia' : ['iceland']
    ,'croacia' : ['croatia','hrvatska']
    ,'nigeria' : []
    ,'brasil' : ['brazil']
    ,'suiza' : ['switzerland','suisse','svizzera','schweiz']
    ,'costa rica' : []
    ,'serbia' : ['cрбија']
    ,'alemania' : ['germany','deutschland']
    ,'mexico' : ['méxico']
    ,'suecia' : ['sweden','sverige']
    ,'corea del sur' : ['south korea','대한민국','corea']
    ,'belgica' : ['bélgica','belgium','belgique','belgien']
    ,'panama' : ['panamá']
    ,'inglaterra' : ['england']
    ,'tunez' : ['túnez','tunisia','تونس','tunisie','tunesien']
    ,'polonia' : ['poland','polska']
    ,'senegal' : ['sénégal']
    ,'colombia' : []
    ,'japon' : ['japón','japan','日本','nippon']

}

def traducir(mensaje):
    if mensaje in sinonimos.keys():
        return mensaje
    for key in sinonimos.keys():
        if mensaje in sinonimos.get(key):
            return key
    return None    

def traducir_pais(id_pais):
    session = Session()
    pais = session.query(Pais).filter_by(id=int(id_pais)).first()
    return pais.nombre

def partidos_contra(numero_partido,enemigo,partido):
    horario = datetime.strptime(partido.horario, "%Y:%m:%d:%H:%M")
    if enemigo == partido.equipo1:
        rival = partido.equipo2
    else:
        rival = partido.equipo1
    return '{0}. El partido de {1} contra {2}  es el {3}\n'.format(
         numero_partido,
         traducir_pais(enemigo),
         traducir_pais(rival),
         horario.strftime('%A %d de %B a las %H:%M')
         )