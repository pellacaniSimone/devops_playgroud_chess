import datetime
import random
import uuid
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask import  Flask, render_template, request, session,  redirect,  url_for,  flash, jsonify
from chess_engine.room import Room
import time
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user, current_user
import psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Final
from threading import Thread
from flask_session import Session 

app = Flask(
        __name__,
        static_folder = 'static',
        template_folder = 'static',
        static_url_path=''
    )



"""Scegliere il dominio corretto"""
DB_HOST : Final = "databaseprova.pdsg1aa20222023"
DB_NAME : Final = "webchesstrunk"
DB_USER : Final = "wwwchesslogin"
DB_PASS : Final = "eVfuV"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


# Websocket setting
app.secret_key = 'cairocoders-ednalan'
app.config['SECRET_KEY'] = 'asdfghjkl123!'
app.config['SESSION_TYPE'] = 'filesystem'


# permetta al DOM della pagina di caricarsi più facilmente
Session(app) 
socketRep = SocketIO(app)

#lista dei giochi delle stanze
room=Room()
roomRandom=Room()
roomCrazy=Room()
roomQuadriglia=Room()


# template
VUE="index.html"
HOMEPAGE="firstPage.html"
GAMEPVP="gamepvp.html"
LOGIN_FORM="loginForm.html"

#istanza di LoginManager
login_manager = LoginManager()
login_manager.init_app(app)



# common string
EVENT_RECV = "received my event: "


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return str(self.id)




@login_manager.user_loader
def load_user(user_id):
    """User di questa sessione, creato a partire da utente nel database con user_id corrispondente"""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM users WHERE id_user = %s', (str(user_id),))
    user_data = cursor.fetchone()
    if user_data:
        user = User(user_data['id_user'])
        return user
    return None



first=True # variabile globale per consentire l'accesso ai test di Vue
@app.route('/') #parte loggata
@login_required
def root():
    """flask act as server per vue app"""
    global first
    if first:
        first=True
        app.config['LOGIN_DISABLED'] = False
    else:
        first=True
    return app.send_static_file(VUE)



@app.route('/cypress') # test /cypress
def cypress():
    """disabilita login temporanemante per cypress"""
    app.config['LOGIN_DISABLED'] = True
    global first
    first=False
    return redirect(url_for('root'))


#parte non loggata
@app.route('/index')
def homepage():
    """GuestHomePage"""
    return render_template(HOMEPAGE)

def crea_id():
    """Genera un nome stanza casuale diverso da UUID perchè genera conflitto"""
    app = str("%032x" % random.getrandbits(128))
    return app[0:8:]


room_id_pvp=crea_id() # id stanza
contatore=True # variabile globale che permette alle stanze di avere 2 giocatori, siano essi su pixel che in pvp normale
@app.route('/gamepvp')
def game_pvp():
    """una stanza nuova ogni due volte che si passa di qua"""
    global contatore
    global room_id_pvp 
    if contatore:
        contatore=False
        room_id_pvp = crea_id()
        print ("stanza bianca")
        time.sleep(0.15)
        return render_template(GAMEPVP, color = True , room_id = room_id_pvp , path = True)
    else:
        contatore=True
        print ("stanza nera")
        time.sleep(0.15)
        return render_template(GAMEPVP, color = False , room_id = room_id_pvp , path = True )


@app.route('/gamepixel', methods=['GET'])
def game_pixel():
    """usato le stesse stanze di PVP tanto cambia solo la mod grafica"""
    global contatore
    global room_id_pvp 
    if contatore:
        contatore=False
        room_id_pvp = crea_id()
        print ("stanza bianca")
        time.sleep(0.15)
        return render_template(GAMEPVP, color = True , room_id = room_id_pvp , path = False )
    else:
        contatore=True
        print ("stanza nera")
        time.sleep(0.15)
        return render_template(GAMEPVP, color = False , room_id = room_id_pvp , path = False )



@app.route('/ping', methods=['GET'])
def ping_pong():
    numero=room.join_room()
    return jsonify(numero)

@app.route('/utente', methods=['GET'])
def utente_dati():
    return jsonify({
        'id_user': session['id'],
        'username': session['username']
    })




@socketRep.event
def join_pvp(message):
    """intercetta eventi join"""
    print("funzione join_pvp ")
    print (message)
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1



@socketRep.event
def pvp_room_event(message):
    """intercetta eventi chat PVP"""
    print("funzione pvp_room_event")
    print (message)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
        {'data': message['data'], 'count': session['receive_count']},
        to=message['room'])


@socketRep.event
def my_move(message):
    """Proxy mosse"""
    print("funzione my_move ")
    print (message)
    time.sleep(0.3)
    """intercetta e distribuisce mesaggio"""
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('passaggio_fen' , { 'data': message['string'] , 'mossa': message['mossa'] , 'count': session['receive_count']  } , to=message['room'] )



