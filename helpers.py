def calculate_wp(row, team):

    if row['Home'] == f'@{team}':
        win_multiplier = .7
        loss_multiplier = 1.3
    else:
        win_multiplier = 1.3
        loss_multiplier = .7

    # team is team 1
    if row['Team 1'] == team:
        # team 1 wins
        if row['Score 1'] > row['Score 2']:
            return 1 * win_multiplier, 1 * win_multiplier
        # team 1 loses
        else:
            return 0, 1 * loss_multiplier
    # team is team 2
    else:
        # team 2 loses
        if row['Score 1'] > row['Score 2']:
            return 0, 1 * loss_multiplier
        # team 2 wins
        else:
            return 1 * win_multiplier, 1 * win_multiplier

