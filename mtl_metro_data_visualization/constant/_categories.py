STOP = [
    'interruption service ligne entre',
    'arrêt ligne entre',
    'arrêt service station',
    'arrêt prolongé ligne entre',
    'interruption service prolongée ligne entre',
    'interruption cours',
    "l'interruption service",
    'bonjour service interrompu',
    'bonjour service présentement interrompu',
    'bonjour service maintenant interrompu',
    'arrêt service ligne',
    'nous oblige interrompre service',
    'service interruption continues'
]

NORMAL = [
    'service normal métro',
    'normal métro service',
    'service normal ligne',
    'bonjour service maintenant normal',
    'bonjour service actuellement normal',
    'service normal station',
]

SLOW = [
    'reprise graduelle service ligne',
    'état service métro service reprend graduellement',
    'état service métro reprise graduelle',
    'bonjour ralentissement',
    'ralentissement service ligne',
    'service reprend graduellement',
    'ralentissement service',
    'bonjour service régulier reprend graduellement',
    'bonjour service reprise graduelle',
    'service maintenant reprise graduelle',
    'reprise graduelle service'
]

RESTART = [
    'état service métro service rétabli',
    'bonjour service rétabli',
    'service normal cause ralentissement résolue',
    'service maintenant normal'
]

ELEVATOR = [
    'ascenseur station'
]

STATION = [
    'aucun arrêt trains ligne station',
    'aucun arrêt trains station',
    'fermeture station',
    'trains stopping'
]

EVENT = [
    'couvrefeu maintenant vigueur',
    'dernier train mr63',
    'distribution couvrevisages',
    "férié aujourd'hui",
    'état service métro semaine',
    "merci pour l’information",
    "merci nous l'avoir signalé",
    "merci nous avons transmis",
    "merci nous avons avisé",
    "interruption planifiée",
    "avis clientèle",
    "avis d'interruptions planifiées",
    "bonjour"
]

CATEGORIES = {
    'stop': STOP,
    'normal': NORMAL,
    'slow': SLOW,
    'restart': RESTART,
    'elevator': ELEVATOR,
    'station': STATION,
    'event': EVENT,
}

