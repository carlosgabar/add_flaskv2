from flask import Flask,send_file,Response
from flask import render_template,redirect,session,request,jsonify,url_for
from db import get_connection
import datetime
import os
from werkzeug.utils import secure_filename 
from datetime import datetime
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
from datetime import date

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import io


app=Flask(__name__,template_folder='templates', static_folder='static')
app.secret_key="curso"

idtrabajador=0
id=0

def conectar_bd():

    conect=get_connection()
    return conect

@app.route('/')
def inicio():

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='activo' ''')
    activos=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='progreso' ''')
    progreso=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='finalizado' ''')
    finalizados=cursor.fetchone()

    if not 'login' in session:
        return redirect("/login_admin")

    cursor.execute('''SELECT *
    FROM curso c
    JOIN v_curso v on c.id_curso=v.id_curso_original
                             ''')
        
    cursos=cursor.fetchall()

    print(cursos)
    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos,activos=activos[0],progreso=progreso[0],finalizados=finalizados[0])

@app.route('/login_trabajador')
def login():

    return render_template('login.html')

@app.route('/login_trabajador',methods=['POST'])
def login_trabajador():

    id=request.form['user']
    clave=request.form['password']

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute(''' SELECT id_trabajador,clave FROM trabajador WHERE id_trabajador=%s and clave=%s''',(id,clave))
   
    if cursor.fetchone() is not None:
        session["login"]=True
        session["usuario"]="Trabajador"
        session["id"]=id
        
        return redirect(url_for("menutrabajador",id=id))

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('login.html',mensaje="Acceso Denegado")

@app.route('/trabajador/<int:id>', methods=['GET', 'POST'])
def menutrabajador(id):

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT COUNT(*) FROM curso_trabajador tc 
                   JOIN trabajador t on tc.id_trabajador=t.id_trabajador
                   JOIN curso c on tc.id_curso=c.id_curso
                   WHERE tc.status='activo' and tc.id_trabajador=%s ''',(id,))
    activos=cursor.fetchone()
    
    cursor.execute('''SELECT COUNT(*) FROM curso_trabajador tc 
                   JOIN trabajador t on tc.id_trabajador=t.id_trabajador
                   JOIN curso c on tc.id_curso=c.id_curso
                   WHERE tc.status='finalizado' and tc.id_trabajador=%s ''',(id,))
    finalizados=cursor.fetchone()
    
    cursor.execute('''SELECT COUNT(*) FROM curso_trabajador tc 
                   JOIN trabajador t on tc.id_trabajador=t.id_trabajador
                   JOIN curso c on tc.id_curso=c.id_curso
                   WHERE tc.status='espera' and tc.id_trabajador=%s ''',(id,))
    espera=cursor.fetchone()

    cursor.execute('''SELECT c.nombre,v.ponente,v.descripcion FROM curso c
				   JOIN v_curso v on c.id_curso=v.id_curso_original 
                   JOIN curso_trabajador tc on v.id_vcurso=tc.id_curso
                   JOIN trabajador t on tc.id_trabajador=t.id_trabajador
                   WHERE v.status='activo' and tc.status='activo' and t.id_trabajador=%s ''',(id,))
    
    cursosactivos=cursor.fetchall()

    cursor.execute('''SELECT c.nombre,v.ponente,v.descripcion FROM curso c
				   JOIN v_curso v on c.id_curso=v.id_curso_original 
                   JOIN curso_trabajador tc on v.id_vcurso=tc.id_curso
                   JOIN trabajador t on tc.id_trabajador=t.id_trabajador
                   WHERE v.status='progreso' and tc.status='progreso' and t.id_trabajador=%s ''',(id,))
    
    cursosprogreso=cursor.fetchall()

    cursor.execute('''SELECT c.nombre,v.ponente,v.descripcion FROM curso c
				   JOIN v_curso v on c.id_curso=v.id_curso_original 
                   JOIN curso_trabajador tc on v.id_vcurso=tc.id_curso
                   JOIN trabajador t on tc.id_trabajador=t.id_trabajador
                   WHERE v.status='finalizado' and tc.status='finalizado' and t.id_trabajador=%s ''',(id,))
    
    cursosfinalizados=cursor.fetchall()

    print(cursosfinalizados)
    
    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_trabajador.html',activos=activos[0],espera=espera[0],finalizados=finalizados[0],
                           cursosactivos=cursosactivos,cursosprogreso=cursosprogreso,cursosfinalizados=cursosfinalizados,id=id)

