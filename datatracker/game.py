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

@bp.route('/consoleProjection')
def console_projection():
    api_result = requests.get('https://api.dccresource.com/api/games')
    games = api_result.json()
    game_after2013=[]
    for game in games:
        if game['year'] is None:
            continue
        elif game['year'] >= 2013:
            game_after2013.append(game)
    console = []
    for game in game_after2013:
        if game['platform'] not in console:
            console.append(game['platform'])
    _ps3_sales = 0
    _x360_sales = 0
    _3ds_sales = 0
    _ps4_sales = 0
    _xone_sales = 0
    _wiiu_sales = 0
    _wii_sales = 0
    _pc_sales = 0
    _psv_sales = 0
    _ds_sales = 0
    _psp_sales = 0
    for current_game in game_after2013:
        switcher
    return render_template('Views/console_projection.html', console=console)
