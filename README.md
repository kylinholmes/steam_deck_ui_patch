# steam_deckui_patch

The Deck UI patch will patch the regular desktop steam to look like the brand new SteamDeck UI.
This patch tool currently works on Linux (Flatpak and Regular) as well as Windows.
If the patch tool cannot find your working steam directory you can manually supply your own.

### Usage
```
usage: deckuipatch.py [-h] [-r] [-f] [-l] [path]

Patches the steamdeck UI into desktop steam.

positional arguments:
  path           Path to your local steam install.

options:
  -h, --help     show this help message and exit
  -r, --remove   Removes the steamdeck ui patch from
                 steam.
  -f, --flatpak  Tells the patch tool to look for a
                 flatpak install of steam.
  -l, --launch   Launches steam in deck mode after patch.
```

### Select your own path
```
python3 deckuipatch.py "/path/to/steam"
```

##### Link to source: https://www.reddit.com/r/SteamDeck/comments/t57l4t/how_to_get_the_steam_deck_ui_on_windowsany_linux/
