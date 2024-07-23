from frame_hierarchy_analyzer import get_frames, analyze_hierarchy
import curses

def new_window(title, nlines, ncols, begin_y, begin_x):
    win = curses.newwin(nlines, ncols, begin_y, begin_x)
    win.border()
    win.addstr(0, max(0, (ncols - 1) // 2 - len(title) // 2), title, curses.color_pair(1) | curses.A_BOLD)
    win.refresh()
    return win

def main(stdscr):

    def update_key_window():
        keys = [
            "A: Switch window",
            "B: 22222",
            "C: 3333"
        ]
        wins['key'] = new_window(title = "Keys", 
                                nlines = len(keys) + 2, 
                                ncols = max([len(i) for i in keys]) + 2, 
                                begin_y = 0, 
                                begin_x = 0
                                )
        for i, key in enumerate(keys):
            wins['key'].addstr(i + 1, 1, key)
        wins['key'].refresh()
    
    def update_window(name, content, begin_y, begin_x):
        lines = content.split('\n')
        wins[name] = new_window(title = name[0].upper() + name[1:],
                                nlines = len(lines) + 2,
                                ncols = max([len(i) for i in lines]) + 2,
                                begin_y = begin_y,
                                begin_x = begin_x
                                )
        for i, line in enumerate(lines):
            wins[name].addstr(i + 1, 1, line)
        wins[name].refresh()

    wins = {"main": stdscr}
    curses.curs_set(False)
    wins["main"].clear()
    wins["main"].refresh()
    update_key_window()
    
    input_word = ""
    
    while True:
        update_window("Input 1", f"Enter a word and press Enter: {input_word}", 0, 20)
        key = stdscr.getch()
        
        if key == ord('\n'):
            update_window("Frame Relation 1", str(root.find(input_word)), 8, 20)
        
        elif key == curses.KEY_BACKSPACE or key == 127:
            if len(input_word) > 0:
                input_word = input_word[:-1]
        else:
            input_word += chr(key)
        
        stdscr.refresh()
    
    
    
    stdscr.getch()

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