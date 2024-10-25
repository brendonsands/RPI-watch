import pandas as pd
import helpers

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

    # get list of teams that played less than 10 games - assume not d1
    game_counts = pd.concat([df_year['Team 1'], df_year['Team 2']]).value_counts()
    small_teams = game_counts[game_counts < 10].keys().to_list()

    ignore_dict = {x : pd.NA for x in small_teams}

    # if a team played less than 10 games, don't count their games in RPI
    df_year['Team 1'] = df_year['Team 1'].replace(small_teams, pd.NA)
    df_year['Team 2'] = df_year['Team 2'].replace(small_teams, pd.NA)

    df_year = df_year.dropna()

    for team in set(df_year['Team 1']).intersection(set(df_year['Team 2'])):
        
        # Winning Percentage
        WP_numerator = 0
        WP_denominator = 0

        # all games for team
        team_df = df_year[(df_year['Team 1'] == team) | (df_year['Team 2'] == team)]

        # apply winning percentage formula to teams schedule
        yearly_results = team_df.apply(helpers.calculate_wp, axis = 1, team = team)

        # sum up total WP and possible WP
        WP_numerator, WP_denominator = tuple(sum(x) for x in zip(*yearly_results))

        # save to cache
        WP_cache[team] = WP_numerator/WP_denominator

        #Opponent Winning Percentage
        opponents = set(team_df['Team 1']).intersection(set(team_df['Team 2']))
        opponents.remove(team)

        for opponent in opponents:

            OWP_numerator = 0
            OWP_denominator = 0

            # all games for opponent
            opponent_df = df_year[(df_year['Team 1'] == opponent) | (df_year['Team 2'] == opponent)]

            # ignore games against team
            opponent_df = opponent_df[(opponent_df['Team 1'] != team) & (opponent_df['Team 2'] != team)]

            # apply winning percentage formula to opp's schedule
            yearly_results_opp = opponent_df.apply(helpers.calculate_wp, axis = 1, team = opponent)

            # sum up modified WP for opponent
            WP_numerator_opp, WP_denominator_opp = tuple(sum(x) for x in zip(*yearly_results_opp))

            OWP_numerator += WP_numerator_opp / WP_denominator_opp
            OWP_denominator += 1
        

        OWP_cache[team] = OWP_numerator/OWP_denominator

print(OWP_cache)