import requests
from flask import Blueprint, request, render_template, flash, url_for
from werkzeug.utils import redirect

from .Models.game import Game


bp = Blueprint('game', __name__)


@bp.route('/searchGame', methods=('GET', 'POST'))
def search_game():
    error_message = "No results for that search"
    if request.method == 'GET':
        return render_template('Views/gameSearch.html')
    else:
        api_result = requests.get('https://api.dccresource.com/api/games')
        games = api_result.json()
        search_game_title = request.form['title']

        game_search_results = []

        for game in games:
            if game['name'] == search_game_title:
                game_search_results.append(game)

        if len(game_search_results) == 1:
            return render_template('Views/gameSearch.html', game=game_search_results[0])
        elif len(game_search_results) > 1:
            game_stats_combined = combine_game_stats(game_search_results)
            return render_template('Views/gameSearch.html', game=game_stats_combined, game_by_console=game_search_results)
        else:
            return render_template('Views/gameSearch.html', error_message=error_message)


@bp.route('/consoleProjection')
def console_projection():
    api_result = requests.get('https://api.dccresource.com/api/games')
    games = api_result.json()
    games_after_2013 = games_after_date(games, 2013)
    consoles = get_consoles(games_after_2013)
    console_totals = get_console_totals(games_after_2013, consoles)
    return render_template('Views/consoleProjection.html', labels=consoles, data=console_totals)


@bp.route('/sampleQuestion')
def plot_game_stats():
    api_result = requests.get('https://api.dccresource.com/api/games')
    games = api_result.json()
    genres = get_genres(games)
    genre_totals = get_genre_totals(games, genres)
    return render_template('Views/sampleQuestion.html', data=genre_totals, labels=genres)


@bp.route('/bonusQuestion')
def plot_bonus_question():
    api_result = requests.get('https://api.dccresource.com/api/games')
    games = api_result.json()
    consoles = get_consoles(games)
    games_by_console = sort_games_by_console(games, consoles)
    games_by_console_and_publisher = sort_games_by_publisher(games_by_console)

    return render_template('Views/bonusQuestion.html', dataset=games_by_console_and_publisher, labels=consoles)


def games_after_date(games, date):
    games_filtered = []
    for game in games:
        if game['year'] is None:
            continue
        elif game['year'] >= date:
            games_filtered.append(game)
    return games_filtered


def sort_games_by_publisher(games_by_console):
    games_by_console_and_publisher = {}
    for console in games_by_console:
        games_by_console_and_publisher[console] = {}
    for console, games in games_by_console.items():
        for game in games:
            if game['publisher'] not in games_by_console_and_publisher[game['platform']]:
                games_by_console_and_publisher[game['platform']][game['publisher']] = 1
            elif game['publisher'] in games_by_console_and_publisher[game['platform']]:
                games_by_console_and_publisher[game['platform']][game['publisher']] += 1
    return games_by_console_and_publisher


def sort_games_by_console(games, consoles):
    games_by_console = {}
    for console in consoles:
        games_by_console[console] = []
    for game in games:
        for key in games_by_console:
            if game['platform'] == key:
                games_by_console[key].append(game)
                break
    return games_by_console


def get_genres(games):
    genres = []
    for game in games:
        if game['genre'] not in genres:
            genres.append(game['genre'])
    return genres


def get_consoles(games):
    consoles = []
    for game in games:
        if game['platform'] not in consoles:
            consoles.append(game['platform'])
    return consoles


def get_console_totals(games, consoles):
    console_totals = []
    for console in consoles:
        console_totals.append(0)
    for game in games:
        for index, console in enumerate(consoles):
            if game['platform'] == console:
                console_totals[index] += game['globalSales']
                break
    for index, total in enumerate(console_totals):
        console_totals[index] = round(total, 2)
    return console_totals


def get_genre_totals(games, genres):
    genre_totals = []
    for genre in genres:
        genre_totals.append(0)
    for game in games:
        for index, genre in enumerate(genres):
            if game['genre'] == genre:
                genre_totals[index] += 1
    return genre_totals


def get_publishers(games):
    publishers = []
    for game in games:
        if game['publisher'] not in publishers:
            publishers.append(game['publisher'])
    return publishers


def get_publisher_totals(games, publishers):
    publisher_totals = []
    for publisher in publishers:
        publisher_totals.append(0)
    for game in games:
        for index, publisher in enumerate(publishers):
            if game['publisher'] == publisher:
                publisher_totals[index] += 1
    return publisher_totals


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
    game_combined['platform'] = game_combined['platform'][:-2]
    game_combined['naSales'] = round(game_combined['naSales'], 2)
    game_combined['euSales'] = round(game_combined['euSales'], 2)
    game_combined['jpSales'] = round(game_combined['jpSales'], 2)
    game_combined['otherSales'] = round(game_combined['otherSales'], 2)
    game_combined['globalSales'] = round(game_combined['globalSales'], 2)
    return game_combined
