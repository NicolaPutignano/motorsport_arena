EVENT_TYPES = [
    ('SingleRace', 'SingleRace'),
    ('Championship', 'Championship'),
    ('League', 'League')
]

STATUS_CHOICES = [
    ('Scheduled', 'Scheduled'),
    ('In progress', 'In progress'),
    ('Finished', 'Finished'),
    ('Deleted', 'Deleted'),
]

RACE_TIME_PROGRESS = [
    ('Continuous', 'Continuous'),
    ('Fixed', 'Fixed')
]

RACE_LENGTH_TYPE = [
    ('Laps', 'Laps'),
    ('Minutes', 'Minutes')
]

RACE_WEATHER = [
    ('Sunrise', 'Sunrise'),
    ('Morning', 'Morning'),
    ('Late morning', 'Late morning'),
    ('Noon', 'Noon'),
    ('Afternoon', 'Afternoon'),
    ('Late afternoon', 'Late afternoon'),
    ('Evening', 'Evening'),
    ('Sunset', 'Sunset'),
    ('Night', 'Night'),
    ('Midnight', 'Midnight')
]

RACE_PENALTY = [
    ('No', 'No'),
    ('Limited', 'Limited'),
    ('Moderate', 'Moderate'),
    ('Complete', 'Complete')
]

CAR_TRACTION = [
    ('FWD', 'Front-Wheel Drive'),
    ('RWD', 'Rear-Wheel Drive'),
    ('AWD', 'All-Wheel Drive')
]

CAR_ENGINE_POS = [
    ('F', 'Front'),
    ('MF', 'Front-Mid'),
    ('MR', 'Rear-Mid'),
    ('R', 'Rear')
]

CAR_WHEEL_TYPE = [
    ('Factory', 'Factory'),
    ('Race', 'Race'),
    ('Upgraded', 'Upgraded'),
]

CAR_STEER_POS = [
    ('C', 'Central'),
    ('L', 'Left'),
    ('R', 'Right')
]

CFG = [
    ('E', 'E'),
    ('F', 'F'),
    ('I', 'I'),
    ('R', 'R'),
    ('V', 'V'),
    ('VR', 'VR'),
    ('W', 'W'),

]

IND = [
    ('DSC', 'DSC'),
    ('EV', 'EV'),
    ('NA', 'Naturally Aspirated'),
    ('T', 'T'),
    ('T4', 'T4'),
    ('TT', 'TT'),
]

EVENT_DOC_DIR = ['event_documents/']
