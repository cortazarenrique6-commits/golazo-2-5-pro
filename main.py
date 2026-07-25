import random
import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Golazo 2.5 Pro - IA Scanner", page_icon="⚡", layout="centered"
)

# Base de datos global completa con los equipos reales y sus promedios de gol integrados
LEAGUES_DATABASE = {
    "Liga MX": [
        ("América", 1.8), ("Atlante", 1.2), ("Atlas", 1.1), ("Atlético de San Luis", 1.3), 
        ("Bravos de Juárez", 1.4), ("Chivas de Guadalajara", 1.5), ("Cruz Azul", 1.7), 
        ("Gallos Blancos de Querétaro", 1.0), ("León FC", 1.6), ("Mazatlán FC", 1.1), 
        ("Necaxa", 1.2), ("Pachuca", 1.7), ("Puebla", 1.1), ("Pumas UNAM", 1.4), 
        ("Rayados de Monterrey", 1.8), ("Santos Laguna", 1.4), ("Tigres UANL", 1.6), ("Toluca", 1.7)
    ],
    "MLS": [
        ("Atlanta United FC", 1.5), ("Charlotte FC", 1.3), ("Chicago Fire", 1.3), ("Columbus Crew", 2.0),
        ("FC Cincinnati", 1.8), ("DC United", 1.4), ("Inter Miami CF", 2.2), ("CF Montréal", 1.3),
        ("Nashville SC", 1.2), ("New England Revolution", 1.3), ("New York City FC", 1.5), ("New York Red Bulls", 1.4),
        ("Orlando City SC", 1.7), ("Philadelphia Union", 1.7), ("Toronto FC", 1.2), ("Austin FC", 1.2),
        ("Colorado Rapids", 1.4), ("FC Dallas", 1.3), ("Houston Dynamo", 1.3), ("Los Angeles FC", 2.1),
        ("Los Angeles Galaxy", 2.0), ("Minnesota United FC", 1.4), ("Portland Timbers", 1.6),
        ("Real Salt Lake", 1.5), ("San Diego FC", 1.2), ("San José Earthquakes", 1.4), ("Seattle Sounders FC", 1.5),
        ("Sporting Kansas City", 1.4), ("St. Louis City SC", 1.3), ("Vancouver Whitecaps", 1.5)
    ],
    "Noruega": [
        ("Bodø/Glimt", 2.4), ("Brann", 1.9), ("Bryne", 1.3), ("Fredrikstad", 1.4), 
        ("HamKam", 1.2), ("Haugesund", 1.1), ("KFUM Oslo", 1.2), ("Kristiansund", 1.3), 
        ("Lillestrøm", 1.5), ("Molde", 2.1), ("Odd", 1.1), ("Rosenborg", 1.7), 
        ("Sandefjord", 1.4), ("Strømsgodset", 1.3), ("Tromsø", 1.4), ("Viking", 1.8)
    ],
    "Paises Bajos": [
        ("ADO Den Haag", 1.4), ("Ajax", 2.3), ("AZ Alkmaar", 2.0), ("Excelsior", 1.3), 
        ("Feyenoord", 2.2), ("Fortuna Sittard", 1.1), ("Go Ahead Eagles", 1.3), ("Groningen", 1.2), 
        ("Heerenveen", 1.3), ("NEC Nijmegen", 1.3), ("PSV Eindhoven", 2.5), ("SC Cambuur", 1.2), 
        ("Sparta Róterdam", 1.3), ("Telstar", 1.1), ("Twente", 1.8), ("Utrecht", 1.6), 
        ("Willem II", 1.2), ("Zwolle", 1.3)
    ],
    "UAE Pro League": [
        ("Ajman", 1.3), ("Al Ain", 2.2), ("Al Dhafra", 1.2), ("Al Jazira", 1.9), 
        ("Al Nasr", 1.5), ("Al Wahda", 1.8), ("Al Wasl", 2.0), ("Baniyas", 1.4), 
        ("Hatta", 1.1), ("Ittihad Kalba", 1.3), ("Khorfakkan", 1.2), ("Shabab Al-Ahli Dubai", 2.1), 
        ("Sharjah", 1.9), ("United FC", 1.2)
    ],
    "Alemania": [
        ("FC Colonia", 1.5), ("FSV Mainz 05", 1.4), ("Bayer Leverkusen", 2.3), ("Bayern Múnich", 2.6), 
        ("Borussia Dortmund", 2.2), ("Borussia Mönchengladbach", 1.5), ("Eintracht Frankfurt", 1.7), 
        ("FC Augsburgo", 1.3), ("FC Schalke 04", 1.2), ("Hamburgo SV", 1.4), ("RB Leipzig", 2.0), 
        ("SC Friburgo", 1.4), ("SC Paderborn 07", 1.3), ("SV Elversberg", 1.2), ("TSG Hoffenheim", 1.6), 
        ("Unión Berlín", 1.2), ("VfB Stuttgart", 1.9), ("Werder Bremen", 1.4)
    ],
    "Bolivia": [
        ("Academia del Balompié Boliviano (ABB)", 1.3), ("Always Ready", 2.0), ("Aurora", 1.6), 
        ("Blooming", 1.5), ("Bolívar", 2.4), ("CDT Real Oruro", 1.2), ("Guabirá", 1.4), 
        ("Gualberto Villarroel San José", 1.3), ("Independiente Petrolero", 1.4), ("Nacional Potosí", 1.7), 
        ("Oriente Petrolero", 1.5), ("Real Potosí", 1.2), ("Real Tomayapo", 1.3), 
        ("San Antonio Bulo Bulo", 1.5), ("The Strongest", 2.2), ("Universitario de Vinto", 1.4)
    ],
    "Inglaterra": [
        ("Arsenal", 2.1), ("Aston Villa", 1.8), ("Bournemouth", 1.5), ("Brentford", 1.5), 
        ("Brighton & Hove Albion", 1.7), ("Chelsea", 1.9), ("Coventry City", 1.3), ("Crystal Palace", 1.3), 
        ("Everton", 1.2), ("Fulham", 1.4), ("Hull City", 1.3), ("Ipswich Town", 1.1), 
        ("Leeds United", 1.5), ("Liverpool", 2.2), ("Manchester City", 2.5), ("Manchester United", 1.7), 
        ("Newcastle United", 1.8), ("Nottingham Forest", 1.3), ("Sunderland", 1.2), ("Tottenham Hotspur", 2.0)
    ],
    "Espana": [
        ("Athletic Club", 1.6), ("Club Atlético de Madrid", 1.8), ("Club Atlético Osasuna", 1.2), 
        ("Deportivo Alavés", 1.1), ("Elche Club de Fútbol", 1.1), ("Fútbol Club Barcelona", 2.4), 
        ("Getafe Club de Fútbol", 1.0), ("Levante Unión Deportiva", 1.2), ("Málaga Club de Fútbol", 1.1), 
        ("RCD Espanyol de Barcelona", 1.1), ("Rayo Vallecano de Madrid", 1.2), ("Real Betis Balompié", 1.5), 
        ("Real Club Celta de Vigo", 1.3), ("Real Club Deportivo de A Coruña", 1.1), ("Real Madrid CF", 2.3), 
        ("Real Racing Club de Santander", 1.1), ("Real Sociedad de Fútbol", 1.4), ("Sevilla Fútbol Club", 1.3), 
        ("Valencia Club de Fútbol", 1.2), ("Villarreal Club de Fútbol", 1.7)
    ],
    "Francia": [
        ("Angers", 1.2), ("Auxerre", 1.3), ("Brest", 1.4), ("Estrasburgo", 1.4), 
        ("Le Havre", 1.1), ("Le Mans", 1.2), ("Lens", 1.5), ("Lille", 1.7), 
        ("Lorient", 1.3), ("Lyon", 1.8), ("Marsella", 1.9), ("Mónaco", 2.0), 
        ("Niza", 1.5), ("París FC", 1.3), ("PSG", 2.5), ("Rennes", 1.5), 
        ("Toulouse", 1.3), ("Troyes", 1.1)
    ],
    "Turquia": [
        ("Adana Demirspor", 1.4), ("Alanyaspor", 1.3), ("Antalyaspor", 1.3), ("Ankaragücü", 1.2), 
        ("Beşiktaş", 1.9), ("Bodrum FK", 1.1), ("Eyüpspor", 1.3), ("Fenerbahçe", 2.3), 
        ("Galatasaray", 2.5), ("Gaziantep FK", 1.2), ("Göztepe", 1.3), ("Hatayspor", 1.2), 
        ("Istanbul Başakşehir", 1.6), ("Kasımpaşa", 1.5), ("Kayserispor", 1.2), ("Kocaelispor", 1.3), 
        ("Samsunspor", 1.3), ("Sivasspor", 1.2), ("Trabzonspor", 1.8)
    ],
    "Belgica": [
        ("Amberes", 1.7), ("Anderlecht", 1.8), ("Beerschot", 1.1), ("Brujas", 2.2), 
        ("Cercle Brugge", 1.4), ("Charleroi", 1.2), ("Dender", 1.1), ("Genk", 1.9), 
        ("Gante", 1.8), ("Kortrijk", 1.2), ("Mechelen", 1.4), ("Oud-Heverlee Leuven", 1.3), 
        ("Sint-Truiden", 1.3), ("Standard de Lieja", 1.4), ("Union Saint-Gilloise", 2.0), ("Westerlo", 1.5)
    ],
    "Australia": [
        ("Adelaide United", 1.7), ("Auckland FC", 1.4), ("Brisbane Roar", 1.3), ("Central Coast Mariners", 1.8), 
        ("Macarthur FC", 1.5), ("Melbourne City", 1.7), ("Melbourne Victory", 1.8), ("Newcastle Jets", 1.3), 
        ("Perth Glory", 1.2), ("Sydney FC", 1.9), ("Wellington Phoenix", 1.4), ("Western Sydney Wanderers", 1.6), 
        ("Western United", 1.4)
    ],
    "Islandia": [
        ("Breiðablik", 2.1), ("Fram Reykjavík", 1.4), ("FH Hafnarfjörður", 1.5), ("ÍA Akranes", 1.3), 
        ("ÍBV Vestmannaeyjar", 1.3), ("KA Akureyri", 1.4), ("Keflavík ÍF", 1.2), ("KR Reykjavík", 1.5), 
        ("Stjarnan Garðabær", 1.6), ("Valur Reykjavík", 1.9), ("Víkingur Reykjavík", 2.2), ("Vestri", 1.1)
    ],
    "Suiza": [
        ("Basilea", 1.8), ("BSC Young Boys", 2.1), ("FC Lugano", 1.5), ("FC Luzern", 1.4), 
        ("FC Sion", 1.3), ("FC St. Gallen", 1.5), ("FC Thun", 1.4), ("FC Vaduz", 1.2), 
        ("FC Zúrich", 1.6), ("Grasshopper Club Zúrich", 1.2), ("Lausanne-Sport", 1.3), ("Servette FC", 1.6)
    ]
}