@app.route('/inscribirse_trabajador', methods=['GET', 'POST'])
def incribirsetrabajador():

    id = session.get('id')

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT *
        FROM curso c
        JOIN v_curso v on c.id_curso=v.id_curso_original
        WHERE v.status='progreso' ''')
    
    cursos=cursor.fetchall()

    conectar.commit()
    cursor.close()
    conectar.close()


    return render_template('inscribirse_trabajador.html',id=id,cursos=cursos)


@app.route('/login_admin')
def loginadmin():

    return render_template('login_admin.html')

@app.route('/menu')
def menu():

    return render_template('menu.html')

@app.route('/menu_admin')
def menuadmin():

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='activo' ''')
    activos=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='progreso' ''')
    progreso=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='finalizado' ''')
    finalizados=cursor.fetchone()

    cursor.execute('''SELECT * FROM curso''')
    cursos=cursor.fetchall()
    print(cursos)
    conectar.commit()
    cursor.close()
    conectar.close()


    return render_template('menu_administrador.html',cursos=cursos,activos=activos[0],progreso=progreso[0],finalizados=finalizados[0])


@app.route('/login_admin',methods=['POST'])
def admin():

    usuario=request.form['user']
    clave=request.form['password']

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT id_user,password FROM administrador WHERE id_user=%s and password=%s''',(usuario,clave))

    if cursor.fetchone() is not None:
            session["login"]=True
            session["usuario"]="Administrador"
            return redirect("/")

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('login_admin.html',mensaje="Acceso Denegado")

@app.route('/cerrar_admin')
def cerrarsesion():
    
    session.clear()
    return redirect('/login_admin')


@app.route('/cerrar_trabajador')
def cerrarsesiont():
    
    session.clear()
    return redirect('/login_trabajador')

@app.route('/crear',methods=['POST'])
def crear():

    mensaje=False
    global id
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='activo' ''')
    activos=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='progreso' ''')
    progreso=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='finalizado' ''')
    finalizados=cursor.fetchone()

    nombre=request.form['nombrecurso']
    nombreponente=request.form['nombreponente']
    fechainicio=request.form['fechainicio']
    fechafin=request.form['fechafin']
    minparticipantes=request.form['minparticipantes']
    maxparticipantes=request.form['maxparticipantes']
    parrafo=request.form['descripcion']
    localidad=request.form['localidad']
    salon=request.form['salon']
    tiempo=request.form['horainicio']
    canthoras=request.form['canthoras']

    print(tiempo)

    documento   = request.files['documento']
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actuall
    filename = secure_filename(documento.filename) #Nombre original del archivoo
            
    extension           = os.path.splitext(filename)[1]
    print(extension)
    
    id=id+1
    variable='documento'+str(id)
    nuevoNombreFile     = variable+filename 
    print(nuevoNombreFile)
     
    cargar= os.path.join (basepath, 'static/archivos', nuevoNombreFile)    
    documento.save(cargar)

    hora1=datetime.strptime(tiempo,'%H:%M').time()
    fecha1=datetime.strptime(fechainicio,'%Y-%m-%d')
    fecha2=datetime.strptime(fechafin,'%Y-%m-%d')

    fechayhora=datetime.combine(fecha1,hora1)
    
    if fecha2 >= fecha1:

        cursor.execute('''INSERT INTO curso (id_curso, nombre)
                VALUES (nextval('curso_id_curso_seq'),%s)''',
                (nombre,))
        
        conectar.commit()
        
        cursor.execute('''SELECT id_curso FROM curso WHERE nombre=%s''',(nombre,))
        id_curso=cursor.fetchone()[0]
        print(id_curso)
        
        cursor.execute('''INSERT INTO v_curso (id_vcurso, ponente,fecha_inicio,fecha_fin,minimo,maximo,descripcion,localidad,salon,hora,canthoras,id_curso_original)
                VALUES (nextval('sec_vcurso'),%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)
                       RETURNING id_vcurso''',
                (nombreponente,fechayhora,fechafin,minparticipantes,maxparticipantes,parrafo,localidad,salon,tiempo,canthoras,id_curso))
        
        
        id_vcurso = cursor.fetchone()[0]
        conectar.commit()

        cursor.execute('''INSERT INTO h_curso(id_curso_original,cant_horas,id_vcurso) VALUES(%s,%s,%s)''',
                       (id_curso,canthoras,id_vcurso))

        
    else:

        mensaje=True

    cursor.execute('''SELECT *
    FROM curso c
    JOIN v_curso v on c.id_curso=v.id_curso_original
                             ''')
    cursos=cursor.fetchall()
    print(cursos)

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos,mensaje=mensaje,activos=activos[0],progreso=progreso[0],finalizados=finalizados[0])

