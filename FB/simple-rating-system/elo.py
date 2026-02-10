from multiprocessing import RawArray


class elo:
    def __init__(self):
        self.players = {}
        self.initial_rating = 1500
        self.k_factor = 20

    def get_lin_rating(self, player):
        player_rating = self.get_elo_rating(player)
        return 10 ** (player_rating / 400)

    def get_elo_rating(self, player):
        return self.players[player] if player in self.players else self.initial_rating

    def change_rating(self, player, change):
        if player not in self.players:
            self.players[player] = 1500
        self.players[player] += change

    def log_game(self, teams, results):
        total_results = sum(results)
        normalised_results = [i / total_results for i in results]

        total_rating = 0
        total_players = 0
        team_ratings = []
        team_indv_ratings = []
        for team in teams:
            team_rating = 0
            indv_ratings = []
            for player in team:
                player_rating = self.get_lin_rating(player)
                team_rating += player_rating
                indv_ratings.append(player_rating)

                total_players += 1
            team_ratings.append(team_rating)
            team_indv_ratings.append(indv_ratings)
            total_rating += team_rating

        adjusted_k_factor = total_players / len(teams) * self.k_factor

        for team_idx, team in enumerate(teams):
            team_rating = team_ratings[team_idx]
            team_indv_rating = team_indv_ratings[team_idx]
            actual_result = normalised_results[team_idx]
            win_prob = team_rating / total_rating

            delta = actual_result - win_prob
            net_pnl = adjusted_k_factor * delta

            for player_idx, player in enumerate(team):
                player_contribution = team_indv_rating(player_idx) / team_rating
                player_pnl = net_pnl * player_contribution
                self.change_rating(player, player_pnl)
