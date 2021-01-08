import jsonpickle
from flask import request, abort, Blueprint

from app.main.services.games_service import GamesService

games_blueprint = Blueprint("games", __name__)

DEFAULT_PAGE_SIZE = 100
mode_query_params = ["blitz", "bullet", "rapid", "all"]


@games_blueprint.route('/games/<string:username>', methods=['GET'])
def get_games_by_username(username):
    mode_query_param = str.lower(request.args.get("mode", "all", type=str))
    page_number_query_param = request.args.get("pageNumber", 0, type=int)
    page_size_query_param = request.args.get("pageSize", DEFAULT_PAGE_SIZE, type=int)
    use_cache_query_param = request.args.get("useCache", False, type=bool)
    if mode_query_param is not None and mode_query_param not in mode_query_params:
        abort(400, "Invalid game mode query provided: {0}. Valid values are: {1} ".format(mode_query_param,
                                                                                          ", ".join(mode_query_params)))
    games = GamesService.get_games(username, mode_query_param, page_number_query_param, page_size_query_param,
                                   use_cache_query_param)

    add_next_page_links(games, page_number_query_param, page_size_query_param)

    return jsonpickle.encode(games, unpicklable=False), {'Content-Type': 'application/json; charset=utf-8'}


def add_next_page_links(games, page_number_query_param, page_size_query_param):
    if games.total - ((DEFAULT_PAGE_SIZE * page_number_query_param) + page_size_query_param) > 0:
        next_page_number = page_number_query_param + 1
        next_page_link = request.full_path.replace(f"pageNumber={page_number_query_param}",
                                                   f"pageNumber={next_page_number}")
        games.next_page = next_page_link
