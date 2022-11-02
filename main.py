import pygame
from game import *
from utils import *
import os
import termcolor
import time


pygame.init()
pygame.font.init()

init_box_place = (20, (WIN_HEIGHT/2 - 3*Box.HEIGHT/2))

Boxes = [
    [Box(*init_box_place),
     Box(init_box_place[0] + Box.WIDTH, init_box_place[1]),
     Box(init_box_place[0] + 2 * Box.WIDTH, init_box_place[1])],

    [Box(init_box_place[0], init_box_place[1] + Box.HEIGHT),
     Box(init_box_place[0] + Box.WIDTH, init_box_place[1] + Box.HEIGHT),
     Box(init_box_place[0] + 2 * Box.WIDTH, init_box_place[1] + Box.HEIGHT)],

    [Box(init_box_place[0], init_box_place[1] + 2 * Box.HEIGHT),
     Box(init_box_place[0] + Box.WIDTH, init_box_place[1] + 2 * Box.HEIGHT),
     Box(init_box_place[0]+ 2 * Box.WIDTH, init_box_place[1] + 2 * Box.HEIGHT)],
]


def draw_window(win: pygame.Surface, mainText: str, text: str, notifications: list[str]):
    # Set background color
    win.fill(COLORS["WHITE"])

    # show mainText
    _text = MAIN_TEXT_FONT.render(mainText, 1, COLORS["BLACK"])
    win.blit(_text, (20, 15))
    
    # show text
    _text = TEXT_FONT.render(text, 1, COLORS["BLACK"])
    win.blit(_text, (20, WIN_HEIGHT - 30 - _text.get_height()))
    
    # show notifications
    _H = 250
    for notification in notifications:
        _text = NOTIFICATIONS_FONT.render(notification, 1, COLORS["BLACK"])
        win.blit(_text, (WIN_WIDTH - 10 - _text.get_width(), _H))
        _H += _text.get_height()

    # Drawing the board {global variable Boxes}
    global Boxes
    for row in Boxes:
        for box in row:
            box.draw(win)

    # Updating the screen
    pygame.display.update()



def get_init_user_inputs():
    os.system("cls")
    termcolor.cprint("Welcome to Tic Tac Toe GAME!", color="green")
    termcolor.cprint("This game is created by: Mounir MELZI", color="red")
    print()
    termcolor.cprint("This game is multiplayers game, so there is two players", color="blue")
    while True:
        player1 = input("Would you like the first player be a human or AI player? (H - AI): ").upper()
        if player1 in ["H", "AI"]:
            break
    print()
    while True:
        player2 = input("Would you like the second player be a human or AI player? (H - AI): ").upper()
        if player2 in ["H", "AI"]:
            break
    
    player1_name = "AI"
    player2_name = "AI"
    if player1 == "H" or player2 == "H":
            os.system("cls")
            termcolor.cprint("Welcome to Tic Tac Toe GAME!", color="green")
            termcolor.cprint("This game is created by: Mounir MELZI", color="red")
            if player1 == "H":
                player1_name = input("Player 1: Please enter your name: ")
            if player2 == "H":
                player2_name = input("Player 2: Please enter your name: ")

    AI1_level = None
    AI2_level = None

    if player1 == "AI" or player2 == "AI":
        os.system("cls")
        termcolor.cprint("Welcome to Tic Tac Toe GAME!", color="green")
        termcolor.cprint("This game is created by: Mounir MELZI", color="red")
        if player1 == "AI":
            while True:
                try:
                    AI1_level = int(input("Enter AI player 1 level (1-2-3): "))
                except ValueError:
                    continue
                else:
                    if 0 < AI1_level < 4:
                        break
        if player2 == "AI":
            while True:
                try:
                    AI2_level = int(input("Enter AI player 2 level (1-2-3): "))
                except ValueError:
                    continue
                else:
                    if 0 < AI2_level < 4:
                        break

    os.system("cls")

    return {
        "player1": player1,
        "player2": player2,
        "name1": player1_name,
        "name2": player2_name,
        "ai1_level": AI1_level,
        "ai2_level": AI2_level,
    }


