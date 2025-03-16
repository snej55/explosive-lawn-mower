# Explosive Lawn Mower Simulator

This project is an overengineered lawn mower simulator.

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
