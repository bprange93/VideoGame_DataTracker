import requests
from flask import Blueprint, request, render_template, flash, url_for
from werkzeug.utils import redirect

from .Models.game import Game


bp = Blueprint('game', __name__)


@bp.route('/searchGame', methods=('GET', 'POST'))
def search_game():
    error_message = "No results for that search"
    if request.method == 'GET':
        return render_template('Views/game_search.html')
    else:
        api_result = requests.get('https://api.dccresource.com/api/games')
        games = api_result.json()
        chosen_game = request.form['title']

        for title in games:
            if title['name'] == chosen_game:
                return render_template('Views/game_search.html', title=title)

        return render_template('Views/game_search.html', error_message=error_message)