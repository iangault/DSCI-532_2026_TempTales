import os
from pathlib import Path

import chatlas as ctl
from dotenv import load_dotenv
from ibis import _
from querychat import QueryChat
from shinychat.types import HistoryOptions

from .utils import df_monthly

load_dotenv()

chat = ctl.ChatGoogle(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model = "gemini-3.5-flash-lite",
    system_prompt = """
        You are a climate data assistant for the TempTales dashboard.

        You help users explore historical temperature data across countries.
        This is the dataset provided for you: 
        * temperature_data:
            Monthly average temperature per country.    

        When possible:
        - Answer questions using the dataset
        - Suggest useful data queries
        - Help interpret climate trends
        - Be concise and clear
    """
)

################### Revised using ibis expressions
# round the AvgTemp
df_monthly = df_monthly.mutate(AvgTemp=_.AvgTemp.round(2))

# subset to top 100 population countries to decrease sample size (originally 243)
top100_countries = [
    "India",
    "China",
    "United States",
    "Indonesia",
    "Pakistan",
    "Nigeria",
    "Brazil",
    "Bangladesh",
    "Russia",
    "Mexico",
    "Ethiopia",
    "Japan",
    "Philippines",
    "Egypt",
    "Congo (Democratic Republic Of The)",
    "Vietnam",
    "Iran",
    "Turkey",
    "Germany",
    "Thailand",
    "United Kingdom",
    "France",
    "Tanzania",
    "South Africa",
    "Italy",
    "Kenya",
    "Burma",
    "Colombia",
    "South Korea",
    "Uganda",
    "Spain",
    "Argentina",
    "Algeria",
    "Sudan",
    "Ukraine",
    "Iraq",
    "Afghanistan",
    "Poland",
    "Canada",
    "Morocco",
    "Saudi Arabia",
    "Uzbekistan",
    "Peru",
    "Angola",
    "Malaysia",
    "Mozambique",
    "Ghana",
    "Yemen",
    "Nepal",
    "Venezuela",
    "Madagascar",
    "Cameroon",
    "Côte D'Ivoire",
    "North Korea",
    "Australia",
    "Niger",
    "Taiwan",
    "Sri Lanka",
    "Burkina Faso",
    "Mali",
    "Romania",
    "Malawi",
    "Chile",
    "Kazakhstan",
    "Zambia",
    "Guatemala",
    "Ecuador",
    "Syria",
    "Netherlands",
    "Senegal",
    "Cambodia",
    "Chad",
    "Somalia",
    "Zimbabwe",
    "Guinea",
    "Rwanda",
    "Benin",
    "Burundi",
    "Tunisia",
    "Bolivia",
    "Belgium",
    "Haiti",
    "Cuba",
    "Dominican Republic",
    "Czech Republic",
    "Greece",
    "Jordan",
    "Portugal",
    "Azerbaijan",
    "Sweden",
    "Honduras",
    "United Arab Emirates",
    "Hungary",
    "Belarus",
    "Tajikistan",
    "Austria",
    "Switzerland",
    "Israel",
    "Sierra Leone",
    "Laos"
]

################### Revised using ibis expressions
# df_monthly = df_monthly[df_monthly["Country"].isin(top100_countries)]
df_monthly = df_monthly.filter(_.Country.isin(top100_countries))

_GREETING_CACHE = Path(__file__).parent / ".querychat_greeting.txt"

qc = QueryChat(
    df_monthly.execute(),
    "temperature_data",
    client=chat,
    greeting=_GREETING_CACHE if _GREETING_CACHE.exists() else None,
    history=HistoryOptions(store="memory"),
)

if not _GREETING_CACHE.exists():
    _GREETING_CACHE.write_text(qc.generate_greeting())

