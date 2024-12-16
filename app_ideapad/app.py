from flask import Flask
from flask import render_template,redirect,session,request,jsonify,url_for
from db import get_connection
import datetime
import os
from werkzeug.utils import secure_filename 
from datetime import datetime

app=Flask(__name__,template_folder='templates', static_folder='static')
app.secret_key="curso"


id=0

def conectar_bd():

    conect=get_connection()
    return conect

@app.route('/')
def inicio():

    if not 'login' in session:
        return redirect("/login_admin")
    
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT * FROM curso''')
    cursos=cursor.fetchall()
    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos)

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

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_trabajador.html',activos=activos[0],espera=espera[0],finalizados=finalizados[0])

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

    cursor.execute('''SELECT * FROM curso''')
    cursos=cursor.fetchall()
    print(cursos)
    conectar.commit()
    cursor.close()
    conectar.close()


    return render_template('menu_administrador.html',cursos=cursos)


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

@app.route('/crear',methods=['POST'])
def crear():

    mensaje=False
    global id
    conectar=conectar_bd()
    cursor=conectar.cursor()

    nombre=request.form['nombrecurso']
    nombreponente=request.form['nombreponente']
    fechainicio=request.form['fechainicio']
    fechafin=request.form['fechafin']
    minparticipantes=request.form['minparticipantes']
    maxparticipantes=request.form['maxparticipantes']
    parrafo=request.form['descripcion']
    localidad=request.form['localidad']
    salon=request.form['salon']
    tiempo=request.form['tiempo']

    print(tiempo)

    documento   = request.files['documento']
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
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
    print(fechayhora)

    if fecha2 >= fecha1:

        cursor.execute('''INSERT INTO curso (id_curso, nombre, ponente,fecha_inicio,fecha_fin,minimo,maximo,descripcion,localidad,salon,hora)
                VALUES (nextval('curso_id_curso_seq'),%s, %s, %s,%s,%s,%s,%s,%s,%s,%s)''',
                (nombre,nombreponente,fechayhora,fechafin,minparticipantes,maxparticipantes,parrafo,localidad,salon,tiempo))


    else:

        mensaje=True

    cursor.execute('''SELECT * FROM curso''')
    cursos=cursor.fetchall()
    print(cursos)

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos,mensaje=mensaje)

@app.route('/editar',methods=['POST'])
def editar():

    conectar=conectar_bd()
    cursor=conectar.cursor()

    id = request.form['idformacion']
    opcion=request.form['status']
    nombre=request.form['nombrecurso']
    nombreponente=request.form['nombreponente']
    fechainicio=request.form['fechainicio']
    fechafin=request.form['fechafin']
    minparticipantes=request.form['minparticipantes']
    maxparticipantes=request.form['maxparticipantes']
    parrafo=request.form['descripcion']
    localidad=request.form['localidad']
    salon=request.form['salon']

    fecha1=datetime.strptime(fechainicio,'%Y-%m-%d')
    fecha2=datetime.strptime(fechafin,'%Y-%m-%d')

    if fecha2 >= fecha1:

        cursor.execute('''UPDATE curso SET nombre=%s,ponente=%s,fecha_inicio=%s,fecha_fin=%s
                ,minimo=%s,maximo=%s ,descripcion=%s,localidad=%s,salon=%s,status=%s WHERE id_curso=%s ''', (nombre,nombreponente,fechainicio,fechafin,minparticipantes,maxparticipantes,parrafo,
                                                                                                   localidad,salon,opcion,id))

    cursor.execute('''SELECT * FROM curso''')
    cursos=cursor.fetchall()
    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editarid(id):
  
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT * FROM  curso WHERE id_curso=%s ''' ,(id,))
    detalle=cursor.fetchone()
    
    print(detalle[2])

    cursor.execute('''SELECT * FROM curso''')
    cursos=cursor.fetchall()

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',datos=detalle,cursos=cursos)

@app.route('/eliminar/<int:id>/<int:idcurso>', methods=['GET', 'POST'])
def eliminarid(id,idcurso):
    print(idcurso)
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT * FROM curso''')
    cursos=cursor.fetchall()

    cursor.execute('''DELETE FROM curso_trabajador WHERE id_curso=%s and id_trabajador=%s''',(idcurso,id))

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos)


@app.route('/visualizar')
def visualizar():

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT * FROM curso WHERE status='finalizado' ''')
    finalizados=cursor.fetchall()

    cursor.execute('''SELECT * FROM curso WHERE status='progreso' ''')
    progreso=cursor.fetchall()

    cursor.execute('''SELECT * FROM curso WHERE status='activo' ''')
    activos=cursor.fetchall()
  
    print(activos)

    conectar.commit()
    cursor.close()
    conectar.close()

    #AQUI PARA LISTAR CURSOS POR: CURSOS ACTIVO(LA GENTE PUEDE INSCRIBIRSE)
    #CURSOS EN ESPERA(CURSO SOLO EDITABLE POR ADMINISTRADOR)
    #CURSOS FINALIZADOS(CURSOS QUE YA TERMINO SU FECHA)

    return render_template('visualizar_admin.html',finalizados=finalizados,progreso=progreso,activos=activos)

