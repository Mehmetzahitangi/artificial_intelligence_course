import pandas as pd
import plotly.express as px
from collections import defaultdict
import copy
import random

# Do not modify the line below.
countries = ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Falkland Islands", "Guyana", "Paraguay",
             "Peru", "Suriname", "Uruguay", "Venezuela"]

# Do not modify the line below.
colors = ["blue", "green", "red", "yellow"]


# check if a color is usable for a country
def constraint_adjacent(count, color, neighbors, assignment):

    for country in neighbors[count]:

        if country in assignment:

            if assignment[country] == color:
                return False

    return True


def mrv(constraint_problem, assignment):
    country = constraint_problem.unassigned[0]
    min = len(constraint_problem.possible_values(country, assignment))

    for value in constraint_problem.unassigned:

        if len(constraint_problem.possible_values(value, assignment)) < min:
            country = value
            min = len(constraint_problem.possible_values(value, assignment))

    return country


# Backtracking search function
def backtracking_search(constraint_problem):
    return backtracking({}, constraint_problem)





# Backtracking
def backtracking(assignment, constraint_problem):

    if len(constraint_problem.unassigned) == 0:
        return assignment

    # Get the country 
    country = mrv(constraint_problem, assignment)

    cp_list = constraint_problem.domains
    random.shuffle(cp_list)

    for color in cp_list:

        if constraint_problem.constraints(country, color, neighbors, assignment):
            assignment[country] = color
            constraint_problem.unassigned.remove(country)

            for neighbor in constraint_problem.neighbors[country]:
                if len(constraint_problem.possible_values(neighbor, assignment)) == 0:
                    return 'Failure'

            result = backtracking(assignment, constraint_problem)
            if result != 'Failure':
                return result


        if country in assignment:
            del assignment[country]
            constraint_problem.unassigned.append(country)

    return 'Failure'




# Constraint Satisfaction Problem
class constraint_problem:

    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.unassigned = variables
        self.initial = ()

    def possible_values(self, country, assignment):
        possible = copy.deepcopy(self.domains)
        
        for value in self.domains:
            if not self.constraints(country, value, self.neighbors, assignment):
                possible.remove(value)
        return possible

# Function to check the final result
def check(result, countries, colors):

    for key, value in result.items():

        if key not in countries:
            raise CountryNotFound(key)

        if value not in colors:
            ColorNotFound(value)


# Do not modify this method, only call it with an appropriate argument.
# colormap should be a dictionary having countries as keys and colors as values.
def plot_choropleth(colormap):
    fig = px.choropleth(locationmode="country names",
                        locations=countries,
                        color=countries,
                        color_discrete_sequence=[colormap[c] for c in countries],
                        scope="south america")
    fig.show()



# Implement main to call necessary functions
if __name__ == "__main__":

    counts = copy.deepcopy(countries)

    # Neighborhood dictionary
    neighbors = defaultdict(list)

    # Adding neighbors into the dictionary:
    neighbors['Argentina'] = ['Bolivia', 'Brazil', 'Chile', 'Paraguay', 'Uruguay']
    neighbors['Bolivia'] = ['Argentina', 'Brazil', 'Chile', 'Paraguay', 'Peru']
    neighbors['Brazil'] = ['Argentina', 'Bolivia', 'Colombia', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela']
    neighbors['Chile'] = ['Argentina', 'Bolivia', 'Peru']
    neighbors['Colombia'] = ['Brazil', 'Ecuador', 'Peru', 'Venezuela']
    neighbors['Ecuador'] = ['Colombia', 'Peru']
    neighbors['Falkland Islands'] = []
    neighbors['Guyana'] = ['Brazil', 'Suriname', 'Venezuela']
    neighbors['Paraguay'] = ['Argentina', 'Bolivia', 'Brazil']
    neighbors['Peru'] = ['Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador']
    neighbors['Suriname'] = ['Brazil', 'Guyana']
    neighbors['Uruguay'] = ['Argentina', 'Brazil']
    neighbors['Venezuela'] = ['Brazil', 'Colombia', 'Guyana']

    


    csp_outputs = constraint_problem(counts, colors, neighbors, constraint_adjacent)

    # Backtracking search 
    result = backtracking_search(csp_outputs)

    check(result, countries, colors)
    print("Our code result")
    plot_choropleth(colormap=result)


    
    # coloring test
    colormap_test = {"Argentina": "blue", "Bolivia": "red", "Brazil": "yellow", "Chile": "yellow", "Colombia": "red",
                     "Ecuador": "yellow", "Falkland Islands": "yellow", "Guyana": "red", "Paraguay": "green",
                     "Peru": "green", "Suriname": "green", "Uruguay": "red", "Venezuela": "green"}
    
    print("Result that on the PDF")
    plot_choropleth(colormap=colormap_test)


# Errors

class ColorNotFound(Exception):
    def __init__(self, color):
        print("{} does not exist!".format(color))

class CountryNotFound(Exception):
    def __init__(self, country):
        print("{} does not exist!".format(country))