@app.route('/editar',methods=['POST'])
def editar():

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='activo' ''')
    activos=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='progreso' ''')
    progreso=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='finalizado' ''')
    finalizados=cursor.fetchone()

    id = request.form['idformacion']
    opcion=request.form['status']
    nombre=request.form['nombrecursoo']
    nombreponente=request.form['nombreponentee']
    fechainicio=request.form['fechainicioo']
    fechafin=request.form['fechafinn']
    minparticipantes=request.form['minparticipantess']
    maxparticipantes=request.form['maxparticipantess']
    parrafo=request.form['descripcion']
    localidad=request.form['localidadd']
    salon=request.form['salonn']
    tiempo=request.form['horainicio']
    canthoras=request.form['canthoras']
    print("aqui",canthoras)

    hora1=datetime.strptime(tiempo,'%H:%M').time()
    fecha1=datetime.strptime(fechainicio,'%Y-%m-%d')
    fecha2=datetime.strptime(fechafin,'%Y-%m-%d')

    fechayhora=datetime.combine(fecha1,hora1)

    if fecha2 >= fecha1:

        cursor.execute('''UPDATE v_curso SET fecha_inicio=%s,fecha_fin=%s,minimo=%s,maximo=%s,descripcion=%s,status=%s,hora=%s,canthoras=%s,
                       ponente=%s,localidad=%s,salon=%s WHERE id_vcurso=%s''',(fechainicio,fechafin,minparticipantes,maxparticipantes,parrafo,opcion,tiempo,canthoras,
                        nombreponente,localidad,salon,id))
        
        #EDITAR UN CURSO, POR LO CUAL LAS HORAS NO SE SUMAN, SE ACTUALIZA
        #HAY QUE CREAR UN MODULO DONDE SE PERMITA CREAR UNA NUEVA VERSION DEL CURSO Y AHI SI SE AUMENTA LA CANTIDAD DE HORAS
        #cursor.execute('''SELECT cant_horas FROM h_curso WHERE id_curso=%s''',(id,))
        #horas=cursor.fetchone()
        #horast=horas[0]
        #print(horast)
       # print(canthoras)
        #totalhoras=int(canthoras)+int(horast)

        cursor.execute('''UPDATE h_curso SET cant_horas=%s WHERE id_vcurso=%s''',(canthoras,id))
            

    cursor.execute('''SELECT * FROM curso C JOIN v_curso v on c.id_curso=v.id_curso_original 
    ''')
    cursos=cursor.fetchall()
    print(cursos)
    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos,activos=activos[0],progreso=progreso[0],finalizados=finalizados[0])

@app.route('/crearversion',methods=['POST'])
def crearversion():

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='activo' ''')
    activos=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='progreso' ''')
    progreso=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='finalizado' ''')
    finalizados=cursor.fetchone()

    id = request.form['idformacion__']
    print("AQUI ID: ",id)
    opcion=request.form['status']
    nombre=request.form['nombrecursoo']
    print(nombre)
    nombreponente=request.form['nombreponentee']
    fechainicio=request.form['fechainicioo']
    fechafin=request.form['fechafinn']
    minparticipantes=request.form['minparticipantess']
    maxparticipantes=request.form['maxparticipantess']
    parrafo=request.form['descripcion']
    localidad=request.form['localidadd']
    salon=request.form['salonn']
    tiempo=request.form['horainicio']
    canthoras=request.form['canthoras']
    print("aqui",canthoras)

    hora1=datetime.strptime(tiempo,'%H:%M').time()
    fecha1=datetime.strptime(fechainicio,'%Y-%m-%d')
    fecha2=datetime.strptime(fechafin,'%Y-%m-%d')

    fechayhora=datetime.combine(fecha1,hora1)

    if fecha2 >= fecha1:


        cursor.execute('''INSERT INTO v_curso (id_vcurso, ponente,fecha_inicio,fecha_fin,minimo,maximo,descripcion,localidad,salon,hora,canthoras,id_curso_original)
                VALUES (nextval('sec_vcurso'),%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)
                       RETURNING id_vcurso''',
                (nombreponente,fechayhora,fechafin,minparticipantes,maxparticipantes,parrafo,localidad,salon,tiempo,canthoras,id))
        
        #cursor.execute('''SELECT cant_horas FROM h_curso WHERE id_curso=%s''',(id,))
        #horas=cursor.fetchone()
        #horast=horas[0]
        #print(horast)
       # print(canthoras)
        #totalhoras=int(canthoras)+int(horast)

        id_vcurso = cursor.fetchone()[0]
        print(id_vcurso)
        conectar.commit()

        cursor.execute('''INSERT INTO h_curso(id_curso_original,cant_horas,id_vcurso) VALUES(%s,%s,%s)''',
                       (id,canthoras,id_vcurso))
            

    cursor.execute('''SELECT * FROM curso C JOIN v_curso v on c.id_curso=v.id_curso_original 
    ''')
    cursos=cursor.fetchall()
    print(cursos)
    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos,activos=activos[0],progreso=progreso[0],finalizados=finalizados[0])

   
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editarid(id):
  
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='activo' ''')
    activos=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='progreso' ''')
    progreso=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='finalizado' ''')
    finalizados=cursor.fetchone()

    cursor.execute('''SELECT * FROM curso c JOIN v_curso v on c.id_curso=v.id_curso_original  WHERE v.id_curso_original=%s
 ''' ,(id,))
    detalle=cursor.fetchone()
    
    print(detalle[2])

    cursor.execute('''SELECT * FROM curso c JOIN v_curso v on c.id_curso=v.id_curso_original''')
    cursos=cursor.fetchall()

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',datos=detalle,cursos=cursos,activos=activos[0],progreso=progreso[0],finalizados=finalizados[0])

@app.route('/eliminar/<int:id>/<int:idcurso>', methods=['GET', 'POST'])
def eliminarid(id,idcurso):
    print(idcurso)
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT *
    FROM curso c
    JOIN v_curso v on c.id_curso=v.id_curso_original
                             ''')
    cursos=cursor.fetchall()

    cursor.execute('''DELETE FROM curso_trabajador WHERE id_curso=%s and id_trabajador=%s''',(idcurso,id))

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos)

