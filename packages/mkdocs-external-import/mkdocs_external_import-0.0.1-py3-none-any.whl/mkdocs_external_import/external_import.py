import mkdocs
import re
import requests
from urllib.parse import urlparse


class ImportConfig(mkdocs.config.base.Config):
    shortname = mkdocs.config.config_options.Type(str, default='import-external-content')


class Import(mkdocs.plugins.BasePlugin[ImportConfig]):
    def __init__(self):
        self.import_block = None
        self.logger = mkdocs.plugins.get_plugin_logger(__name__)

    def on_page_markdown(self,
                         markdown: str,
                         page: mkdocs.structure.pages.Page,
                         config: mkdocs.config.defaults.MkDocsConfig,
                         files: mkdocs.structure.files.Files) -> str | None:
        for instance in re.finditer(fr'(```{self.config.shortname}([^`]+)```)', markdown):
            if len(instance.groups()):
                replace = instance.groups()[0]
                url = instance.groups()[1]
                url = urlparse(url)
                self.logger.info(f'Importing external content from: {url.geturl()}')

                content = requests.get(url.geturl()).content.decode('utf-8')
                markdown = markdown.replace(replace, content)

        return markdown
