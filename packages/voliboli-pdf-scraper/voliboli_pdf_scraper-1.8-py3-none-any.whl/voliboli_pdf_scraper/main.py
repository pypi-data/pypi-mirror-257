#!/usr/bin/python
import logging
import tabula as tb
import multiprocessing
from .constants import *
import numpy as np

logging.basicConfig(level=logging.INFO)

# boundaries
TEAM1_UB = 180
TEAM1_LB = 340
TEAM2_UB = 425
TEAM2_LB = 580

def unpack_df(df):
    a = []
    for (colName, colData) in df.items():
        a.append(colName)
        for d in colData:
            a.append(str(d))

    return a

def autocomplete_teamname(name):
    for m,w in zip(team_names_men, team_names_women):
        if name in m:
            return m
        elif name in w:
            return w
    return None

def scrape_pdf(file, upper_bound, left_bound, lower_bound, right_bound, debug):
    res = tb.read_pdf(file, area = (upper_bound, left_bound, lower_bound, right_bound), pages = '1')[0]
    if debug: logging.debug(res)

    return unpack_df(res)

def resolve_names(numbers, teams, team, gender, debug):
    names = []
    for num in numbers:
        try:
            names.append(teams[team][str(num)])
        except:
            if debug: logging.warning(f"Failed to match shirt number #{num} to a {gender} in team {team}!")
            return None
    return names

def extract_players(upper_bound, lower_bound, ateam, file, debug):
    team_numbers = scrape_pdf(file, upper_bound, 20, lower_bound, 40, debug)

    # Unpack names based on player number - men's (in case of failure try women's)
    names = resolve_names(team_numbers, teams_men, ateam, 'men', debug)
    if names is None:
        names = resolve_names(team_numbers, teams_women, ateam, 'women', debug)
    if not names:
        raise Exception("Failed to resolve numbers to names while processing")

    if debug: logging.info(f"Players names from {ateam}: {names}")

    # call the function for each item in parallel
    pool = multiprocessing.Pool()
    conf = [(file, upper_bound, 190, lower_bound, 240, debug),
            (file, upper_bound, 230, lower_bound, 250, debug),
            (file, upper_bound, 250, lower_bound, 270, debug),
            (file, upper_bound, 270, lower_bound, 290, debug),
            (file, upper_bound, 290, lower_bound, 310, debug),
            (file, upper_bound, 310, lower_bound, 330, debug),
            (file, upper_bound, 330, lower_bound, 350, debug),
            (file, upper_bound, 350, lower_bound, 380, debug),
            (file, upper_bound, 380, lower_bound, 400, debug),
            (file, upper_bound, 400, lower_bound, 420, debug),
            (file, upper_bound, 420, lower_bound, 450, debug),
            (file, upper_bound, 450, lower_bound, 470, debug),
            (file, upper_bound, 470, lower_bound, 490, debug),
            (file, upper_bound, 490, lower_bound, 510, debug),
            (file, upper_bound, 510, lower_bound, 530, debug),
            (file, upper_bound, 530, lower_bound, 560, debug),
            (file, upper_bound, 560, lower_bound, 580, debug)]
    result =  [names]
    # Outputs returned in order 
    for res in pool.starmap(scrape_pdf, conf):
        result.append(res)

    # Transpose scraped statistics from columns to rows
    transposed = np.array(result).T.tolist()
    pool.close()

    return transposed

def process_pdf(file, debug):
    if debug: logging.info("Processing PDF...")
    try:
        game = scrape_pdf(file, 40, 300, 85, 480, debug)
        if debug: logging.info(game)
        team1, team2 = game
        if (ateam1 := autocomplete_teamname(team1)) is None:
            logging.error(f"Failed to resolve team name: {team1}")
            return
        if (ateam2 := autocomplete_teamname(team2)) is None:
            logging.error(f"Failed to resolve team name: {team2}")
            return

        if debug: logging.info(f"Match: {ateam1} - {ateam2}")
        result = scrape_pdf(file, 40, 550, 85, 570, debug)
        if debug: logging.info(f"Result: {result}")
        date = scrape_pdf(file, 105, 70, 115, 150, debug)
        if debug: logging.info(f"Date: {date}")
        location = scrape_pdf(file, 120, 70, 135, 150, debug)
        if debug: logging.info(f"Location: {location}")
        if debug: logging.debug(result, date, location)

        players1 = extract_players(TEAM1_UB, TEAM1_LB, ateam1, file, debug)
        if debug: logging.info(players1)
        players2 = extract_players(TEAM2_UB, TEAM2_LB, ateam2, file, debug)
        if debug: logging.info(players2)

        return result, date, location, ateam1, ateam2, players1, players2
    except Exception as e:
        logging.error(e)
        return None