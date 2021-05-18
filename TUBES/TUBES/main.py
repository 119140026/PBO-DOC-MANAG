import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'document'

mysql = MySQL(app)

#category
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM category")
    data = cur.fetchall()
    cur.close()

    return render_template('category.html', category=data )

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Berhasil Ditambahkan")
        no = request.form['No']
        name = request.form['Name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO category (No, Name) VALUES (%s, %s)", (no, name))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:categoryid>', methods = ['GET'])
def delete(categoryid):
    flash("Data Berhasil Dihapus")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM category WHERE Category_ID=%s", (categoryid))
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        no = request.form['No']
        categoryid = request.form['Category_ID']
        name = request.form['Name']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE category
               SET No=%s, Name=%s
               WHERE Category_ID=%s
            """, (no, name, categoryid))
        flash("Data Berhasil Di Update")
        mysql.connection.commit()
        return redirect(url_for('Index'))

#topic
@app.route('/topic')
def t():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM topic")
    data = cur.fetchall()
    cur.close()

    return render_template('topic.html', topic=data )

@app.route('/insertt', methods = ['POST'])
def insertt():

    if request.method == "POST":
        flash("Data Berhasil Ditambahkan")
        topic = request.form['Topic']
        alamat = request.form['Storage_Folder']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO topic (Topic, Storage_Folder) VALUES (%s, %s)", ( topic, alamat))
        mysql.connection.commit()
        return redirect(url_for('t'))

@app.route('/deletet/<string:topicid>', methods = ['GET'])
def deletet(topicid):
    flash("Data Berhasil Dihapus")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM topic WHERE Topic_ID=%s", (topicid))
    mysql.connection.commit()
    return redirect(url_for('t'))

@app.route('/updatet',methods=['POST','GET'])
def updatet():

    if request.method == 'POST':
        topicid = request.form['Topic_ID']
        topic = request.form['Topic']
        alamat = request.form['Storage_Folder']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE topic
               SET Topic=%s, Storage_Folder=%s
               WHERE Topic_ID=%s
            """, (topic, alamat, topicid))
        flash("Data Berhasil Di Update")
        mysql.connection.commit()
        return redirect(url_for('t'))

#document

@app.route('/document')
def d():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM document")
    data = cur.fetchall()
    cur.close()

    return render_template('document.html', document=data )

@app.route('/insertd', methods = ['POST'])
def insertd():

    if request.method == "POST":
        flash("Data Berhasil Ditambahkan")
        categoryid = request.form['Category_ID']
        topicid = request.form['Topic_ID']
        tags = request.form['Tags']
        nama = request.form['Nama_File']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO document (Category_ID, Topic_ID, Tags, Nama_File) VALUES (%s, %s, %s, %s)", (categoryid, topicid, tags, nama))
        mysql.connection.commit()
        return redirect(url_for('d'))

@app.route('/deleted/<string:documentid>', methods = ['GET'])
def deleted(documentid):
    flash("Data Berhasil Dihapus")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM document WHERE ID_Dokumen=%s", (documentid))
    mysql.connection.commit()
    return redirect(url_for('d'))

@app.route('/updated',methods=['POST','GET'])
def updated():

    if request.method == 'POST':
        documentid = request.form['ID_Dokumen']
        categoryid = request.form['Category_ID']
        topicid = request.form['Topic_ID']
        tags = request.form['Tags']
        nama = request.form['Nama_File']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE document
               SET Category_ID=%s, Topic_ID=%s, Tags=%s, Nama_File=%s
               WHERE ID_Dokumen=%s
            """, (categoryid, topicid, tags, nama, documentid))
        flash("Data Berhasil Di Update")
        mysql.connection.commit()
        return redirect(url_for('d'))

app.config["DOCUMENT_UPLOADS"] = 'Minervas/TUBES/uploads'
app.config["ALLOWED_DOCUMENT_EXTENSIONS"] = ["PDF", "XLS", "XLSX", "PPT", "PPTX", "TXT", "DOC", "DOCX"]

def allowed_document(filename):

     return '.' in filename and filename.rsplit('.', 1)[1].upper() in app.config["ALLOWED_DOCUMENT_EXTENSIONS"]

@app.route("/upload", methods=["GET", "POST"])
def upload_document():

    if request.method == "POST":

        if request.files:

            document = request.files["document"]

            if document.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_document(document.filename):
                filename = secure_filename(document.filename)

                document.save(os.path.join(app.config["DOCUMENT_UPLOADS"], filename))

                print("Document saved")
                return  'file ' + filename +' di simpan' + ' <a href="/upload">kembali</a>'
                return redirect(request.url)

            else:
                print("That file Document extension is not allowed")
                return redirect(request.url)

    return render_template("upload.html")

from flask import send_file, send_from_directory, safe_join, abort

# app.config["CLIENT_DOCUMENT"] = 'TUBES/TUBES/uploads'

@app.route('/download/<doc>')
def downloadFile (doc):
    path = doc
    return send_file(path, as_attachment=True)
 
if __name__ == "__main__":
    app.run(debug=True)
