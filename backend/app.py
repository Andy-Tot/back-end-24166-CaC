from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL
from flask import render_template,request
from flask import render_template,request,redirect


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='sistema'
mysql.init_app(app)
@app.route('/')
def index():
        sql = "SELECT * FROM `sistema`.`clientes`;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        clientes=cursor.fetchall()
        print(clientes)
        conn.commit()
        return render_template('clientes/index.html', clientes=clientes)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `sistema`.`clientes` WHERE id=%s", (id))
    conn.commit()
    return redirect('/')
@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `sistema`.`clientes` WHERE id=%s", (id))
    clientes=cursor.fetchall()
    conn.commit()
    return render_template('clientes/edit.html', clientes=clientes)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    id=request.form['txtID']
    sql = "UPDATE `sistema`.`clientes` SET `nombre`=%s, `correo`=%s WHERE id=%s;"
    datos=(_nombre,_correo,id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

@app.route('/create')
def create():   
        return render_template('clientes/create.html')

@app.route('/store', methods=['POST'])
def storage():
        _nombre=request.form['txtNombre']
        _correo=request.form['txtCorreo']
        sql = "INSERT INTO `sistema`.`clientes` (`id`, `nombre`, `correo`) VALUES (NULL, %s, %s);"
        datos=(_nombre,_correo)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,datos)
        conn.commit()
        return render_template('clientes/index.html')
if __name__=='__main__':
    app.run(debug=True)