@app.route('/certificado/<int:id>/<int:idcurso>', methods=['GET', 'POST'])
def certificadoid(id, idcurso):
    conectar = conectar_bd()
    cursor = conectar.cursor()

    cursor.execute('''SELECT *
    FROM curso c
    JOIN v_curso v on c.id_curso=v.id_curso_original
                             ''')
    cursos = cursor.fetchall()

    cursor.execute(''' SELECT t.nombre, t.apellido, t.id_trabajador, c.nombre, v.ponente,v.canthoras
                   FROM trabajador t
                   JOIN curso_trabajador tc ON t.id_trabajador = tc.id_trabajador
                   JOIN v_curso v ON tc.id_curso = v.id_vcurso
				   JOIN curso c ON v.id_curso_original=c.id_curso
                   WHERE tc.status='finalizado' AND v.status='finalizado' 
                   AND tc.id_curso=%s AND t.id_trabajador=%s''', (idcurso, id))

    persona = cursor.fetchall()

    # Crear un objeto BytesIO para almacenar el PDF en memoria
    packet = io.BytesIO()
    width, height = letter
    c = canvas.Canvas(packet, pagesize=(width * 2, height * 2))

    reportlab.rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

    for person in persona:
        
        nombre_completo = f"{person[0]} {person[1]}"
        mayus=nombre_completo.title()
        cedula=str(person[2])
        titulo=person[3]
        ponente=person[4].title()
        canthoras=str(person[5])
        hoy=str(date.today())
        
        titulo="Normas industriales REGLAS ISO:20031 connn validez internacional paradddd ofimaticas microsoft"
   
        partes=dividir_titulo(titulo)
        c.setFillColorRGB(139/255,119/255,40/255) # Set font colour
        c.setFont('VeraBd', 35)                   # Set font type and font size
        c.drawCentredString(360, 330, mayus)    # Set position to write text ("watermark")

        c.setFillColorRGB(0,0,0) # Set font colour
        c.setFont('VeraBd', 15)                   # Set font type and font size
        c.drawCentredString(365, 307, cedula)    # Set position to write text ("watermark")

        if len(titulo) < 30:
            c.setFillColorRGB(139/256,119/255,40/255) # Set font colour
            c.setFont('VeraBd', 30)                   # Set font type and font size
            c.drawCentredString(360, 220,titulo)    # Set position to write text ("watermark")

        elif len(partes)<=2:
            c.setFillColorRGB(139/256,119/255,40/255) # Set font colour
            c.setFont('VeraBd', 30)                   # Set font type and font size
            c.drawCentredString(360, 220,partes[0])    # Set position to write text ("watermark")
            
            c.setFillColorRGB(139/256,119/255,40/255) # Set font colour
            c.setFont('VeraBd', 30)                   # Set font type and font size
            c.drawCentredString(360, 190,partes[1])    # Set position to write text ("watermark")
      

        else:
            c.setFillColorRGB(139/256,119/255,40/255) # Set font colour
            c.setFont('VeraBd', 30)                   # Set font type and font size
            c.drawCentredString(360, 220,partes[0])    # Set position to write text ("watermark")
            
            c.setFillColorRGB(139/256,119/255,40/255) # Set font colour
            c.setFont('VeraBd', 30)                   # Set font type and font size
            c.drawCentredString(360, 190,partes[1])    # Set position to write text ("watermark")

            c.setFillColorRGB(139/256,119/255,40/255) # Set font colour
            c.setFont('VeraBd', 30)                   # Set font type and font size
            c.drawCentredString(360, 160,partes[2])    # Set position to write text ("watermark")

        c.setFillColorRGB(0,0,0) # Set font colour
        c.setFont('VeraBd', 15)                   # Set font type and font size
        c.drawCentredString(185, 17, '8')    # Set position to write text ("watermark")

        c.setFillColorRGB(0,0,0) # Set font colour
        c.setFont('VeraBd', 15)                   # Set font type and font size
        c.drawCentredString(185, 17, canthoras)    # Set position to write text ("watermark")

        c.setFillColorRGB(0,0,0) # Set font colour
        c.setFont('VeraBd', 15)                   # Set font type and font size
        c.drawCentredString(550, 80, ponente)    # Set position to write text ("watermark")

        c.setFillColorRGB(0,0,0) # Set font colour
        c.setFont('VeraBd', 10)                   # Set font type and font size
        c.drawCentredString(670, 18, hoy)    # Set position to write text ("watermark")

    c.save()

    # Obtener el PDF existente
    existing_pdf = PdfReader(open("certificado.pdf", "rb"))
    page = existing_pdf.pages[0]

    packet.seek(0)
    new_pdf = PdfReader(packet)
    page.merge_page(new_pdf.pages[0])

    # Preparar la respuesta para descargar el PDF
    output = PdfWriter()
    output.add_page(page)

    # Crear un objeto BytesIO para el PDF final
    pdf_output = io.BytesIO()
    output.write(pdf_output)
    pdf_output.seek(0)

    # Configurar la respuesta para la descarga
    return Response(pdf_output, mimetype='application/pdf', headers={
        'Content-Disposition': f'attachment; filename="{person[0].replace(" ", "_")}_certificate.pdf"'
    })


