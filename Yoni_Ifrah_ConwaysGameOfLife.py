import pygame
from pygame.constants import KEYUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT, \
                             K_p, K_q, K_ESCAPE, K_SPACE


def product(*args, repeat=1):
    """
    Here we use to find the cartesian product from the given args, the output is lexicographic ordered.
    The product is tuples that are emitted in sorted order.
    :param args:tuple, (-1, 0, 1)
    :param repeat:int, specify the number of repetitions
    """
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


class Life(object):

    def __init__(self, width, height):
        """
        initializing function
        :param width:int, the width of the screen
        :param height:int, the height of the screen
        """
        self.width = width
        self.height = height
        cells = (width + 2) * (height + 2)

        # Matrix of False
        self.live = [False] * cells

        # Matrix of True
        self.in_bounds = [True] * cells

        # Matrix of 0
        self.neighbours = [0] * cells

        for i in range(width + 2):
            self.in_bounds[i] = self.in_bounds[-i] = False
        for j in range(height):
            k = (j + 1) * (width + 2)
            self.in_bounds[k - 1] = self.in_bounds[k] = False
        self.neighbourhood = [y * (width + 2) + x
                              for x, y in product((-1, 0, 1), repeat=2)
                              if x or y]
        self.needs_update = set()

    def cell(self, x, y):
        """Return the cell number corresponding to the coordinates (x, y).
        :param:int, x which is width+2
        :param:int, y which is height+2
        """
        return (self.width + 2) * (y + 1) + x + 1

    def set(self, p, value):
        """Set cell number 'p' to 'value' (True=live, False=dead).
        :param:int, p
        :param:boolean: value
        """
        if value != self.live[p] and self.in_bounds[p]:
            self.live[p] = value
            self.needs_update.add(p)
            adjust = 1 if value else -1
            for n in self.neighbourhood:
                n += p
                if self.in_bounds[n]:
                    self.neighbours[n] += adjust
                    self.needs_update.add(n)

    def update(self, steps=1):
        """Updating the frame by 1 (step)."""
        for _ in range(steps):
            u = [(p, self.live[p], self.neighbours[p]) for p in self.needs_update]
            self.needs_update = set()
            for p, live, neighbours in u:
                if live and not 2 <= neighbours <= 3:
                    self.set(p, False)
                elif not live and neighbours == 3:
                    self.set(p, True)

    def paste(self, s, x, y):
        """
        paste the surfboard gun pattern on the top left corner at (x, y).
        :param s:string, surfboard_gun which is the life pattern when o = live, any other character = dead
        :param x:int, 8
        :param y:int, 1
        """
        # enumerate tracking the line with his j index
        for j, line in enumerate(s.strip().splitlines()):
            for i, char in enumerate(line.strip()):
                self.set(self.cell(x + i, y + j), char == 'o')


class PygameLife(Life):
    def __init__(self, width, height, background=pygame.Color('black'), foreground=pygame.Color('white'), cell_size=4):
        """
        initializing function
        :param width: int, 100
        :param height: int, 60
        :param background:pygame object for color representations, black
        :param foreground:pygame object for color representations, white
        :param cell_size:int, 4
        """
        super(PygameLife, self).__init__(width, height)

        self.background = background
        self.foreground = foreground
        self.cell_size = cell_size

    def draw(self):
        """
        Setting the color on screen according to the width, height, cells amd colors
        """
        screen = pygame.display.get_surface()
        screen.fill(self.background)
        c = self.cell_size
        for w in range(self.width):
            for h in range(self.height):
                if self.live[self.cell(w, h)]:
                    screen.fill(self.foreground, pygame.Rect(w * c, h * c, c, c))
        pygame.display.flip()

    def screen_cell(self, pos):
        """
        Return the cell number corresponding to screen position 'pos', or
        None if the position is out of bounds.
        :param:tuple, pos
        """
        x, y = pos
        x //= self.cell_size
        y //= self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cell(x, y)
        return None

    def run(self):
        """
        For Pause: K_SPACE = SPACE, K_p = p

        To Quit: K_ESCAPE = Esc, K_q = q
        """
        pygame.init()
        pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
        paused = False
        drawing = False
        running = True
        while running:
            for event in pygame.event.get():
                user_press = event.type

                # if the user pressed q or Esc the program will close
                if user_press == QUIT or user_press == KEYUP and event.key in (K_q, K_ESCAPE):
                    running = False

                # if the user pressed p or SPACE to pause
                elif user_press == KEYUP and event.key in (K_p, K_SPACE):
                    paused = not paused

                # if the user clicked on the mouse cases
                elif user_press == MOUSEBUTTONDOWN and event.button == 1:
                    paused = True
                    p = self.screen_cell(event.pos)
                    drawing = not self.live[p]
                    self.set(p, drawing)
                elif user_press == MOUSEMOTION and event.buttons[0]:
                    paused = True
                    self.set(self.screen_cell(event.pos), drawing)
            if paused:
                pygame.display.set_caption('Paused (SPACE/P to run)')
            else:
                pygame.display.set_caption('Conways Game Of Life')
                self.update()
            self.draw()
        pygame.quit()


def instructions():
    msg = """
    To Pause the game need to press:\n\tP or SPACE\n
    To Quit the game need to press:\n\tQ or Esc\n
    While the game is running\n\tThe user can click with the mouse on the screen in order to create more living cells
    Then will need to press SPACE or P to continue running
    """
    print(msg)


def main():
    surfboard_gun = '''
    ........................o...........
    ......................o.o...........
    ............oo......oo............oo
    ...........o...o....oo............oo
    oo........o.....o...oo..............
    oo........o...o.oo....o.o...........
    ..........o.....o.......o...........
    ...........o...o....................
    ............oo......................'''

    instructions()
    game = PygameLife(140, 120)
    game.paste(surfboard_gun, 8, 1)
    game.run()


if __name__ == '__main__':
    main()