@app.route('/loginForm.html', methods=['GET' , 'POST'])
def login():
    """Form per procedura di login"""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    """Check if "username" and "password" POST requests exist (user submitted form)"""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
        """Check if account exists using MySQL"""
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        """Fetch one record and return result"""
        account = cursor.fetchone()
        if account:
            password_rs = account['password']
            print(password_rs)
            """If account exists in users table in out database"""
            if check_password_hash(password_rs, password):
                """Create session data, we can access this data in other routes"""
                session['loggedin'] = True
                session['id'] = account['id_user']
                session['username'] = account['username']
                user = User(account['id_user'])
                login_user(user)
                flash('You have successfully logged!')
                """Redirect to home page"""
                return redirect(url_for('root'))
            else:
                """Account doesnt exist or username/password incorrect"""
                flash('Incorrect username/password')
        else:
            """Account doesnt exist or username/password incorrect"""
            flash('Incorrect username/password')
    return render_template(LOGIN_FORM)


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester


@app.route('/gioca')
@socketRep.on('connect_quadriglia')
def unirsi():
    print(roomQuadriglia.roomsState)
    room_id=roomQuadriglia.join_room(4)
    session["room"]=room_id ##aggiunta per mantenere un concetto di sessione così da scollegare le persone
    print(roomQuadriglia.roomsState)
    emit("codice", room_id)
    join_room(room_id)
    numero=roomQuadriglia.utenti_in_stanza(room_id)
    if numero==2:
        print("sono dentro e sto emmettendo il colore nero")
        emit("nero", "b")
    elif numero== 3: 
        emit("squadra", "seconda")
    elif numero==4:
        emit("nero2", "b")  
    emit( 'conta', numero, to=room_id)


@socketRep.on('connection')
def unirsi(data,  methods=['GET', 'POST']):
    if data=="normale":
        room_id=room.join_room()
        numero=room.utenti_in_stanza(room_id)
        print("sono dentro la richiesta normale")
    elif data=="random":
        room_id=roomRandom.join_room()
        numero=roomRandom.utenti_in_stanza(room_id)
        print("sono dentro la richiesta random")
    elif data=="crazy":
        room_id=roomCrazy.join_room()
        numero=roomCrazy.utenti_in_stanza(room_id)
        print("sono dentro la richiesta crazy")
    print(room_id)    
    print(numero)
    join_room(room_id)
    emit("codice", room_id)
    session["room"]=room_id    
    if numero==2:
        emit("nero", "b")
    emit( "conta", numero, to=room_id)    

@socketRep.on("disconnessione")
def disconesso(data,  methods=['GET', 'POST']):
    print("disconnessione")
    stanza=session.get("room")  
    print(stanza)
    emit('abbandono', to=stanza)
    if data=="normale":
        room.ha_lasciato(stanza)
        print(room.roomsState)
        print(" abbandono normale")
    elif data=="random":
        roomRandom.ha_lasciato(stanza)
        print("abbandono random")
    elif data=="crazy":
        roomCrazy.ha_lasciato(stanza)
        print("abbandono crazy")
    elif data=="quadriglia":
        roomQuadriglia.ha_lasciato(stanza)
        print("abbandono quadriglia")



@socketRep.on('mossa')
def handle_movememnts(data, mossa, stanza,  methods=['GET', 'POST']):
    print(EVENT_RECV + str(data))
    print(EVENT_RECV + str(stanza))
    emit("scacchiera", data, to=stanza)
    emit("elencoMosse", mossa, to=stanza)
    """crazyHouse"""
    if mossa.get("captured") is not None:
       emit("pezzoPreso", (mossa.get("captured"), mossa.get("color")), to=stanza)



@socketRep.on('inserire')    
def handle_insert_piece(data,stanza,methods=['GET', 'POST']):  
    """crazy house inserimento di un pezzo"""
    x=data.index(" ")
    stringa=list(data)
    x+=1 # mi trovava lo spazio e dopo 1 c'è la lettera che indica il turno
    if stringa[x] == 'w':
        stringa[x]= 'b'
    else:
        stringa[x] = 'w'
    data="".join(stringa)    
    emit("scacchiera", data, to=stanza)


@socketRep.on('inserire2')    
def handle_insert_piece(data,stanza,methods=['GET', 'POST']):  
    """quadriglia inserimento di un pezzo nella seconda scacchiera"""
    x=data.index(" ")
    stringa=list(data)
    x+=1## mi trovava lo spazio e dopo 1 c'è la lettera che indica il turno
    if stringa[x] == 'w':
        stringa[x]= 'b'
    else:
        stringa[x] = 'w'
    data="".join(stringa)    
    emit("scacchiera2", data, to=stanza)    


