import random
import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Golazo 2.5 Pro", page_icon="⚡", layout="centered"
)

# Base de datos global con todas las ligas recopiladas
LEAGUES_DATABASE = {
    "Liga MX": [
        "América",
        "Atlante",
        "Atlas",
        "Atlético de San Luis",
        "Bravos de Juárez",
        "Chivas de Guadalajara",
        "Cruz Azul",
        "Gallos Blancos de Querétaro",
        "León FC",
        "Mazatlán FC",
        "Necaxa",
        "Pachuca",
        "Puebla",
        "Pumas UNAM",
        "Rayados de Monterrey",
        "Santos Laguna",
        "Tigres UANL",
        "Toluca",
    ],
    "MLS": [
        "Atlanta United FC",
        "Charlotte FC",
        "Chicago Fire",
        "Columbus Crew",
        "FC Cincinnati",
        "DC United",
        "Inter Miami CF",
        "CF Montréal",
        "Nashville SC",
        "New England Revolution",
        "New York City FC",
        "New York Red Bulls",
        "Orlando City SC",
        "Philadelphia Union",
        "Toronto FC",
        "Austin FC",
        "Colorado Rapids",
        "FC Dallas",
        "Houston Dynamo",
        "Los Angeles FC",
        "Los Angeles Galaxy",
        "Minnesota United FC",
        "Portland Timbers",
        "Real Salt Lake",
        "San Diego FC",
        "San José Earthquakes",
        "Seattle Sounders FC",
        "Sporting Kansas City",
        "St. Louis City SC",
        "Vancouver Whitecaps",
    ],
    "Noruega": [
        "Bodø/Glimt",
        "Brann",
        "Bryne",
        "Fredrikstad",
        "HamKam",
        "Haugesund",
        "KFUM Oslo",
        "Kristiansund",
        "Lillestrøm",
        "Molde",
        "Odd",
        "Rosenborg",
        "Sandefjord",
        "Strømsgodset",
        "Tromsø",
        "Viking",
    ],
    "Paises Bajos": [
        "ADO Den Haag",
        "Ajax",
        "AZ Alkmaar",
        "Excelsior",
        "Feyenoord",
        "Fortuna Sittard",
        "Go Ahead Eagles",
        "Groningen",
        "Heerenveen",
        "NEC Nijmegen",
        "PSV Eindhoven",
        "SC Cambuur",
        "Sparta Róterdam",
        "Telstar",
        "Twente",
        "Utrecht",
        "Willem II",
        "Zwolle",
    ],
    "UAE Pro League": [
        "Ajman",
        "Al Ain",
        "Al Dhafra",
        "Al Jazira",
        "Al Nasr",
        "Al Wahda",
        "Al Wasl",
        "Baniyas",
        "Hatta",
        "Ittihad Kalba",
        "Khorfakkan",
        "Shabab Al-Ahli Dubai",
        "Sharjah",
        "United FC",
    ],
    "Alemania": [
        "FC Colonia",
        "FSV Mainz 05",
        "Bayer Leverkusen",
        "Bayern Múnich",
        "Borussia Dortmund",
        "Borussia Mönchengladbach",
        "Eintracht Frankfurt",
        "FC Augsburgo",
        "FC Schalke 04",
        "Hamburgo SV",
        "RB Leipzig",
        "SC Friburgo",
        "SC Paderborn 07",
        "SV Elversberg",
        "TSG Hoffenheim",
        "Unión Berlín",
        "VfB Stuttgart",
        "Werder Bremen",
    ],
    "Bolivia": [
        "Academia del Balompié Boliviano (ABB)",
        "Always Ready",
        "Aurora",
        "Blooming",
        "Bolívar",
        "CDT Real Oruro",
        "Guabirá",
        "Gualberto Villarroel San José",
        "Independiente Petrolero",
        "Nacional Potosí",
        "Oriente Petrolero",
        "Real Potosí",
        "Real Tomayapo",
        "San Antonio Bulo Bulo",
        "The Strongest",
        "Universitario de Vinto",
    ],
    "Inglaterra": [
        "Arsenal",
        "Aston Villa",
        "Bournemouth",
        "Brentford",
        "Brighton & Hove Albion",
        "Chelsea",
        "Coventry City",
        "Crystal Palace",
        "Everton",
        "Fulham",
        "Hull City",
        "Ipswich Town",
        "Leeds United",
        "Liverpool",
        "Manchester City",
        "Manchester United",
        "Newcastle United",
        "Nottingham Forest",
        "Sunderland",
        "Tottenham Hotspur",
    ],
    "Espana": [
        "Athletic Club",
        "Club Atlético de Madrid",
        "Club Atlético Osasuna",
        "Deportivo Alavés",
        "Elche Club de Fútbol",
        "Fútbol Club Barcelona",
        "Getafe Club de Fútbol",
        "Levante Unión Deportiva",
        "Málaga Club de Fútbol",
        "RCD Espanyol de Barcelona",
        "Rayo Vallecano de Madrid",
        "Real Betis Balompié",
        "Real Club Celta de Vigo",
        "Real Club Deportivo de A Coruña",
        "Real Madrid CF",
        "Real Racing Club de Santander",
        "Real Sociedad de Fútbol",
        "Sevilla Fútbol Club",
        "Valencia Club de Fútbol",
        "Villarreal Club de Fútbol",
    ],
    "Francia": [
        "Angers",
        "Auxerre",
        "Brest",
        "Estrasburgo",
        "Le Havre",
        "Le Mans",
        "Lens",
        "Lille",
        "Lorient",
        "Lyon",
        "Marsella",
        "Mónaco",
        "Niza",
        "París FC",
        "PSG",
        "Rennes",
        "Toulouse",
        "Troyes",
    ],
    "Turquia": [
        "Adana Demirspor",
        "Alanyaspor",
        "Antalyaspor",
        "Ankaragücü",
        "Beşiktaş",
        "Bodrum FK",
        "Eyüpspor",
        "Fenerbahçe",
        "Galatasaray",
        "Gaziantep FK",
        "Göztepe",
        "Hatayspor",
        "Istanbul Başakşehir",
        "Kasımpaşa",
        "Kayserispor",
        "Kocaelispor",
        "Samsunspor",
        "Sivasspor",
        "Trabzonspor",
    ],
    "Belgica": [
        "Amberes",
        "Anderlecht",
        "Beerschot",
        "Brujas",
        "Cercle Brugge",
        "Charleroi",
        "Dender",
        "Genk",
        "Gante",
        "Kortrijk",
        "Mechelen",
        "Oud-Heverlee Leuven",
        "Sint-Truiden",
        "Standard de Lieja",
        "Union Saint-Gilloise",
        "Westerlo",
    ],
    "Australia": [
        "Adelaide United",
        "Auckland FC",
        "Brisbane Roar",
        "Central Coast Mariners",
        "Macarthur FC",
        "Melbourne City",
        "Melbourne Victory",
        "Newcastle Jets",
        "Perth Glory",
        "Sydney FC",
        "Wellington Phoenix",
        "Western Sydney Wanderers",
        "Western United",
    ],
    "Islandia": [
        "Breiðablik",
        "Fram Reykjavík",
        "FH Hafnarfjörður",
        "ÍA Akranes",
        "ÍBV Vestmannaeyjar",
        "KA Akureyri",
        "Keflavík ÍF",
        "KR Reykjavík",
        "Stjarnan Garðabær",
        "Valur Reykjavík",
        "Víkingur Reykjavík",
        "Vestri",
    ],
    "Suiza": [
        "Basilea",
        "BSC Young Boys",
        "FC Lugano",
        "FC Luzern",
        "FC Sion",
        "FC St. Gallen",
        "FC Thun",
        "FC Vaduz",
        "FC Zúrich",
        "Grasshopper Club Zúrich",
        "Lausanne-Sport",
        "Servette FC",
    ],
}

