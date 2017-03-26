from pelican import signals
from traitlets.config import Config
from nbconvert import HTMLExporter
import io
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
    enabled = True
    file_extensions = ['ipynb']

    def read(self, source_path):
        '''Parse content and metadata for ipynb files'''
        
        exporter = HTMLExporter(template_file='basic',
                                preprocessors=[RemoveEmptyCells, FirstCellMeta])
        content, info = exporter.from_filename(source_path)
        content=content+LATEX_CUSTOM_SCRIPT
        metadata={}
        # Change to standard pelican metadata
        for k,v in FirstCellMeta.data.items():
            metadata[k]= self.process_metadata(k, v)
        keys = [k.lower() for k in metadata.keys()]
        return content, metadata