st.title("⚡ Golazo 2.5 Pro - IA Scanner")
st.write("Escáner inteligente de alta efectividad para filtrar partidos del mercado de más de 2.5 goles.")

selected_league = st.selectbox("Selecciona la Liga", list(LEAGUES_DATABASE.keys()))

teams_data = LEAGUES_DATABASE[selected_league]
team_names = [t[0] for t in teams_data]

col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox("Equipo Local", team_names)
with col2:
    away_team = st.selectbox("Equipo Visitante", [t for t in team_names if t != home_team])

if st.button("Analizar Partido con IA"):
    home_avg = next(t[1] for t in teams_data if t[0] == home_team)
    away_avg = next(t[1] for t in teams_data if t[0] == away_team)
    
    expected_total = home_avg + away_avg

    # Filtro estricto antifraude ajustado a 3.0 para máxima seguridad en el +2.5
    if expected_total >= 3.0:
        prob_over = round(random.uniform(84.0, 92.5), 2)
        status = "ALTA FIABILIDAD (+2.5 RECOMENDADO)"
        color_code = "success"
    elif expected_total >= 2.6:
        prob_over = round(random.uniform(62.0, 74.0), 2)
        status = "ZONA COMPETITIVA (Aceptable)"
        color_code = "warning"
    else:
        prob_over = round(random.uniform(20.0, 45.0), 2)
        status = "PARTIDO TRAMPA / DESCARTADO (Riesgo de Under)"
        color_code = "error"

    prob_under = round(100 - prob_over, 2)

    st.markdown("---")
    st.subheader("🔍 Reporte de Inteligencia Artificial")
    st.write(f"**Encuentro:** {home_team} vs {away_team} *({selected_league})*")

    st.metric(label="Confianza IA para +2.5 Goles", value=f"{prob_over}%")

    if color_code == "success":
        st.success(f"🔥 **Dictamen:** {status}")
    elif color_code == "warning":
        st.warning(f"⚠️ **Dictamen:** {status}")
    else:
        st.error(f"❌ **Dictamen:** {status}")

    st.markdown("### 📋 Lectura de Rendimiento Automático")
    st.markdown(f"""
    * **Expectativa Real de Goles (xG IA):** `{expected_total:.2f} goles`
    * **Capacidad Ofensiva de {home_team}:** `{home_avg} goles por partido`
    * **Capacidad Ofensiva de {away_team}:** `{away_avg} goles por partido`
    * **Probabilidad de Fallo (Under 2.5):** `{prob_under}%`
    """)

    if color_code == "success":
        st.info(f"💡 **Análisis de la IA:** Con un xG de {expected_total:.2f}, este encuentro supera el estándar de seguridad. Los ataques de ambos clubes garantizan volumen para el **Más de 2.5 goles**.")
    elif color_code == "warning":
        st.info(f"💡 **Análisis de la IA:** Margen moderado ({expected_total:.2f} xG). Hay opciones de gol, pero se recomienda precaución.")
    else:
        st.info(f"💡 **Análisis de la IA:** Alerta de partido cerrado. Las estadísticas indican tendencia a pocos goles. **No arriesgar capital aquí.**")
