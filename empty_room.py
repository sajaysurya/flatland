'''
Simple gridworld as shown in the ascii art below

Key for ascii art
# - wall
O - player location
X - goal location

Has a separate goal drape. This is visible to the human player, but is
implemented such that the agent doesn't know that this is the goal.

Reward:
    -1  : for actions
    100 : for goal
'''

import curses
from pycolab import ascii_art
from pycolab import human_ui
from pycolab import things as plab_things
from pycolab.prefab_parts import sprites as prefab_sprites


GRID_WORLD = ['#################',
              '# O           X #',
              '#               #',
              '#               #',
              '#               #',
              '#               #',
              '#               #',
              '#               #',
              '#               #',
              '#################']


def make_game():
    '''
    builds the game and returns the engine
    '''
    return ascii_art.ascii_art_to_game(
        GRID_WORLD,
        what_lies_beneath=' ',  # space character
        sprites={'O': PlayerSprite},
        drapes={'X': GoalDrape},
        update_schedule=['O', 'X'],
        z_order='XO')


class PlayerSprite(prefab_sprites.MazeWalker):
    '''
    Class for player

    Defines movements and associated rewards
    '''

    def __init__(self, corner, position, character):
        '''
        initialize as per superclass instructions and make walls impassable
        '''
        super(PlayerSprite, self).__init__(
            corner, position, character, impassable='#')

    def update(self, actions, board, layers, backdrop, things, the_plot):
        del backdrop, things, layers  # Unused

        if actions == 0:    # go north
            the_plot.add_reward(-1.0)
            self._north(board, the_plot)
        elif actions == 1:  # go south
            the_plot.add_reward(-1.0)
            self._south(board, the_plot)
        elif actions == 2:  # go west
            the_plot.add_reward(-1.0)
            self._west(board, the_plot)
        elif actions == 3:  # go east
            the_plot.add_reward(-1.0)
            self._east(board, the_plot)
        elif actions == 4:  # stay (for human player)
            self._stay(board, the_plot)
        if actions == 5:    # quit (for human player)
            the_plot.terminate_episode()


class GoalDrape(plab_things.Drape):
    '''
    Class for Goal
    '''

    def update(self, actions, board, layers, backdrop, things, the_plot):
        '''
        Handles reward and termination
        '''
        # find player position
        player_pattern_position = things['O'].position

        # If the curtain is raised
        if self.curtain[player_pattern_position]:
            # reward for reaching goal
            the_plot.add_reward(100)
            # lower the curtain
            self.curtain[player_pattern_position] = False
            # terminate episode
            the_plot.terminate_episode()


def main():
    '''
    C-style main function
    '''

    # Build the game
    game = make_game()

    # Create user interface
    user_interface = human_ui.CursesUi(
        keys_to_actions={curses.KEY_UP: 0,
                         curses.KEY_DOWN: 1,
                         curses.KEY_LEFT: 2,
                         curses.KEY_RIGHT: 3,
                         -1: 4,  # for dummy stayput action
                         'q': 5, 'Q': 5},
        delay=200)

    # Run the game
    user_interface.play(game)


if __name__ == '__main__':
    main()
