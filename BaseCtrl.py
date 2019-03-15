from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
# from collections import defaultdict, setdefault
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

import pymysql
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Venu0p@l@localhost/TeamPlayer'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Venug0p@l@localhost:3306/TeamPlayer'
db = SQLAlchemy(app)

class Team(db.Model):
    __tablename__ = 'Team' 
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(80))
    team_image = db.Column(db.String(120))

    def __repr__(self):
        return "<Team(team_name='%s', team_id='%s)>" % (
                                self.team_name, self.team_id)


class Player(db.Model):
    """docstring for Player"""
    __tablename__ = 'Player'
    player_id = db.Column(db.Integer, primary_key=True)
    player_fname = db.Column(db.String(80))
    player_lname = db.Column(db.String(80))
    team_id = db.Column(db.Integer, db.ForeignKey('Team.team_id'))

    def __repr__(self):
        return "<Team(player_name='%s', player_id='%s, team_id='%s)>" % (
                                self.player_name, self.player_id, self.team_id)
        
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/detail', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        teams = get_team()
        if teams:
            return render_template('team-players.html', teams=teams)
        else:
            return render_template('team-players.html')
    else:
        flash('Invalid username or password. Please try again!')
        return render_template('login.html')


@app.route('/teamplayer', methods=['POST'])
def add_team_player():
    if request.form['add_team_play'] == 'Add Team':
        return render_template('addteam.html')
    else:
        teams = get_team()
        return render_template('addplayer.html', teams=teams)


@app.route('/addteam', methods=['POST', 'GET'])
def add_team():
    if request.method == 'POST':
        result = request.form
        team = Team.query.filter_by(team_name=result['team_name']).first()
        if not team:
            team1 = Team(team_name=result['team_name'])
            db.session.add(team1)
            db.session.commit()
            flash(result['team_name'] + ' is added successfully')
            teams = get_team()
            return render_template('team-players.html', teams=teams)
        else:
            flash(result['team_name'] + ' is already present')
            return render_template('addteam.html')


@app.route('/player_information', methods = ['POST', 'GET'])
def player_information():
    if request.method == 'POST':
        result = request.form
        import pdb; pdb.set_trace()
        team = Player(player_fname=result['player_first_name'], player_lname=result['player_last_name'], team_id=result['team_selected'])
        db.session.add(team)
        db.session.commit()
        return render_template('team-players.html')

def get_team():
    teams = Team.query.all()
    return teams

@app.route('/detail/<int:team_id>', methods=['POST', 'GET'])
def team_edit(team_id):
    if request.method == 'POST':
        import pdb; pdb.set_trace()
        return render_template('addteam.html')

app.secret_key = os.urandom(24)
app.run()
