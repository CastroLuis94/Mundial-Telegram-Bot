import locale

from telegram.ext import Updater, CommandHandler
from auxiliares import *
import telegram

locale.setlocale(locale.LC_TIME, 'es_AR.utf8')


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

id_admin = 265964072



def start(bot, update):
    update.message.reply_text(
        'Hola ' + update.message.from_user.first_name + ''', este bot devuelve datos de la Copa Mundial de la FIFA Rusia 2018.\n Use el comando /help para mas informacion.        
        ''')
    
def listener(bot, update):
    id = update.message.chat_id
    ##print(update.message.text)

def help(bot, update):
    update.message.reply_text(
    """Este es un bot sin findes de lucro el cual aun esta en desarrollo, si quieren saber mas sobre este bot puede comunicarse con @Castroluis94.\n Estos son los comandos disponibles para usar:
/grupos: Este comando devuelve una imagen de todos los grupos.
/grupo X: Este comando toma una letra y devuelve la imagen de ese grupo solo
/cuantoFalta: Este comando devuelve cuantos dias, horas y minutos faltan para que empiece el mundial.
/proximoPartido X: Este comando toma un pais y te devuelve el proximo partido de ese equipo.
/partidosde X: Este comando toma un pais y devuelve TODOS los partidos que tiene programado ese equipo. """ 
    )

def grupos(bot, update):
    bot.send_photo(chat_id=update.message.chat_id, photo=open('Grupos.jpg', 'rb'))

def datos(bot,update):
    message = update.message.text
    message = message.replace('/datos ','')
    message = message.strip()
    mensaje = traducir(message)
    return

