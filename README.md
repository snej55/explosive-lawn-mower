# Explosive Lawn Mower Simulator

This project is an overengineered lawn mower simulator. It was made for the Hackclub Scrapyard Hackathon on the 15th of March 2025.

![https://github.com/snej55/explosive-lawn-mower/blob/master/screenshot0.png](https://github.com/snej55/explosive-lawn-mower/blob/master/Screenshot%202025-03-15%20194840.png)

## How does it work?

It was made using python and pygame-ce, with pymunk for the physics, and uses spritestacks to create a 3d effect for the objects in the game. It uses a tile based system to cache and render the grass, allowing the world to contain over 400,000 blades of grass!

## Play (Easy):

You can download the compiled binary from here: [ELMS Compiled](https://github.com/snej55/exploding_lawn_mower_compiled)

### Run it yourself:

If you're not on windows, no worries! It's as simple as download the code as a zip from github and extracting it or cloning it,
```
git clone https://github.com/snej55/explosive-lawn-mower.git
```
Then install the requirements.txt using pip:
```
pip3 install -r requirements.txt
```
And run it!
```
python3 main.py
```

## Controls:
Arrow keys 

R to mow the lawn

## DISCLAIMER:

This project was developed with a (relatively) beefy computer. If yours isn't, it might struggle to render all of the grass. If it does struggle, try decreasing the `DENSITY` value in `src/grass.py` (or experiment with `TILE_SIZE` in `src/bip.py`).
