import os
import imgkit
from jinja2 import Template
from crearBase import Session, Partidos, Pais
from auxiliares import info_equipo,traducir_pais
BASE_PATH = os.path.dirname(os.path.realpath(__name__))



def Tarjeta(pais):
    pais = traducir_pais(pais.id)
    pais = session.query(Pais).filter_by(nombre = pais).first()
    foto = "../home/luis/dev/Mundial-Telegram-Bot/banderas/{0}.jpg".format(pais.nombre)
    puntos,victorias,empates,derrotas,goles_favor,goles_contra = info_equipo(pais.nombre)
    partidos_jugados = int(victorias) + int(empates) + int(derrotas)
    GFxP = 0
    GCxP = 0
    if partidos_jugados != 0:
        GFxP = int(goles_favor) / partidos_jugados
        GCxP = int(goles_contra) / partidos_jugados
    data_pais = {'nombre' : pais.nombre, 'victorias' : victorias,
                    'empates' : empates, 'derrotas' : derrotas, 'goles_favor' : goles_favor,
                    'goles_contra' : goles_contra, 'foto' : foto, 'GFxP' : str(GFxP),
                    'GCxP' : str(GCxP), 'partidos_jugados' : str(partidos_jugados) }
    with open(os.path.join(BASE_PATH,'estadisticas.html'), 'r') as f:
        template = Template(f.read())
    css = os.path.join(BASE_PATH, 'estadisticas.css')
    img = imgkit.from_string(template.render(data_pais = data_pais), 'Stats{0}.jpg'.format(pais.nombre.upper()), css=css)


if __name__ == "__main__":
    session = Session()
    paises = session.query(Pais)
    for pais in paises:
        Tarjeta(pais)

