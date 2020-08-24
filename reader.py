from pelican import signals
from nbconvert import HTMLExporter
from pelican.readers import BaseReader

from .preprocess import config_pres, Metadata
from bs4 import BeautifulSoup


def register():
    """
    Register the new "ipynb" reader
    """
    def add_reader(arg):
        arg.settings["READERS"]["ipynb"] = ipynbReader
    signals.initialized.connect(add_reader)

def get_file_name(full_path):
    filename = full_path.split('/')[-1]
    clean_name = '.'.join(filename.split('.')[:-1])
    return clean_name.strip()

class ipynbReader(BaseReader):
    '''ipynb Reader for pelican
    A part of the code derived from pelican-ipynb
    '''
    enabled = True
    file_extensions = ['ipynb']
    DEFAULT_CELL_PENALTY = 120
    DEFAULT_SUMMARY_SIZE = 600

    def read(self, source_path):
        '''Parse content and metadata for ipynb files'''
        exporter = HTMLExporter(template_file='basic',
                                preprocessors=config_pres(self.settings))
        content, info = exporter.from_filename(source_path)

        # Math Support
        summary = ""
        text = 0
        soup = BeautifulSoup(content, 'html.parser')
        penalty = self.settings.get('CELL_PENALTY', self.DEFAULT_CELL_PENALTY)
        summary_size = self.settings.get('SUMMARY_SIZE', self.DEFAULT_SUMMARY_SIZE)
        for cell in soup.find_all('div', recursive=False):
            delta = len(cell.get_text())# penalty for each cell
            delta += penalty * len(cell.find_all('div', ["input", 'output_wrapper'], recursive=False))

            if text and text+delta >= summary_size*1.1 or text > summary_size:
                break
            text += delta
            summary += str(cell)
        metadata = {'title': get_file_name(source_path), 'summary': summary}

        metadata.update(Metadata.data)
        metadata['summary'] = summary

        # Change Metadata.data to standard pelican metadata
        for k, v in metadata.items():
            metadata[k] = self.process_metadata(k, v)
        return content, metadata