@app.route('/verificaInserimento', methods=['POST'])
def fen_to_matrix():
    """CrazyHouse controllo stringa per sapere se si può inserire in quel punto
    prende 3 elementi in ingresso fen: la stringa fen attuale, riga e colonna che sono la casella dove si vuole inserire
    """
    post_data=request.get_json()
    fen=post_data.get('fen')
    riga=post_data.get('riga')
    colonna=int(post_data.get('colonna'))
    riga=7-int(riga)
    print(fen)
    fen = fen.split(' ')[0]  # estrae solo la parte dei pezzi
    rows = fen.split('/')
    matrix = []
    for row in rows:
        matrix_row = []
        for char in row:
            if char.isdigit():
                matrix_row.extend(['1'] * int(char))
            else:
                matrix_row.append(char)
        matrix.append(matrix_row)

    if matrix[riga][colonna]=='1':
        print("yeahhhhhh")
        return (jsonify(True))
    else:
        print ("nooooooo")
        return (jsonify(False))
        

@socketRep.on('mossa2')
def handle_my_custom_event(data, mossa, stanza,  methods=['GET', 'POST']):
    """Quadriglia, parto con la creazione di un'altra funzione simil mossa che serve a differenziare le mosse tra le due scacchiere """
    print(EVENT_RECV + str(data))
    print(EVENT_RECV + str(stanza))
    emit("scacchiera2", data, to=stanza)
    emit("elencoMosse", mossa, to=stanza)
    """cattura quadriglia""" 
    if mossa.get("captured") is not None:
       emit("pezzoPreso2", (mossa.get("captured"), mossa.get("color")), to=stanza)

@socketRep.on('message')
def handle_chat(data,stanza, methods=['GET', 'POST']):
    print(EVENT_RECV + str(data))
    emit("message", data, to=stanza)

@app.route('/fine_partita', methods=['GET','POST'])
def fine_partita():
    post_data=request.get_json()
    n_mosse=post_data.get('Nmosse')
    colore=post_data.get('colore')
    id_user=post_data.get('id_user')
    username=post_data.get('username')
    now = datetime.utcnow()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    gamemode =post_data.get('modalita')
    print("FUNZIONE FINE PARTITA")
    date = now.strftime('%Y-%m-%d')
    if(colore == 'w'):
        cursor.execute("INSERT INTO game (id_game,game_mode,date,n_moves) VALUES (DEFAULT,%s,%s,%s)", ( gamemode, date, n_mosse,))
        conn.commit()
    cursor.execute('SELECT max(id_user) FROM users', (id_user) ) # ?
    print(cursor.fetchone())
    id_of_new_row = cursor.fetchone()[0]
    cursor.execute("INSERT INTO play (username,id_game) VALUES (%s,%s)", ( username, id_of_new_row,))
    conn.commit()
    conn.close()
    return None


@socketRep.on('stringaRandom')   
def genera_unimorechess(stanza, methods=['GET', 'POST']):
    """ rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR """
   # if end == None:                 """nel caso si voglia dare una stringa finale diversa"""
    end = ' w KQkq - 0 1'
    """Tutte le pedine meno i re sono in posizione casuale, per evitare uno scacco matto"""
    pedine = 'rnbqbnrpppppppp'
    pedine = ''.join(random.sample(pedine, 15))
    pedine = pedine[0:4] + "k" + pedine[4:]
    s = pedine[0:8] + "/" + pedine [8:] + "/8/8/8/8/" + pedine[8:].upper() + "/" + pedine[0:8].upper() + " " + end
    print(s)
    emit("stringa", str(s), to=stanza)



@app.route('/logout' , methods=['GET','POST'])
@login_required
def logout():
    """Remove session data, this will log the user out"""
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    logout_user()
    """Redirect to login page"""
    return redirect(url_for('homepage'))


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'surname' in request.form and 'username' in request.form and 'password2' in request.form:
        """Create variables for easy access"""
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password2 = request.form['password2']
        surname = request.form['surname']
        _hashed_password = generate_password_hash(password)
        """Check if account exists using MySQL"""
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cursor.fetchone()
        print(account)
        """If account exists show error and validation checks"""
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif len(password) < 6 :
            flash('password must have at least 6 characters')
            return redirect(url_for('dashboard'))
        elif password != password2 :
            flash('the passwords must be the same')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email or not name or not surname:
            flash('Please fill out the form!')
        else:
            """Account doesnt exists and the form data is valid, now insert new account into users table"""
            cursor.execute("INSERT INTO users (id_user,username,password,name,surname,email,score,record,is_owner) VALUES (DEFAULT,%s,%s,%s,%s,%s,0,null,false)", ( username, _hashed_password, name, surname, email))
            conn.commit()
            flash('You have successfully registered!')
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            account = cursor.fetchone()
            user = User(account['id_user'])
            login_user(user)
            """if user.is_authenticated: Redirect to home page (logged in)"""
            return redirect(url_for('root'))
    elif request.method == 'POST':
        """Form is empty... (no POST data)"""
        flash('Please fill out the form!')
    """Show registration form with message (if any)"""
    return render_template("register.html")



if __name__ == '__main__':

    Thread.run(socketRep.run(app, debug=True))


