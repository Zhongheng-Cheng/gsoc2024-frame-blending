from frame_hierarchy_analyzer import get_frames, analyze_hierarchy
import curses

def new_window(title, nlines, ncols, begin_y, begin_x):
    win = curses.newwin(nlines, ncols, begin_y, begin_x)
    win.border()
    win.addstr(0, max(0, (ncols - 1) // 2 - len(title) // 2), title, curses.color_pair(1) | curses.A_BOLD)
    win.refresh()
    return win

def main(stdscr):
    
    def update_window(name, content, begin_y, begin_x):
        assert type(content) in [str, list]
        if type(content) == str:
            lines = content.split('\n')
        elif type(content) == list:
            lines = content
        nlines = len(lines) + 2
        ncols = max([len(i) for i in lines]) + 2
        wins[name] = new_window(title = name,
                                nlines = nlines,
                                ncols = ncols,
                                begin_y = begin_y,
                                begin_x = begin_x
                                )
        for i, line in enumerate(lines):
            wins[name].addstr(i + 1, 1, line)
        wins[name].refresh()
        return nlines + begin_y, ncols + begin_x

    wins = {"main": stdscr}
    curses.curs_set(False)
    wins["main"].clear()
    wins["main"].refresh()
    key_content = [
        "ctrl + C: Quit",
        "A: Switch window",
        "B: 22222",
        "C: 3333"
    ]
    key_end_y, key_end_x = update_window("key", key_content, 0, 0)
    
    input_word = ""
    
    
    while True:
        input1_end_y, input1_end_x = update_window("input_1", f"Enter a word and press Enter: {input_word}", 0, key_end_x)
        key = stdscr.getch()
        
        if key == ord('\n'):
            update_window("frame Relation 1", str(root.find(input_word)), input1_end_y, key_end_x)
        
        elif key == curses.KEY_BACKSPACE or key == 127:
            if len(input_word) > 0:
                input_word = input_word[:-1]
        else:
            input_word += chr(key)
        
        stdscr.refresh()


def tmp_main(stdscr):
    # Clear screen
    stdscr.clear()
    
    # Initialize windows
    height, width = 10, 20
    win1 = curses.newwin(height, width, 0, 0)
    win2 = curses.newwin(height, width, 0, width)
    win3 = curses.newwin(height, width, height, 0)
    win4 = curses.newwin(height, width, height, width)
    
    windows = [win1, win2, win3, win4]
    focus_index = 0

    def draw_borders():
        for win in windows:
            win.border(0)
            win.refresh()

    def update_focus():
        for i, win in enumerate(windows):
            if i == focus_index:
                win.attron(curses.A_REVERSE)
            else:
                win.attroff(curses.A_REVERSE)
            win.refresh()

    draw_borders()

    stdscr.getch()
    update_focus()
    stdscr.getch()
    
    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP:
            focus_index = (focus_index - 2) % 4
        elif key == curses.KEY_DOWN:
            focus_index = (focus_index + 2) % 4
        elif key == curses.KEY_LEFT:
            focus_index = (focus_index - 1) % 4
        elif key == curses.KEY_RIGHT:
            focus_index = (focus_index + 1) % 4
        elif key == ord('q'):
            break
        else:
            windows[focus_index].addch(1, 1, key)
            windows[focus_index].refresh()

        update_focus()


if __name__ == "__main__":
    foldername = "frame"
    frames = get_frames(foldername)
    frame_relation = "Inheritance"
    root = analyze_hierarchy(frames, frame_relation)
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.wrapper(main)