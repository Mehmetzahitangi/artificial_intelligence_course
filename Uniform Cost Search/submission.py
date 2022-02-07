import csv
from queue import PriorityQueue
from collections import defaultdict
import sys


class CityNotFoundError(Exception):
    def __init__(self, city):
        print("{} does not exist" .format(city))


class CitiesSameError(Exception):
    def __init__(self):
        print("Your Starting and Target cities can not be same.")


# Implement this function to read data into an appropriate data structure.
def build_graph(path):
    graph = Graph_Part()
    all_cities = []
    
    # read road map file
    with open(path, newline='', encoding="utf8") as roads:
        reader = csv.DictReader(roads)
        
        for row in reader:
            city1 = row['city1']
            city2 = row['city2']
            distance = row['distance']

            if city1 not in all_cities:
                all_cities.append(city1)
                
            if city2 not in all_cities:
                all_cities.append(city2)

            graph.edges[city1].append(city2)
            graph.edges[city2].append(city1)
            graph.costs[cost_key(city1, city2)] = distance
            
    return graph, all_cities


# Implement this function to perform uniform cost search on the graph.
def uniform_cost_search(graph, start, end):
    frontier = PriorityQueue()
    explored = set()
    frontier.put((0, start, [start]))

    while frontier.not_empty:
        cost, state, cost_path = frontier.get()
        explored.add(state)

        if state == end:
            minimum_cost = cost
            print("The shortest path for you: " + str(cost_path))
            print("Distance = " + str(minimum_cost))
            return "Distance is calculated"
           

        for neighbor in graph.neighbors(state):
            if neighbor not in explored:
                neighbor_cost = cost + int(graph.get_cost(state, neighbor))
                frontier.put((neighbor_cost, neighbor, cost_path + [neighbor]))

    return "There is a trouble"



class Graph_Part:

    def __init__(self):
        self.edges = defaultdict(list)
        self.costs = {}

    def get_cost(self, starting_city, target_city):
        
        return self.costs[(cost_key(starting_city, target_city))]
    

    def neighbors(self, vertex):
        return self.edges[vertex]



def cost_key(city1, city2):
    cities = [city1, city2]
    cities.sort() # alphabetical  order the two cities
    sorted_cities = cities[0] + cities[1]

    return sorted_cities


# Implement main to call functions with appropriate try-except blocks
if __name__ == "__main__":
    
    try:
        print("Welcome the distance calculate app.\n")
        
        file_path = input('Please enter the road map file path: ')
        
        graph, all_cities = build_graph(file_path)

        starting_city = input('Please enter your starting city: ') 
        
        if starting_city in all_cities:
            print("The city is exist")
        else:
            raise CityNotFoundError(starting_city)
            
        target_city = input('Please enter your target city: ') 
        
        if target_city in all_cities:
            print("The city is exist")
        else:
            raise CityNotFoundError(target_city)

        if starting_city == target_city:
            print("Your Starting and Target cities can not be same.") 
            sys.exit()
            
        uniform_cost_search(graph, starting_city, target_city)
    

    except CityNotFoundError:
        print('Please try with a valid city')
        
    except FileNotFoundError:
        print("File not found!")
        