@app.route('/visualizarpor', methods=['POST'])
def visualizarpor():

    opcion=request.form['status_']
    desde=request.form['desde_']
    hasta=request.form['hasta_']
    print(opcion)
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT * FROM curso WHERE status=%s AND fecha_inicio>=%s AND fecha_inicio<=%s ''',(opcion,desde,hasta))
    cursos=cursor.fetchall()
    
    conectar.commit()
    cursor.close()
    conectar.close()

    rows = '' 
    for curso in cursos: 
        rows += f''' <tr> 
        <td>{curso[0]}</td> 
        <td>{curso[1]}</td> 
        <td>{curso[2]}</td> 
        <td>{curso[3]}</td> 
        <td>{curso[4]}</td> 
        <td>{curso[5]}</td> 
        <td>{curso[6]}</td> 
        <td>{curso[10]}</td>
        <td>
                <form action="{url_for('visualizarcurso', id=curso[0])}" method="get" style="display:inline;">
                  <button type="submit">Visualizar</button>
                </form>
        </td>
        </tr> '''
    
    return rows


@app.route('/curso/<int:id>', methods=['GET', 'POST'])
def visualizarcurso(id):

    conectar=conectar_bd()
    cursor=conectar.cursor()    

    cursor.execute('''SELECT * FROM curso WHERE id_curso=%s ''',(id,))
    curso=cursor.fetchall()

    cursor.execute('''SELECT COUNT(tc.id_trabajador) 
                   FROM curso_trabajador tc 
                   JOIN curso c ON tc.id_curso = c.id_curso
                   WHERE c.id_curso=%s 
                   ''',(id,))
    inscritos=cursor.fetchone()

    cursor.execute('''SELECT t.id_trabajador, t.nombre,t.apellido 
                   FROM trabajador t
                   JOIN curso_trabajador tc on t.id_trabajador = tc.id_trabajador
                   JOIN curso c on tc.id_curso = c.id_curso
                   WHERE c.id_curso=%s 
                   ''',(id,))
    trabajadores=cursor.fetchall()

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('visualizar_curso_admin.html',curso=curso,inscritos=inscritos[0],trabajadores=trabajadores)


@app.route('/agregar',methods=['POST'])
def agregar():

 
    opcion=request.form['statuss']
    print("la opcion es :" ,opcion)
    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute(''' SELECT * FROM curso WHERE status=%s ''',(opcion,))
    cursos=cursor.fetchall()

    conectar.commit()
    cursor.close()
    conectar.close()

    rows = '' 
    for curso in cursos: 
        rows += f''' <tr> 
        <td>{curso[0]}</td> 
        <td>{curso[1]}</td> 
        <td>{curso[2]}</td> 
        <td>{curso[3]}</td> 
        <td>{curso[4]}</td> 
        <td>{curso[5]}</td> 
        <td>{curso[6]}</td> 
        <td>{curso[10]}</td>
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

    cursor.execute('''SELECT COUNT(*) FROM curso WHERE id_curso=%s ''',(id_curso,))
    existecurso=cursor.fetchone()

    cursor.execute('''SELECT * FROM curso''')
    cursos=cursor.fetchall()

    if existe[0]>0 and existecurso[0]>0:

        cursor.execute('''INSERT INTO curso_trabajador (id_curso,id_trabajador) VALUES (%s,%s)''',(id_curso,id_trabajador))

        
    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('menu_administrador.html',cursos=cursos)

@app.route('/cal')
def cal():

    conectar=conectar_bd()
    cursor=conectar.cursor()

    cursor.execute('''SELECT nombre,fecha_inicio,fecha_fin FROM curso WHERE status='activo' ''')
    cursos=cursor.fetchall()

    conectar.commit()
    cursor.close()
    conectar.close()

    return render_template('cal.html')

@app.route('/eventoscalendario')
def eventos():

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

if __name__=='__main__':

    app.run(debug=True)

