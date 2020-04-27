from arcade import Window, Sprite, SpriteList, \
    load_texture, start_render, draw_text, color
import arcade
from entities import Background
from pyglet.gl import GL_NEAREST

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class EnumGameState:
    title = 0
    game = 1
    game_over = 2

class MyGame(Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.char_list = None
        self.shoot_list = None
        self.particule_list = None
        self.background = None
        self.sky_list = None
        self.score_list = None
        self.life_list = None
        self.ship = None

        # Set up other settings
        self.score = 0
        self.time = 0
        self.frame = 0
        self.fps = 0
        self.combo = 0
        self.life = 3
        self.music = None
        self.music_timer = 0

    def setup(self):

        self.background = SpriteList()
        self.sky_list = SpriteList()
        self.particule_list = SpriteList()
        self.ship_list = SpriteList()
        self.score_list = SpriteList()
        self.life_list = SpriteList()

        # Set up lane 1
        ship_texture = []
        for i in range(6):
            ship_texture.append(
                load_texture(f"qs../ressources/E_Run_{i+1}.png")
            )

        ship = Sprite("../ressources/E_Run_1.png",
                      center_x=SCREEN_WIDTH//10,
                      center_y=SCREEN_HEIGHT//2,
                      scale= 2)
        self.ship = ship
        self.ship_list.append(ship)

        for tier in range(3):

            background = Background("../ressources/E_Sky_1.png", SCREEN_WIDTH)
            background.center_y = ((SCREEN_HEIGHT // 3) * tier + 1) + 100
            background.center_x = SCREEN_WIDTH // 2
            background.change_x = - 2
            self.background.append(background)

            background = Background("../ressources/E_Sky_1.png", SCREEN_WIDTH)
            background.center_y = ((SCREEN_HEIGHT // 3) * tier + 1) + 100
            background.center_x = SCREEN_WIDTH + SCREEN_WIDTH // 2
            background.change_x = - 2
            self.background.append(background)

        for tier in range(3):
            sky = Background("../ressources/E_Sky_2.png", SCREEN_WIDTH)
            sky.center_y = ((SCREEN_HEIGHT // 3) * tier + 1) + 100
            sky.center_x = SCREEN_WIDTH // 2
            sky.change_x = - 6
            self.sky_list.append(sky)

            sky = Background("./ressources/E_Sky_2.png", SCREEN_WIDTH)
            sky.center_y = ((SCREEN_HEIGHT // 3) * tier + 1) + 100
            sky.center_x = SCREEN_WIDTH + SCREEN_WIDTH // 2
            sky.change_x = - 6
            self.sky_list.append(sky)

        # Set up life system
        self.life = 3
        life_pos = [SCREEN_WIDTH // 2 + 40, SCREEN_HEIGHT - 30]
        for life_sprite in range(self.life):
            self.life_list.append(Sprite("../ressources/Life_Orb.png",
                                                center_x=life_pos[0],
                                                center_y=life_pos[1]))
            life_pos[0] += 40

        # Set up Combo and Score and difficulty
        self.score_list.append(Sprite("../ressources/Score_Box.png",
                                             center_x=700,
                                             center_y=560,
                                             scale=1.2))
        self.score = 0
        self.combo = 0
        self.time = 0
        self.frame = 0
        self.fps = 0

    def on_draw(self):
        """
        Function to draw the game (on_draw)
        """
        start_render()

        # Draw all the sprites (order determine Z axis)
        self.sky_list.draw(filter=GL_NEAREST)
        self.background.draw(filter=GL_NEAREST)
        self.particule_list.draw(filter=GL_NEAREST)
        self.ship_list.draw(filter=GL_NEAREST)
        self.score_list.draw(filter=GL_NEAREST)
        self.life_list.draw(filter=GL_NEAREST)

        # Put the text on the screen.
        output = f"{self.score}"
        draw_text(output, 693, 560, color.DARK_RED, 15)
        combo = f"{self.combo}"
        draw_text(combo, 693, 542, color.DARK_RED, 15)

        # Put the fps on the bottom left
        fps = f"FPS: {self.fps}"
        draw_text(fps, 730, 10, color.YELLOW, 14)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        if key == arcade.key.UP:
            self.ship.change_y += 5
        elif key == arcade.key.DOWN:
            self.ship.change_y -= 5
        elif key == arcade.key.LEFT:
            self.ship.change_x -= 5
        elif key == arcade.key.RIGHT:
            self.ship.change_x += 5
        elif key == arcade.key.SPACE:
            particule = Sprite("../ressources/Life_Orb.png",
                               center_x=self.ship.right,
                               center_y=self.ship.center_y)
            particule.change_x = 3
            self.particule_list.append(particule)

    def on_key_release(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            self.ship.change_y = 0
        elif key == arcade.key.DOWN:
            self.ship.change_y = 0
        elif key == arcade.key.LEFT:
            self.ship.change_x = 0
        elif key == arcade.key.RIGHT:
            self.ship.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.time += delta_time
        self.frame += 1
        if self.time >= 1:
            self.fps = self.frame
            self.frame = 0
            self.time = 0

        # Update Sprite_Lists
        self.sky_list.update()
        self.background.update()
        self.score_list.update()
        self.ship_list.update()
        self.particule_list.update()
        self.life_list.update()

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "3 Keys on the Run")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
