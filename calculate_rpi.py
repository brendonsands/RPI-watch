import pandas as pd

df = pd.read_csv('scores.csv', names = ['Date', 
                                        'Team 1', 
                                        'Score 1', 
                                        'Team 2', 
                                        'Score 2', 
                                        'Home'])

df['Year'] = df['Date'].apply(lambda x: x.split('/')[2])

points_dict = { ('win','at') : 1.3,
                ('win', 'vs') : .7,
                ('lose', 'at'): .7,
                ('lose','vs'): 1.3
} 

# Create OWP, OOWP cache
WP_cache = dict()
OWP_cache = dict()
OOWP_cache = dict()

# loop through years in dataset
for year in df['Year'].unique():

    # subset based on year
    df_year = df[df['Year'] == year]

    # get list of teams that played less than 10 games 
    game_counts = pd.concat([df_year['Team 1'], df_year['Team 2']]).value_counts()
    small_teams = game_counts[game_counts < 10].keys().to_list()

    # if a team played less than 10 games, don't count their games in RPI
    df_year['Team 1'] = df_year[df_year['Team 1'] == pd.NA]
    df_year['Team 2'] = df_year[df_year['Team 2'] == pd.na]

    df_year = df_year.dropna()
    
    for team in df_year['Team 1'].unique():
        
        # Calculate Winning Percentage'    
        WP_numerator = 0
        WP_denominator = 0

