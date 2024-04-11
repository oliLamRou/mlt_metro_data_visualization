import pandas as pd
from datetime import timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz='US/Eastern')

def time_df(start, end):
    #Create a time serie with day as freq
    #NOTE: freq could be a parm so can check per hour
    years = pd.DataFrame(columns=['date'], data=pd.date_range(start, end, freq='d', tz='US/Eastern'))
    
    #Adding year, month, day, weekdays columns
    years['year'] = pd.to_datetime(years['date']).dt.year
    years['month'] = pd.to_datetime(years['date']).dt.month
    years['day'] = pd.to_datetime(years['date']).dt.day
    years['weekday'] = pd.to_datetime(years['date']).dt.weekday
    years['dayofyear'] = pd.to_datetime(years['date']).dt.dayofyear
    years['quarter'] = pd.to_datetime(years['date']).dt.quarter
    years['weekofyear'] = pd.to_datetime(years['date']).dt.isocalendar()['week']
    return years

VERTE = {
    'angrignon': 1,
    'monk': 2,
    'jolicoeur': 3,
    'verdun': 4,
    'lasalle': 5,
    'charlevoix': 6,
    'lionel-groulx': 7,
    'atwater': 8,
    'guy-concordia': 9,
    'concordia': 9,
    'peel': 10,
    'mcgill': 11,
    'place-des-arts': 12,
    'saint-laurent': 13,
    'berri-uqam': 14,
    'beaudry': 15,
    'papineau': 16,
    'frontenac': 17,
    'préfontaine': 18,
    'joliette': 19,
    'pie-ix': 20,
    'viau': 21,
    'assomption': 22,
    'cadillac': 23,
    'langelier': 24,
    'radisson': 25,
    'honoré-beaugrand': 26,
}

ORANGE = {
    'côte-vertu': 1,
    'du collège': 2,
    'de la savane': 3,
    'namur': 4,
    'plamondon': 5,
    'snowdon': 6,
    'villa-maria': 7,
    'vendôme': 8,
    'place-saint-henri': 9,
    'lionel-groulx': 10,
    'georges-vanier': 11,
    "lucien-l'allier": 12,
    'bonaventure': 13,
    'square-victoria–oaci': 14,
    "place-d'armes": 15,
    'champ-de-mars': 16,
    'berri-uqam': 17,
    'sherbrooke': 18,
    'mont-royal': 19,
    'laurier': 20,
    'rosemont': 21,
    'beaubien': 22,
    'jean-talon': 23,
    'jarry': 24,
    'crémazie': 25,
    'sauvé': 26,
    'henri-bourassa': 27,
    'cartier': 28,
    'de la concorde': 29,
    'montmorency': 30
}

JAUNE = {
    'berri-uqam': 1,
    'jean-drapeau': 2,
    'longueuil–université-de-sherbrooke': 3
}

BLEUE = {
    'snowdon': 1,
    'côte-des-neiges': 2,
    'université-de-montréal': 3,
    'édouard-montpetit': 4,
    'outremont': 5,
    'acadie': 6,
    'parc': 7,
    'de castelnau': 8,
    'jean-talon': 9,
    'fabre': 10,
    "d'iberville": 11,
    'saint-michel': 12
}

REM = {
    'brossard': 1,
    'du quartier': 2,
    'panama': 3,
    'île-des-soeurs': 4,
    'gare centrale': 5,
}

LINES_STATIONS = {
    'stm_Bleue': BLEUE,
    'stm_Jaune': JAUNE,
    'stm_Orange': ORANGE,
    'stm_Verte': VERTE,
    'REM_infoservice': REM,
}