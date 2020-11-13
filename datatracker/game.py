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
        search_game_title = request.form['title']

        game_search_results = []

        for game in games:
            # .contains for partial searches
            if game['name'] == search_game_title:
                game_search_results.append(game)

        if len(game_search_results) == 1:
            return render_template('Views/game_search.html', game=game_search_results[0])
        elif len(game_search_results) > 1:
            game_stats_combined = combine_game_stats(game_search_results)
            return render_template('Views/game_search.html', game=game_stats_combined, game_by_console=game_search_results)
        else:
            return render_template('Views/game_search.html', error_message=error_message)


@bp.route('/sampleQuestion')
def plot_game_stats():
    api_result = requests.get('https://api.dccresource.com/api/games')
    games = api_result.json()

    # returns list of unique genres
    genres = get_genres(games)

    # returns list of totals by genre
    genre_totals = get_genre_totals(games, genres)

    return render_template('Views/sampleQuestion.html', data=genre_totals, labels=genres)


def get_genres(games):
    genres = []
    for game in games:
        if game['genre'] not in genres:
            genres.append(game['genre'])
    return genres


def get_genre_totals(games, genres):
    genre_totals = []

    for genre in genres:
        genre_totals.append(0)

    for game in games:
        if game['genre'] == 'Sports':
            genre_totals[0] += 1
        elif game['genre'] == 'Platform':
            genre_totals[1] += 1
        elif game['genre'] == 'Racing':
            genre_totals[2] += 1
        elif game['genre'] == 'Role-Playing':
            genre_totals[3] += 1
        elif game['genre'] == 'Puzzle':
            genre_totals[4] += 1
        elif game['genre'] == 'Misc':
            genre_totals[5] += 1
        elif game['genre'] == 'Shooter':
            genre_totals[6] += 1
        elif game['genre'] == 'Simulation':
            genre_totals[7] += 1
        elif game['genre'] == 'Action':
            genre_totals[8] += 1
        elif game['genre'] == 'Fighting':
            genre_totals[9] += 1
        elif game['genre'] == 'Adventure':
            genre_totals[10] += 1
        elif game['genre'] == 'Strategy':
            genre_totals[11] += 1
    return genre_totals


def combine_game_stats(game_list):
    game_combined = {
        'name': game_list[0]['name'],
        'year': game_list[0]['year'],
        'platform': '',
        'publisher': game_list[0]['publisher'],
        'genre': game_list[0]['genre'],
        'naSales': 0,
        'euSales': 0,
        'jpSales': 0,
        'otherSales': 0,
        'globalSales': 0
    }
    for current_game in game_list:
        game_combined['platform'] += (current_game['platform']) + ', '
        game_combined['naSales'] += current_game['naSales']
        game_combined['euSales'] += current_game['euSales']
        game_combined['jpSales'] += current_game['jpSales']
        game_combined['otherSales'] += current_game['otherSales']
        game_combined['globalSales'] += current_game['globalSales']

    # remove extra ', ' from end of platform
    game_combined['platform'] = game_combined['platform'][:-2]

    # round all values to 2 decimals
    game_combined['naSales'] = round(game_combined['naSales'], 2)
    game_combined['euSales'] = round(game_combined['euSales'], 2)
    game_combined['jpSales'] = round(game_combined['jpSales'], 2)
    game_combined['otherSales'] = round(game_combined['otherSales'], 2)
    game_combined['globalSales'] = round(game_combined['globalSales'], 2)
    return game_combined


@bp.route('/consoleProjection')
def console_projection():
    api_result = requests.get('https://api.dccresource.com/api/games')
    games = api_result.json()
    game_after2013 = []
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
        if current_game['platform'] == "PS3":
            _ps3_sales += current_game['globalSales']
        elif current_game['platform'] == "X360":
            _x360_sales += current_game['globalSales']
        elif current_game['platform'] == "3DS":
            _3ds_sales += current_game['globalSales']
        elif current_game['platform'] == "PS4":
            _ps4_sales += current_game['globalSales']
        elif current_game['platform'] == "XOne":
            _xone_sales += current_game['globalSales']
        elif current_game['platform'] == "WiiU":
            _wiiu_sales += current_game['globalSales']
        elif current_game['platform'] == "Wii":
            _wii_sales += current_game['globalSales']
        elif current_game['platform'] == "PC":
            _pc_sales += current_game['globalSales']
        elif current_game['platform'] == "PSV":
            _psv_sales += current_game['globalSales']
        elif current_game['platform'] == "DS":
            _ds_sales += current_game['globalSales']
        elif current_game['platform'] == "PSP":
            _psp_sales += current_game['globalSales']
    sales_by_console_totals = [round(_ps3_sales, 2), round(_x360_sales, 2), round(_3ds_sales, 2), round(_ps4_sales, 2),
                               round(_xone_sales, 2), round(_wiiu_sales, 2), round(_wii_sales, 2), round(_pc_sales, 2),
                               round(_psv_sales, 2), round(_ds_sales, 2), round(_psp_sales, 2)]

    return render_template('Views/console_projection.html', console=console, sales=sales_by_console_totals)
