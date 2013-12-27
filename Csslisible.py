import http
import sublime
import sublime_plugin
import urllib


class CsslisibleCommand(sublime_plugin.TextCommand):
    def __init__(self, *args, **kwargs):
        super(CsslisibleCommand, self).__init__(*args, **kwargs)
        self.settings = sublime.load_settings('Csslisible.sublime-settings')

    def run(self, edit):
        # We check for selections if no selections are present we run the API
        # on the whole file
        regions = self.view.sel()

        if len(regions[0]) == 0 and self.view.size() > 0:
            regions = [sublime.Region(0, self.view.size())]

        for region in regions:
            original = self.view.substr(region)
            result = self.cssLisibleApiCall(original)
            if result:
                result = self.normalize_line_endings(result)
                self.view.replace(edit, region, result)

    def normalize_line_endings(self, string):
        string = string.replace('\r\n', '\n').replace('\r', '\n')
        line_endings = self.view.settings().get('default_line_ending')
        if line_endings == 'windows':
            string = string.replace('\n', '\r\n')
        elif line_endings == 'mac':
            string = string.replace('\n', '\r')
        return string

    def cssLisibleApiCall(self, string):
        url = urllib.parse.urlparse(self.settings.get('csslisible_URL'))
        data = {
            'api': '1',
            'clean_css': string,

            'distance_selecteurs': self.settings.get('distance_selecteurs'),
            'type_indentation': self.settings.get('type_indentation'),
            'type_separateur': self.settings.get('type_separateur'),
            'selecteurs_multiples_separes': self.settings.get('selecteurs_multiples_separes'),
            'valeurs_multiples_separees': self.settings.get('valeurs_multiples_separees'),
            'hex_colors_format': self.settings.get('hex_colors_format'),
            'colors_format': self.settings.get('colors_format'),
            'raccourcir_valeurs': self.settings.get('raccourcir_valeurs'),
        }
        params = urllib.parse.urlencode(data)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        try:
            conn = http.client.HTTPConnection(url.netloc, timeout=5)
            conn.request("POST", url.path, params, headers)
        except http.client.HTTPException as e:
            sublime.error_message('%s: HTTP error %s contacting API' % (__name__, str(e)))
        else:
            response = conn.getresponse().read()
            conn.close()
            return str(response, encoding='UTF-8')
        return False
