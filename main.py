import random
import pandas as pd
import streamlit as st
from scipy.stats import poisson

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
    "Selecciona la liga, los equipos e introduce los promedios (puedes usar coma o punto)."
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

# Usamos text_input para evitar errores con las comas del teclado
home_input = st.text_input("Promedio de goles esperados (Local)", "1.5")
away_input = st.text_input("Promedio de goles esperados (Visitante)", "1.2")

if st.button("Calcular Predicción y Análisis"):
    try:
        # Reemplazamos la coma por punto automáticamente para que Python no falle
        home_avg = float(home_input.replace(",", "."))
        away_avg = float(away_input.replace(",", "."))
    except ValueError:
        st.error(
            "⚠️ Por favor, introduce valores numéricos válidos (ej. 1.5 o 1,5)."
        )
        st.stop()

    expected_total = home_avg + away_avg

    # Probabilidades exactas con Distribución de Poisson para +2.5 goles
    p0 = poisson.pmf(0, expected_total)
    p1 = poisson.pmf(1, expected_total)
    p2 = poisson.pmf(2, expected_total)

    prob_under_2_5 = (p0 + p1 + p2) * 100
    prob_over_2_5 = (1 - (p0 + p1 + p2)) * 100

    st.markdown("---")
    st.subheader("📊 Resultado del Análisis")
    st.write(f"**Encuentro:** {home_team} vs {away_team} *({selected_league})*")

    st.metric(
        label="Probabilidad de Más de 2.5 Goles",
        value=f"{prob_over_2_5:.2f}%",
    )

    if prob_over_2_5 >= 55.0:
        st.success("🔥 **Dictamen:** Alta probabilidad. ¡Mercado recomendado (+2.5)!")
    else:
        st.warning(
            "⚠️ **Dictamen:** Precaución. Tendencia a pocos goles o partido cerrado."
        )

    # Bloque de Análisis Estadístico
    st.markdown("### 📋 Análisis Táctico y Estadístico")
    st.markdown(
        f"""
    * **Goles Totales Esperados (xG Combinado):** `{expected_total:.2f} goles`
    * **Probabilidad de Menos de 2.5 Goles:** `{prob_under_2_5:.2f}%`
    * **Tendencia Ofensiva Local ({home_team}):** `{home_avg}` goles estimados.
    * **Tendencia Ofensiva Visitante ({away_team}):** `{away_avg}` goles estimados.
    """
    )

    if expected_total >= 3.0:
        st.info(
            f"💡 **Nota del Analista:** Las estadísticas de {home_team} y {away_team} apuntan a un duelo abierto con alta tendencia a superar los 2.5 tantos."
        )
    elif expected_total >= 2.3:
        st.info(
            f"💡 **Nota del Analista:** Escenario equilibrado. Con un xG de {expected_total:.2f}, está en la línea límite para el mercado de más de 2.5."
        )
    else:
        st.info(
            f"💡 **Nota del Analista:** Perfil conservador. Los promedios indican un partido cerrado con baja expectativa de goles."
        )
