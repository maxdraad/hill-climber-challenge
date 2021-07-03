# hill-climber-challenge (alpha version)

This repository is made to host a challenge to implement a hill climbing/similated annealing algorithm in a virtual 3D world.

Your players have to do this by navigating through a virtual 3d world via an API. The goal is to reach the highest point in this world.
They get dropped randomly and only know the height of their current position.

Players can interact with the api by making a random move (and cancelling without penalty), or moving in any direction(north/east/south/west), 
or move to a specific coordinate using moveto(x,y). They do this by doing a simple get request containing their player name. They will get their score (height) returned to use for their game strategy.

**Main components of this repo, for now just run the file:**
- hosting.py: You will use this to host the game. Also contains the game logic.
- hill_climber.py: An example of how to interact with the api
- generate_world.py: Generates a 3d landscape from random noise. Code mostly copied from a repo I forgot
- plot_3d_word.py: See a 3d representation of the world you just generated

**Quick start:**
- First run hosting.py
- Then run hill_climber.py to simulate both random behaviour and a simple hill climber
- Check the scoreboard on the main host to see how the strategies compare

Have fun :)
