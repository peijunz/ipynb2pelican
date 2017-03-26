from pelican import signals
from nbconvert import HTMLExporter
from pelican.readers import BaseReader

from .preprocess import *
from .math import LATEX_CUSTOM_SCRIPT

def register():
    """
    Register the new "ipynb" reader
    """
    def add_reader(arg):
        arg.settings["READERS"]["ipynb"] = IPythonNB
    signals.initialized.connect(add_reader)

class ipynbReader(BaseReader):
    # A part of the code derived from pelican-ipynb
    enabled = True
    file_extensions = ['ipynb']

    def read(self, source_path):
        '''Parse content and metadata for ipynb files'''
        assert(FirstCellMeta in pres)
        exporter = HTMLExporter(template_file='basic',
                                preprocessors=pres)
        content, info = exporter.from_filename(source_path)
        content=content+LATEX_CUSTOM_SCRIPT
        metadata={}
        # Change to standard pelican metadata
        for k,v in FirstCellMeta.data.items():
            metadata[k]= self.process_metadata(k, v)
        return content, metadata
