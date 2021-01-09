class Games:
    def __init__(self, username, mode, all_games, total_count):
        self.username = username
        self.mode = mode
        self.total = total_count
        self.next_page = None
        self.games = all_games


class Game:
    def __init__(self, date, mode, position, opponent, result, rating):
        self.date = date
        self.mode = mode
        self.position = position
        self.opponent = opponent
        self.result = result
        self.rating = rating


class Rating:
    def __init__(self, total, change):
        self.total = total
        self.change = change
