from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
# from collections import defaultdict, setdefault
from base64 import b64encode

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
    team_image = db.Column(db.BLOB)

    def __repr__(self):
        return "<Team(team_name='%s', team_id='%s, team_image='%s')>" % (
                                self.team_name, self.team_id, self.team_image)


class Player(db.Model):
    """docstring for Player"""
    __tablename__ = 'Player'
    player_id = db.Column(db.Integer, primary_key=True)
    player_fname = db.Column(db.String(80))
    player_lname = db.Column(db.String(80))
    player_image = db.Column(db.BLOB)
    team_id = db.Column(db.Integer, db.ForeignKey('Team.team_id'))

    def __repr__(self):
        return "<Player(player_fname='%s', player_lname='%s', player_id='%s, team_id='%s, player_image='%s')>" % (
                                self.player_fname, self.player_lname, self.player_id, self.team_id, self.player_image)
        
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
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
    if request.form['add_template'] == 'Add Team':
        return render_template('addteam.html')
    elif request.form['add_template'] == 'Add Player':
        teams = get_team()
        return render_template('addplayer.html', teams=teams)
    else:
        return getAllPlayers()

@app.route('/addteam', methods=['POST', 'GET'])
def add_team():
    if request.method == 'POST':
        result = request.form
        teamImage = request.files['teamImage'].read()
        team = Team.query.filter_by(team_name=result['team_name']).first()
        if not team:
            team1 = Team(team_name=result['team_name'], team_image=teamImage)
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
        if request.files:
            playerImage = request.files['playerImage'].read()
        else:
            playerImage = None
        player = Player(player_image=playerImage, player_fname=result['player_first_name'], 
                        player_lname=result['player_last_name'], team_id=result['team_selected'])
class Team(db.Model):
    __tablename__ = 'Team' 
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(80))
    team_image = db.Column(db.BLOB)

    def __repr__(self):
        return "<Team(team_name='%s', team_id='%s, team_image='%s')>" % (
                                self.team_name, self.team_id, self.team_image)


class Player(db.Model):
    """docstring for Player"""
    __tablename__ = 'Player'
    player_id = db.Column(db.Integer, primary_key=True)
    player_fname = db.Column(db.String(80))
    player_lname = db.Column(db.String(80))
    player_image = db.Column(db.BLOB)
    team_id = db.Column(db.Integer, db.ForeignKey('Team.team_id'))

    def __repr__(self):
        return "<Player(player_fname='%s', player_lname='%s', player_id='%s, team_id='%s, player_image='%s')>" % (
                                self.player_fname, self.player_lname, self.player_id, self.team_id, self.player_image)
        
@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('main_page.html')

@app.route('/homepage')
def homepage():
    return redirect('/player_information')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
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
    if request.form['add_template'] == 'Add Team':
        return render_template('addteam.html')
    elif request.form['add_template'] == 'Add Player':
        teams = get_team()
        return render_template('addplayer.html', teams=teams)
    else:
        return getAllPlayers()

@app.route('/addteam', methods=['POST', 'GET'])
def add_team():
    if request.method == 'POST':
        result = request.form
        teamImage = request.files['teamImage'].read()
        team = Team.query.filter_by(team_name=result['team_name']).first()
        if not team:
            team1 = Team(team_name=result['team_name'], team_image=teamImage)
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
        if request.files:
            playerImage = request.files['playerImage'].read()
        else:
            playerImage = None
        player = Player(player_image=playerImage, player_fname=result['player_first_name'], 
                        player_lname=result['player_last_name'], team_id=result['team_selected'])
        db.session.add(player)
        db.session.commit()
    teams = get_team()
    if teams:
        return render_template('team-players.html', teams=teams)
    else:
        return render_template('team-players.html')

def get_team():
    teams = Team.query.all()
    for each in teams:
        if each.team_image is not None:
            each.team_image = b64encode(each.team_image)
    return teams



@app.route('/edit_team/<int:team_id>', methods=['POST', 'GET', 'PUT'])
def team_edit(team_id):
    if request.method == 'GET':
        team = Team.query.filter_by(team_id=team_id).one()
        if team.team_image is not None:
            team.team_image =b64encode(team.team_image)
        return render_template('edit_team.html', team=team)


@app.route('/update_team', methods=['POST', 'GET'])
def updateteam():
    if request.method == 'POST':
        result = request.form
        teamImage = request.files['teamImage'].read()
        team = Team.query.filter_by(team_id=result.get('team_id')).one() 
        team.team_name = result.get('team_name')
        team.team_image = teamImage
        db.session.commit()
        teams = get_team()
        if teams:
            return render_template('team-players.html', teams=teams)

@app.route('/deleteTeam/<int:team_id>', methods=['POST', 'GET'])
def delete_team(team_id):
    if request.method == 'GET':
        Team.query.filter_by(team_id=team_id).delete()
        db.session.commit()
        teams = get_team()
        if teams:
            return render_template('team-players.html', teams=teams)
        else:
            return render_template('team-players.html')

@app.route('/display_selected_team/<int:team_id>', methods=['POST', 'GET'])
def display_selected_team(team_id):
    if request.method == 'GET':
        result_dict = {}
        teams = get_team()
        players = Player.query.join(Team, Player.team_id==team_id).\
        add_columns(Player.player_fname,Player.player_lname,Team.team_name,Player.player_id)
        result_dict['teams'] = teams
        result_dict['players']= players
        return render_template('viewplayers.html', result=result_dict)

@app.route('/deletePlayer/<int:player_id>', methods=['POST', 'GET'])
def delete_player(player_id):
    if request.method == 'GET':
        Player.query.filter_by(player_id=player_id).delete()
        db.session.commit()
        return getAllPlayers()

def getAllPlayers():
    result_dict = {}
    teams = get_team()
    players = db.session.query(Player, Team).join(Team, Player.team_id==Team.team_id)
    for each in players:
        if each.Player.player_image is not None:
            each.Player.player_image = b64encode(each.Player.player_image)
    result_dict['teams'] = teams
    result_dict['players']= players
    return render_template('viewplayers.html', result=result_dict)

@app.route('/edit_player/<int:player_id>', methods=['POST', 'GET'])
def player_edit(player_id):
    if request.method == 'GET':
        result = {}
        player = Player.query.filter_by(player_id=player_id).one()
        player.player_image = b64encode(player.player_image)
        teams = get_team()
        result['player'] = player
        result['teams'] = teams
        return render_template('edit_player_info.html', results=result)

@app.route('/update_player', methods=['POST', 'GET'])
def updateplayer():
    if request.method == 'POST':
        result = request.form
        player = Player.query.filter_by(player_id=result.get('player_id')).one()
        player.player_fname = result.get('player_fname')
        player.player_lname = result.get('player_lname')
        player.team_id = result.get('team_selected')
        if request.files:
            player.player_image = request.files['playerImage'].read()
        db.session.commit()
        return getAllPlayers()

@app.route('/threshold', methods=['GET'])
def threshold():
    team_id = request.values['team_id']
    result_dict = {}
    teams = get_team()
    players = db.session.query(Player, Team).join(Team, Player.team_id==team_id)
    for each in players:
        if each.Player.player_image is not None:
            each.Player.player_image = b64encode(each.Player.player_image)
    result_dict['teams'] = teams
    result_dict['players']= players
    return render_template('viewplayers.html', result=result_dict)


app.secret_key = os.urandom(24)
app.run()
