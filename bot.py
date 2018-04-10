import locale

from telegram.ext import Updater, CommandHandler
from auxiliares import *
from funciones_admin import *
import telegram

locale.setlocale(locale.LC_TIME, 'es_AR.utf8')


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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
/partidosde X: Este comando toma un pais y devuelve TODOS los partidos que tiene programado ese equipo.  
/tabla X: Toma una letra de un grupo y te devuelve la tabla de resultados de ese grupo.  """
  )

def tabla(bot,update):
    message = update.message.text
    message = message.lower()
    message = message.replace('/tabla','')
    grupo = message.strip()
    bot.send_photo(chat_id=update.message.chat_id, photo=open('Tabla{0}.jpg'.format(grupo.upper()), 'rb'))
 

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
    proximo_partido_izquierda = session.query(Partidos).filter_by(equipo1=pais.id).order_by('horario')
    proximo_partido_derecha = session.query(Partidos).filter_by(equipo2=pais.id).order_by('horario')
    proximo_partidos = list(proximo_partido_izquierda) + list(proximo_partido_derecha)
    proximo_mas_temprano = None
    for partido in proximo_partidos:
        if partido.ya_termino is False:
            if proximo_mas_temprano is None:
                proximo_mas_temprano = partido
            if partido.horario < proximo_mas_temprano.horario:
                proximo_mas_temprano = partido
    
    if proximo_mas_temprano != None:
        if nombre == traducir_pais(proximo_mas_temprano.equipo1):
            enemigo = session.query(Pais).filter_by(id=proximo_mas_temprano.equipo2).first()
        else:
            enemigo = session.query(Pais).filter_by(id=proximo_mas_temprano.equipo1).first()
        
        horario = datetime.strptime(proximo_mas_temprano.horario, "%Y:%m:%d:%H:%M")
        update.message.reply_text(
            'El proximo partido de {0} es el {1} contra {2}'.format(
                pais.nombre,
                horario.strftime('%A %d de %B a las %H:%M'),
                enemigo.nombre
            )  
        )
    else:
        update.message.reply_text(
            'Este pais no tiene proximos partidos registrados.'
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
    partidos_agregados = 1
    for indice in range(0, len(partidos)):
        if partidos[indice].ya_termino is False:
            rival = partidos[indice].equipo1
            horario = datetime.strptime(partidos[indice].horario, "%Y:%m:%d:%H:%M")
            partido += partidos_contra(str(partidos_agregados),rival, partidos[indice])
            partidos_agregados += 1

    if partido != '':
        update.message.reply_text(
            partido 
        )
    else:
        update.message.reply_text(
            'Este pais no tiene futuros partidos registrados.' 
        )




def estadisticas(bot, update):
    message = update.message.text
    message = message.lower()
    message = message.replace('/estadisticas','')
    message = message.strip()
    session = Session()
    pais = session.query(Pais).filter_by(nombre=message).first()
    partidos_izquierda =  session.query(Partidos).filter_by(equipo1=pais.id).order_by('horario')
    partidos_derecha = session.query(Partidos).filter_by(equipo2=pais.id).order_by('horario')
    partidos = list(partidos_izquierda) + list(partidos_derecha)
    victorias = 0
    empates = 0
    derrotas = 0
    goles_favor = 0
    goles_contra = 0
    partidos_jugados = 0
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
            partidos_jugados += 1
    update.message.reply_text(
        """ victorias : {0}. empates: {1}. derrotas: {2}. \ngoles a favor: {3}. goles en contra: {4}. partidos jugados: {5}""".format(
        victorias,empates,derrotas,goles_favor,goles_contra,partidos_jugados)
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
    updater.dispatcher.add_handler(CommandHandler('estadisticas', estadisticas))
    updater.dispatcher.add_handler(CommandHandler('terminarpartido', terminar_partido))
    updater.dispatcher.add_handler(CommandHandler('menuadmin', menu_admin))
    updater.dispatcher.add_handler(CommandHandler('tabla', tabla))
    ##updater.dispatcher.add_handler(CommandHandler('listen',listener))

    updater.start_polling()
    updater.idle()