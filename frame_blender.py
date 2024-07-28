from frame_hierarchy_analyzer import get_frames, analyze_hierarchy
import curses

class Window():
    def __init__(self, title, begin_y, begin_x, nlines=None, ncols=None, content=''):
        self.title = title
        self.content = content
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.start_line = 0
        lines = content.split('\n')
        if nlines:
            self.nlines = nlines
        else:
            self.nlines = len(lines)
        if ncols:
            self.ncols = ncols
        else:
            line_len = max([len(i) for i in lines])
            title_len = len(title)
            self.ncols = max(line_len, title_len)
        self.win = curses.newwin(self.nlines + 2, self.ncols + 2, begin_y, begin_x)
        self.focus = False
        self.update_content(content)
        return
    
    def end_yx(self):
        return self.nlines + 2 + self.begin_y, self.ncols + 2 + self.begin_x
    
    def update_focus(self, focus: bool):
        if focus:
            self.focus = True
            self.win.addstr(0, max(0, (self.ncols + 2 - len(self.title)) // 2), self.title, curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE)
        else:
            self.focus = False
            self.win.addstr(0, max(0, (self.ncols + 2 - len(self.title)) // 2), self.title)
        self.win.refresh()
        return
    
    def update_content(self, content: str = "", start_line: int = 0):
        if not content:
            content = self.content
        else:
            self.content = content
        self.win.clear()
        self.win.border()
        self.update_focus(self.focus)
        lines = content.split('\n')
        for i in range(min(self.nlines, len(lines) - start_line)):
            self.win.addstr(i + 1, 1, lines[i + start_line][:self.ncols])
        self.win.refresh()
        return

class WindowGroup():
    def __init__(self, wins={}):
        self.focus_index = 0
        self.wins = wins
        self.win_hier = None
        self.update_windows_focus()
        self.frame_input_count = 0
        self.cursor_x = 0
        return
    
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
    
    def add_frame_hierarchy(self, frame_relation_control):
        title = frame_relation_control.hierarchy_title()
        content = str(frame_relation_control.hierarchy_root().find(self.focus_win().frame))
        win = Window(title, 0, self.wins["Frame 1"].end_yx()[1], nlines=stdscr_height-2, content=content)
        win.update_content(start_line=3)
        self.win_hier = win
        return

    def remove_frame_input(self):
        if self.frame_input_count > 1:
            title = f"Frame {self.frame_input_count}"
            self.wins[title].win.clear()
            self.wins[title].win.refresh()
            del self.wins[title]
            self.frame_input_count -= 1
        return
    
    def remove_frame_hierarchy(self):
        win = self.win_hier
        win.win.clear()
        win.win.refresh()
        del win
        self.win_hier = None
        return
    
    def update_windows_focus(self):
        for i, win in enumerate(self.wins.values()):
            if i == self.focus_index:
                win.update_focus(True)
                self.cursor_x = len(win.frame)
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
    
    def update_cursor(self):
        curses.curs_set(2)
        self.focus_win().win.move(1, self.cursor_x + 1)
        self.focus_win().win.refresh()
        return


class FrameRelationGroup():
    def __init__(self, frames):
        self.roots = {}
        self.index = 0
        self.relations = ["Inheritance", "Perspective", "Usage", "Subframe"]
        for relation in self.relations:
            self.roots[relation + ": children"] = analyze_hierarchy(frames, relation)
            self.roots[relation + ': parents'] = analyze_hierarchy(frames, relation, reverse_order=True)
        return
    
    def hierarchy_title(self):
        return list(self.roots.keys())[self.index]
    
    def hierarchy_root(self):
        title = self.hierarchy_title()
        return self.roots[title]
    
    def next_relation(self):
        self.index = (self.index + 1) % len(self.roots)
        return
    
    def reset_index(self):
        self.index = 0
        return
    

def main(stdscr):
    global stdscr_height, stdscr_width

    foldername = "frame"
    frames = get_frames(foldername)
    frame_relation_control = FrameRelationGroup(frames)
    stdscr.clear()
    stdscr.refresh()

    win_logo_content = r"""
    ______                             ____  __               __         
   / ____/________ _____ ___  ___     / __ )/ /__  ____  ____/ /__  _____
  / /_  / ___/ __ `/ __ `__ \/ _ \   / __  / / _ \/ __ \/ __  / _ \/ ___/
 / __/ / /  / /_/ / / / / / /  __/  / /_/ / /  __/ / / / /_/ /  __/ /    
/_/   /_/   \__,_/_/ /_/ /_/\___/  /_____/_/\___/_/ /_/\__,_/\___/_/     
"""[1:] # remove the '\n' in the front
    logo_lines = win_logo_content.split('\n')
    stdscr_height, stdscr_width = stdscr.getmaxyx()
    start_y = stdscr_height - len(logo_lines) - 2
    start_x = stdscr_width - max(len(line) for line in logo_lines) - 2
    win_logo = Window("", start_y, start_x, content=win_logo_content)

    win_key_content = """\
ESC:        Quit
+:          Add Frame
-:          Remove Frame
Arrow
 up/down:   Switch frame
Enter:      Confirm frame
          & Enter hierarchy
Tab:        Switch relation"""
    win_key = Window("Keys", 0, 0, content=win_key_content)

    window_group = WindowGroup()
    window_group.add_frame_input(0, win_key.end_yx()[1])


    while True:
        window_group.update_cursor()

        key = stdscr.getch()
        
        # Quit
        if key == 27: # ESC
            break

        # Switch frame
        elif key == curses.KEY_DOWN:
            window_group.next_focus()
        elif key == curses.KEY_UP:
            window_group.prev_focus()

        # Add/remove frame
        elif key == ord('+'):
            window_group.add_frame_input(window_group.frame_input_count * 4, win_key.end_yx()[1])
        elif key == ord('-'):
            window_group.remove_frame_input()

        # Switch Frame Hierarchy
        elif key == ord('\t') or key == 9: # TAB
            frame_relation_control.next_relation()

        # Enter frame Hierarchy
        elif key == ord('\n'):
            pass
        
        # Text operations
        elif key == curses.KEY_BACKSPACE or key == 127:
            window_group.focus_win().frame = window_group.focus_win().frame[:window_group.cursor_x - 1] + window_group.focus_win().frame[window_group.cursor_x:]
            window_group.cursor_x = max(window_group.cursor_x - 1, 0)
        elif key == curses.KEY_LEFT:
            window_group.cursor_x = max(window_group.cursor_x - 1, 0)
        elif key == curses.KEY_RIGHT:
            window_group.cursor_x = min(window_group.cursor_x + 1, len(window_group.focus_win().frame))
        else: # input characters
            window_group.focus_win().frame = window_group.focus_win().frame[:window_group.cursor_x] + chr(key) + window_group.focus_win().frame[window_group.cursor_x:]
            window_group.cursor_x += 1
        
        # Update windows display
        if window_group.win_hier:
            window_group.remove_frame_hierarchy()

        win_logo.update_content()
        win_key.update_content()

        hierarchy = frame_relation_control.hierarchy_root().find(window_group.focus_win().frame)
        if hierarchy:
            window_group.add_frame_hierarchy(frame_relation_control)

        window_group.focus_win().update_content(window_group.focus_win().frame)
        stdscr.refresh()
    
    return


if __name__ == "__main__":
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.wrapper(main)