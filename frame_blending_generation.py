from frame_hierarchy_analyzer import get_frames, analyze_hierarchy
import curses

class Window():
    def __init__(self, title, begin_y, begin_x, nlines=None, ncols=None, content=''):
        self.title = title
        self.begin_y = begin_y
        self.begin_x = begin_x
        lines = content.split('\n')
        if nlines:
            self.nlines = nlines + 2
        else:
            self.nlines = len(lines) + 2
        if ncols:
            self.ncols = ncols + 2
        else:
            line_len = max([len(i) for i in lines])
            title_len = len(title)
            self.ncols = max(line_len, title_len) + 2
        self.win = curses.newwin(self.nlines, self.ncols, begin_y, begin_x)
        self.win.border()
        self.win.addstr(0, max(0, (self.ncols - len(self.title)) // 2), self.title)
        self.win.refresh()
        self.update_content(content)
        self.focus = False
        return
    
    def end_yx(self):
        return self.nlines + self.begin_y, self.ncols + self.begin_x
    
    def update_focus(self, focus: bool):
        if focus:
            self.focus = True
            self.win.addstr(0, max(0, (self.ncols - len(self.title)) // 2), self.title, curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE)
        else:
            self.focus = False
            self.win.addstr(0, max(0, (self.ncols - len(self.title)) // 2), self.title)
        self.win.refresh()
        return
    
    def update_content(self, content):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            self.win.addstr(i + 1, 1, line)
        self.win.refresh()

class WindowGroup():
    def __init__(self, wins={}):
        self.focus_index = 0
        self.wins = wins
        self.update_windows_focus()
        return
    
    # def __getattribute__(self, __name: str) -> Window:
    #     return self.wins[__name]
    
    def add(self, title, win):
        self.wins[title] = win
        return
    
    def update_windows_focus(self):
        for i, win in enumerate(self.wins.values()):
            if i == self.focus_index:
                win.update_focus(True)
            else:
                win.update_focus(False)
        return
    
    def next_focus(self):
        self.focus_index = (self.focus_index + 1) % len(self.wins)
        self.update_windows_focus()
        return
    
    def focus_win(self):
        title = list(self.wins.keys())[self.focus_index]
        win = self.wins[title]
        return win
    

def main(stdscr):

    curses.curs_set(False)
    stdscr.clear()
    stdscr.refresh()

    win_key_content = """\
ctrl+C: Quit
Tab: Switch window
B: ...
C: ..."""
    win_key = Window("key", 0, 0, content=win_key_content)

    win_input_1 = Window("Frame_1", 0, win_key.end_yx()[1], ncols=20)
    win_input_1.word = ""
    win_input_2 = Window("Frame_2", 0, win_input_1.end_yx()[1], ncols=20)
    win_input_2.word = ""
    wins_group = WindowGroup({win.title: win for win in [win_input_1, win_input_2]})
    
    while True:

        key = stdscr.getch()
        
        if key == ord('\n'):
            pass
        elif key == curses.KEY_TAB: # Tab
            wins_group.next_focus()
        elif key == curses.KEY_BACKSPACE or key == 127:
            wins_group.focus_win().word = wins_group.focus_win().word[:-1]
        else:
            wins_group.focus_win().word += chr(key)
        wins_group.focus_win().update_content(wins_group.focus_win().word)
        
        stdscr.refresh()


if __name__ == "__main__":
    foldername = "frame"
    frames = get_frames(foldername)
    frame_relation = "Inheritance"
    root = analyze_hierarchy(frames, frame_relation)
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.wrapper(main)