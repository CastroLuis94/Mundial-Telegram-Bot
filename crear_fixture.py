import os
import imgkit
from datetime import datetime, timedelta
import locale
from jinja2 import Template
from crearBase import Session, Partidos, Pais
from auxiliares import traducir_pais
BASE_PATH = os.path.dirname(os.path.realpath(__name__))

locale.setlocale(locale.LC_TIME, 'es_AR.utf8')

def partidos_fixture(grupo):
    session = Session()
    paises = list(session.query(Pais).filter_by(grupo=grupo))
    partidos = []
    for pais in paises:
        partidos_de_un_equipo = session.query(Partidos).filter_by(equipo1=pais.id).all()
        partidos += partidos_de_un_equipo
    partidos = sorted(partidos,key=lambda partido:  partido.horario)
    return partidos


def crearFixture(letra):
    session = Session()
    partidos = partidos_fixture(letra)
    info_partidos = []
    for partido in partidos:
        pais1 = partido.equipo1
        pais2 = partido.equipo2
        foto1 = "../home/luis/dev/Mundial-Telegram-Bot/banderas/{0}.jpg".format(traducir_pais(pais1))
        foto2 = "../home/luis/dev/Mundial-Telegram-Bot/banderas/{0}.jpg".format(traducir_pais(pais2))
        gf,gc = partido.resultado.split("-") 
        horario = datetime.strptime(partido.horario, "%Y:%m:%d:%H:%M")
        horario = "{0} {1} de {2} a las {3}".format(
                    horario.strftime("%A").title(),
                    horario.strftime("%d"),
                    horario.strftime("%B").title(),
                    horario.strftime("%H:%M")
                    )
        if partido.ya_termino:
            horario = "Finalizó"
        data_partido = {'pais1':traducir_pais(pais1), 'pais2':traducir_pais(pais2),'foto1':foto1,
                        'foto2':foto2, 'gf':gf, 'gc':gc, 'horario':horario}
        # print(data_partido)
        info_partidos.append(data_partido)
   
    
   
   
   

    with open(os.path.join(BASE_PATH,'fixture.html'), 'r') as f:
        template = Template(f.read())
    css = os.path.join(BASE_PATH, 'fixture.css')
    img = imgkit.from_string(template.render(info_partidos=info_partidos , letra = letra), 'fixture{0}.jpg'.format(letra.upper()), css=css)


if __name__ == "__main__":
    grupos = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    for letra in grupos:
        crearFixture(letra)