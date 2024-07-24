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
        self.focus = False
        self.update_content(content)
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
        self.win.clear()
        self.win.border()
        self.update_focus(self.focus)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            self.win.addstr(i + 1, 1, line)
        self.win.refresh()

class WindowGroup():
    def __init__(self, wins={}):
        self.focus_index = 0
        self.wins = wins
        self.update_windows_focus()
        self.frame_input_count = 0
        return
    
    # def __getattribute__(self, __name: str) -> Window:
    #     return self.wins[__name]
    
    def add(self, win):
        self.wins[win.title] = win
        self.update_windows_focus()
        return
    
    def add_frame_input(self, start_y, start_x):
        self.frame_input_count += 1
        title = f"Frame {self.frame_input_count}"
        win_input = Window(title, start_y, start_x, ncols=20)
        win_input.frame = ""
        self.add(win_input)
        return
    
    def remove_frame_input(self):
        if self.frame_input_count > 1:
            title = f"Frame {self.frame_input_count}"
            self.wins[title].win.clear()
            self.wins[title].win.refresh()
            del self.wins[title]
            self.frame_input_count -= 1
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
    
    def prev_focus(self):
        self.focus_index = (self.focus_index - 1 + len(self.wins)) % len(self.wins)
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

    logo = """\
    ______                             ____  __               __         
   / ____/________ _____ ___  ___     / __ )/ /__  ____  ____/ /__  _____
  / /_  / ___/ __ `/ __ `__ \/ _ \   / __  / / _ \/ __ \/ __  / _ \/ ___/
 / __/ / /  / /_/ / / / / / /  __/  / /_/ / /  __/ / / / /_/ /  __/ /    
/_/   /_/   \__,_/_/ /_/ /_/\___/  /_____/_/\___/_/ /_/\__,_/\___/_/     
"""
    logo_content = logo.split('\n')
    height, width = stdscr.getmaxyx()
    start_y = height - len(logo_content) - 2
    start_x = width - max(len(line) for line in logo_content) - 2
    win_logo = Window("", start_y, start_x, content=logo)

    win_key_content = """\
ESC: Quit
+: Add Frame
-: Remove Frame
up/down: Switch frame
Enter: Confirm frame
Tab: ..."""
    win_key = Window("key", 0, 0, content=win_key_content)
    window_group = WindowGroup()
    window_group.add_frame_input(0, win_key.end_yx()[1])

    # win_tmp = Window("TMP", 30, 0, ncols=100, content="test")
    
    while True:

        key = stdscr.getch()
        
        if key == 27: # ESC
            break
        elif key == curses.KEY_DOWN:
            window_group.next_focus()
        elif key == curses.KEY_UP:
            window_group.prev_focus()
        elif key == ord('+'):
            window_group.add_frame_input(window_group.frame_input_count * 4, win_key.end_yx()[1])
        elif key == ord('-'):
            window_group.remove_frame_input()
        elif key == curses.KEY_BACKSPACE or key == 127:
            window_group.focus_win().frame = window_group.focus_win().frame[:-1]
        else:
            window_group.focus_win().frame += chr(key)
        window_group.focus_win().update_content(window_group.focus_win().frame)
        
        stdscr.refresh()
    
    return


if __name__ == "__main__":
    foldername = "frame"
    frames = get_frames(foldername)
    frame_relation = "Inheritance"
    root = analyze_hierarchy(frames, frame_relation)
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.wrapper(main)