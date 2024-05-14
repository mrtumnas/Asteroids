# Asteroids
Recreation of the classic Asteroids game

Using W, A, S, and D to move the ship around the screen, and space to shoot. Dodge moving asteroids while trying to score points. Get hit 3 times and it's game over. If all asteroids are cleared, move to the next level with the number of asteroids increasing by one each time. This was my first full python project where I didn't completely follow a tutorial, however I still used plenty of stack overflow and other threads to learn the pygame library.

************************************************************
Changes to make in the future if I come back to this project
- Update sprites to look more like asteroids, adding multiple different ones that'll be randomly generated.
- Create a level display so the player knows how far they've made it
- Create a highscore log that'll save your highscores and load them when starting the game
- Fix the velocity bug for bullets, which causes them to have the ships velocity adding to them as the ship continues to move after firing them
- Add simple music and sound effects
- Create better hit detection. Currently everything uses rectangles so the collision isn't very accurate on the corners of the asteroids.
