from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.videoplayer import VideoPlayer
from project4 import*


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) # returns a temporary object of the superclass, which allows you to call its methods.
        # Create a background image and adds it to the screen
        bg_img = Image(source='images/menu/background_menu.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(bg_img)

        # Create an image with the text "TIC TAC TOE" and adds it to the screen
        img = Image(source='images/menu/tictactoe_Label.png', size_hint=(0.8, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.85}, allow_stretch=True, keep_ratio=False)
        self.add_widget(img)

        # Create a button and an image with the text "Play" and adds it to the screen
        img = Image(source='images/menu/play_button.png', size_hint=(0.4, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.45}, allow_stretch=True, keep_ratio=False)
        button = Button(size_hint=(.4, .3), pos_hint={"center_x": 0.5, "center_y": 0.45}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_screen(name='Game', direction='up'))
        self.add_widget(img)
        self.add_widget(button)

        # Create a button and an image of the Setting and adds it to the screen
        img = Image(source='images/settings/setting_image.png', size_hint=(0.1, 0.1), pos_hint={'x': 0.9, 'y': 0.9})
        button = Button(size_hint=(.1, .1), pos_hint={"x": 0.9, "y": 0.9}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_screen(name='Settings', direction='left'))
        self.add_widget(button)
        self.add_widget(img)

        # Create a button and an image with the text "Instructions" and adds it to the screen
        img = Image(source='images/instaructions/instaructions_button.png', size_hint=(0.6, 0.15), pos_hint={'center_x': 0.5, 'center_y': 0.15}, allow_stretch=True, keep_ratio=False)
        button = Button(size_hint=(.6, .15), pos_hint={"center_x": 0.5, "center_y": 0.15}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_screen(name='Instructions', direction='right'))
        self.add_widget(img)
        self.add_widget(button)

    def change_screen(self, name, direction): # gets a name of a screen and a direction and go to that screen in this direction
        self.manager.transition.direction = direction
        self.manager.transition.duration = 2
        self.manager.current = name


class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) # returns a temporary object of the superclass, which allows you to call its methods.
        # Create the backGround of the screen
        bg_img = Image(source='images/instaructions/background_instructions.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'y': 0})
        self.add_widget(bg_img)

        # Create a video and adds it to the screen
        self.video = VideoPlayer(source='images/instaructions/instructions_video.mp4', options={'eos': 'loop'}, size_hint=(0.9, 0.45), pos_hint={'center_x': 0.5, 'y': 1/3})
        self.add_widget(self.video)

        # Create an image with the text 'Instructions' and add it to the screen
        img = Image(source='images/instaructions/instaructions_image.png', size_hint=(1/2, 0.2), pos_hint={'center_x': 1 / 2, 'y': 0.8}, allow_stretch=True, keep_ratio=False)
        self.add_widget(img)


        # 1/3 of the screen will be a scrollview
        self.scroll = ScrollView(size_hint=(1, 1/3), pos_hint={'center_x': 0.5, 'y': 0})
        self.add_widget(self.scroll)

        # Create a floatlayout for the scrollview part of the screen
        self.scroll.layout = FloatLayout(size_hint=(1, 4))
        self.scroll.add_widget(self.scroll.layout)

        # Create a label with the text NOTE... and add it to the screen scroll layout
        label = Label(text='*NOTE: this is a ScrollView page!', halign='center', pos_hint={"center_x": 0.5, "center_y": 0.98}, font_size=24, color=(1, 0, 0, 1), bold=True)
        self.scroll.layout.add_widget(label)

        # Create the instructions text and adds it to the screen scroll layout
        label = Label(text='The Rules of the game : \n To WIN you need four zeros connected in a row in a column or in a diagonal \n To LOSE the computer need four x\'s connected in a row in a column or in a diagonal\n If you won, lost or scored a draw the message will apper on the screen', halign='center', pos_hint={"center_x": 0.5, "center_y": 0.9}, font_size=18, color=(1, 1, 1, 1))
        self.scroll.layout.add_widget(label)

        label = Label(text='The Menu Screen: \n To go to the Instructions Screen press with your mouse on the "Instructions" image \n To go to the Game Screen press with your mouse on the "Play" image', halign='center', pos_hint={"center_x": 0.5, "center_y": 0.75}, font_size=18, color=(1, 1, 1, 1))
        self.scroll.layout.add_widget(label)

        label = Label(text='The Instructions Screen: \n To go to the Menu Screen press with your mouse on the "Menu" image', halign='center', pos_hint={"center_x": 0.5, "center_y": 0.6}, font_size=18, color=(1, 1, 1, 1))
        self.scroll.layout.add_widget(label)

        label = Label(text='The Game Screen: \n To go to the Menu Screen press with your mouse on the "Menu" image\n To start a new game press with your mouse on the "Reset" label\n To place your pick press with your mouse on the cell you want to pick', halign='center', pos_hint={"center_x": 0.5, "center_y": 0.45}, font_size=18, color=(1, 1, 1, 1))
        self.scroll.layout.add_widget(label)

        label = Label(text='The Settings Screen: \n To go to the Menu Screen press with your mouse on the "Menu" image \n To change the color of your player, click on the arrows below the label "choose your player"\n To change the color of the computer player, click on the arrows below the label "choose the computer player"\n To decide who will play first click on the button to the right of the label "select"\n To decide THE LEVEL of the game click on the arrow\'s to the right of the label "difficulty" (right - harder, left - easier)', halign='center', pos_hint={"center_x": 0.5, "center_y": 0.3}, font_size=16, color=(1, 1, 1, 1))
        self.scroll.layout.add_widget(label)

        # Create a button and an image with the text 'menu' and adds it to the screen scroll layout
        img = Image(source='images/menu/menu_image.png', size_hint=(1 / 3, 0.15), pos_hint={'center_x': 0.5, 'y': 0.01}, allow_stretch=True, keep_ratio=False)
        button = Button(size_hint=(1 / 3, .15), pos_hint={"center_x": 0.5, "y": 0.01}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_screen(name='menu', direction='left'))
        self.scroll.layout.add_widget(button)
        self.scroll.layout.add_widget(img)

    def change_screen(self, name, direction): # gets a name of a screen and a direction and go to that screen in this direction
        self.manager.transition.direction = direction
        self.manager.transition.duration = 2
        self.manager.current = name

    def on_pre_leave(self): # when ever you leave the screen the video will pause
        self.video.state = "pause"


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) # returns a temporary object of the superclass, which allows you to call its methods.

        self.levels = ['images/settings/easy_image.png', 'images/settings/medium_image.png', 'images/settings/hard_image.png']  # array with all the images of the difficulty level

        self.colors = ['black', 'blue', 'dark_blue', 'dark_green', 'gold', 'gray', 'green', 'light_blue', 'light_green', 'olive', 'oreng', 'pink', 'purpel', 'red', 'yellow']
        self.x_images = [f'images/settings/x_images/x_picture_{color}.png' for color in self.colors]  # array with all the images of the X player
        self.x_indicts = 0  # indicts which x_image to use

        self.o_images = [f'images/settings/o_images/o_picture_{color}.png' for color in self.colors]  # array with all the images of the O player
        self.o_indicts = 0  # indicts which o_image to use

        # Create a background image and adds it to the screen
        bg_img = Image(source='images/settings/background_settings.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(bg_img)

        # Create an image of the difficulty and adds it to the screen
        img = Image(source='images/settings/difficulty_image.png', pos_hint={'center_x': 0.15, 'center_y': 0.85}, size_hint=(0.2, 0.2), allow_stretch=True, keep_ratio=False)
        self.add_widget(img)

        # Create an image of the difficulty level and adds it to the screen
        self.img_level = Image(source=self.levels[1], pos_hint={'center_x': 0.6, 'center_y': 0.85}, size_hint=(0.15, 0.15), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.img_level)

        # Create an image and button of the left arrow of the difficulty and adds it to the screen
        img = Image(source='images/settings/easier_image.png', pos_hint={'center_x': 0.4, 'center_y': 0.85}, size_hint=(0.1, 0.1), allow_stretch=True, keep_ratio=False)
        button = Button(pos_hint={'center_x': 0.4, 'center_y': 0.85}, size_hint=(0.1, 0.1), background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.make_easier())
        self.add_widget(img)
        self.add_widget(button)

        # Create an image and button of the right arrow of the difficulty and adds it to the screen
        img = Image(source='images/settings/harder_image.png', pos_hint={'center_x': 0.8, 'center_y': 0.85}, size_hint=(0.1, 0.1), allow_stretch=True, keep_ratio=False)
        button = Button(pos_hint={'center_x': 0.8, 'center_y': 0.85}, size_hint=(0.1, 0.1), background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.make_harder())
        self.add_widget(img)
        self.add_widget(button)

        # Create an image of the select and adds it to the screen
        img = Image(source='images/settings/select_image.png', pos_hint={'center_x': 0.30, 'center_y': 0.55}, size_hint=(0.35, 0.15), allow_stretch=True, keep_ratio=False)
        self.add_widget(img)

        # Create a button and an image of who start the game and adds it to the screen
        self.img_who_start = Image(source='images/settings/you_second.png', size_hint=(0.3, 0.15), pos_hint={'center_x': 0.7, 'center_y': 0.55}, allow_stretch=True, keep_ratio=False)
        button_who_start = Button(size_hint=(0.3, 0.15), pos_hint={'center_x': 0.7, 'center_y': 0.55}, background_color=(0, 0, 0, 0))
        button_who_start.bind(on_press=lambda instance: self.who_start())
        self.add_widget(self.img_who_start)
        self.add_widget(button_who_start)

        # create an image of the text "choose your player" and add it to the screen
        img = Image(source='images/settings/choose_your_player.png', size_hint=(0.25, 0.15), pos_hint={'center_x': 0.2, 'center_y': 0.35})
        self.add_widget(img)
        # Create an image of the o_picture and adds it to the screen
        self.o_img = Image(source=self.o_images[self.o_indicts], size_hint=(0.1, 0.1), pos_hint={'center_x': 0.2, 'center_y': 0.25})
        self.add_widget(self.o_img)
        # Create an image and button of the right arrow of the o_image and adds it to the screen
        img = Image(source='images/settings/right_arrow.png', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.3, 'center_y': 0.25})
        button = Button(size_hint=(0.1, 0.1), pos_hint={'center_x': 0.3, 'center_y': 0.25}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_o(1))
        self.add_widget(img)
        self.add_widget(button)
        # Create an image and button of the left arrow of the o_image and adds it to the screen
        img = Image(source='images/settings/left_arrow.png', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.1, 'center_y': 0.25})
        button = Button(size_hint=(0.1, 0.1), pos_hint={'center_x': 0.1, 'center_y': 0.25}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_o(-1))
        self.add_widget(img)
        self.add_widget(button)

        # create an image of the text "choose the computer player" and add it to the screen
        img = Image(source='images/settings/choose_computer_player.png', size_hint=(0.35, 0.15), pos_hint={'center_x': 0.8, 'center_y': 0.35})
        self.add_widget(img)
        # Create an image of the x_picture and adds it to the screen
        self.x_img = Image(source=self.x_images[self.x_indicts], size_hint=(0.1, 0.1), pos_hint={'center_x': 0.8, 'center_y': 0.25})
        self.add_widget(self.x_img)
        # Create an image and button of the right arrow of the x_image and adds it to the screen
        img = Image(source='images/settings/right_arrow.png', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.9, 'center_y': 0.25})
        button = Button(size_hint=(0.1, 0.1), pos_hint={'center_x': 0.9, 'center_y': 0.25}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_x(1))
        self.add_widget(img)
        self.add_widget(button)
        # Create an image and button of the left arrow of the x_image and adds it to the screen
        img = Image(source='images/settings/left_arrow.png', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.7, 'center_y': 0.25})
        button = Button(size_hint=(0.1, 0.1), pos_hint={'center_x': 0.7, 'center_y': 0.25}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_x(-1))
        self.add_widget(img)
        self.add_widget(button)

        # Create a button and an image with the text 'menu' and adds it to the screen
        img = Image(source='images/menu/menu_image.png', size_hint=(1 / 3, 0.15), pos_hint={'center_x': 0.5, 'y': 0.01}, allow_stretch=True, keep_ratio=False)
        button = Button(size_hint=(1 / 3, .15), pos_hint={"center_x": 0.5, "y": 0.01}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_screen(name='menu', direction='right'))
        self.add_widget(button)  # Adds the "Restart" button to the screen.
        self.add_widget(img)

    def who_start(self):  # Change the images of who start the game
        if self.img_who_start.source == 'images/settings/you_second.png':
            self.img_who_start.source = 'images/settings/you_first.png'
        else:
            self.img_who_start.source = 'images/settings/you_second.png'

    def make_harder(self): # Change the images of the difficulty level of the game to harder one
        if self.img_level.source == self.levels[1]:
            self.img_level.source = self.levels[2]
        elif self.img_level.source == self.levels[0]:
            self.img_level.source = self.levels[1]

    def make_easier(self): # Change the images of the difficulty level of the game to easier one
        if self.img_level.source == self.levels[1]:
            self.img_level.source = self.levels[0]
        elif self.img_level.source == self.levels[2]:
            self.img_level.source = self.levels[1]

    def change_o(self, number): # Change the images of O player color
        self.o_indicts = self.o_indicts+number
        self.o_img.source = self.o_images[self.o_indicts % len(self.o_images)]

    def change_x(self, number): # Change the images of X player color
        self.x_indicts = self.x_indicts+number
        self.x_img.source = self.x_images[self.x_indicts % len(self.x_images)]

    def change_screen(self, name, direction): # gets a name of a screen and a direction and go to that screen in this direction
        self.manager.transition.direction = direction
        self.manager.transition.duration = 2
        self.manager.current = name


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) # returns a temporary object of the superclass, which allows you to call its methods.
        self.myModel = Model(self)  # Creates an instance of the Model class.

        # Set up the background of the game screen
        self.Set_Up_Background()

        self.layout = FloatLayout()
        self.add_widget(self.layout)  # Adds the layout to the screen.

        self.Set_Up_New_Game()  # Sets up a new game.

    def Set_Up_Background(self):
        # Create a background image and adds it to the screen
        bg_img = Image(source='images/game/background_game.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(bg_img)

        # Creates and adds the "menu" button and image to the screen.
        img = Image(source='images/menu/menu_image.png', size_hint=(1 / 4, 0.15), pos_hint={'center_x': 5/6, 'y': 0.01}, allow_stretch=True, keep_ratio=False)
        button = Button(size_hint=(1 / 4, .15), pos_hint={"center_x": 5/6, "y": 0.01}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.change_screen(name='menu', direction='down'), )
        self.add_widget(button)  # Adds the "Restart" button to the screen.
        self.add_widget(img)

        # Creates and adds the "Reset" button and image to the screen.
        img = Image(source='images/game/reset_image.png', size_hint=(1 / 4, 0.1), pos_hint={'center_x': 1 / 6, 'y': 0.01}, allow_stretch=True, keep_ratio=False)
        button = Button(size_hint=(1 / 4, .1), pos_hint={"center_x": 1 / 6, "y": 0.01}, background_color=(0, 0, 0, 0))
        button.bind(on_press=lambda instance: self.Set_Up_New_Game())
        self.add_widget(button)  # Adds the "Restart" button to the screen.
        self.add_widget(img)

        self.addCellsToBoatd()

    def Set_Up_New_Game(self):
        self.layout.clear_widgets()

        self.myModel.reset_game()  # re-setting the default arguments

    def addCellsToBoatd(self):
        # Creates Cells and adds them to the game board.
        for line in range(4):
            for col in range(4):
                temp_cell = Cell(self, line, col)  # Creates a Cells with line and col attributes.
                self.add_widget(temp_cell)  # Adds the button to the screen.

    def CellReact(self, choosenButton):
        # This method is called when a button is pressed.
        self.myModel.playerTurn(choosenButton.col + choosenButton.line*4)
        # Shows the appropriate message depending on the winner.
        if self.myModel.win == 'lose':
            img = Image(source='images/game/you_lose_image.png', size_hint=(1 / 2, 0.15), pos_hint={'center_x': 0.5, 'y': 0.8}, allow_stretch=True, keep_ratio=False)
            self.layout.add_widget(img)
        elif self.myModel.win == 'win':
            img = Image(source='images/game/you_win_image.png', size_hint=(1/2, 0.3), pos_hint={'center_x': 0.5, 'y': 0.7}, allow_stretch=True, keep_ratio=False)
            self.layout.add_widget(img)
        elif self.myModel.game.turn > 16:
            img = Image(source='images/game/tie_image.png', size_hint=(0.4, 0.4), pos_hint={'center_x': 0.5, 'center_y': 0.5}, allow_stretch=True, keep_ratio=False)
            self.layout.add_widget(img)

    def place_Pick(self, source, place):  # gets a source and place and adds the source to the screen in the place
        img = Image(source=source, size_hint=(12 / 80, 1 / 7), pos_hint={'x': float(1 / 6.5 * (place % 4 + 1) + 0.03), 'y': float(1 - (1 / 6 * (place // 4 + 2)))})
        self.layout.add_widget(img)

    def change_screen(self, name, direction): # gets a name of a screen and a direction and go to that screen in this direction
        self.manager.transition.direction = direction
        self.manager.transition.duration = 2
        self.manager.current = name

    def on_pre_enter(self): # before we enter to this screen we activate the function from myModel
        self.myModel.pre_enter()


class Cell(Button):
    def __init__(self, graphBoard, line, col):
        # Call the constructor of the parent class (Button)
        Button.__init__(self)
        self.line = line
        self.col = col
        self.gb = graphBoard
        self.size_hint = (12/80, 1/7)
        self.pos_hint = {'x': 1/6.5*(col+1)+0.03, 'y': 1-(1/6*(line+2))}
        self.background_color = (0, 0, 0, 0)

    def on_press(self):
        # Call the CellReact method of the GraphBoard instance when the cell is pressed
        self.gb.CellReact(self)


class Model:
    def __init__(self, board):
        self.board = board # gets the GameScreen
        self.game = Game() # gets the Game
        self.win = 'not over' # the state of the current game
        self.difficulty = 'images/settings/medium_image.png' # the current difficulty level
        self.difficulty_level = {'images/settings/medium_image.png': 0.3, 'images/settings/easy_image.png': 0.5, 'images/settings/hard_image.png': 0} # all the possible difficulty levels with the presenter of playing dam
        self.x_source = 'images/settings/x_picture_red.png' # the current player of X
        self.o_source = 'images/settings/o_picture_black.png' # the current player of O
        self.image_who_start = 'images/settings/you_second.png' # the current state of who start the game

    def computerTurn(self):
        if self.game.turn <= 16 and self.win == 'not over': # will the game is not over
            rnd = random.uniform(0, 1) # Decides whether to play stupid or smart
            if rnd > self.difficulty_level[self.difficulty]:
                place = self.game.model_predict()
                print(rnd, place)
            else:
                place = self.game.computer_turn()
            # placed the image of the player in his spot
            self.game.board[place] = 2
            self.board.place_Pick(source=self.x_source, place=place)
            self.win = self.game.check_win()

    def playerTurn(self, place):
        if self.game.board[place] == 1 and self.win == 'not over':  # will the game is not over
            # placed the image of the player in his spot
            self.game.board[place] = 0
            self.board.place_Pick(source=self.o_source, place=place)
            self.game.turn += 1
            self.win = self.game.check_win()
            self.computerTurn() # plays the computer turn

    def reset_game(self): # restart the game
        self.board.reshima = []
        self.game.init_board()
        self.game.turn = 1
        self.win = 'not over'
        if self.image_who_start == 'images/settings/you_second.png':
            self.computerTurn()

    def pre_enter(self): # Before entering the screen, check if anything has changed in the settings. If so reset the game
        something_change = False
        if self.image_who_start != self.board.manager.get_screen('Settings').img_who_start.source:
            something_change = True
        if self.x_source != self.board.manager.get_screen('Settings').x_img.source:
            something_change = True
        if self.o_source != self.board.manager.get_screen('Settings').o_img.source:
            something_change = True
        if self.difficulty != self.board.manager.get_screen('Settings').img_level.source:
            something_change = True
        self.difficulty = self.board.manager.get_screen('Settings').img_level.source
        self.x_source = self.board.manager.get_screen('Settings').x_img.source
        self.o_source = self.board.manager.get_screen('Settings').o_img.source
        self.image_who_start = self.board.manager.get_screen('Settings').img_who_start.source
        if something_change:
            self.board.Set_Up_New_Game()


class TicTacToeApp(App):
    def build(self): # return all the screens
        sm = ScreenManager()  # Create the screen manager
        # adds all the screens to the screen manager
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='Game'))
        sm.add_widget(InstructionsScreen(name='Instructions'))
        sm.add_widget(SettingsScreen(name='Settings'))
        return sm


if __name__ == '__main__':
    TicTacToeApp().run()
