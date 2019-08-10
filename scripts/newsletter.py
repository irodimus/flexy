import os
import settings
import yaml


class Newsletter:

    def __init__(self, default_flow_style=False):
        self.default_flow_style = default_flow_style

    def load_config(self):
        file_path = os.path.join(settings.NEWSLETTER_DIR, settings.NEWSLETTER_CONFIG_FILE)

        with open(file_path, 'r') as yaml_file:
            config = yaml.full_load(yaml_file)

        return config

    def write_config(self, params):
        file_path = os.path.join(settings.NEWSLETTER_DIR, settings.NEWSLETTER_CONFIG_FILE)

        with open(file_path, 'w') as yaml_file:
            yaml.dump(params, yaml_file, default_flow_style=self.default_flow_style)

    def _format_header(self, title):
        return f'<h2>{title}:</h2><br>'

    def _format_list(self, value):
        return f'<li>{value}</li>'

    def write_newsletter(self):
        config = self.load_config()

        html = f'<<html><head></head><body>'
        for title, values in config.items():
            html += self._format_header(title)

            for value in values:
                html += self._format_list(value)

        return html + '</body></html>'


if __name__ == '__main__':
    html = Newsletter().write_newsletter()
