import sublime
import sublime_plugin
import requests
import threading

settings = sublime.load_settings('Csslisible.sublime-settings')


class CsslisibleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # We check for selections if no selections are present we run the API
        # on the all file
        sels = self.view.sel()

        if len(sels[0]) == 0 and self.view.size() > 0:
            sels = [sublime.Region(0, self.view.size())]

        # We start one thread per selection so we don't lock up the interface
        # while waiting for the response from the API
        threads = []
        for sel in sels:
            string = self.view.substr(sel)
            thread = CssLisibleApiCall(sel, string)
            threads.append(thread)
            thread.start()

        # We clear all selection because we are going to manually set them
        self.view.sel().clear()

        # This creates an edit group so we can undo all changes in one go
        edit = self.view.begin_edit('csslisible')

        self.handle_threads(edit, threads)

    def handle_threads(self, edit, threads, offset=0, i=0, dir=1):
        next_threads = []
        for thread in threads:
            if thread.is_alive():
                next_threads.append(thread)
                continue
            if thread.result == False:
                continue
            offset = self.replace(edit, thread, offset)
        threads = next_threads

        if len(threads):
            # This animates a little activity indicator in the status area
            before = i % 8
            after = (7) - before
            if not after:
                dir = -1
            if not before:
                dir = 1
            i += dir
            self.view.set_status('csslisible', 'Csslisible [%s=%s]' % \
                (' ' * before, ' ' * after))

            sublime.set_timeout(lambda: self.handle_threads(edit, threads,
                                offset, i, dir), 100)
            return

        self.view.end_edit(edit)

        self.view.erase_status('csslisible')
        selections = len(self.view.sel())
        sublime.status_message('Csslisible successfully run on %s selection%s' %
            (selections, '' if selections == 1 else 's'))

    def replace(self, edit, thread, offset):
        sel = thread.sel
        original = thread.original
        result = thread.result

        # Here we adjust each selection for any text we have already inserted
        if offset:
            sel = sublime.Region(sel.begin() + offset,
                sel.end() + offset)

        result = self.normalize_line_endings(result)
        self.view.replace(edit, sel, result)

        # We add the end of the new text to the selection
        end_point = sel.begin() + len(result)
        self.view.sel().add(sublime.Region(end_point, end_point))

        return offset + len(result) - len(original)

    def normalize_line_endings(self, string):
        string = string.replace('\r\n', '\n').replace('\r', '\n')
        line_endings = self.view.settings().get('default_line_ending')
        if line_endings == 'windows':
            string = string.replace('\n', '\r\n')
        elif line_endings == 'mac':
            string = string.replace('\n', '\r')
        return string


class CssLisibleApiCall(threading.Thread):
    def __init__(self, sel, string):
        self.sel = sel
        self.original = string
        self.result = None
        self.distance_selecteurs = settings.get('distance_selecteurs')
        self.type_indentation = settings.get('type_indentation'),
        self.type_separateur = settings.get('type_separateur'),
        self.hex_colors_format = settings.get('hex_colors_format'),
        self.selecteurs_multiples_separes = settings.get('selecteurs_multiples_separes'),
        threading.Thread.__init__(self)

    def run(self):
        try:
            payload = {
                        'api': '1',
                        'distance_selecteurs': self.distance_selecteurs,
                        'type_indentation': self.type_indentation,
                        'type_separateur': self.type_separateur,
                        'hex_colors_format': self.hex_colors_format,
                        'selecteurs_multiples_separes': self.selecteurs_multiples_separes,
                        'clean_css': self.original
                    }
            data = requests.post("http://csslisible.com/", payload)
            self.result = data.text
            return

        except (requests.HTTPError) as (e):
            err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))

        sublime.error_message(err)
        self.result = False
