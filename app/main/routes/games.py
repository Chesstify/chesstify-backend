import jsonpickle
from flask import request, abort, Blueprint
from requests.models import PreparedRequest

from app.main.services.games_service import GamesService

games_blueprint = Blueprint("games", __name__)

DEFAULT_GAME_MODE = "all"
DEFAULT_PAGE_SIZE = 100
DEFAULT_PAGE_NUMBER = 0
PAGE_NUMBER = "pageNumber"
USE_CACHE = "useCache"
MODE = "mode"
PAGE_SIZE = "pageSize"
GAME_MODES = ["blitz", "bullet", "rapid", "all"]


@games_blueprint.route('/games/<string:username>', methods=['GET'])
def get_games_by_username(username):
    game_mode_query = str.lower(request.args.get(MODE, "%s" % DEFAULT_GAME_MODE, type=str))
    page_number_query = request.args.get(PAGE_NUMBER, DEFAULT_PAGE_NUMBER, type=int)
    page_size_query = request.args.get(PAGE_SIZE, DEFAULT_PAGE_SIZE, type=int)
    use_cache_query = request.args.get(USE_CACHE, False, type=bool)
    if game_mode_query is not None and game_mode_query not in GAME_MODES:
        abort(400, "Invalid game mode query provided: {0}. Valid values are: {1} ".format(game_mode_query,
                                                                                          ", ".join(GAME_MODES)))
    games = GamesService.get_games(username, game_mode_query, page_number_query, page_size_query,
                                   use_cache_query)
    set_next_page_url(games, game_mode_query, page_number_query, page_size_query)

    return jsonpickle.encode(games, unpicklable=False), {'Content-Type': 'application/json; charset=utf-8'}


def set_next_page_url(games, mode, page_number, page_size):
    if games.total - ((page_size * page_number) + page_size) > 0:
        page_number += 1
        params = {MODE: mode, USE_CACHE: True, PAGE_NUMBER: page_number, PAGE_SIZE: page_size}
        prepared_request = PreparedRequest()
        prepared_request.prepare_url(request.base_url, params)

        games.next_page = prepared_request.url.split(request.host)[1]
