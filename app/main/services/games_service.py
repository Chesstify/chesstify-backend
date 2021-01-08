import datetime

from app.main.models.games import Game, Games
from app.main.util.games_requests import GamesClient

DATE_FORMAT_DD_MM_YYYY = "%d/%m/%Y"
RESULTS_TYPES = {
    "Win": ["win"],
    "Loss": ["lose", "checkmated", "timeout", "resigned", "abandoned"],
    "Draw": ["agreed", "stalemate", "repetition", "insufficient", "50move", "timevsinsufficent"]}


class GamesService:
    @staticmethod
    def get_games(username, game_mode, page_number, page_size, use_cache):
        api = GamesService.__games_from_api(username, use_cache)
        games = [GamesService.__create_game(username, game) for game in api]
        filtered_games = GamesService.__filter_games_by_game_mode(game_mode, games)
        paginated_games = GamesService.__paginate_games(filtered_games, page_number, page_size)
        return Games(username, game_mode, paginated_games, len(filtered_games))

    @staticmethod
    def __games_from_api(username, use_cache):
        if use_cache:
            all_games_response = GamesClient().get_all_games_from_cache(username)
        else:
            all_games_response = GamesClient().get_all_games(username)

        flattened_games = [game for game_list in all_games_response for game in game_list]
        return sorted(flattened_games, key=lambda game: game["end_time"], reverse=True)

    @staticmethod
    def __create_game(username, game):
        date = GamesService.__get_date(game)
        mode = GamesService.__get_mode(game)
        position = GamesService.__get_position(game, username)
        opponent = GamesService.__get_opponent(game, position)
        result = GamesService.__get_result(game, position)
        rating = GamesService.__get_rating(game, position)

        return Game(date, mode, position, opponent, result, rating)

    @staticmethod
    def __get_date(game):
        game_date_epoch = game["end_time"]
        return datetime.datetime.utcfromtimestamp(game_date_epoch).strftime(DATE_FORMAT_DD_MM_YYYY)

    @staticmethod
    def __get_mode(game):
        return game["time_class"]

    @staticmethod
    def __get_position(game, username):
        white_username = game["white"]["username"]
        return "white" if white_username == username else "black"

    @staticmethod
    def __get_opponent(game, position):
        opposite_position = "black" if position == "white" else "white"
        return game[opposite_position]["username"]

    @staticmethod
    def __get_result(game, position):
        result_code = game[position.lower()]["result"]
        for key, value in RESULTS_TYPES.items():
            if result_code in value:
                return key
        return "Unknown"

    @staticmethod
    def __get_rating(game, position):
        rating = game[position]["rating"]
        return {"rating": {
            "total": rating,
            "change": "-"
        }}

    @staticmethod
    def __filter_games_by_game_mode(game_mode, games):
        return [game for game in games if game.mode == game_mode or game_mode == "all"]

    @staticmethod
    def __paginate_games(filtered_games, page_number, page_size):
        return [filtered_games[i:i + page_size] for i in range(0, len(filtered_games), page_size)][
            page_number]
