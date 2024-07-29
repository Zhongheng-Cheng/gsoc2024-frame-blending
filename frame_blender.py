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
    
    def update_content(self, content: str = ""):
        if not content:
            content = self.content
        else:
            self.content = content
        self.win.clear()
        self.win.border()
        self.update_focus(self.focus)
        lines = content.split('\n')
        for i in range(min(self.nlines, len(lines))):
            self.win.addstr(i + 1, 1, lines[i][:self.ncols])
        self.win.refresh()
        return
    
class HierarchyWindow(Window):
    def __init__(self, title, begin_y, begin_x, nlines=None, ncols=None, content=''):
        super().__init__(title, begin_y, begin_x, nlines, ncols, content)
        self.start_line = 0
        self.focus_line_index = 0
        self.selected_frame = ''
        return
    
    def update_content(self, content: str = ""):
        if not content:
            content = self.content
        else:
            self.content = content
        self.win.clear()
        self.win.border()
        self.update_focus(self.focus)
        lines = content.split('\n')
        for i in range(min(self.nlines, len(lines) - self.start_line)):
            self.win.addstr(i + 1, 1, lines[i + self.start_line][:self.ncols])
        if self.focus == True:
            focus_line = lines[self.focus_line_index]
            start_index = focus_line.rfind(' ') + 1
            self.selected_frame = focus_line[start_index:]
            self.win.addstr(self.focus_line_index - self.start_line + 1, start_index + 1, focus_line[start_index:], curses.color_pair(2))
        self.win.refresh()
        return
    
    def next_frame(self):
        content_nlines = len(self.content.split('\n'))
        self.focus_line_index = min(self.focus_line_index + 1, content_nlines - 1)
        self.start_line = max(self.start_line, self.focus_line_index - self.nlines + 1)
        return
    
    def prev_frame(self):
        self.focus_line_index = max(self.focus_line_index - 1, 0)
        self.start_line = min(self.focus_line_index, self.start_line)
        return


class WindowGroup():
    def __init__(self):
        self.focus_index = [0, 0]
        self.wins = [
            [], # frame input windows
            [], # hierarchy windows
        ]
        return
    
    def add(self, win, column=0):
        self.wins[column].append(win)
        self.update_windows_focus()
        return
    
    def add_frame_input(self, start_y, start_x):
        title = f"Frame {len(self.wins[0]) + 1}"
        win_input = Window(title, start_y, start_x, ncols=20)
        win_input.cursor_x = 0
        self.add(win_input)
        return
    
    def add_frame_hierarchy(self, frame_relation_control):
        title = frame_relation_control.hierarchy_title()
        content = str(frame_relation_control.hierarchy_root().find(self.focus_win().content)).strip()
        win = HierarchyWindow(title, 0, self.wins[0][0].end_yx()[1], nlines=min(stdscr_height-2, len(content.split('\n'))), content=content)
        self.wins[1].append(win)
        return

    def remove_frame_input(self):
        if len(self.wins[0]) > 1:
            self.wins[0][-1].win.clear()
            self.wins[0][-1].win.refresh()
            del self.wins[0][-1]
        return
    
    def remove_frame_hierarchy(self):
        win = self.wins[1][0]
        win.start_line = 0
        win.focus_line_index = 0
        win.win.clear()
        win.win.refresh()
        del self.wins[1][0]
        return
    
    def update_windows_focus(self):
        for col in self.wins:
            for win in col:
                win.update_focus(False)
        win = self.focus_win()
        win.update_focus(True)
        win.cursor_x = len(win.content)
        return
    
    def next_focus(self):
        self.focus_index[1] = (self.focus_index[1] + 1) % len(self.wins[0])
        self.update_windows_focus()
        return
    
    def prev_focus(self):
        self.focus_index[1] = (self.focus_index[1] - 1 + len(self.wins[0])) % len(self.wins[0])
        self.update_windows_focus()
        return
    
    def enter_hier_focus(self):
        curses.curs_set(0)
        self._tmp_focus_index = self.focus_index
        self.focus_index = [1, 0]
        self.update_windows_focus()
        return

    def quit_hier_focus(self):
        win = self.wins[1][0]
        win.update_focus(False)
        win.update_content()
        self.focus_index = self._tmp_focus_index
        self.update_cursor()
        self.update_windows_focus()
        return
    
    def focus_win(self) -> Window:
        """
        Return the current focused window.
        """
        col, i = self.focus_index
        win = self.wins[col][i]
        return win
    
    def update_cursor(self):
        curses.curs_set(2)
        win = self.focus_win()
        win.win.move(1, win.cursor_x + 1)
        win.win.refresh()
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
    window_group.update_cursor()

    while True:

        # Refresh windows display
        win_logo.update_content()
        window_group.focus_win().update_content()
        
        key = stdscr.getch()
        
        # Quit
        if key == 27: # ESC
            break
        
        # When focus on frame input windows
        elif window_group.focus_index[0] == 0:
            
            # Switch frame
            if key == curses.KEY_DOWN:
                window_group.next_focus()
            elif key == curses.KEY_UP:
                window_group.prev_focus()

            # Add/remove frame
            elif key == ord('+'):
                window_group.add_frame_input(len(window_group.wins[0]) * 4, win_key.end_yx()[1])
            elif key == ord('-'):
                window_group.remove_frame_input()

            # Switch Frame Hierarchy
            elif key == ord('\t') or key == 9: # TAB
                frame_relation_control.next_relation()
            
            # Enter frame Hierarchy
            elif key == ord('\n'):
                if window_group.focus_win().content and window_group.wins[1]:
                    window_group.enter_hier_focus()
                    continue

            # Text operations
            else:
                win = window_group.focus_win()
                if key == curses.KEY_BACKSPACE or key == 127:
                    win.content = win.content[:win.cursor_x - 1] + win.content[win.cursor_x:]
                    win.cursor_x = max(win.cursor_x - 1, 0)
                elif key == curses.KEY_LEFT:
                    win.cursor_x = max(win.cursor_x - 1, 0)
                elif key == curses.KEY_RIGHT:
                    win.cursor_x = min(win.cursor_x + 1, len(win.content))
                else: # input characters
                    win.content = win.content[:win.cursor_x] + chr(key) + win.content[win.cursor_x:]
                    win.cursor_x += 1

            window_group.update_cursor()

            if window_group.wins[1]:
                window_group.remove_frame_hierarchy()
            hierarchy = frame_relation_control.hierarchy_root().find(window_group.focus_win().content)
            if hierarchy:
                window_group.add_frame_hierarchy(frame_relation_control)
            
        
        # When focus on hierarchy window
        elif window_group.focus_index[0] == 1:

            # Quit frame hierarchy
            if key == curses.KEY_BACKSPACE or key == 127:
                window_group.quit_hier_focus()
            
            # Switch frame
            elif key == curses.KEY_DOWN:
                window_group.wins[1][0].next_frame()
            elif key == curses.KEY_UP:
                window_group.wins[1][0].prev_frame()
            
            # Confirm frame
            elif key == ord('\n'):
                frame = window_group.wins[1][0].selected_frame
                window_group.quit_hier_focus()
                window_group.remove_frame_hierarchy()
                window_group.focus_win().update_content(frame)
        
    return


if __name__ == "__main__":
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.wrapper(main)