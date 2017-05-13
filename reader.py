from pelican import signals
from nbconvert import HTMLExporter
from pelican.readers import BaseReader

from .preprocess import config_pres, Metadata
from .math import Mathjax


def register():
    """
    Register the new "ipynb" reader
    """
    def add_reader(arg):
        arg.settings["READERS"]["ipynb"] = ipynbReader
    signals.initialized.connect(add_reader)


class ipynbReader(BaseReader):
    '''ipynb Reader for pelican
    A part of the code derived from pelican-ipynb
    '''
    enabled = True
    file_extensions = ['ipynb']

    def read(self, source_path):
        '''Parse content and metadata for ipynb files'''
        exporter = HTMLExporter(template_file='basic',
                                preprocessors=config_pres(self.settings))
        content, info = exporter.from_filename(source_path)

        # Math Support
        content += Mathjax.config(self.settings)
        metadata = {}

        # Change Metadata.data to standard pelican metadata
        for k, v in Metadata.data.items():
            metadata[k] = self.process_metadata(k, v)
        return content, metadata