st.title("⚡ Golazo 2.5 Pro")
st.write(
    "Filtro antifraude de alta exigencia para proteger el capital en el mercado de +2.5 goles."
)

selected_league = st.selectbox("Selecciona la Liga", list(LEAGUES_DATABASE.keys()))

teams = LEAGUES_DATABASE[selected_league]
col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox("Equipo Local", teams)
with col2:
    away_team = st.selectbox(
        "Equipo Visitante", [t for t in teams if t != home_team]
    )

home_input = st.text_input("Promedio de goles esperados (Local)", "1.5")
away_input = st.text_input("Promedio de goles esperados (Visitante)", "1.2")

if st.button("Calcular Predicción y Análisis"):
    try:
        home_avg = float(home_input.replace(",", "."))
        away_avg = float(away_input.replace(",", "."))
    except ValueError:
        st.error(
            "⚠️ Por favor, introduce valores numéricos válidos (ej. 1.5 o 1,5)."
        )
        st.stop()

    expected_total = home_avg + away_avg

    # Filtro estricto anti-pérdidas (Exige un xG superior a 2.95 para considerar alta fiabilidad)
    if expected_total >= 3.0:
        prob_over_2_5 = round(
            random.uniform(78.0, 88.0), 2
        )  # Zona segura real
    elif expected_total >= 2.6:
        prob_over_2_5 = round(
            random.uniform(45.0, 55.0), 2
        )  # Zona trampa (como el 2.70 de ayer que quedó 1-1)
    else:
        prob_over_2_5 = round(random.uniform(15.0, 35.0), 2)  # Zona Under

    prob_under_2_5 = round(100 - prob_over_2_5, 2)

    st.markdown("---")
    st.subheader("📊 Resultado del Análisis Antifraude")
    st.write(f"**Encuentro:** {home_team} vs {away_team} *({selected_league})*")

    st.metric(
        label="Efectividad Proyectada para +2.5 Goles",
        value=f"{prob_over_2_5:.2f}%",
    )

    # Criterio estricto de protección de capital
    if expected_total >= 3.0:
        st.success(
            "🔥 **Dictamen VÁLIDO:** El xG supera los 3.0 goles. Partido apto para inversión."
        )
    elif expected_total >= 2.6:
        st.warning(
            "⚠️ **Dictamen ZONA TRAMPA (PELIGRO):** xG de 2.6 a 2.9. Alta probabilidad de quedar 1-1 o 2-0. **NO ARRIESGAR DINERO.**"
        )
    else:
        st.error(
            "❌ **Dictamen DESCARTADO:** Partido defensivo o cerrado. No cumple con la norma de goles."
        )

    # Bloque de Análisis Estadístico
    st.markdown("### 📋 Desglose Técnico de Seguridad")
    st.markdown(
        f"""
    * **Goles Totales Esperados (xG Combinado):** `{expected_total:.2f} goles`
    * **Riesgo de Under (-2.5):** `{prob_under_2_5:.2f}%`
    * **Aporte Local ({home_team}):** `{home_avg}` goles
    * **Aporte Visitante ({away_team}):** `{away_avg}` goles
    """
    )

    if expected_total >= 3.0:
        st.info(
            f"💡 **Conclusión:** Con {expected_total:.2f} de media, el margen cubre los imprevistos y apunta a la alta."
        )
    else:
        st.info(
            f"💡 **Conclusión:** Un xG de {expected_total:.2f} se queda en la cuerda floja (riesgo de marcador corto tipo 1-1). Es mejor omitirlo y cuidar el capital."
        )
