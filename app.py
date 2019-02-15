#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Coded by @the_it_dev (M.B.C.M)

from flask import Flask, render_template, redirect, request, flash, url_for
from mocks import User
from flask_sqlalchemy import SQLAlchemy
import re

regexMail = r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]{2,6}$"
regexTel = r"^[0-9]{9,}$"
regexStr = r"^[a-zA-Z]{3,}$"

app = Flask(__name__)
app.secret_key = 'RacineCRUD_FL'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    """Model représentant les users. """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), unique=False, nullable=False)
    prenom = db.Column(db.String(80), unique=False, nullable=False)
    mdp = db.Column(db.String(80), unique=False, nullable=False)
    mail = db.Column(db.String(120), unique=True, nullable=False)
    tel = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "<User {}.{}>".format(self.prenom, self.nom)

@app.route("/")
def home():
    users = User.query.all()
    return render_template('pages/index.html', users=users)

@app.route("/ajout/", methods=['GET', 'POST'])
def ajouter_user():
    if request.method == 'POST':
        user = User(nom=request.form['nom'], prenom=request.form['prenom'], tel=request.form['tel'],
                    mail=request.form['mail'])
        if request.form['mdp'] == request.form['cmdp']:
            user.mdp = request.form['mdp']
            verifier = verif(user)
            existe = exist(user)
            if verifier is True:
                if existe is False:
                    db.session.add(user)
                    db.session.commit()
                    flash(u'User ajouté avec succés !', 'ajout_s')
                    return redirect(url_for('home'))
                else:
                    flash(existe['erreur'], 'ajout_er')
                    return redirect(url_for('ajouter_user'))
            else:
                flash(verifier['erreur'], 'ajout_er')
                return redirect(url_for('ajouter_user'))
        else:
            flash(u'Les mots de passe doivent être identique', 'ajout_er')
            return redirect(url_for('ajouter_user'))
    return render_template('pages/ajouter.html')



@app.route("/modifier/<int:id>/", methods=['GET', 'POST'])
def modifier_user(id):
    user = User.query.get(id)
    if user is None:
        flash(u'Le user que vous essayez de modifier n\'existe pas !', 'modif_er')
        return redirect(url_for('home'))
    elif request.method == 'POST' and user is not None:
        user.nom = request.form['nom']
        user.prenom = request.form['prenom']
        user.tel = request.form['tel']
        user.mail = request.form['mail']
        if request.form['mdp'] == request.form['cmdp']:
            print(request.form)
            user.mdp = request.form['mdp']
            verifier = verif(user)
            print('{} - {}'.format(user.mail, user.tel))
            print('verif  = {}'.format(verifier))
            existe = exist(user)
            print('existe = {}'.format(existe))
            if verifier is True:
                if existe is False:
                    db.session.commit()
                    flash(u'User modifié avec succés !', 'modif_s')
                    return redirect(url_for('home'))
                else:
                    flash(existe['erreur'], 'modif_er')
                    return redirect(url_for('modifier_user', id=id))
            else:
                flash(verifier['erreur'], 'modif_er')
                return redirect(url_for('modifier_user', id=id))
        else:
            flash(u'Les mots de passe doivent être identique', 'modif_er')
            return redirect(url_for('modifier_user', id=id))   
    return render_template('pages/modifier.html', user=user)

@app.route("/supprimer/<int:id>/", methods=['GET'])
def supprimer_user(id):
    user = User.query.get(id)
    if user is None:
        flash(u'Le user que vous essayez de supprimer n\'existe pas !', 'sup_er')
        return redirect(url_for('home'))
    else:
        db.session.delete(user)
        db.session.commit()
        flash(u'User supprimé avec succés !', 'sup_s')
        return redirect(url_for('home'))

@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def erreur(error):
    """
    Vue gérant quelques erreurs.
    """
    return render_template('errors/error.html', code=error.code), error.code

@app.template_filter('crypt')
def crypter(msg):
    """
    Ceci est un filtre permettant de masquer ou cryptrer un message passé en argument
    en fonction de sa taille, c'est à dire son nombre de caractères. 
    """
    taille_msg = len(msg)
    msg_crypter = '*'
    for i in range(taille_msg):
        msg_crypter += '*'
    return msg_crypter

def verif(user):
    """
    Fonction utilitaire permettant de vérifier la validité du mail, du n° de tel, du nom, 
    et du prénom.
     """
    if re.match(regexStr, user.nom):
        if re.match(regexStr, user.prenom):
            if re.match(regexMail, user.mail):
                if re.match(regexTel, user.tel):
                    return True
                else:
                    return {'erreur': 'N° de telephone invalide !'}
            else:
                return {'erreur': 'Adresse mail invalide !'}
        else:
            return {'erreur': 'Le nom doit comporter plus de 3 caractères.'}
    else:
        return {'erreur': 'Le nom doit comporter plus de 3 caractères.'}

def exist(usr):
    """
    Fonction utilitaire permettant de vérifier si le mail et/ou l'adresse email n'existe
    pas dèjà. 
    """
    users = User.query.all()
    if usr in users:
        users.remove(usr)
    for user in users:
        if user.mail == usr.mail:
            print(user.mail +' '+ usr.mail)
            return {'erreur' : 'Ce mail existe déjà !'}
        if user.tel == usr.tel:
            return {'erreur' : 'Ce numero de telephone existe déjà !'}
    return False

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)