def dividir_titulo(titulo, limite_caracteres=28):
    """
    Divide un título en dos o tres partes, buscando los primeros espacios después del límite de caracteres.

    Args:
        titulo: El título completo como una cadena de texto.
        limite_caracteres: El número máximo de caracteres en la primera parte.

    Returns:
        Una lista con las partes del título.
    """

    partes = []
    inicio = 0
    while inicio < len(titulo):
        # Encontrar el siguiente espacio o el final del título
        fin = titulo.find(" ", inicio + limite_caracteres)
        if fin == -1:
            fin = len(titulo)

        # Agregar la parte al resultado
        partes.append(titulo[inicio:fin].strip())
        inicio = fin

    return partes


@app.route('/visualizar')
def visualizar():

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT * FROM curso C JOIN v_curso v on c.id_curso=v.id_curso_original WHERE v.status='finalizado' ''')
    finalizados=cursor.fetchall()

    cursor.execute('''SELECT * FROM curso C JOIN v_curso v on c.id_curso=v.id_curso_original WHERE v.status='progreso' ''')
    progreso=cursor.fetchall()

    cursor.execute('''SELECT * FROM curso C JOIN v_curso v on c.id_curso=v.id_curso_original WHERE v.status='activo' ''')
    activos=cursor.fetchall()
  
    print(activos)

    conectar.commit()
    cursor.close()
    conectar.close()

    #AQUI PARA LISTAR CURSOS POR: CURSOS ACTIVO(EL CURSO EMPEZO)
    #CURSOS EN ESPERA(CURSO SOLO EDITABLE POR ADMINISTRADOR, EN ESPERA, LA GENTE PUEDE INSCRIBIRSE)
    #CURSOS FINALIZADOS(CURSOS QUE YA TERMINO SU FECHA)

    return render_template('visualizar_admin.html',finalizados=finalizados,progreso=progreso,activos=activos)

@app.route('/visualizarpor', methods=['POST'])
def visualizarpor():

    opcion=request.form['status_']
    desde=request.form['desde_']
    hasta=request.form['hasta_']
    print(desde)
    print(hasta)
    print(opcion)
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT * FROM curso C JOIN v_curso v on c.id_curso=v.id_curso_original 
                   WHERE v.status=%s AND v.fecha_inicio>=%s AND v.fecha_fin<=%s ''',(opcion,desde,hasta))
    cursos=cursor.fetchall()
    print(cursos)
    conectar.commit()
    cursor.close()
    conectar.close()

    rows = '' 
    for curso in cursos: 
        rows += f''' <tr> 
        <td>{curso[2]}</td> 
        <td>{curso[1]}</td> 
        <td>{curso[12]}</td> 
        <td>{curso[3]}</td> 
        <td>{curso[4]}</td> 
        <td>{curso[5]}</td> 
        <td>{curso[6]}</td> 
        <td>{curso[8]}</td>
        <td>
                <form action="{url_for('visualizarcurso', id=curso[0])}" method="get" style="display:inline;">
                  <button type="submit">Visualizar</button>
                </form>
        </td>

        </tr> 

        
        '''
    
    return rows