def main():
    info = get_init_user_inputs()

    # Creation des objects
    clock = pygame.time.Clock()

    # initialize the window
    win = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Tic Tac Toe GAME!")
    
    # Creating the game and the players accourding to info:
    if info["player1"] == "H":
        player1 = Player(maximizing=True, name=info["name1"], symbole="X")
    else:
        player1 = AIplayer(maximizing=True, name="AI-Player1", symbole="X", level=info["ai1_level"])
    if info["player2"] == "H":
        player2 = Player(maximizing=False, name=info["name2"], symbole="O")
    else:
        player2 = AIplayer(maximizing=False, name="AI-Player2", symbole="O", level=info["ai2_level"])
    game = Game(player1, player2)

    # Empty board boxes
    global Boxes

    mainText = f"It is {game.currentPlayer.name} turn to play the next move !..."
    text = ""
    notifications = [""] * 5

    move_played = (None, None)
    symbol_played = None
    player_name = None

    # main loop
    run = True
    while run:

        draw_window(
            win,
            mainText=mainText,
            text=text,
            notifications=notifications,
        )
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


            if event.type == pygame.MOUSEBUTTONDOWN and not isinstance(game.currentPlayer, AIplayer) and run:
                pos = list(pygame.mouse.get_pos())
                pos[0] -= init_box_place[0]
                pos[1] -= init_box_place[1]
                if 0 < pos[0] < Box.WIDTH:
                    x = 0
                elif Box.WIDTH < pos[0] < 2 * Box.WIDTH:
                    x = 1
                elif 2 * Box.WIDTH < pos[0] < 3 * Box.WIDTH:
                    x = 2
                if 0 < pos[1] < Box.HEIGHT:
                    y = 0
                elif Box.HEIGHT < pos[1] < 2 * Box.HEIGHT:
                    y = 1
                elif 2 * Box.HEIGHT < pos[1] < 3 * Box.HEIGHT:
                    y = 2

                if (y, x) in game.board.valideMoves():
                    symbol_played = game.currentPlayer.symbole
                    player_name = game.currentPlayer.name
                    move_played = game.playMove(y, x)
                    notifications = [notification for notification in notifications[1:]]
                    notifications += [f"{player_name} has placed {symbol_played} in position {move_played[0] + 1, move_played[1] + 1}"]
                    mainText = f"It is {game.currentPlayer.name} turn to play the next move !..."
                    text = f"{player_name} has placed {symbol_played} in position {move_played[0] + 1, move_played[1] + 1}"
                    Boxes[move_played[0]][move_played[1]].set(symbol_played)
                    run = not game.isEnd()
                    draw_window(
                        win,
                        mainText=mainText,
                        text=text,
                        notifications=notifications,
                    )


        if isinstance(game.currentPlayer, AIplayer) and run:
            symbol_played = game.currentPlayer.symbole
            player_name = game.currentPlayer.name
            move_played = game.playMove()
            notifications = [notification for notification in notifications[1:]]
            notifications += [f"{player_name} has placed {symbol_played} in position {move_played[0] + 1, move_played[1] + 1}"]
            mainText = f"It is {game.currentPlayer.name} turn to play the next move !..."
            text = f"{player_name} has placed {symbol_played} in position {move_played[0] + 1, move_played[1] + 1}"        
            Boxes[move_played[0]][move_played[1]].set(symbol_played)
            run = not game.isEnd()
            draw_window(
                win,
                mainText=mainText,
                text=text,
                notifications=notifications,
            )


        if not run:
            notifications = [notification for notification in notifications[1:]] + [""]

            if not player1.isWinner(game) and not player2.isWinner(game):
                text = "Tie Game! no winner ..."
            elif player1.isWinner(game):
                text = f"THE WINNER IS: {player1.name}"
            elif player2.isWinner(game):
                text = f"THE WINNER IS: {player2.name}"
            
            for counter in range(20):                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    
                notifications[-1] = f"Game will be closed after {20 - counter}s"
                draw_window(
                    win,
                    mainText="END OF GAME !!",
                    text=text,
                    notifications=notifications,
                )

                time.sleep(1)

            break


        clock.tick(30)


    pygame.quit()
    quit()



if __name__ == "__main__":
    main()

