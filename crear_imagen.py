import os
import imgkit
from jinja2 import Template

BASE_PATH = os.path.dirname(os.path.realpath(__name__))


data = [
        {
            'nombre': 'A',
            'equipos': [
                {'nombre': 'Argentina'},
                {'nombre': 'Brasil'}
            ]
        },
        {
            'nombre': 'B',
            'equipos': [
                {'nombre': 'Ecuador'},
                {'nombre': 'Mexico'}
            ]
        }
    ]

with open(os.path.join(BASE_PATH,'grupo.html'), 'r') as f:
    template = Template(f.read())

    for grupo in data:
        css = os.path.join(BASE_PATH, 'grupo.css')
        img = imgkit.from_string(template.render(grupo=grupo), 'out_{0}.jpg'.format(grupo['nombre']), css=css)