@app.route('/curso/<int:id>', methods=['GET', 'POST'])
def visualizarcurso(id):

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT * FROM curso C JOIN v_curso v on c.id_curso=v.id_curso_original  WHERE v.id_curso_original=%s ''',(id,))
    curso=cursor.fetchall()
    print(curso)

    cursor.execute('''SELECT COUNT(tc.id_trabajador) 
                   FROM curso_trabajador tc 
                   JOIN v_curso v ON tc.id_curso = v.id_curso_original
                   WHERE v.id_curso_original=%s 
                   ''',(id,))
    inscritos=cursor.fetchone()

    cursor.execute('''SELECT t.id_trabajador, t.nombre,t.apellido 
                   FROM trabajador t
                   JOIN curso_trabajador tc on t.id_trabajador = tc.id_trabajador
                   JOIN v_curso v on tc.id_curso = v.id_curso_original
                   WHERE v.id_curso_original=%s 
                   ''',(id,))

    trabajadores=cursor.fetchall()

    cursor.execute('''SELECT status FROM v_curso WHERE id_curso_original=%s''',(id,))
    verificar=cursor.fetchone()
    print(verificar)

    certificados=False
    if verificar[0] =='finalizado':

        certificados=True
      
    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('visualizar_curso_admin.html',curso=curso,inscritos=inscritos[0],trabajadores=trabajadores,certificados=certificados)


@app.route('/agregar',methods=['POST'])
def agregar():

 
    opcion=request.form['statuss']
    print("la opcion es :" ,opcion)
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute(''' SELECT * FROM curso C JOIN v_curso v on c.id_curso=v.id_curso_original 
                   WHERE v.status=%s ''',(opcion,))
    cursos=cursor.fetchall()

    conectar.commit()
    cursor.close()
    conectar.close()

    rows = '' 
    for curso in cursos: 
        rows += f''' <tr> 
        <td>{curso[2]}</td> 
        <td>{curso[1]}</td> 
        <td>{curso[12]}</td> 
        <td>{curso[3]}</td> 
        <td>{curso[4]}</td> 
        <td>{curso[5]}</td> 
        <td>{curso[6]}</td> 
        <td>{curso[8]}</td>
        </tr> '''
    
    print(rows)
    
    return rows


@app.route('/agregartrabajador',methods=['POST'])
def agregartrabajador():

    id_trabajador=request.form['id']
    id_curso=request.form['idcurso']

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT COUNT(*) FROM trabajador WHERE id_trabajador=%s ''',(id_trabajador,))
    existe=cursor.fetchone()

    cursor.execute('''SELECT COUNT(*) FROM v_curso v WHERE v.id_vcurso=%s ''',(id_curso,))
    existecurso=cursor.fetchone()

    cursor.execute('''SELECT * FROM curso C JOIN v_curso v on c.id_curso=v.id_curso_original ''')
    cursos=cursor.fetchall()

    if existe[0]>0 and existecurso[0]>0:

        cursor.execute('''INSERT INTO curso_trabajador (id_ct,id_curso,id_trabajador) VALUES (nextval('sec_curso_trabajador'),%s,%s)''',(id_curso,id_trabajador))

        
    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos)

