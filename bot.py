from telegram.ext import Updater, CommandHandler
from datetime import datetime, timedelta
from horarios import comienzo_del_mundial
import sqlite3



import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')




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
    ,'corea del sur' : ['south korea','대한민국']
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
    print(mensaje)
    if mensaje in sinonimos.keys():
        return mensaje
    for key in sinonimos.keys():
        if mensaje in sinonimos.get(key):
            return key
    return None    






def start(bot, update):
    update.message.reply_text(
        'Hola ' + update.message.from_user.first_name + ''', este bot devuelve datos de la Copa Mundial de la FIFA Rusia 2018.
Use el comando /help para mas informacion.        
        ''')
    
def listener(bot, update):
    id = update.message.chat_id
    ##print(update.message.text)

def help(bot, update):
    update.message.reply_text(
    """Estos son los comandos disponibles para usar:
/grupos: Este comando devuelve una imagen de todos los grupos.
/grupo X: Este comando toma una letra y devuelve la imagen de ese grupo solo
/cuantoFalta: Este comando devuelve cuantos dias, horas y minutos faltan para que empiece el mundial.
    """ 
    )

def grupos(bot, update):
    bot.send_photo(chat_id=update.message.chat_id, photo=open('Grupos.png', 'rb'))

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
"""Error de tipeo, los grupos van de la A a la H.
""" 
    )   
        return
    if grupo_seleccionado in grupos_del_mundial:
        archivo = 'Grupo' + grupo_seleccionado + '.png'
        print(archivo)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(archivo, 'rb'))
       
    else:
        update.message.reply_text(
"""Esta caracter no corresponde a un grupo valido, los grupos van de la A a la H.
""" 
    )




if __name__ == "__main__":
    updater = Updater('502678844:AAHREBEvtxfckKlnfF38_dVpLXu7BsNpjy0')

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('grupos', grupos))
    updater.dispatcher.add_handler(CommandHandler('grupo', grupo))
    updater.dispatcher.add_handler(CommandHandler('cuantoFalta', cuantoFalta))
    ##updater.dispatcher.add_handler(CommandHandler('listen',listener))

    updater.start_polling()
    updater.idle()