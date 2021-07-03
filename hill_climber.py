import requests

url = "http://127.0.0.1:5000/hillclimber"

def random():
    i = 0
    while i < 1000:
        i += 1
        current_score = 0
        requests.get(f"http://127.0.0.1:5000/hillclimber?name=random_player&move=random")

def hill_climber():
    i = 0
    while i < 1000:
        i += 1
        current_score = 0
        response = requests.get(f"http://127.0.0.1:5000/hillclimber?name=hill_climber&move=random")
        score = response.json()['score']
        if score > current_score:
            current_score = score
        else:
            requests.get(f"http://127.0.0.1:5000/hillclimber?name=hill_climber&move=cancel")

# Now implement: Simulated annealing ;)

random()
hill_climber()