@app.route('/estadisticas',methods=['POST'])
def estadisticas():

    desde=request.form['desde']
    hasta=request.form['hasta']
    mostrar=request.form['stat']

    print(mostrar)

    conectar=conectar_bd()
    cursor=conectar.cursor() 

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='activo' ''')
    activos=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='progreso' ''')
    progreso=cursor.fetchone()

    cursor.execute(''' SELECT COUNT(*) FROM v_curso v WHERE v.status='finalizado' ''')
    finalizados=cursor.fetchone()


    #HORAS DE FORMACION POR GERENCIA
    if mostrar=='stat3':

        cursor.execute('''SELECT t.departamento, SUM(v.canthoras)
        FROM trabajador t
        JOIN curso_trabajador tc on t.id_trabajador=tc.id_trabajador
        JOIN v_curso v on tc.id_curso=v.id_vcurso
        WHERE tc.status='finalizado' and v.status='finalizado'
        AND v.fecha_inicio>=%s AND v.fecha_fin<=%s
        GROUP BY t.departamento''' ,(desde,hasta))
        valores=cursor.fetchall()

        titulo="Horas de Formacion por Gerencia"

    elif mostrar=='stat2':

         #HORAS DE FORMACION POR CURSOS

        cursor.execute('''SELECT c.nombre, SUM(hc.cant_horas) AS total_horas
                    FROM h_curso hc
                    JOIN curso c ON hc.id_curso_original = c.id_curso
                    JOIN (
                    SELECT id_curso_original
                    FROM v_curso
                    WHERE status = 'finalizado'
                    AND fecha_inicio >= %s
                    AND fecha_fin <= %s
                        GROUP BY id_curso_original
                    ) AS v ON c.id_curso = v.id_curso_original
                    GROUP BY c.nombre
                    ''',(desde,hasta))
        
        valores=cursor.fetchall()

        titulo="Horas de Formacion por Cursos"

    elif mostrar=='stat1':

        #PARTICIPANTES ASISTENTES POR CURSOS

        cursor.execute('''SELECT c.nombre, COUNT(tc.id_trabajador)
            FROM curso c
            JOIN v_curso v on c.id_curso=v.id_curso_original   
            JOIN curso_trabajador tc on v.id_vcurso=tc.id_curso
            JOIN trabajador t on tc.id_trabajador=t.id_trabajador
            WHERE v.status='finalizado' and tc.status='finalizado'
            AND v.fecha_inicio>=%s AND v.fecha_fin<=%s
            GROUP by c.nombre''',(desde,hasta))

        valores=cursor.fetchall()

        titulo="Participantes Asistentes por Cursos"
        

    elif mostrar=='stat4':

         #PARTICIPANTES ASISTENTES POR GERENCIA

        cursor.execute('''
    SELECT t.departamento, COUNT(tc.id_trabajador)
    FROM trabajador t
    JOIN curso_trabajador tc on t.id_trabajador=tc.id_trabajador
    JOIN v_curso v on tc.id_curso=v.id_vcurso
    AND v.fecha_inicio>=%s AND v.fecha_fin<=%s 
    GROUP by t.departamento
''',(desde,hasta))

        valores=cursor.fetchall()

        titulo="Participantes Asistentes por Cursos"


    columnas=[]
    numeros=[]
    for i,j in valores:
        columnas.append(i)
        numeros.append(j)

    print(columnas)
    print(numeros)

    conectar.commit()
    cursor.close()
    conectar.close()


    return render_template('estadisticas.html',columnas=columnas,numeros=numeros,activos=activos[0],progreso=progreso[0],finalizados=finalizados[0],titulo=titulo)


