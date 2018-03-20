import os
import imgkit
from jinja2 import Template
from crearBase import Session, Partidos, Pais
from auxiliares import info_equipo
BASE_PATH = os.path.dirname(os.path.realpath(__name__))



def crearTabla(letra):
    session = Session()
    paises = session.query(Pais).filter_by(grupo=letra)
    info_paises = []
    for pais in paises:
        puntos,victorias,empates,derrotas,goles_favor,goles_contra = info_equipo(pais.nombre)
        data_pais = {'nombre':pais.nombre,'puntos': puntos, 'victorias': victorias,
                        'empates': empates, 'derrotas' : derrotas, 'goles_favor': goles_favor,
                        'goles_contra': goles_contra}
        info_paises.append(data_pais)
    info_paises = sorted(info_paises,key=lambda dict:  dict['nombre'])
    info_paises = sorted(info_paises,key=lambda dict:  dict['goles_contra'] - dict['goles_favor'] )
    info_paises = sorted(info_paises,key=lambda dict:  -dict['puntos'])

    with open(os.path.join(BASE_PATH,'grupo.html'), 'r') as f:
        template = Template(f.read())
    css = os.path.join(BASE_PATH, 'grupo.css')
    img = imgkit.from_string(template.render(info_paises=info_paises), 'Tabla{0}.jpg'.format(letra.upper()), css=css)


if __name__ == "__main__":
    grupos = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    for letra in grupos:
        crearTabla(letra)

