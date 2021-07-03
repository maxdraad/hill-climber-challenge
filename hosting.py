import flask
from flask import request, jsonify
import random
import pandas as pd

#https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    score_board = pd.DataFrame({'name': [player.get_name() for player in players],
                                'high score': [player.get_score() for player in players]})
    return f"<h1>Scoreboard</h1>" \
           f"<p><br>{score_board.sort_values(by=['high score'], ascending=False).to_html()}</p>"

class Player:
    def __init__(self, name, grid, starting_pos):
        self.name = name
        self.coords = starting_pos
        self.last_node = starting_pos
        self.tried_moves = []
        self.move_set = False
        self.steps = 0
        self.opposite_moves = {
            'north': 'south',
            'south': 'north',
            'west' : 'east',
            'east' : 'west'
        }
        self.grid = grid
        self.grid_limit = 100
        self.steps_limit = 1000

    def move_to(self, x, y):
        distance = abs(self.coords[0] - x) + abs(self.coords[1] - y)
        if (self.steps + distance) < self.steps_limit:
            self.steps += distance
            self.coords = [x, y]
            self.last_node = [x, y]
            self.move_set = False
            self.tried_moves = []


    def move(self, move):
        # if (0 <= self.coords[0] <= self.grid_limit) and (0 <= self.coords[1] <= self.grid_limit):
        if self.steps < 1000:
            self.steps += 1
            self.last_node = self.coords.copy()
            if move == 'north':
                self.coords[1] = self.coords[1] + 1
            elif move == 'south':
                self.coords[1] = self.coords[1] - 1
            elif move == 'west':
                self.coords[0] = self.coords[0] - 1
            elif move == 'east':
                self.coords[0] = self.coords[0] + 1

    def random_move(self):
        all_moves = ['north', 'west', 'south', 'east']
        unvisited_moves = list(set(all_moves) - set(self.tried_moves))
        move = random.choice(unvisited_moves)
        if self.move_set == True:
            self.last_node = self.coords.copy()
            self.tried_moves = [self.opposite_moves[move]]
            self.move_set = False
        else:
            self.move_set = True
            self.tried_moves.append(move)
        self.move(move)


    def cancel(self):
        if len(self.tried_moves) == 4:
            self.tried_moves = []
            # self.steps -= 3
        if len(self.tried_moves) == 1:
            self.tried_moves = [self.opposite_moves[self.tried_moves[0]]]
        self.move_set = False
        self.coords = self.last_node

    def get_json(self):
        return {
            'x': self.coords[0],
            'y': self.coords[1],
            'step': self.steps,
            'score': self.get_score()
        }

    def get_name(self):
        return self.name

    def get_coords(self):
        return self.coords

    def get_score(self):
        try:
            score = self.grid.loc[(self.grid['x'] == self.coords[0]) & (self.grid['y'] == self.coords[1])]['z'].values[0]
        except:
            score = -1
        return score


    def get_all_debug(self):
        return f"Name: {self.name}, Coord: {self.coords}, last node: {self.last_node}" \
               f", tried moves: {self.tried_moves}, move set: {self.move_set}, steps: {self.steps}, score: {self.get_score()}"

players = []
grid = pd.read_csv("hillclimber.csv")

@app.route('/hillclimber', methods=['GET'])
def step():
    name = request.args['name']
    current_player = None
    for player in players:
        if name == player.get_name():
            current_player = player
    if not current_player:
        new_player = Player(name, grid, [45, 22])
        players.append(new_player)
        current_player = new_player
    return move(current_player)

def move(current_player):
    move = request.args['move']
    if move == 'random':
        current_player.random_move()
    elif move == 'cancel':
        current_player.cancel()
    elif move in ['north', 'west', 'south', 'east']:
        current_player.move(move)
    elif move == 'moveto':
        current_player.move_to(int(request.args['x']), int(request.args['y']))
    # print(current_player.get_all_debug())
    # return jsonify([current_player.get_score()])
    return jsonify(current_player.get_json())


app.run()