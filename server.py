from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import itertools
from sqlalchemy import or_


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///footapp.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
app.config['UPLOADED_DOCUMENTS_DEST'] = 'documents' 
db = SQLAlchemy(app)

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Tournaments(db.Model):
    tournament_id = db.Column(db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(100), nullable=False)
    implementation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class UserTournaments(db.Model):
    participation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.tournament_id'), nullable=False)

class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    year_of_foundation = db.Column(db.Integer, nullable=False)
    coach = db.Column(db.String(100), nullable=False)
    games = db.Column(db.Integer, default=0, nullable=False)
    victories = db.Column(db.Integer, default=0, nullable=False)
    nobodys = db.Column(db.Integer, default=0, nullable=False)
    defeats = db.Column(db.Integer, default=0, nullable=False)
    goals_scored = db.Column(db.Integer, default=0, nullable=False)
    missed_balls = db.Column(db.Integer, default=0, nullable=False)
    goal_difference = db.Column(db.Integer, default=0, nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.tournament_id'), nullable=False)

class Players(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    height = db.Column(db.Numeric(precision=5, scale=2), default=0, nullable=False)  # Зміна типу на числодроби
    weight = db.Column(db.Numeric(precision=5, scale=2), default=0, nullable=False)  # Зміна типу на числодроби
    game_number = db.Column(db.Integer, default=0, nullable=False)

class Matches(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    match_date = db.Column(db.Date, nullable=False)
    match_time = db.Column(db.Time, nullable=False)
    stadium = db.Column(db.String(100), nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    home_team_goals = db.Column(db.Integer, default=0, nullable=False)
    away_team_goals = db.Column(db.Integer, default=0, nullable=False)

class Goals(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.match_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    time_of_goal = db.Column(db.Integer, default=0, nullable=False)

class Assistants(db.Model):
    assistant_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.match_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    time_of_assist = db.Column(db.Integer, default=0, nullable=False)
  
class Calendar(db.Model):
    calendar_id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)

# Створення таблиць бази даних
# with app.app_context():
#     db.create_all()
    
# Очищення бази даних
# with app.app_context():
#     db.session.query(Users).delete()  # Видалення всіх записів з таблиці користувачів
#     db.session.query(Tournaments).delete()  # Видалення всіх записів з таблиці турнірів 
#     db.session.query(UserTournaments).delete()  # Видалення всіх записів з таблиці користувачів-турнірів 
#     db.session.query(Teams).delete()  # Видалення всіх записів з таблиці команд 
#     db.session.query(Players).delete()  # Видалення всіх записів з таблиці команд 
#     db.session.query(Matches).delete()  # Видалення всіх записів з таблиці гравців 
#     db.session.query(Goals).delete()  # Видалення всіх записів з таблиці гравців 
#     db.session.query(Assistants).delete()  # Видалення всіх записів з таблиці гравців 
#     db.session.query(Calendar).delete()  # Видалення всіх записів з таблиці гравців 
#     db.session.commit()  # Збереження змін


# with app.app_context():
#     db.session.query(Teams).update({
#         Teams.games: 0,
#         Teams.victories: 0,
#         Teams.nobodys: 0,
#         Teams.defeats: 0,
#         Teams.goals_scored: 0,
#         Teams.missed_balls: 0,
#         Teams.goal_difference: 0,
#         Teams.points: 0
#     })

#     # Зберегти зміни у базі даних
#     db.session.commit()


@app.route('/signupform', methods=['POST'])
def signupform():
    data = request.get_json() 
    existing_user = Users.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Користувач з такою поштою вже існує'})
    else:
        password = data['password']
        hashed_password = generate_password_hash(password)
        new_user = Users(first_name=data['firstName'], last_name=data['lastName'], email=data['email'], password=hashed_password)
        db.session.add(new_user)  
        db.session.commit()  
        return jsonify({'message': 'Користувач успішно доданий до бази даних'})

@app.route('/loginform', methods=['POST'])
def loginform():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = Users.query.filter_by(email=email).first()  # Пошук користувача за email у базі даних
    if user is None:
        return jsonify({'error': 'Користувача з таким email не знайдено'})
    elif not check_password_hash(user.password, password):  # Перевірка пароля захешованого користувача
        return jsonify({'error': 'Неправильний пароль'})
    else:
        return jsonify({'firstName': user.first_name, 'lastName': user.last_name, 'email': user.email})

@app.route('/user-tournaments', methods=['POST'])
def user_tournaments():
    data = request.get_json()
    user_email = data['email']
    user = Users.query.filter_by(email=user_email).first()  # Знаходимо користувача за email у базі даних
    if user is None:
        return jsonify({'error': 'Користувача з таким email не знайдено'})
    else:
        user_tournaments = UserTournaments.query.filter_by(user_id=user.user_id).join(Tournaments).add_columns(Tournaments.tournament_id, Tournaments.tournament_name, Tournaments.implementation_date).all()
        tournaments_data = [{'id':row.tournament_id, 'tournamentName': row.tournament_name, 'implementationDate': row.implementation_date.strftime("%Y-%m-%d %H:%M:%S")} for row in user_tournaments]
        return jsonify({'userTournaments': tournaments_data})

@app.route('/add-tournament', methods=['POST'])
def add_tournament():
    data = request.get_json()
    user_email = data['email']
    tournament_name = data['tournament_name']
    user = Users.query.filter_by(email=user_email).first()  # Знаходимо користувача за email у базі даних
    if user is None:
        return jsonify({'error': 'Користувача з таким email не знайдено'})
    else:
        new_tournament = Tournaments(tournament_name=tournament_name)
        db.session.add(new_tournament)
        db.session.commit()
        user_tournament_relation = UserTournaments(user_id=user.user_id, tournament_id=new_tournament.tournament_id)
        db.session.add(user_tournament_relation)
        db.session.commit()
        return jsonify({'message': 'Новий турнір успішно доданий для користувача'})

@app.route('/tournamentsDelete/<int:tournament_id>', methods=['DELETE'])
def delete_tournament(tournament_id):
    tournament_to_delete = Tournaments.query.get(tournament_id)
    if tournament_to_delete:
        try:
            # Delete teams related to the tournament
            teams_to_delete = Teams.query.filter_by(tournament_id=tournament_id).all()
            for team in teams_to_delete:
                # Delete players related to the team
                players_to_delete = Players.query.filter_by(team_id=team.team_id).all()
                for player in players_to_delete:
                    db.session.delete(player)
                db.session.delete(team)

            # Delete matches related to the tournament
            matches_to_delete = Matches.query.filter((Matches.home_team_id.in_([team.team_id for team in teams_to_delete])) | (Matches.away_team_id.in_([team.team_id for team in teams_to_delete]))).all()
            for match in matches_to_delete:
                # Delete goals related to the match
                goals_to_delete = Goals.query.filter_by(match_id=match.match_id).all()
                for goal in goals_to_delete:
                    db.session.delete(goal)

                # Delete assistants related to the match
                assistants_to_delete = Assistants.query.filter_by(match_id=match.match_id).all()
                for assistant in assistants_to_delete:
                    db.session.delete(assistant)

                db.session.delete(match)
            
            # Delete records from the Calendar table related to the tournament
            calendar_records_to_delete = Calendar.query.filter(
                (Calendar.home_team_id.in_([team.team_id for team in teams_to_delete])) |
                (Calendar.away_team_id.in_([team.team_id for team in teams_to_delete]))
            ).all()
            for calendar_record in calendar_records_to_delete:
                db.session.delete(calendar_record)

            # Delete user-tournament relations
            user_tournaments_to_delete = UserTournaments.query.filter_by(tournament_id=tournament_id).all()
            for user_tournament in user_tournaments_to_delete:
                db.session.delete(user_tournament)

            db.session.delete(tournament_to_delete)
            db.session.commit()

            return jsonify({'message': 'Tournament and related records successfully deleted'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Tournament not found'})

@app.route('/tournamentsEdit/<int:tournament_id>', methods=['PUT'])
def edit_tournament(tournament_id):
    data = request.get_json()
    tournament_to_edit = Tournaments.query.get(tournament_id)  # Знаходимо турнір за його ID
    if tournament_to_edit:
        tournament_to_edit.tournament_name = data['tournamentName']  # Змінюємо назву турніру
        db.session.commit()  # Зберігаємо зміни в базі даних
        return jsonify({'message': 'Tournament name successfully updated'})
    else:
        return jsonify({'error': 'Tournament not found'})

@app.route('/add-teams', methods=['POST'])
def add_team_to_tournament():
    data = request.get_json()
    tournamentId = data['tournamentId']
    team_name = data['name']
    country = data['country']
    yearOfFoundation = data['yearOfFoundation']
    coach = data['coach']
    games = data['games']
    victories = data['victories']
    nobodys = data['nobodys']
    defeats = data['defeats']
    goalsScored = data['goalsScored']
    missedBalls = data['missedBalls']
    goalDifference = data['goalDifference']
    points = data['points']
    tournament = Tournaments.query.filter_by(tournament_id=tournamentId).first()
    if tournament is None:
        return jsonify({'error': 'Турніру з даним ID не існує'})
    new_team = Teams(name=team_name, country=country, year_of_foundation=yearOfFoundation, coach=coach, games=games, victories=victories, nobodys=nobodys, defeats=defeats, goals_scored=goalsScored, missed_balls=missedBalls, goal_difference=goalDifference, points=points, tournament_id=tournamentId)
    db.session.add(new_team)
    db.session.commit()
    return jsonify({'message': 'Команда успішно додана до турніру'})

@app.route('/teams', methods=['POST'])
def fetch_teams():
    data = request.get_json()
    tournamentId = data['tournamentId']
    teams = Teams.query.filter_by(tournament_id=tournamentId).all()
    if teams:
        serialized_teams = [
            {
                'team_id': team.team_id,
                'name': team.name,
                'country': team.country,
                'yearOfFoundation': team.year_of_foundation,
                'coach': team.coach
            }
            for team in teams
        ]
        return jsonify({'teams': serialized_teams})
    else:
        return jsonify({'error': 'Команди для цього турніру не знайдено'})

@app.route('/teamsDelete/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team_to_delete = Teams.query.get(team_id)
    if team_to_delete:
        try:
            # Видаляємо гравців, пов'язаних з командою
            players_to_delete = Players.query.filter_by(team_id=team_id).all()
            for player in players_to_delete:
                # Видаляємо голи, пов'язані з гравцем
                goals_to_delete = Goals.query.filter_by(player_id=player.player_id).all()
                for goal in goals_to_delete:
                    db.session.delete(goal)

                # Видаляємо асистентів, пов'язаних з гравцем
                assistants_to_delete = Assistants.query.filter_by(player_id=player.player_id).all()
                for assistant in assistants_to_delete:
                    db.session.delete(assistant)

                db.session.delete(player)

            # Видаляємо матчі, пов'язані з командою
            matches_to_delete = Matches.query.filter((Matches.home_team_id == team_id) | (Matches.away_team_id == team_id)).all()
            for match in matches_to_delete:
                # Видаляємо голи, пов'язані з матчем
                goals_to_delete = Goals.query.filter_by(match_id=match.match_id).all()
                for goal in goals_to_delete:
                    db.session.delete(goal)

                # Видаляємо асистентів, пов'язаних з матчем
                assistants_to_delete = Assistants.query.filter_by(match_id=match.match_id).all()
                for assistant in assistants_to_delete:
                    db.session.delete(assistant)

                db.session.delete(match)

             # Delete records from the Calendar table
            calendar_records_to_delete = Calendar.query.filter(
                (Calendar.home_team_id == team_id) | (Calendar.away_team_id == team_id)
            ).all()
            for calendar_record in calendar_records_to_delete:
                db.session.delete(calendar_record)

            # Видаляємо команду
            db.session.delete(team_to_delete)
            db.session.commit()

            return jsonify({'message': "Команда та пов'язані записи успішно видалені"})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Команду не знайдено'})

@app.route('/edit-teams/<int:team_id>', methods=['PATCH'])
def edit_teams(team_id):
    data = request.get_json()
    team_to_edit = Teams.query.get(team_id)  # Знаходимо команду за його ID
    if team_to_edit:
        team_to_edit.name = data['name']  # Змінюємо назву команди
        team_to_edit.country = data['country'] 
        team_to_edit.year_of_foundation = data['yearOfFoundation']  
        team_to_edit.coach = data['coach']  
        db.session.commit()  # Зберігаємо зміни в базі даних
        return jsonify({'message': 'Команду оновлено'})
    else:
        return jsonify({'error': 'Team not found'})

@app.route('/add-player', methods=['POST'])
def add_player():
    data = request.get_json()
    new_player = Players(
        first_name=data['firstName'],
        last_name=data['lastName'],
        team_id=data['teamId'],
        position=data['position'],
        birthday=datetime.strptime(data['birthday'], '%Y-%m-%d').date(),
        height=data['height'],
        weight=data['weight'],
        game_number=data['gameNumber']
    )
    team = Teams.query.filter_by(team_id=data['teamId']).first()
    if team is None:
        return jsonify({'error': 'Команди з даним ID не існує'})
    db.session.add(new_player)
    db.session.commit()
    return jsonify({'message': 'Гравець успішно доданий в базу даних'})

@app.route('/players', methods=['POST'])
def fetch_players():
    data = request.get_json()
    tournamentId = data['tournamentId']
    # Вибрати всі команди для вказаного турніру
    teams = Teams.query.filter_by(tournament_id=tournamentId).all()
    # Зібрати ідентифікатори команд у список
    team_ids = [team.team_id for team in teams]
    # Вибрати всіх гравців, які є у вибраних командах
    players = Players.query.filter(Players.team_id.in_(team_ids)).all()
    if players:
        serialized_players = [
            {
                'player_id': player.player_id,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'team_id': player.team_id,
                'position': player.position,
                'birthday': player.birthday.strftime('%Y-%m-%d'),  # При потребі форматування дати
                'height': player.height,  # Перетворення на float
                'weight': player.weight,  # Перетворення на float
                'game_number': player.game_number,
            }
            for player in players
        ]
        return jsonify({'players': serialized_players})
    else:
        return jsonify({'error': 'Гравців для цього турніру не знайдено'})

@app.route('/playersDelete/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player_to_delete = Players.query.get(player_id)
    if player_to_delete:
        try:
            # Видалення голів, пов'язаних із гравцем
            goals_to_delete = Goals.query.filter_by(player_id=player_id).all()
            for goal in goals_to_delete:
                db.session.delete(goal)
            # Видалення асистентів, пов'язаних із гравцем
            assistants_to_delete = Assistants.query.filter_by(player_id=player_id).all()
            for assistant in assistants_to_delete:
                db.session.delete(assistant)
            db.session.delete(player_to_delete)
            db.session.commit()
            return jsonify({'message': "Гравець та пов'язані записи успішно видалені"})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Гравця не знайдено'})
    
@app.route('/edit-players/<int:player_id>', methods=['PATCH'])
def edit_players(player_id):
    data = request.get_json()
    player_to_edit = Players.query.get(player_id)  # Знаходимо гравця за його ID
    if player_to_edit:
        player_to_edit.first_name = data['firstName']  # Змінюємо гравця
        player_to_edit.last_name = data['lastName'] 
        player_to_edit.team_id = data['teamId']  
        player_to_edit.position = data['position']  
        player_to_edit.birthday = datetime.strptime(data['birthday'], '%Y-%m-%d').date()  
        player_to_edit.height = data['height']  
        player_to_edit.weight = data['weight']  
        player_to_edit.game_number = data['gameNumber']  
        db.session.commit()  # Зберігаємо зміни в базі даних
        return jsonify({'message': 'Гравця оновлено'})
    else:
        return jsonify({'error': 'Гравця не знайдено'})
    
@app.route('/add-match', methods=['POST'])
def add_match():
    try:
        data = request.json
        match_date = data['matchDate']
        match_time = data['matchTime']
        stadium = data['stadium']
        home_team_id = data['homeTeamId']
        away_team_id = data['awayTeamId']
        home_team_goals = data['homeTeamGoals']
        away_team_goals = data['awayTeamGoals']
        data_goals_home = data['dataGoalsHome']
        data_goals_away = data['dataGoalsAway']

        # Save the match details to the Matches table
        new_match = Matches(
            match_date=datetime.strptime(match_date, '%Y-%m-%d').date(),
            match_time=datetime.strptime(match_time, '%H:%M').time(),
            stadium=stadium,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            home_team_goals=home_team_goals,
            away_team_goals=away_team_goals
        )
        db.session.add(new_match)
        db.session.commit()

        # Save the goals to the Goals table
        for goal_data in data_goals_home:
            new_goal = Goals(
                match_id=new_match.match_id,
                team_id=home_team_id,
                player_id=goal_data['playerId'],
                time_of_goal=goal_data['minute']
            )
            db.session.add(new_goal)

        for goal_data in data_goals_away:
            new_goal = Goals(
                match_id=new_match.match_id,
                team_id=away_team_id,
                player_id=goal_data['playerId'],
                time_of_goal=goal_data['minute']
            )
            db.session.add(new_goal)

        # Save the asist to the Assistants table
        for asist_data in data_goals_home:
            if asist_data['assistant'] and asist_data['assistant'] != 'pen':
                new_asist = Assistants(
                    match_id=new_match.match_id,
                    team_id=home_team_id,
                    player_id=asist_data['assistant'],
                    time_of_assist=asist_data['minute']
                )
                db.session.add(new_asist)

        for asist_data in data_goals_away:
            if asist_data['assistant'] and asist_data['assistant'] != 'pen':
                new_asist = Assistants(
                    match_id=new_match.match_id,
                    team_id=away_team_id,
                    player_id=asist_data['assistant'],
                    time_of_assist=asist_data['minute']
                )
                db.session.add(new_asist)

        # Update Teams table for home and away teams
        home_team = Teams.query.get(home_team_id)
        away_team = Teams.query.get(away_team_id)

        # Update games played for both teams
        home_team.games += 1
        away_team.games += 1

        # Update goals scored and missed balls for both teams
        home_team.goals_scored += home_team_goals
        home_team.missed_balls += away_team_goals
        away_team.goals_scored += away_team_goals
        away_team.missed_balls += home_team_goals


        # Update goal difference for both teams
        home_team.goal_difference = home_team.goals_scored - home_team.missed_balls
        away_team.goal_difference = away_team.goals_scored - away_team.missed_balls

        # Update points, victories, defeats, and nobodys for both teams based on match result
        if home_team_goals > away_team_goals:
            home_team.points += 3
            home_team.victories += 1
            away_team.defeats += 1
        elif away_team_goals > home_team_goals:
            away_team.points += 3
            away_team.victories += 1
            home_team.defeats += 1
        else:
            home_team.points += 1
            away_team.points += 1
            home_team.nobodys += 1
            away_team.nobodys += 1

        db.session.commit()

        return jsonify({'message': 'Match added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/matches', methods=['POST'])
def fetch_matches():
    data = request.get_json()
    tournamentId = data['tournamentId']
    # Вибрати всі команди для вказаного турніру
    teams = Teams.query.filter_by(tournament_id=tournamentId).all()
    team_ids = [team.team_id for team in teams]
    matches = Matches.query.filter((Matches.home_team_id.in_(team_ids)) | (Matches.away_team_id.in_(team_ids))).all()
    goals_data = Goals.query.filter(Goals.match_id.in_([match.match_id for match in matches])).all()    
    assistants_data = Assistants.query.filter(Assistants.match_id.in_([match.match_id for match in matches])).all()
    if matches:
        serialized_matches = [
            {
                'match_id': match.match_id,
                'match_date': match.match_date.strftime('%Y-%m-%d'),  
                'match_time': match.match_time.strftime("%H:%M:%S"),
                'stadium': match.stadium,
                'home_team_id': match.home_team_id,
                'away_team_id': match.away_team_id,
                'home_team_goals': match.home_team_goals, 
                'away_team_goals': match.away_team_goals,  
                'goals': [{'goal_id':goal.goal_id, 'team_id': goal.team_id, 'player_id': goal.player_id, 'time_of_goal': goal.time_of_goal} for goal in goals_data if goal.match_id == match.match_id],
                'assistants': [{'assistant_id': assistant.assistant_id, 'team_id': assistant.team_id, 'player_id': assistant.player_id, 'time_of_assist': assistant.time_of_assist} for assistant in assistants_data if assistant.match_id == match.match_id]
            }
            for match in matches
        ]
        return jsonify({'matches': serialized_matches})
    else:
        return jsonify({'error': 'Матчів для цього турніру не знайдено'})

@app.route('/standings', methods=['POST'])
def standings():
    data = request.get_json()
    tournamentId = data['tournamentId']
    teams = Teams.query.filter_by(tournament_id=tournamentId).all()
    if teams:
        serialized_teams = [
            {
                'team_id': team.team_id,
                'name': team.name,
                'games': team.games,
                'victories': team.victories,
                'nobodys': team.nobodys,
                'defeats': team.defeats,
                'goals_scored': team.goals_scored,
                'missed_balls': team.missed_balls,
                'goal_difference': team.goal_difference,
                'points': team.points,
            }
            for team in teams
        ]
        return jsonify({'standings': serialized_teams})
    else:
        return jsonify({'error': 'Команди для цього турніру не знайдено'})

@app.route('/statisticsGoals', methods=['POST'])
def statisticsGoals():
    data = request.get_json()
    tournamentId = data['tournamentId']
    teams = Teams.query.filter_by(tournament_id=tournamentId).all()
    team_ids = [team.team_id for team in teams]
    matches = Matches.query.filter((Matches.home_team_id.in_(team_ids)) | (Matches.away_team_id.in_(team_ids))).all()
    goals_data = Goals.query.filter(Goals.match_id.in_([match.match_id for match in matches])).all()    
    if goals_data:
        serialized_teams = [
            {
                'goal_id': goal.goal_id,
                'team_id': goal.team_id,
                'player_id': goal.player_id,
            }
            for goal in goals_data
        ]
        return jsonify({'goals_data': serialized_teams})
    else:
        return jsonify({'error': 'Голів для цього турніру не знайдено'})

@app.route('/statisticsAsists', methods=['POST'])
def statisticsAsists():
    data = request.get_json()
    tournamentId = data['tournamentId']
    teams = Teams.query.filter_by(tournament_id=tournamentId).all()
    team_ids = [team.team_id for team in teams]
    matches = Matches.query.filter((Matches.home_team_id.in_(team_ids)) | (Matches.away_team_id.in_(team_ids))).all()
    assistants_data = Assistants.query.filter(Assistants.match_id.in_([match.match_id for match in matches])).all()
    if assistants_data:
        serialized_teams = [
            {
                'assistant_id': asist.assistant_id,
                'team_id': asist.team_id,
                'player_id': asist.player_id,
            }
            for asist in assistants_data
        ]
        return jsonify({'assistants_data': serialized_teams})
    else:
        return jsonify({'error': 'Асистів для цього турніру не знайдено'})
    

@app.route('/create-match-calendar', methods=['POST'])
def create_match_calendar():
    data = request.get_json()
    tournament_id = data['tournament_id']

    teams = Teams.query.filter_by(tournament_id=tournament_id).all()
    team_ids = [team.team_id for team in teams]

    Calendar.query.filter(
        or_(Calendar.home_team_id.in_(team_ids), Calendar.away_team_id.in_(team_ids)),
        Calendar.round_number.isnot(None),
        Calendar.home_team_id.isnot(None),
        Calendar.away_team_id.isnot(None)
    ).delete()
    db.session.commit()

    # Generate unique pairs of teams for each round
    matchups = list(itertools.combinations(team_ids, 2))
    random.shuffle(matchups)

    # Assign matchups to rounds in the calendar table
    round_number = 1
    played_matchups = set()

    while matchups:
        round_matchups = matchups[:len(teams) // 2]
        matchups = matchups[len(teams) // 2:]

        for home_team_id, away_team_id in round_matchups:
            # Check if this matchup has already been played and away_team_id is not the same as home_team_id
            if (home_team_id, away_team_id) not in played_matchups and (away_team_id, home_team_id) not in played_matchups and home_team_id != away_team_id:
                new_match = Calendar(round_number=round_number, home_team_id=home_team_id, away_team_id=away_team_id)
                db.session.add(new_match)

                # Add this matchup to the set of played matchups
                played_matchups.add((home_team_id, away_team_id))

        round_number += 1

    db.session.commit()
    return jsonify({'message': 'Match calendar created successfully'})


# API endpoint to fetch the match calendar
@app.route('/fetch-match-calendar', methods=['POST'])
def fetch_match_calendar():
    data = request.get_json()
    tournament_id = data['tournament_id']

    # Check if tournament_id is provided
    if tournament_id is None:
        return jsonify({'error': 'Tournament ID is required'}), 400

    # Retrieve the calendar for the specified tournament
    calendar = Calendar.query.filter(
        (Calendar.round_number.isnot(None)) &
        (Calendar.home_team_id.isnot(None)) &
        (Calendar.away_team_id.isnot(None)) &
        ((Calendar.home_team_id.in_(db.session.query(Teams.team_id).filter_by(tournament_id=tournament_id))) |
         (Calendar.away_team_id.in_(db.session.query(Teams.team_id).filter_by(tournament_id=tournament_id))))
    ).all()

    # Format the calendar data
    match_calendar = [{'round_number': match.round_number, 'home_team_id': match.home_team_id, 'away_team_id': match.away_team_id} for match in calendar]

    return jsonify(match_calendar)
    
if __name__ == '__main__':
    app.run(debug=True)

