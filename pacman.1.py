import random
from termcolor import colored

def get_initial_map():
    return [
        "|--------|",
        "|G..|..G.|",
        "|...PP...|",
        "|G....@|.|",
        "|...P..|.|",
        "|--------|"
    ]

ui_wall = [
    "......",
    "......",
    "......",
    "......"
]

ui_ghost = [
    " .-.  ",
    "| OO| ",
    "|   | ",
    "'^^^' "
]

ui_hero = [
    " .--. ",
    "/ _.-'",
    "\\  '-.",
    " '--' "
]

ui_empty = [
    "      ",
    "      ",
    "      ",
    "      "
]

ui_pill = [
    "      ",
    " .-.  ",
    " '-'  ",
    "      "
]

wall_color = "blue"
ghost_color = "red"
pacman_color = "yellow"
pill_color = "grey"

def render_map(game_map):
    for row in game_map:
        for piece in range(4):
            for point in row:
                if point == 'G':
                    print(colored(ui_ghost[piece], ghost_color), end='')
                elif point == '|' or point == '-':
                    print(colored(ui_wall[piece], wall_color), end='')
                elif point == '@':
                    print(colored(ui_hero[piece], pacman_color), end='')
                elif point == '.':
                    print(ui_empty[piece], end='')
                elif point == 'P':
                    print(colored(ui_pill[piece], pill_color), end='')
            print("", end='\n')

def find_all_ghosts(game_map):
    ghosts = []
    for x in range(len(game_map)):
        for y in range(len(game_map[x])):
            if game_map[x][y] == 'G':
                ghosts.append([x, y])
    return ghosts

def find_pacman(game_map):
    for x in range(len(game_map)):
        for y in range(len(game_map[x])):
            if game_map[x][y] == '@':
                return x, y
    return -1, -1

def move_ghosts(game_map, ghosts_on_pills):
    all_ghosts = find_all_ghosts(game_map)
    new_ghosts_on_pills = []
    for ghost in all_ghosts:
        old_ghost_x, old_ghost_y = ghost
        was_on_pill = (old_ghost_x, old_ghost_y) in ghosts_on_pills

        possible_directions = [
            [old_ghost_x, old_ghost_y + 1],  
            [old_ghost_x + 1, old_ghost_y],  
            [old_ghost_x, old_ghost_y - 1],  
            [old_ghost_x - 1, old_ghost_y]
        ]

        random.shuffle(possible_directions)
        for next_ghost_x, next_ghost_y in possible_directions:
            if 0 <= next_ghost_x < len(game_map) and 0 <= next_ghost_y < len(game_map[0]):
                target = game_map[next_ghost_x][next_ghost_y]
                if target not in ('|', '-', 'G'):
                    is_pacman = target == '@'
                    is_pill = target == 'P'
                    if is_pacman:
                        return True, False, new_ghosts_on_pills  # Pacman caught!
                    # Restore pill if ghost was on a pill, else empty
                    if was_on_pill:
                        game_map[old_ghost_x] = game_map[old_ghost_x][:old_ghost_y] + "P" + game_map[old_ghost_x][old_ghost_y+1:]
                    else:
                        game_map[old_ghost_x] = game_map[old_ghost_x][:old_ghost_y] + "." + game_map[old_ghost_x][old_ghost_y+1:]
                    # Place ghost
                    game_map[next_ghost_x] = game_map[next_ghost_x][:next_ghost_y] + "G" + game_map[next_ghost_x][next_ghost_y+1:]
                    # If ghost moved onto a pill, remember it
                    if is_pill:
                        new_ghosts_on_pills.append((next_ghost_x, next_ghost_y))
                    break
        else:
            # Ghost didn't move, keep pill memory if needed
            if was_on_pill:
                new_ghosts_on_pills.append((old_ghost_x, old_ghost_y))
    return False, None, new_ghosts_on_pills

def move_pacman(game_map, key):
    pacman_x, pacman_y = find_pacman(game_map)
    next_pacman_x, next_pacman_y = pacman_x, pacman_y

    if key == 'a':
        next_pacman_y -= 1
    elif key == 's':
        next_pacman_x += 1
    elif key == 'w':
        next_pacman_x -= 1
    elif key == 'd':
        next_pacman_y += 1
    else:
        return False, False

    if not (0 <= next_pacman_x < len(game_map) and 0 <= next_pacman_y < len(game_map[0])):
        return False, False

    target = game_map[next_pacman_x][next_pacman_y]
    if target in ('|', '-'):
        return False, False
    if target == 'G':
        return True, False

    # Move Pacman
    game_map[pacman_x] = game_map[pacman_x][:pacman_y] + "." + game_map[pacman_x][pacman_y+1:]
    game_map[next_pacman_x] = game_map[next_pacman_x][:next_pacman_y] + "@" + game_map[next_pacman_x][next_pacman_y+1:]
    return False, True

def count_pills(game_map):
    return sum(row.count('P') for row in game_map)

def render_final(game_map, win):
    final_board_color = "green" if win else "red"
    for row in game_map:
        for piece in range(4):
            for point in row:
                if point == 'G':
                    print(colored(ui_ghost[piece], final_board_color), end='')
                elif point == '|' or point == '-':
                    print(colored(ui_wall[piece], final_board_color), end='')
                elif point == '@':
                    print(colored(ui_hero[piece], final_board_color), end='')
                elif point == '.':
                    print(colored(ui_empty[piece], final_board_color), end='')
                elif point == 'P':
                    print(colored(ui_pill[piece], final_board_color), end='')
            print("", end='\n')

def main():
    game_map = get_initial_map()
    ghosts_on_pills = []
    game_finished = False
    win = False

    while not game_finished:
        render_map(game_map)
        caught, _, ghosts_on_pills = move_ghosts(game_map, ghosts_on_pills)
        if caught:
            win = False
            break

        key = input("Move (w/a/s/d): ")
        caught, moved = move_pacman(game_map, key)
        if caught:
            win = False
            break

        if count_pills(game_map) == 0:
            win = True
            break

    render_final(game_map, win)
    if win:
        print("You win! :)")
    else:
        print("You lost! :/")

if __name__ == "__main__":
    main()