def cuantoFalta(bot,update):
    hora_actual = datetime.utcnow()
    cuanto_falta = comienzo_del_mundial - hora_actual  
    if cuanto_falta >= timedelta(minutes=1):
        update.message.reply_text(
            "El mundial empieza en {0} dias, {1} horas y {2} minutos".format(cuanto_falta.days, cuanto_falta.seconds // 3600 , cuanto_falta.seconds // 60 % 60)
        )
    else:
        update.message.reply_text(
        "El mundial ya empezó"
        )
    return


def grupo(bot, update):
    message = update.message.text
    message = message.upper()
    message = message.replace('/GRUPO ','')
    message = message.strip()
    grupos_del_mundial = [chr(x) for x in range(65,73)]
    if len(message) == 1:
        grupo_seleccionado = message[len(message)-1].upper()
    else:
        update.message.reply_text(
            """Error de tipeo, los grupos van de la A a la H.\n""" 
    )   
        return
    if grupo_seleccionado in grupos_del_mundial:
        archivo = 'Grupo' + grupo_seleccionado + '.jpg'
        bot.send_photo(chat_id=update.message.chat_id, photo=open(archivo, 'rb'))
       
    else:
        update.message.reply_text(
            """Este caracter no corresponde a un grupo valido, los grupos van de la A a la H.\n""" 
    )

def registrarse(bot, update):
    user = Usuario(update.message.from_user.first_name,update.message.from_user.id)
    session = Session()
    chat_id = {'chat_id' : user.chat_id}
    el_usuario_esta = session.query(Usuario).filter_by(**chat_id).first()
    if el_usuario_esta is None:
        session.add(user)
        session.commit()
    else:
        return

    """
    kb = [[telegram.KeyboardButton("Option 1")],
          [telegram.KeyboardButton("Option 2")]]
    kb_markup = telegram.ReplyKeyboardMarkup(kb)
    bot.send_message(chat_id=update.message.chat_id,   
                     reply_markup=kb_markup)
     """  
    return

def proximoPartido(bot,update):
    message = update.message.text
    message = message.lower()
    message = message.replace('/proximopartido ','')
    nombre = traducir(message.strip())
    if nombre is None:
        update.message.reply_text(
            'Error al escribir el nombre de un pais del mundial'
        )
        return
    session = Session()
    pais = session.query(Pais).filter_by(nombre=nombre).first()
    proximo_partido_izquierda = session.query(Partidos).filter_by(equipo1=pais.id).order_by('horario').first()
    proximo_partido_derecha = session.query(Partidos).filter_by(equipo2=pais.id).order_by('horario').first()
    proximo_partido = proximo_partido_derecha if proximo_partido_derecha.horario < proximo_partido_izquierda.horario else proximo_partido_izquierda
    if nombre == traducir_pais(proximo_partido.equipo1):
        enemigo = session.query(Pais).filter_by(id=proximo_partido.equipo2).first()
    else:
        enemigo = session.query(Pais).filter_by(id=proximo_partido.equipo1).first()
    
    horario = datetime.strptime(proximo_partido.horario, "%Y:%m:%d:%H:%M")

    update.message.reply_text(
        'El proximo partido de {0} es el {1} contra {2}'.format(
            pais.nombre,
            horario.strftime('%A %d de %B a las %H:%M'),
            enemigo.nombre
        )  
    )


def partidosde(bot,update):
    message = update.message.text
    message = message.lower()
    message = message.replace('/partidosde ','')
    nombre = traducir(message.strip())
    if nombre is None:
        update.message.reply_text(
            'Error al escribir el nombre de un pais del mundial'
        )
        return
    session = Session()
    pais = session.query(Pais).filter_by(nombre=nombre).first()
    partidos_izquierda = session.query(Partidos).filter_by(equipo1=pais.id).order_by('horario')
    partidos_derecha = session.query(Partidos).filter_by(equipo2=pais.id).order_by('horario')
    partidos = list(partidos_izquierda) + list(partidos_derecha)
    partido = ''
    for indice in range(0, len(partidos)):
        rival = partidos[indice].equipo1
        horario = datetime.strptime(partidos[indice].horario, "%Y:%m:%d:%H:%M")
        partido += partidos_contra(str(indice + 1),rival, partidos[indice])

    update.message.reply_text(
        partido 
    )

def modificar_partido(bot,update):
    if update.message.chat_id == id_admin:
        message = update.message.text
        message = message.lower()
        message = message.replace('/modificarpartido ','')
        equipo1, equipo2 , resultado , clase = message.split(',')
        session = Session()
        pais1 = session.query(Pais).filter_by(nombre=equipo1).first()
        pais2 = session.query(Pais).filter_by(nombre=equipo2).first()
        partidos_izquierda =  session.query(Partidos).filter_by(equipo1=pais1.id).order_by('horario')
        partidos_derecha = session.query(Partidos).filter_by(equipo2=pais1.id).order_by('horario')
        partidos = list(partidos_izquierda) + list(partidos_derecha)
        partido_a_modificar = None
        for partido in partidos:
            if clase == partido.clase_de_partido and (pais2.id == partido.equipo1 or pais2.id == partido.equipo2):
                partido_a_modificar = partido 
        if partido_a_modificar is None:
            update.message.reply_text(
                'El partido no existe'
            )
            return
        partido_a_modificar.resultado = resultado
        session.commit()
        update.message.reply_text(
                'Se ha modificado el partido con exito'
            )
        return
    else:
        update.message.reply_text(
            'No sos admin.'
        )

def agregar_partido(bot,update):
    if update.message.chat_id == id_admin:
        message = update.message.text
        message = message.lower()
        message = message.replace('/agregarpartido','')
        partido = message.split(',')
        equipo1, equipo2 , horario, clase = partido
        equipo1 = equipo1.strip()
        equipo2 = equipo2.strip()
        horario = horario.strip()
        clase = clase.strip()
        session = Session()
        pais1 = session.query(Pais).filter_by(nombre=equipo1).first()
        pais2 = session.query(Pais).filter_by(nombre=equipo2).first()
        if pais1 is None or pais2 is None:
            update.message.reply_text(
                'El nombre de algun pais esta mal'
            )
            return
        partidos_izquierda =  session.query(Partidos).filter_by(equipo1=pais1.id).order_by('horario')
        partidos_derecha = session.query(Partidos).filter_by(equipo2=pais1.id).order_by('horario')
        partidos = list(partidos_izquierda) + list(partidos_derecha)
        for partido in partidos:
            if partido.ya_termino == False and (pais2.id == partido.equipo1 or pais2.id == partido.equipo2):
                update.message.reply_text(
                    'El partido ya existe.'
                )
                return
        partido_a_agregar = Partidos(pais1.id,pais2.id,horario,clase)
        session.add(partido_a_agregar)
        session.commit()
        update.message.reply_text(
            'Partido agregado exitosamente'
        )
    else:
        update.message.reply_text(
            'No sos admin.'
        )


if __name__ == "__main__":
    updater = Updater('502678844:AAHREBEvtxfckKlnfF38_dVpLXu7BsNpjy0')

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('grupos', grupos))
    updater.dispatcher.add_handler(CommandHandler('grupo', grupo))
    updater.dispatcher.add_handler(CommandHandler('cuantoFalta', cuantoFalta))
    updater.dispatcher.add_handler(CommandHandler('registrarse', registrarse))
    updater.dispatcher.add_handler(CommandHandler('proximopartido', proximoPartido))
    updater.dispatcher.add_handler(CommandHandler('partidosde', partidosde))
    updater.dispatcher.add_handler(CommandHandler('modificarpartido', modificar_partido))
    updater.dispatcher.add_handler(CommandHandler('agregarpartido', agregar_partido))
    ##updater.dispatcher.add_handler(CommandHandler('listen',listener))

    updater.start_polling()
    updater.idle()