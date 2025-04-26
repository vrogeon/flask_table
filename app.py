from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///textblocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TextBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TextBlock {self.title}>'


# Create database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    text_blocks = TextBlock.query.order_by(TextBlock.date_created.desc()).all()
    return render_template('index.html', text_blocks=text_blocks)


@app.route('/add', methods=['POST'])
def add_text_block():
    title = request.form['title']
    content = request.form['content']

    new_text_block = TextBlock(title=title, content=content)

    try:
        db.session.add(new_text_block)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your text block'


@app.route('/delete/<int:id>')
def delete(id):
    text_block_to_delete = TextBlock.query.get_or_404(id)

    try:
        db.session.delete(text_block_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that text block'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    text_block = TextBlock.query.get_or_404(id)

    if request.method == 'POST':
        text_block.title = request.form['title']
        text_block.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your text block'
    else:
        return render_template('update.html', text_block=text_block)


if __name__ == '__main__':
    app.run(debug=True)