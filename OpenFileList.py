import sublime, sublime_plugin
import os.path


def getViews(self, list_mode):
    if list_mode == "active_group":
        return self.window.views_in_group(self.window.active_group())
    elif list_mode == "window":
        return self.window.views()

class OpenFileListCommand(sublime_plugin.WindowCommand):
    settings = None
    def run(self, list_mode):
        if self.settings == None:
            self.settings = sublime.load_settings("OpenFileList.sublime-settings")

        views = getViews(self, list_mode)

        # Fallback: if current group has no views,
        # then list all views in current window
        if list_mode != "window" and len(views) < 1 and self.settings.get('list_by_window_fallback') == True:
            views = getViews(self, "window")

        names = []
        current_index = False
        i = -1
        for view in views:
            i += 1
            view_path = view.file_name() or view.name() or 'untitled'
            view_name = os.path.basename(view_path)

            if view.id() == self.window.active_view().id():
                current_index = i

            if view.is_dirty():
                view_name += " " + self.settings.get('mark_dirty_file_char')

            names.append([view_name, view_path])

        names[current_index][0] = self.settings.get('mark_current_file_char') + " " + names[current_index][0]

        def on_done(index):
            if index >= 0:
                self.window.focus_view(views[index])
            else:
                self.window.focus_view(views[current_index])

        if int(sublime.version()) > 3000:
            self.window.show_quick_panel(names, on_done, sublime.MONOSPACE_FONT, current_index, on_done)
        else:
            self.window.show_quick_panel(names, on_done)
