"""
iou.py
~~~~~~
Calculates the amount of money each person owes for utilites based on the
amount they paid for each utility.
"""
import argparse
import math
import json
import sys


def entrypoint(config):
    """
    Entrypoint into utilities calculations. Reads the utilities from config
    and calculates who owes who.

    Parameters
    ----------
    config : str
        The path to that months config file.
    """
    utilities = read_config(config)
    split_the_difference(utilities)


def read_config(config):
    """
    Reads the file that the string config points to. Should be a JSON file.
    Returns the data stored in the config as a dict.

    Parameters
    ----------
    config : str
        The path that months config file.

    Returns
    -------
    dict
        The configuration in a dictionary.
    """
    try:
        with open(config, "rb") as config_file:
            return json.loads(config_file.read())
    except FileNotFoundError:
        print("Config file could not be loaded in, check the provided path.")
        sys.exit(1)


def split_the_difference(utilities):
    """
    Splits the difference between the parties

    Parameters
    ----------
    utilities : dict
        The utilities and their values in a dictionary.
    """
    utils_grand_total = get_utils_total(utilities)
    print(f"\n{'#' * 80}\n")
    print(f"The grand total for utilities this month was: $ {zformat(utils_grand_total)}\n")
    individual_paid = get_individuals_paid(utilities)
    each_owe = split_total(utils_grand_total, split_by=len(utilities.keys()))
    print(f"Splitting this evenly results in everyone paying {each_owe}\n")
    i_o_u(individual_paid, each_owe)
    print(f"\n{'#' * 80}\n")


def get_utils_total(utilities):
    """
    Calculates the grand total for that months utilities.

    Parameters
    ----------
    utilities : dict
        The utilities and their values in a dictionary

    Returns
    -------
    int
        The total cost of utilities for a month
    """
    total = 0
    for utils in utilities.values():
        total += math.fsum(utils.values())
    return round(total, 2)


def get_individuals_paid(utilities):
    """
    Returns how much an invidual paid for their utilities

    Parameters
    ----------
    utilities : dict
        The utilities and their values in a dictionary

    Returns
    -------
    dict
        The individuals and what they paid as the value.
    """
    indivs = {}
    for indiv in utilities:
        indivs[indiv] = sum(utilities[indiv].values())
    return indivs


def get_paid_most(individuals):
    """
    Returns whoever paid the most based on their total for the month

    Parameters
    ----------
    individuals : dict
        A dictionary of individuals and how much money they spent.

    Returns
    -------
    str
        The name of who paid the most.
    """
    return max(individuals, key=lambda key: individuals[key])


def get_paid_least(individuals):
    """
    Returns whoever paid the least based on their total for the month

    Parameters
    ----------
    individuals : dict
        A dictionary of individuals and how much money they spent.

    Returns
    -------
    str
        The name of who paid the least.
    """
    return min(individuals, key=lambda key: individuals[key])


def split_total(total, split_by):
    """
    Splits the total by however many are included in split_by.

    Parameters
    ----------
    total : int
        The grand total for utilities
    split_by : int
        The number of individuals to split the cost by.

    Returns
    -------
    list
        A list of what the even split should be.
    """
    separated = str(total / split_by).split(".")
    integer = int(separated[0])
    decimal = int(separated[1])
    if decimal > 100:
        rounded_dec = int(float("." + str(decimal)) * 100) / 100
        owes = [integer + rounded_dec for i in range(split_by - 1)]
        owes.append(round(integer + rounded_dec + 0.01, 2))
        return owes
    return [integer + float("." + str(decimal)) for i in range(split_by)]


def i_o_u(indiv_paid, each_owe):
    """
    Figures out who owes who how much. and prints the results.

    Parameters
    ----------
    indiv_paid : dict
        The individuals and how much they paid.
    each_owe : list
        The equal split for the month.
    """
    owed, indebted = get_owed_indebted(indiv_paid, each_owe)
    print()
    for debtor in indebted:
        print(f"{debtor} owes:")
        for owes, value in owed.items():
            if value > 0:
                # Debtor has paid off their debt, move on to the next debtor.
                if indebted[debtor] == 0:
                    break
                if indebted[debtor] >= value:
                    print(f"\t{owes} $ {zformat(round(value,2))} for this month's utilities.")
                    indebted[debtor] = indebted[debtor] - value
                    owed[owes] = value - value
                else:
                    print(f"\t{owes} $ {zformat(round(indebted[debtor], 2))} for this months utilites.")
                    owed[owes] = value - indebted[debtor]
                    indebted[debtor] = 0


def get_owed_indebted(indiv_paid, each_owe):
    """
    Returns dictionaries of who is owed money and how much and who owes
    money and how much.

    Parameters
    ----------
    indiv_paid : dict
        The individuals and how much they paid.
    each_owe : list
        The equal split for the month.

    Returns
    -------
    dict
        A dictionary sorted by values of who is owed how much.
    dict
        A dictionary sorted by values of who owes how much.
    """
    owed = {}
    indebted = {}
    for indiv, paid in indiv_paid.items():
        if paid > each_owe[0]:
            owed[indiv] = round(paid - each_owe[0], 2)
            print(
                f"{indiv} paid $ {zformat(paid)} and is owed "
                f"$ {zformat(round(paid - each_owe[0], 2))} for this months utilities."
            )
        elif indiv == get_paid_least(indiv_paid):
            indebted[indiv] = round(each_owe[-1] - paid, 2)
            print(
                f"{indiv} paid $ {zformat(paid)} and owes "
                f"$ {zformat(round(each_owe[-1] - paid, 2))} for this months utitlities."
            )
        else:
            indebted[indiv] = round(each_owe[0] - paid, 2)
            print(
                f"{indiv} paid $ {zformat(paid)} and owes "
                f"$ {zformat(round(each_owe[0] - paid, 2))} for this months utitlities."
            )
    return sort_by_value(owed), sort_by_value(indebted)

def sort_by_value(dictionary):
    """
    Sorts a dictionary by its values.

    Parameters
    ----------
    dictionary : dict
        A dictionary to sort by value.
    
    Returns
    -------
    dict
        The same dictionary sorted by values.
    """
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}

def zformat(num):
    """
    Formats a number to have 2 decimal places for money purposes

    Parameters
    ----------
    num : float
        A number to format

    Returns
    -------
    str
        A money formatted version of the number
    """
    split_num = str(num).split(".")
    number_part = split_num[0]
    try:
        decimal = split_num[1]
        if len(decimal) < 2:
            decimal = decimal.ljust(2, "0")
        return f"{number_part}.{decimal}"
    except IndexError:
        return f"{number_part}.00"


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "-c",
        "--config",
        type=str,
        dest="config",
        required=True,
        help=(
            "This argument should be used to provide a JSON config file to the script."
            "Config files should have the individuals who pay utilities as keys and the"
            "utilities and amounts they paid for the month. Use a single config file for"
            "a month."
        ),
    )
    ARGS = PARSER.parse_args()
    entrypoint(ARGS.config)
