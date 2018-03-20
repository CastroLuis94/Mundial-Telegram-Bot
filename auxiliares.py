from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, relationship
from crearBase import Session, Pais, Partidos, Usuario




def restar_hora(hora1,hora2):
        formato = "%m:%d:%H:%M"
        h1 = datetime.strptime(hora1, formato)
        h2 = datetime.strptime(hora2, formato)
        resultado = h1 - h2
        return "En {0} dias, {1} horas y {2} minutos".format(resultado.days, resultado.seconds // 3600 , resultado.seconds // 60 % 60)


formato = "%Y:%m:%d:%H:%M"
comienzo_del_mundial = datetime.strptime("2018:6:14:15:00", formato)

sinonimos = {
    'argentina' : []
    ,'rusia' : ['russia','pоссия']
    ,'arabia saudita' : ['arabia', 'arabia saudi','saudita','saudi arabia','العربية السعودية']
    ,'egipto' : ['egypt','مصر']
    ,'portugal' : []
    ,'españa' : ['spain']
    ,'marruecos' : ['morocco','المغرب']
    ,'iran' : ['ri de iran', 'ri de irán','irán','ایران']
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
    ,'corea del sur' : ['republica de corea','south korea','대한민국','corea']
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

def info_equipo(pais):
    pais = pais.lower()
    pais = pais.strip()
    session = Session()
    pais = session.query(Pais).filter_by(nombre=pais).first()
    partidos_izquierda =  session.query(Partidos).filter_by(equipo1=pais.id).order_by('horario')
    partidos_derecha = session.query(Partidos).filter_by(equipo2=pais.id).order_by('horario')
    partidos = list(partidos_izquierda) + list(partidos_derecha)
    victorias = 0
    empates = 0
    derrotas = 0
    goles_favor = 0
    goles_contra = 0
    for partido in partidos:
        if partido.ya_termino:
            if pais.id == partido.equipo1:
                goles_equipo1 , goles_equipo2 = partido.resultado.split('-')
                goles_equipo1 = int(goles_equipo1)
                goles_equipo2 = int(goles_equipo2)
                if goles_equipo1 > goles_equipo2:
                    victorias += 1
                else:
                    if goles_equipo1 == goles_equipo2:
                        empates += 1
                    else:
                        derrotas += 1
                goles_favor += goles_equipo1
                goles_contra += goles_equipo2
            else:
                goles_equipo1 , goles_equipo2 = partido.resultado.split('-')
                goles_equipo1 = int(goles_equipo1)
                goles_equipo2 = int(goles_equipo2)
                if goles_equipo1 > goles_equipo2:
                    derrotas += 1
                else:
                    if goles_equipo1 == goles_equipo2:
                        empates += 1
                    else:
                        victorias += 1
                goles_favor += goles_equipo2
                goles_contra += goles_equipo1
    puntos = victorias*3 + empates
    return puntos,victorias,empates,derrotas,goles_favor,goles_contra

