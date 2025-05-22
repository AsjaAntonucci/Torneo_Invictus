import streamlit as st
import pandas as pd
import datetime

# Page configuration
st.set_page_config(
    page_title="Torneo Chanbara",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS per migliorare la leggibilità in modalità scura
st.markdown("""
<style>
    /* Stili per migliorare la leggibilità in modalità scura */
    .dark-mode-text {
        color: rgba(250, 250, 250, 0.95);
        background-color: rgba(0, 0, 0, 0.1);
        padding: 5px;
        border-radius: 3px;
    }
    
    /* Stili per le carte profilo */
    .profile-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Stili per i soprannomi */
    .nickname {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 0;
    }
    
    /* Stili per i nomi completi */
    .fullname {
        font-size: 14px;
        opacity: 0.7;
        margin-top: 0;
    }
    
    /* Stili per i bottoni */
    .stButton button {
        background-color: rgba(49, 51, 63, 0.7);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton button:hover {
        background-color: rgba(49, 51, 63, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Stili per le metriche e statistiche */
    .metric-container {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Stili per i dataframe e tabelle */
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.03);
    }
    
    .dataframe {
        background-color: rgba(255, 255, 255, 0.03);
    }
    
    /* Stili per i titoli */
    h1, h2, h3, h4, h5 {
        color: rgba(255, 255, 255, 0.9);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for Chanbara tournament
if "page" not in st.session_state: 
    st.session_state.page = "login"
if "user" not in st.session_state: 
    st.session_state.user = None
if "tournaments" not in st.session_state:
    st.session_state.tournaments = [
        {
            "id": 1,
            "name": "Torneo Chanbara 2025",
            "registration_open": True,
            "start_date": "2025-06-01",
            "end_date": "2025-06-30"
        },
        {
            "id": 2,
            "name": "Torneo Estate Chanbara",
            "registration_open": True,
            "start_date": "2025-07-15",
            "end_date": "2025-08-15"
        },
        {
            "id": 3,
            "name": "Campionato Regionale",
            "registration_open": True,
            "start_date": "2025-09-01",
            "end_date": "2025-10-15"
        }
    ]

# Per retrocompatibilità
if "tournament" not in st.session_state:
    st.session_state.tournament = st.session_state.tournaments[0]
if "athletes" not in st.session_state:
    st.session_state.athletes = [
        {"id": 1, "name": "Mario Rossi", "nickname": "Super Mario", "email": "mario@example.com", "password": "password", "level": 3, "profile_img": "https://ui-avatars.com/api/?name=Super+Mario&background=random", "tournaments": [1, 3]},
        {"id": 2, "name": "Luigi Verdi", "nickname": "Green Arrow", "email": "luigi@example.com", "password": "password", "level": 2, "profile_img": "https://ui-avatars.com/api/?name=Green+Arrow&background=random", "tournaments": [1, 2]},
        {"id": 3, "name": "Anna Bianchi", "nickname": "Ninja", "email": "anna@example.com", "password": "password", "level": 2, "profile_img": "https://ui-avatars.com/api/?name=Ninja&background=random", "tournaments": [1]},
        {"id": 4, "name": "Sara Neri", "nickname": "Black Samurai", "email": "sara@example.com", "password": "password", "level": 1, "profile_img": "https://ui-avatars.com/api/?name=Black+Samurai&background=random", "tournaments": [2, 3]}
    ]
if "specialties" not in st.session_state:
    st.session_state.specialties = [
        {"id": 1, "name": "kodachi"},
        {"id": 2, "name": "choken free"},
        {"id": 3, "name": "nito"},
        {"id": 4, "name": "tate-kodachi"},
        {"id": 5, "name": "tate-choken"}
    ]
if "challenges" not in st.session_state:
    # Create sample challenges
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    next_week = today + datetime.timedelta(days=7)
    
    st.session_state.challenges = [
        {
            "id": 1,
            "challenger_id": 1,
            "opponent_id": 2,
            "date": tomorrow.isoformat(),
            "specialty_id": 1,
            "winner_id": None
        },
        {
            "id": 2,
            "challenger_id": 3,
            "opponent_id": 4,
            "date": next_week.isoformat(),
            "specialty_id": 3,
            "winner_id": None
        }
    ]

# Helper functions for Chanbara tournament
def get_athlete_by_id(athlete_id):
    """Get athlete information by ID."""
    for athlete in st.session_state.athletes:
        if athlete["id"] == athlete_id:
            return athlete
    return None

def get_athlete_by_email(email):
    """Get athlete information by email."""
    for athlete in st.session_state.athletes:
        if athlete["email"] == email:
            return athlete
    return None

def get_specialty_by_id(specialty_id):
    """Get specialty information by ID."""
    for specialty in st.session_state.specialties:
        if specialty["id"] == specialty_id:
            return specialty
    return None

def authenticate(email, password, is_admin=False):
    """Authenticate a user."""
    if is_admin:
        # Admin authentication (simplified)
        if email == "admin@example.com" and password == "admin123":
            st.session_state.user = {"id": 999, "name": "Admin", "email": email, "is_admin": True, "profile_img": "https://ui-avatars.com/api/?name=Admin&background=red"}
            st.session_state.page = "admin"
            return True
        return False
    else:
        # Athlete authentication
        athlete = get_athlete_by_email(email)
        if athlete and athlete["password"] == password:
            athlete["is_admin"] = False
            st.session_state.user = athlete
            st.session_state.page = "profile"
            return True
        return False

def register_athlete(name, email, password, nickname=None, tournament_id=1):
    """Register a new athlete."""
    # Trova il torneo selezionato
    selected_tournament = None
    for tournament in st.session_state.tournaments:
        if tournament["id"] == tournament_id:
            selected_tournament = tournament
            break
    
    if not selected_tournament:
        return False, "Torneo non trovato"
    
    if not selected_tournament["registration_open"]:
        return False, "Le registrazioni per questo torneo sono chiuse"
    
    # Check if email already exists
    if get_athlete_by_email(email):
        return False, "Email già registrata"
    
    # Use nickname or default to name if not provided
    if not nickname:
        nickname = name.split()[0]  # Use first name as default nickname
    
    # Create new athlete
    new_id = max(athlete["id"] for athlete in st.session_state.athletes) + 1 if st.session_state.athletes else 1
    new_athlete = {
        "id": new_id,
        "name": name,
        "nickname": nickname,
        "email": email,
        "password": password,
        "level": 1,
        "profile_img": f"https://ui-avatars.com/api/?name={nickname.replace(' ', '+')}&background=random",
        "tournaments": [tournament_id]
    }
    
    st.session_state.athletes.append(new_athlete)
    return True, "Registrazione completata con successo"

def delete_athlete(athlete_id):
    """Delete an athlete and all their challenges."""
    # Trova l'atleta da eliminare
    athlete_index = None
    for i, athlete in enumerate(st.session_state.athletes):
        if athlete["id"] == athlete_id:
            athlete_index = i
            break
    
    if athlete_index is None:
        return False, "Atleta non trovato"
    
    # Rimuovi tutte le sfide relative all'atleta
    st.session_state.challenges = [c for c in st.session_state.challenges 
                                 if c["challenger_id"] != athlete_id and c["opponent_id"] != athlete_id]
    
    # Rimuovi l'atleta
    st.session_state.athletes.pop(athlete_index)
    
    return True, "Atleta eliminato con successo"

def modify_athlete(athlete_id, data):
    """Modify an athlete's data."""
    # Trova l'atleta da modificare
    athlete_index = None
    for i, athlete in enumerate(st.session_state.athletes):
        if athlete["id"] == athlete_id:
            athlete_index = i
            break
    
    if athlete_index is None:
        return False, "Atleta non trovato"
    
    # Aggiorna i dati dell'atleta
    for key, value in data.items():
        if key in st.session_state.athletes[athlete_index]:
            st.session_state.athletes[athlete_index][key] = value
    
    return True, "Dati atleta aggiornati con successo"

def enroll_in_tournament(athlete_id, tournament_id):
    """Enroll an athlete in a tournament."""
    # Trova l'atleta
    athlete_index = None
    for i, athlete in enumerate(st.session_state.athletes):
        if athlete["id"] == athlete_id:
            athlete_index = i
            break
    
    if athlete_index is None:
        return False, "Atleta non trovato"
    
    # Trova il torneo
    tournament = None
    for t in st.session_state.tournaments:
        if t["id"] == tournament_id:
            tournament = t
            break
    
    if not tournament:
        return False, "Torneo non trovato"
    
    if not tournament["registration_open"]:
        return False, "Le registrazioni per questo torneo sono chiuse"
    
    # Verifica se l'atleta è già iscritto
    if tournament_id in st.session_state.athletes[athlete_index].get("tournaments", []):
        return False, "Atleta già iscritto a questo torneo"
    
    # Iscrivi l'atleta al torneo
    if "tournaments" not in st.session_state.athletes[athlete_index]:
        st.session_state.athletes[athlete_index]["tournaments"] = []
    
    st.session_state.athletes[athlete_index]["tournaments"].append(tournament_id)
    
    return True, f"Iscrizione al torneo {tournament['name']} completata con successo"

def create_challenge(challenger_id, opponent_id, date, specialty_id):
    """Create a new challenge."""
    if st.session_state.tournament["registration_open"]:
        return False, "Le sfide possono essere create solo dopo la chiusura delle registrazioni"
    
    # Validate challenger and opponent
    challenger = get_athlete_by_id(challenger_id)
    opponent = get_athlete_by_id(opponent_id)
    
    if not challenger or not opponent:
        return False, "Atleta non trovato"
    
    # Check if opponent is of equal or higher level
    if opponent["level"] < challenger["level"]:
        return False, "Puoi sfidare solo atleti di livello pari o superiore"
    
    # Check if specialty exists
    specialty = get_specialty_by_id(specialty_id)
    if not specialty:
        return False, "Specialità non trovata"
    
    # Check if date is in the future
    challenge_date = datetime.date.fromisoformat(date)
    if challenge_date <= datetime.date.today():
        return False, "La data della sfida deve essere futura"
    
    # Check if there's already a challenge between these athletes on this date
    for challenge in st.session_state.challenges:
        if ((challenge["challenger_id"] == challenger_id and challenge["opponent_id"] == opponent_id) or
            (challenge["challenger_id"] == opponent_id and challenge["opponent_id"] == challenger_id)) and \
           challenge["date"] == date:
            return False, "Esiste già una sfida tra questi atleti per questa data"
    
    # Create new challenge
    new_id = max(challenge["id"] for challenge in st.session_state.challenges) + 1 if st.session_state.challenges else 1
    new_challenge = {
        "id": new_id,
        "challenger_id": challenger_id,
        "opponent_id": opponent_id,
        "date": date,
        "specialty_id": specialty_id,
        "winner_id": None
    }
    
    st.session_state.challenges.append(new_challenge)
    return True, "Sfida creata con successo"

def record_challenge_result(challenge_id, winner_id):
    """Record the result of a challenge."""
    # Find the challenge
    for i, challenge in enumerate(st.session_state.challenges):
        if challenge["id"] == challenge_id:
            # Check if result is already recorded
            if challenge["winner_id"] is not None:
                return False, "Il risultato è già stato registrato"
            
            # Check if winner is one of the athletes
            if winner_id != challenge["challenger_id"] and winner_id != challenge["opponent_id"]:
                return False, "Il vincitore deve essere uno degli atleti partecipanti alla sfida"
            
            # Check if the challenge date is today or in the past
            challenge_date = datetime.date.fromisoformat(challenge["date"])
            if challenge_date > datetime.date.today():
                return False, "Non è possibile registrare il risultato di una sfida futura"
            
            # Update challenge with winner
            st.session_state.challenges[i]["winner_id"] = winner_id
            
            # Increase winner's level
            for j, athlete in enumerate(st.session_state.athletes):
                if athlete["id"] == winner_id:
                    st.session_state.athletes[j]["level"] += 1
                    break
            
            return True, "Risultato registrato con successo"
    
    return False, "Sfida non trovata"

def close_registration(tournament_id=None):
    """Close tournament registration."""
    if tournament_id is None:
        # Retrocompatibilità
        st.session_state.tournament["registration_open"] = False
        # Aggiorna anche nell'array dei tornei
        for i, tournament in enumerate(st.session_state.tournaments):
            if tournament["id"] == st.session_state.tournament["id"]:
                st.session_state.tournaments[i]["registration_open"] = False
                break
        return True, "Registrazione chiusa con successo"
    else:
        # Cerca il torneo specifico
        for i, tournament in enumerate(st.session_state.tournaments):
            if tournament["id"] == tournament_id:
                st.session_state.tournaments[i]["registration_open"] = False
                # Aggiorna anche il torneo corrente se è quello selezionato
                if st.session_state.tournament["id"] == tournament_id:
                    st.session_state.tournament["registration_open"] = False
                return True, f"Registrazione per {tournament['name']} chiusa con successo"
        return False, "Torneo non trovato"

def update_tournament_settings(tournament_id, name=None, start_date=None, end_date=None, registration_open=None):
    """Update tournament settings."""
    # Cerca il torneo
    tournament_index = None
    for i, tournament in enumerate(st.session_state.tournaments):
        if tournament["id"] == tournament_id:
            tournament_index = i
            break
    
    if tournament_index is None:
        return False, "Torneo non trovato"
    
    # Aggiorna i campi specificati
    if name:
        st.session_state.tournaments[tournament_index]["name"] = name
    if start_date:
        st.session_state.tournaments[tournament_index]["start_date"] = start_date
    if end_date:
        st.session_state.tournaments[tournament_index]["end_date"] = end_date
    if registration_open is not None:
        st.session_state.tournaments[tournament_index]["registration_open"] = registration_open
    
    # Aggiorna anche il torneo corrente se è quello modificato
    if st.session_state.tournament["id"] == tournament_id:
        st.session_state.tournament = st.session_state.tournaments[tournament_index]
    
    return True, "Impostazioni aggiornate con successo"

def create_tournament(name, start_date, end_date, registration_open=True):
    """Create a new tournament."""
    # Genera un nuovo ID
    new_id = max(t["id"] for t in st.session_state.tournaments) + 1 if st.session_state.tournaments else 1
    
    # Crea il nuovo torneo
    new_tournament = {
        "id": new_id,
        "name": name,
        "registration_open": registration_open,
        "start_date": start_date,
        "end_date": end_date
    }
    
    # Aggiungi il torneo
    st.session_state.tournaments.append(new_tournament)
    
    return True, f"Torneo {name} creato con successo"

def delete_tournament(tournament_id):
    """Delete a tournament."""
    # Trova il torneo
    tournament_index = None
    for i, tournament in enumerate(st.session_state.tournaments):
        if tournament["id"] == tournament_id:
            tournament_index = i
            break
    
    if tournament_index is None:
        return False, "Torneo non trovato"
    
    # Rimuovi il torneo dalle iscrizioni degli atleti
    for i, athlete in enumerate(st.session_state.athletes):
        if "tournaments" in athlete and tournament_id in athlete["tournaments"]:
            st.session_state.athletes[i]["tournaments"].remove(tournament_id)
    
    # Rimuovi tutte le sfide associate al torneo
    # Nota: devi aggiungere il campo tournament_id alle sfide per supportare questa funzionalità
    
    # Rimuovi il torneo
    st.session_state.tournaments.pop(tournament_index)
    
    # Se era il torneo corrente, imposta un altro torneo come corrente
    if st.session_state.tournament["id"] == tournament_id:
        if st.session_state.tournaments:
            st.session_state.tournament = st.session_state.tournaments[0]
        else:
            # Crea un torneo predefinito se non ce ne sono altri
            default_tournament = {
                "id": 1,
                "name": "Torneo Chanbara 2025",
                "registration_open": True,
                "start_date": "2025-06-01",
                "end_date": "2025-06-30"
            }
            st.session_state.tournaments.append(default_tournament)
            st.session_state.tournament = default_tournament
    
    return True, "Torneo eliminato con successo"

def get_rankings():
    """Get rankings sorted by level."""
    rankings = []
    
    for athlete in st.session_state.athletes:
        # Count victories
        victories = sum(1 for challenge in st.session_state.challenges 
                        if challenge["winner_id"] == athlete["id"])
        
        # Count total challenges
        total_challenges = sum(1 for challenge in st.session_state.challenges 
                              if (challenge["challenger_id"] == athlete["id"] or 
                                  challenge["opponent_id"] == athlete["id"]) and
                                 challenge["winner_id"] is not None)
        
        rankings.append({
            "id": athlete["id"],
            "name": athlete["name"],
            "level": athlete["level"],
            "victories": victories,
            "total_challenges": total_challenges,
            "profile_img": athlete["profile_img"]
        })
    
    # Sort by level (descending), then by victories (descending), then by name
    rankings.sort(key=lambda x: (-x["level"], -x["victories"], x["name"]))
    
    return rankings

def get_athlete_challenges(athlete_id):
    """Get upcoming and past challenges for an athlete."""
    today = datetime.date.today()
    upcoming_challenges = []
    past_challenges = []
    
    for challenge in st.session_state.challenges:
        if challenge["challenger_id"] == athlete_id or challenge["opponent_id"] == athlete_id:
            challenge_date = datetime.date.fromisoformat(challenge["date"])
            
            # Get challenger and opponent
            challenger = get_athlete_by_id(challenge["challenger_id"])
            opponent = get_athlete_by_id(challenge["opponent_id"])
            specialty = get_specialty_by_id(challenge["specialty_id"])
            winner = get_athlete_by_id(challenge["winner_id"]) if challenge["winner_id"] else None
            
            # Create a challenge object with all needed info
            challenge_obj = {
                "id": challenge["id"],
                "date": challenge["date"],
                "challenger": challenger["name"] if challenger else "Sconosciuto",
                "opponent": opponent["name"] if opponent else "Sconosciuto",
                "specialty": specialty["name"] if specialty else "Sconosciuta",
                "winner": winner["name"] if winner else None
            }
            
            if challenge_date >= today:
                upcoming_challenges.append(challenge_obj)
            else:
                past_challenges.append(challenge_obj)
    
    # Sort by date
    upcoming_challenges.sort(key=lambda x: x["date"])
    past_challenges.sort(key=lambda x: x["date"], reverse=True)
    
    return upcoming_challenges, past_challenges

def get_possible_opponents(athlete_id):
    """Get possible opponents for an athlete."""
    athlete = get_athlete_by_id(athlete_id)
    if not athlete:
        return []
    
    # Get athletes with equal or higher level
    opponents = [a for a in st.session_state.athletes 
                if a["id"] != athlete_id and a["level"] >= athlete["level"]]
    
    # Sort by level and name
    opponents.sort(key=lambda x: (x["level"], x["name"]))
    
    return opponents

def get_admin_stats():
    """Get statistics for admin dashboard."""
    today = datetime.date.today().isoformat()
    
    total_athletes = len(st.session_state.athletes)
    total_challenges = len(st.session_state.challenges)
    completed_challenges = sum(1 for c in st.session_state.challenges if c["winner_id"] is not None)
    future_challenges = sum(1 for c in st.session_state.challenges if c["date"] > today)
    today_challenges = sum(1 for c in st.session_state.challenges if c["date"] == today)
    
    return {
        "total_athletes": total_athletes,
        "total_challenges": total_challenges,
        "completed_challenges": completed_challenges,
        "future_challenges": future_challenges,
        "today_challenges": today_challenges,
        "registration_open": st.session_state.tournament["registration_open"]
    }

# Page functions
def login():
    """Render the login page."""
    st.title("Accedi al Torneo Chanbara")
    
    tab1, tab2, tab3 = st.tabs(["Atleta", "Admin", "Registrazione"])
    
    with tab1:
        st.subheader("Accesso Atleti")
        email = st.text_input("Email", key="athlete_email")
        password = st.text_input("Password", type="password", key="athlete_password")
        
        if st.button("Accedi come Atleta"):
            if authenticate(email, password):
                st.success("Login effettuato con successo!")
                st.rerun()
            else:
                st.error("Credenziali non valide")
    
    with tab2:
        st.subheader("Accesso Admin")
        admin_email = st.text_input("Email", key="admin_email")
        admin_password = st.text_input("Password", type="password", key="admin_password")
        
        if st.button("Accedi come Admin"):
            if authenticate(admin_email, admin_password, is_admin=True):
                st.success("Login admin effettuato con successo!")
                st.rerun()
            else:
                st.error("Credenziali admin non valide")
        
        st.info("Per demo: Email = admin@example.com, Password = admin123")
    
    with tab3:
        if st.session_state.tournament["registration_open"]:
            st.subheader("Registrazione Nuovo Atleta")
            reg_name = st.text_input("Nome Completo")
            reg_nickname = st.text_input("Soprannome (opzionale)", help="Il soprannome sarà visualizzato in evidenza nel tuo profilo")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_password_confirm = st.text_input("Conferma Password", type="password")
            
            # Opzione per caricare foto profilo
            st.write("Foto profilo (opzionale)")
            uploaded_file = st.file_uploader("Scegli un'immagine", type=["jpg", "jpeg", "png"])
            
            if st.button("Registrati"):
                if not reg_name or not reg_email or not reg_password:
                    st.error("I campi Nome, Email e Password sono obbligatori")
                elif reg_password != reg_password_confirm:
                    st.error("Le password non coincidono")
                else:
                    # Utilizza il soprannome se fornito
                    nickname = reg_nickname if reg_nickname else None
                    
                    # Registra l'atleta
                    success, message = register_athlete(reg_name, reg_email, reg_password, nickname)
                    
                    if success:
                        # Se è stata caricata un'immagine, aggiorna la foto profilo
                        if uploaded_file is not None:
                            # Converti l'immagine in base64 per salvarla
                            import base64
                            bytes_data = uploaded_file.getvalue()
                            encoded_img = base64.b64encode(bytes_data).decode()
                            image_src = f"data:image/{uploaded_file.type.split('/')[-1]};base64,{encoded_img}"
                            
                            # Aggiorna l'immagine profilo dell'atleta appena registrato
                            for athlete in st.session_state.athletes:
                                if athlete["email"] == reg_email:
                                    athlete["profile_img"] = image_src
                                    break
                        
                        st.success(message)
                        # Auto login after registration
                        authenticate(reg_email, reg_password)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.error("Le registrazioni sono chiuse")

def profile_page():
    """Render the athlete profile page."""
    if not st.session_state.user:
        st.session_state.page = "login"
        st.rerun()
        return
    
    athlete = st.session_state.user
    
    # Profile header
    st.title(f"Ciao, {athlete.get('nickname', athlete['name'].split()[0])}!")
    
    # Layout for profile page
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Contenitore per la card del profilo
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        
        # Profile image
        st.image(athlete["profile_img"], width=150)
        
        # Mostro il soprannome in evidenza e il nome completo sotto in piccolo
        st.markdown(f'<div class="nickname">{athlete.get("nickname", athlete["name"].split()[0])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fullname">{athlete["name"]}</div>', unsafe_allow_html=True)
        
        # Informazioni atleta con stile migliorato
        st.markdown(f'<div class="dark-mode-text"><strong>Livello:</strong> {athlete["level"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="dark-mode-text"><strong>Email:</strong> {athlete["email"]}</div>', unsafe_allow_html=True)
        
        # Chiusura del contenitore
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Aggiungi bottone per modificare foto profilo
        if st.button("Modifica Profilo"):
            st.session_state.page = "edit_profile"
            st.rerun()
    
    with col2:
        # Navigation buttons in styled container
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="dark-mode-text">Cosa vuoi fare?</h3>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("⚔️ Sfida", key="sfida_btn"):
                st.session_state.page = "challenge"
                st.rerun()
        
        with col_b:
            if st.button("📊 Ranking", key="ranking_btn"):
                st.session_state.page = "ranking" 
                st.rerun()
        
        with col_c:
            if st.button("📜 Storico", key="storico_btn"):
                st.session_state.page = "history"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display upcoming challenges in a styled container
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="dark-mode-text">Le tue prossime sfide</h3>', unsafe_allow_html=True)
    upcoming_challenges, _ = get_athlete_challenges(athlete["id"])
    
    if upcoming_challenges:
        for challenge in upcoming_challenges:
            st.markdown(f"""
            <div class="dark-mode-text">
                <strong>Data:</strong> {challenge['date']}<br>
                <strong>Sfida:</strong> {challenge['challenger']} vs {challenge['opponent']}<br>
                <strong>Specialità:</strong> {challenge['specialty']}
            </div>
            """, unsafe_allow_html=True)
            st.divider()
    else:
        st.info("Non hai sfide programmate")
    
    st.markdown('</div>', unsafe_allow_html=True)

def edit_profile_page():
    """Render the profile edit page."""
    if not st.session_state.user:
        st.session_state.page = "login"
        st.rerun()
        return
    
    athlete = st.session_state.user
    
    st.title("Modifica Profilo")
    
    # Back button
    if st.button("← Torna al Profilo"):
        st.session_state.page = "profile"
        st.rerun()
    
    # Form per modificare il soprannome
    st.subheader("Modifica Soprannome")
    new_nickname = st.text_input("Soprannome", value=athlete.get("nickname", ""))
    
    # Form per caricare una nuova foto profilo
    st.subheader("Carica Nuova Foto Profilo")
    uploaded_file = st.file_uploader("Scegli un'immagine", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Preview dell'immagine caricata
        st.image(uploaded_file, width=150, caption="Anteprima")
    
    # Salva modifiche
    if st.button("Salva Modifiche"):
        # Aggiorna il soprannome
        if new_nickname:
            # Aggiorna in session_state.user
            st.session_state.user["nickname"] = new_nickname
            
            # Aggiorna anche in athletes
            for i, a in enumerate(st.session_state.athletes):
                if a["id"] == athlete["id"]:
                    st.session_state.athletes[i]["nickname"] = new_nickname
                    break
        
        # Aggiorna la foto profilo
        if uploaded_file is not None:
            import base64
            bytes_data = uploaded_file.getvalue()
            encoded_img = base64.b64encode(bytes_data).decode()
            image_src = f"data:image/{uploaded_file.type.split('/')[-1]};base64,{encoded_img}"
            
            # Aggiorna in session_state.user
            st.session_state.user["profile_img"] = image_src
            
            # Aggiorna anche in athletes
            for i, a in enumerate(st.session_state.athletes):
                if a["id"] == athlete["id"]:
                    st.session_state.athletes[i]["profile_img"] = image_src
                    break
        
        st.success("Profilo aggiornato con successo!")
        st.session_state.page = "profile"
        st.rerun()

def challenge_page():
    """Render the challenge creation page."""
    if not st.session_state.user:
        st.session_state.page = "login"
        st.rerun()
        return
    
    athlete = st.session_state.user
    
    st.title("Proponi una Sfida")
    
    # Back button
    if st.button("← Torna al Profilo"):
        st.session_state.page = "profile"
        st.experimental_rerun()
    
    # Challenge form
    st.subheader("Crea una nuova sfida")
    
    if not st.session_state.tournament["registration_open"]:
        opponents = get_possible_opponents(athlete["id"])
        
        if opponents:
            # Create a selectbox with opponents
            opponent_options = [(o["id"], f"{o['name']} (Liv. {o['level']})") for o in opponents]
            opponent_ids = [id for id, _ in opponent_options]
            opponent_names = [name for _, name in opponent_options]
            
            selected_opponent_index = st.selectbox(
                "Sfida un atleta",
                options=range(len(opponent_names)),
                format_func=lambda i: opponent_names[i]
            )
            selected_opponent_id = opponent_ids[selected_opponent_index]
            
            # Create a selectbox with specialties
            specialty_options = [(s["id"], s["name"]) for s in st.session_state.specialties]
            specialty_ids = [id for id, _ in specialty_options]
            specialty_names = [name for _, name in specialty_options]
            
            selected_specialty_index = st.selectbox(
                "Specialità",
                options=range(len(specialty_names)),
                format_func=lambda i: specialty_names[i]
            )
            selected_specialty_id = specialty_ids[selected_specialty_index]
            
            # Set minimum date to tomorrow
            min_date = datetime.date.today() + datetime.timedelta(days=1)
            challenge_date = st.date_input(
                "Data della sfida",
                min_value=min_date,
                value=min_date
            )
            
            if st.button("Proponi Sfida"):
                success, message = create_challenge(
                    athlete["id"],
                    selected_opponent_id,
                    challenge_date.isoformat(),
                    selected_specialty_id
                )
                
                if success:
                    st.success(message)
                    st.session_state.page = "profile"
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Non ci sono avversari disponibili di livello pari o superiore")
    else:
        st.warning("Le sfide possono essere create solo dopo la chiusura delle registrazioni")
        
        # Admin info for demo purposes
        st.info("Per continuare con la demo, accedi come admin (admin@example.com / admin123) e chiudi le registrazioni dal pannello di amministrazione.")

def ranking_page():
    """Render the rankings page."""
    if not st.session_state.user:
        st.session_state.page = "login"
        st.rerun()
        return
    
    st.title("Classifica del Torneo")
    
    # Back button
    if st.button("← Torna al Profilo"):
        st.session_state.page = "profile"
        st.experimental_rerun()
    
    # Display rankings
    rankings = get_rankings()
    
    # Create a DataFrame for the rankings
    rankings_df = pd.DataFrame([{
        "Posizione": i+1,
        "Nome": r["name"],
        "Livello": r["level"],
        "Vittorie": r["victories"],
        "Sfide Totali": r["total_challenges"]
    } for i, r in enumerate(rankings)])
    
    st.dataframe(rankings_df, use_container_width=True, hide_index=True)
    
    # Display top 3 with more details
    st.subheader("Top 3 Atleti")
    
    top_cols = st.columns(3)
    for i, athlete in enumerate(rankings[:3]):
        if i < 3:  # Ensure we have at least 3 athletes
            with top_cols[i]:
                st.image(athlete["profile_img"], width=100)
                st.subheader(f"{i+1}. {athlete['name']}")
                st.write(f"**Livello:** {athlete['level']}")
                st.write(f"**Vittorie:** {athlete['victories']}")

def history_page():
    """Render the challenge history page."""
    if not st.session_state.user:
        st.session_state.page = "login"
        st.experimental_rerun()
        return
    
    athlete = st.session_state.user
    
    st.title("Storico Sfide")
    
    # Back button
    if st.button("← Torna al Profilo"):
        st.session_state.page = "profile"
        st.experimental_rerun()
    
    # Get all challenges for this athlete
    _, past_challenges = get_athlete_challenges(athlete["id"])
    
    if past_challenges:
        for challenge in past_challenges:
            with st.container():
                st.markdown(f"""
                **Data:** {challenge['date']}  
                **Sfida:** {challenge['challenger']} vs {challenge['opponent']}  
                **Specialità:** {challenge['specialty']}  
                **Vincitore:** {challenge['winner'] if challenge['winner'] else 'Non registrato'}
                """)
                st.divider()
    else:
        st.info("Non hai sfide passate")

def admin_page():
    """Render the admin dashboard."""
    if not st.session_state.user or not st.session_state.user.get("is_admin", False):
        st.session_state.page = "login"
        st.rerun()
        return
    
    st.title("Dashboard Amministrazione")
    
    # Admin tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Atleti", "Sfide", "Tornei", "Impostazioni"])
    
    with tab1:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.header("Panoramica Torneo")
        
        # Selezione torneo corrente
        tournament_options = [(t["id"], t["name"]) for t in st.session_state.tournaments]
        tournament_ids, tournament_names = zip(*tournament_options)
        
        current_tournament_index = tournament_ids.index(st.session_state.tournament["id"]) if st.session_state.tournament["id"] in tournament_ids else 0
        
        selected_tournament_index = st.selectbox(
            "Seleziona Torneo",
            options=range(len(tournament_names)),
            format_func=lambda i: tournament_names[i],
            index=current_tournament_index
        )
        selected_tournament_id = tournament_ids[selected_tournament_index]
        
        # Se il torneo selezionato è diverso dal corrente, cambia il torneo corrente
        if selected_tournament_id != st.session_state.tournament["id"]:
            for t in st.session_state.tournaments:
                if t["id"] == selected_tournament_id:
                    st.session_state.tournament = t
                    st.rerun()
        
        # Stats
        stats = get_admin_stats()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Atleti Totali", stats["total_athletes"])
        
        with col2:
            st.metric("Sfide Totali", stats["total_challenges"])
        
        with col3:
            st.metric("Sfide Completate", stats["completed_challenges"])
        
        # Registration status
        st.subheader("Stato Registrazioni")
        if stats["registration_open"]:
            st.warning(f"Le registrazioni per {st.session_state.tournament['name']} sono aperte")
            if st.button("Chiudi Registrazioni"):
                success, message = close_registration(st.session_state.tournament["id"])
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.success(f"Le registrazioni per {st.session_state.tournament['name']} sono chiuse")
            if st.button("Riapri Registrazioni"):
                update_tournament_settings(
                    st.session_state.tournament["id"],
                    registration_open=True
                )
                st.success(f"Registrazioni per {st.session_state.tournament['name']} riaperte")
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.header("Gestione Atleti")
        
        # Filter for tournament
        tournament_filter = st.selectbox(
            "Filtra per Torneo", 
            options=["Tutti"] + [t["name"] for t in st.session_state.tournaments],
            key="athlete_tournament_filter"
        )
        
        filtered_athletes = st.session_state.athletes
        
        if tournament_filter != "Tutti":
            # Trova l'ID del torneo
            tournament_id = None
            for t in st.session_state.tournaments:
                if t["name"] == tournament_filter:
                    tournament_id = t["id"]
                    break
            
            if tournament_id:
                filtered_athletes = [a for a in st.session_state.athletes 
                                    if "tournaments" in a and tournament_id in a["tournaments"]]
        
        # Display athletes with more details
        if filtered_athletes:
            athletes_data = []
            
            for athlete in filtered_athletes:
                # Get tournaments names
                tournament_names = []
                if "tournaments" in athlete:
                    for t_id in athlete["tournaments"]:
                        for t in st.session_state.tournaments:
                            if t["id"] == t_id:
                                tournament_names.append(t["name"])
                                break
                
                athletes_data.append({
                    "ID": athlete["id"],
                    "Nome": athlete["name"],
                    "Soprannome": athlete.get("nickname", ""),
                    "Email": athlete["email"],
                    "Livello": athlete["level"],
                    "Tornei": ", ".join(tournament_names)
                })
            
            athletes_df = pd.DataFrame(athletes_data)
            st.dataframe(athletes_df, use_container_width=True, hide_index=True)
            
            # Sezione per eliminare un atleta
            st.subheader("Elimina Atleta")
            
            athlete_to_delete = st.selectbox(
                "Seleziona atleta da eliminare",
                options=[f"{a['id']} - {a['name']}" for a in filtered_athletes],
                key="delete_athlete_select"
            )
            
            if st.button("Elimina", key="delete_athlete_btn"):
                athlete_id = int(athlete_to_delete.split(" - ")[0])
                success, message = delete_athlete(athlete_id)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            
            # Sezione per modificare un atleta
            st.subheader("Modifica Atleta")
            
            athlete_to_edit = st.selectbox(
                "Seleziona atleta da modificare",
                options=[f"{a['id']} - {a['name']}" for a in filtered_athletes],
                key="edit_athlete_select"
            )
            
            athlete_id = int(athlete_to_edit.split(" - ")[0])
            athlete = get_athlete_by_id(athlete_id)
            
            if athlete:
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Nome", value=athlete["name"])
                    new_nickname = st.text_input("Soprannome", value=athlete.get("nickname", ""))
                
                with col2:
                    new_email = st.text_input("Email", value=athlete["email"])
                    new_level = st.number_input("Livello", min_value=1, max_value=10, value=athlete["level"])
                
                # Selezione tornei
                st.subheader("Iscrizione ai Tornei")
                tournament_enrollments = []
                
                for tournament in st.session_state.tournaments:
                    is_enrolled = tournament["id"] in athlete.get("tournaments", [])
                    enrollment = st.checkbox(
                        f"{tournament['name']}", 
                        value=is_enrolled,
                        key=f"tournament_{tournament['id']}_athlete_{athlete_id}"
                    )
                    tournament_enrollments.append((tournament["id"], enrollment))
                
                if st.button("Aggiorna Atleta", key="update_athlete_btn"):
                    # Crea dizionario con i dati aggiornati
                    updated_data = {
                        "name": new_name,
                        "nickname": new_nickname,
                        "email": new_email,
                        "level": new_level
                    }
                    
                    # Aggiorna iscrizioni ai tornei
                    updated_enrollments = []
                    for tournament_id, is_enrolled in tournament_enrollments:
                        if is_enrolled:
                            updated_enrollments.append(tournament_id)
                    
                    updated_data["tournaments"] = updated_enrollments
                    
                    success, message = modify_athlete(athlete_id, updated_data)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.info("Nessun atleta trovato con i filtri selezionati")
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.header("Gestione Sfide")
        
        # Filter
        filter_option = st.selectbox(
            "Filtra per",
            options=["Tutte", "In attesa", "Completate"]
        )
        
        # Apply filter
        if filter_option == "In attesa":
            filtered_challenges = [c for c in st.session_state.challenges if c["winner_id"] is None]
        elif filter_option == "Completate":
            filtered_challenges = [c for c in st.session_state.challenges if c["winner_id"] is not None]
        else:
            filtered_challenges = st.session_state.challenges.copy()
        
        # Create a DataFrame for challenges
        if filtered_challenges:
            challenges_data = []
            
            for challenge in filtered_challenges:
                challenger = get_athlete_by_id(challenge["challenger_id"])
                opponent = get_athlete_by_id(challenge["opponent_id"])
                specialty = get_specialty_by_id(challenge["specialty_id"])
                winner = get_athlete_by_id(challenge["winner_id"]) if challenge["winner_id"] else None
                
                if challenger and opponent and specialty:
                    challenges_data.append({
                        "ID": challenge["id"],
                        "Data": challenge["date"],
                        "Sfidante": challenger["name"],
                        "Sfidato": opponent["name"],
                        "Specialità": specialty["name"],
                        "Vincitore": winner["name"] if winner else "Non registrato"
                    })
            
            challenges_df = pd.DataFrame(challenges_data)
            st.dataframe(challenges_df, use_container_width=True, hide_index=True)
            
            # Register result for a challenge
            st.subheader("Registra Risultato")
            
            pending_challenges = [c for c in filtered_challenges if c["winner_id"] is None]
            if pending_challenges:
                challenge_options = []
                
                for c in pending_challenges:
                    challenger = get_athlete_by_id(c["challenger_id"])
                    opponent = get_athlete_by_id(c["opponent_id"])
                    
                    if challenger and opponent:
                        challenge_options.append((
                            c["id"], 
                            f"{challenger['name']} vs {opponent['name']} ({c['date']})"
                        ))
                
                if challenge_options:
                    challenge_ids, challenge_names = zip(*challenge_options)
                    
                    selected_challenge_index = st.selectbox(
                        "Seleziona sfida",
                        options=range(len(challenge_names)),
                        format_func=lambda i: challenge_names[i]
                    )
                    selected_challenge_id = challenge_ids[selected_challenge_index]
                    selected_challenge = next(c for c in pending_challenges if c["id"] == selected_challenge_id)
                    
                    challenger = get_athlete_by_id(selected_challenge["challenger_id"])
                    opponent = get_athlete_by_id(selected_challenge["opponent_id"])
                    
                    if challenger and opponent:
                        winner_options = [(challenger["id"], challenger["name"]), (opponent["id"], opponent["name"])]
                        winner_ids, winner_names = zip(*winner_options)
                        
                        selected_winner_index = st.radio(
                            "Seleziona il vincitore",
                            options=range(len(winner_names)),
                            format_func=lambda i: winner_names[i]
                        )
                        selected_winner_id = winner_ids[selected_winner_index]
                        
                        if st.button("Registra Risultato"):
                            success, message = record_challenge_result(selected_challenge_id, selected_winner_id)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
            else:
                st.info("Nessuna sfida in attesa di risultato")
        else:
            st.info("Nessuna sfida trovata con i filtri selezionati")
    
    with tab4:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.header("Gestione Tornei")
        
        # Display existing tournaments
        tournaments_data = []
        
        for t in st.session_state.tournaments:
            # Conta atleti iscritti
            enrolled_athletes = sum(1 for a in st.session_state.athletes 
                                  if "tournaments" in a and t["id"] in a["tournaments"])
            
            tournaments_data.append({
                "ID": t["id"],
                "Nome": t["name"],
                "Data Inizio": t["start_date"],
                "Data Fine": t["end_date"],
                "Iscrizioni": "Aperte" if t["registration_open"] else "Chiuse",
                "Atleti Iscritti": enrolled_athletes
            })
        
        tournaments_df = pd.DataFrame(tournaments_data)
        st.dataframe(tournaments_df, use_container_width=True, hide_index=True)
        
        # Create new tournament
        st.subheader("Crea Nuovo Torneo")
        
        new_tournament_name = st.text_input("Nome Torneo", key="new_tournament_name")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_start_date = st.date_input("Data Inizio", key="new_start_date")
        
        with col2:
            new_end_date = st.date_input("Data Fine", key="new_end_date")
        
        reg_open = st.checkbox("Iscrizioni Aperte", value=True, key="new_tournament_reg_open")
        
        if st.button("Crea Torneo", key="create_tournament_btn"):
            if not new_tournament_name:
                st.error("Il nome del torneo è obbligatorio")
            elif new_end_date <= new_start_date:
                st.error("La data di fine deve essere successiva alla data di inizio")
            else:
                success, message = create_tournament(
                    new_tournament_name,
                    new_start_date.isoformat(),
                    new_end_date.isoformat(),
                    reg_open
                )
                
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        # Edit tournament
        st.subheader("Modifica Torneo")
        
        edit_tournament = st.selectbox(
            "Seleziona torneo da modificare",
            options=[f"{t['id']} - {t['name']}" for t in st.session_state.tournaments],
            key="edit_tournament_select"
        )
        
        tournament_id = int(edit_tournament.split(" - ")[0])
        tournament = None
        
        for t in st.session_state.tournaments:
            if t["id"] == tournament_id:
                tournament = t
                break
        
        if tournament:
            edit_tournament_name = st.text_input("Nome Torneo", value=tournament["name"], key="edit_tournament_name")
            
            col1, col2 = st.columns(2)
            
            with col1:
                edit_start_date = st.date_input("Data Inizio", value=datetime.date.fromisoformat(tournament["start_date"]), key="edit_start_date")
            
            with col2:
                edit_end_date = st.date_input("Data Fine", value=datetime.date.fromisoformat(tournament["end_date"]), key="edit_end_date")
            
            edit_reg_open = st.checkbox("Iscrizioni Aperte", value=tournament["registration_open"], key="edit_tournament_reg_open")
            
            if st.button("Aggiorna Torneo", key="update_tournament_btn"):
                if not edit_tournament_name:
                    st.error("Il nome del torneo è obbligatorio")
                elif edit_end_date <= edit_start_date:
                    st.error("La data di fine deve essere successiva alla data di inizio")
                else:
                    success, message = update_tournament_settings(
                        tournament_id,
                        edit_tournament_name,
                        edit_start_date.isoformat(),
                        edit_end_date.isoformat(),
                        edit_reg_open
                    )
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        # Delete tournament
        st.subheader("Elimina Torneo")
        
        delete_tournament_select = st.selectbox(
            "Seleziona torneo da eliminare",
            options=[f"{t['id']} - {t['name']}" for t in st.session_state.tournaments],
            key="delete_tournament_select"
        )
        
        if st.button("Elimina Torneo", key="delete_tournament_btn"):
            tournament_id = int(delete_tournament_select.split(" - ")[0])
            
            # Confirm deletion
            confirm = st.checkbox(f"Conferma eliminazione del torneo {delete_tournament_select}", key="confirm_delete_tournament")
            
            if confirm:
                success, message = delete_tournament(tournament_id)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Per favore conferma l'eliminazione selezionando la casella di conferma")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab5:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.header("Impostazioni Torneo Corrente")
        
        # Tournament settings form
        tournament_name = st.text_input("Nome Torneo", value=st.session_state.tournament["name"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Data Inizio", value=datetime.date.fromisoformat(st.session_state.tournament["start_date"]))
        
        with col2:
            end_date = st.date_input("Data Fine", value=datetime.date.fromisoformat(st.session_state.tournament["end_date"]))
        
        if st.button("Salva Impostazioni"):
            success, message = update_tournament_settings(
                tournament_name,
                start_date.isoformat(),
                end_date.isoformat()
            )
            
            if success:
                st.success(message)
                st.experimental_rerun()
            else:
                st.error(message)

# Main function
def main():
    """Main function to render the Chanbara tournament application."""
    # Header
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px solid #ddd;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.image("https://ui-avatars.com/api/?name=Chanbara&size=50&background=random", width=50)
    
    with col2:
        st.title("Torneo Chanbara 2025")
    
    with col3:
        if st.session_state.user:
            if st.button("Logout"):
                st.session_state.user = None
                st.session_state.page = "login"
                st.experimental_rerun()
    
    # Routing based on session state
    if st.session_state.page == "login" or not st.session_state.user:
        login()
    elif st.session_state.page == "profile":
        profile_page()
    elif st.session_state.page == "edit_profile":
        edit_profile_page()
    elif st.session_state.page == "challenge":
        challenge_page()
    elif st.session_state.page == "ranking":
        ranking_page()
    elif st.session_state.page == "history":
        history_page()
    elif st.session_state.page == "admin":
        admin_page()

if __name__ == "__main__":
    main()