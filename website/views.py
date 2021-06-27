from flask.helpers import flash
from flask.json import jsonify
from sqlalchemy.sql.functions import user
from werkzeug.wrappers import request
from website.auth import login
from flask import Blueprint, request
from flask.templating import render_template
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

#names of blueprints
views = Blueprint('views', __name__)

#for About page
@views.route('/about')
def about():
        return render_template("about.html", user=current_user)

#for homepage
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note=Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note is added', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        note = request.form.get('note')
    return render_template("profile.html", user=current_user)