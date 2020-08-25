# 2D Tower Defence
Tower defense game written in Python 3 using Pygame.

Enemies will come at you in waves. Deploy towers to defend yourself, and kill the enemies as they come. You make money for every enemy killed which you can then use to place more towers. More enemies will come at you every wave.

## Requirements
 - Python 3.5.3 or newer
 - Pygame 1.9.3 or newer
 
 ## Installation Instructions
 1. Clone this repository
 2. Create a new virtual environment in this directory
 3. Install the dependencies with `pip install -r requirements.txt`
 4. To launch the game run `python Main.py`
 
 ### Note about MacOS
 To make Pygame run on MacOS, some extra steps are required. See the [official documentation](https://www.pygame.org/wiki/GettingStarted#Mac%20installation) for more information.
 
 ## How To Play
 - At the main menu press the Play button. This will launch a new game. 
 - You can place towers with left click anywhere a white square appears.
 - You can sell a tower with right click. 
 - To start a wave press the Start Wave button in the top left.
 - The wave number, number of enemies left, number of lives left and your money is all displayed at the top of the screen.
 - There is also a pause button at the top of the screen.
 - There is a shop on the right to choose the tower you would like to place. Click the name of a tower to select it. Hover your mouse over it to show a description.

## Screenshots
### Main Menu
![Main Menu](/screenshots/mainmenu.png)

### Game Screen
![Game Screen](/screenshots/gamescreen.png)
![Action shot](/screenshots/towershooting.png)

### The Shop
![The Shop](/screenshots/shop.png)

### Game Over
![Game Over](/screenshots/gameover.png)
