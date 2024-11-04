import sqlite3
from flask import Flask, render_template, abort, request, redirect, url_for  # Agregue redirect
from db import get_db_connection  # Importa la función de conexión

app = Flask(__name__)

# Rutas basicas
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

# Ruta para obtener todos los posts
@app.route('/post', methods=['GET'])
def get_all_post():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()  # Cambié fetchone() a fetchall() para obtener todos los posts
    conn.close()
    return render_template('post/posts.html', posts=posts)

# Ruta para obtener un solo post por ID
@app.route('/post/<int:post_id>', methods=['GET'])
def get_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:  # Verifica si el post existe
        abort(404)
    return render_template('post/post.html', post=post)

# Ruta para crear un nuevo post
@app.route('/post/create', methods=['GET', 'POST'])  # Agregué método GET para cargar el formulario
def create_one_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']  # Corregí 'contend' a 'content'
        
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))  # Cambié '!' a '?'
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))  # Cambié '/post' a 'get_all_post' para redirigir correctamente

    return render_template('post/create.html')

# Ruta para editar un post por ID
@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_one_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if post is None:  # Verifica si el post existe
        abort(404)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))

    return render_template('post/edit.html', post=post)

# Ruta para eliminar un post por ID
@app.route('/post/delete/<int:post_id>', methods=['POST'])  # Cambié <str:post_id> a <int:post_id> ya que id es entero
def delete_one_post(post_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))  # Agregué coma después de post_id para pasar tupla
    conn.commit()
    conn.close()

    return redirect(url_for('get_all_post'))

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')  # Agregué '0.0.0.0' para el host y cerré el paréntesis

########################################################################## END BLOQUE 2