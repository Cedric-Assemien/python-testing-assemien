import datetime
import json
from flask import Flask,render_template,request,redirect,flash,url_for
reservations =[]

#Chargement des clubs
def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

#Chargement des competitions
def loadCompetitions():
    current_year = datetime.datetime.now().year
    with open('competitions.json') as comps:
        competitions = json.load(comps)['competitions']
        filtered_competitions = [comp for comp in competitions if int(comp['date'][:4]) >= 2024]
        return filtered_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/',)
def index():
    competition = [c['name'] for c in competitions]
     
    return render_template('index.html', competitions=competition)
    

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)
    
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('Adresse e-mail invalide. Veuillez entrer une adresse e-mail valide.', 'error')
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
   
    if int(competition['numberOfPlaces']) < placesRequired  :
        flash('Désolé, il n\'y a pas assez de places disponibles.')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    elif int(club ['points']) < placesRequired  :
        flash("Désolé, vous n'avez pas assez de points.")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    elif placesRequired > 12:
        flash('Désolé, vous ne pouvez pas réserver plus de 12 places.')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    elif placesRequired == 0 :
        flash('Désolé, vous pouvez réservez minimum 1 place. ')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    elif placesRequired < 0 :
        flash('Désolé, pas de nombre négatif accepté !!!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    club ['points'] = int (club ['points']) - placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    flash('Génial !! Vous avez réussi à réserver {} places :)'.format(placesRequired))
    return render_template('welcome.html', club=club, competitions=competitions)

    

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))