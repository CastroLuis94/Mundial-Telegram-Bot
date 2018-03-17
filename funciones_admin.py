from crearBase import Session,Pais,Partidos


id_admin = 265964072

def admin_only(fn):
    def chequear_user(bot, update):
        if update.message.chat_id == id_admin:
            return fn(bot,update)
        else:
            update.message.reply_text(
                'No sos admin.'
            )
    return chequear_user


@admin_only
def modificar_partido(bot,update):
    message = update.message.text
    message = message.lower()
    message = message.replace('/modificarpartido ','')
    equipo1, equipo2 , resultado , clase = message.split(',')
    equipo1 = equipo1.strip()
    equipo2 = equipo2.strip()
    resultado = resultado.strip()
    clase = clase.strip()
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

    
@admin_only
def agregar_partido(bot,update):
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

@admin_only
def terminar_partido(bot,update):
    message = update.message.text
    message = message.lower()
    message = message.replace('/terminarpartido ','')
    equipo1, equipo2 , clase = message.split(',')
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
    partido_a_modificar.ya_termino = True
    session.commit()
    update.message.reply_text(
            'Se ha modificado el partido con exito'
        )
    return
        