@app.route('/cal')
def cal():

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT c.nombre,v.fecha_inicio,v.fecha_fin FROM curso c
        JOIN v_curso v on c.id_curso=v.id_curso_original
        WHERE v.status='activo'
    ''')
    cursos=cursor.fetchall()

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('cal.html')

@app.route('/eventoscalendario')
def eventos():
    """
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT c.nombre,c.fecha_inicio,STRING_AGG(t.descripcion,',')
                   FROM curso c
                   INNER JOIN tarea t ON c.id_curso=t.id_curso
                   WHERE c.status='activo' 
                   GROUP BY c.nombre,c.fecha_inicio''')
    
    infocurso=cursor.fetchall()
    print(infocurso)
    lista_add_indice=[]
    i=0
    for tareas in infocurso:
        lista_add_indice.append((*tareas,i))
        i=i+1

    print(lista_add_indice)

    lista_cursos = []
    for curso in lista_add_indice:
        title, start_date, tareas_str, indice = curso
        tareas = tareas_str.split(',')
        lista_cursos.append({
        'title': title,
        'start': start_date.isoformat(),
        'extendedProps': {
            'tareas': [{'tarea': tarea} for tarea in tareas]
        }
    })
        

    conectar.commit()
    cursor.close()
    conectar.close()

    return jsonify(lista_cursos)

    """


    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT c.nombre,v.fecha_inicio FROM curso c
        JOIN v_curso v on c.id_curso=v.id_curso_original
        WHERE v.status='activo' ''')
    
    infocurso=cursor.fetchall()
    print(infocurso)

    lista_cursos = []
    for curso in infocurso:
        title, start_date = curso
        lista_cursos.append({
        'title': title,
        'start': start_date.isoformat()
    })
        
    conectar.commit()
    cursor.close()
    conectar.close()

    print(lista_cursos)

    return jsonify(lista_cursos)


if __name__=='__main__':

    app.run(debug=True)



