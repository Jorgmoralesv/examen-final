from flask import Flask, render_template, abort, request, redirect, url_for, Blueprint, g
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_typves=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

def get_post_or_404(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post is None:
        abort(404, description=f"El Post con ID {post_id} no fue encontrado.")
    return post

post_bp = Blueprint('post_bp', __name__, url_prefix='/posts')

@post_bp.route('/', methods=["GET"])
def list_posts():
    db = get_db()
    posts = db.execute('SELECT * FROM posts ORDER BY id DESC;').fetchall()
    return render_template("post/post_list.html", posts=posts)

@post_bp.route('/<int:post_id>', methods=["GET"])
def view_post(post_id):
    post = get_post_or_404(post_id)
    return render_template("post/post.html", post=post)

@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == "GET":
        return render_template("post/create.html")
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            return render_template("post/create.html", error="El título es requerido.", title=title, content=content)
        
        # Estas líneas estaban mal indentadas en tu imagen.
        # Ahora están al mismo nivel que 'if not title:'
        db = get_db()
        db.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        db.commit()
        return redirect(url_for('post_bp.list_posts'))

@post_bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    post = get_post_or_404(post_id)

    if request.method == "GET":
        return render_template("post/update.html", post=post)
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            return render_template("post/update.html", post=post, error="El título es requerido.")
        
        db = get_db()
        db.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
        db.commit()
        return redirect(url_for('post_bp.list_posts'))

@post_bp.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    get_post_or_404(post_id) 
    
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()
    return redirect(url_for('post_bp.list_posts'))

@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

app.register_blueprint(post_bp)

if __name__ == '__main__':
    with app.app_context():
        init_app(app)

    app.run(debug=True)