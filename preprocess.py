from nbconvert.preprocessors import Preprocessor
import re
import ast
import markdown


class MetaDataExtractionFailure(Exception):
    pass


class Metadata(Preprocessor):
    """Preprocessor to extract metadata from first cell of notebook."""
    data = {}
    md = None

    # Regex for 'key: value' syntax
    key_value_regex = re.compile(
        r'^\s*[*+-]?\s*(?P<key>[a-zA-Z]+)\s*:\s*(?P<value>.*)$')

    @staticmethod
    def extract_cell_metadata(cell):
        """Extract metadata from the given notebook cell source."""
        # Convert Markdown title syntax to 'title:'
        cell = re.sub(r'^#+\s*', 'title: ', cell, flags=re.MULTILINE)

        # Extract metadata from key-value pairs in non-empty lines
        lines = [line.strip() for line in cell.split('\n') if line.strip()]
        metadata = {}
        for line in lines:
            match = Metadata.key_value_regex.match(line)
            if not match:
                raise MetaDataExtractionFailure(
                    'Failed to extract metadata with {l!r}'.format(l=line))
            key, value = match.group('key', 'value')
            metadata[key.lower()] = value
        return metadata

    @staticmethod
    def preprocess(nb, resources):
        '''Process the notebook to extract metadata'''
        Metadata.data = Metadata.extract_cell_metadata(nb.cells[0]['source'])
        nb.cells = nb.cells[1:]
        if not nb.cells:
            raise Exception('No content cells after metadata extraction!')

        if 'summary' in Metadata.data:
            Metadata.data['summary'] = Metadata.md.convert(
                Metadata.data['summary'])
        return nb, resources


class SubCells(Preprocessor):
    """A preprocessor to select a slice of the cells of a notebook"""
    start = 0
    end = None

    @staticmethod
    def preprocess(nb, resources):
        '''Get start/end from subcells metadata'''
        if 'subcells' in Metadata.data:
            SubCells.start, SubCells.end = \
                ast.literal_eval(Metadata.data['subcells'])
        nb.cells = nb.cells[SubCells.start:SubCells.end]
        if not nb.cells:
            raise Exception('No content cells after SubCells!')
        return nb, resources


class RemoveEmpty(Preprocessor):
    '''Remove Empty Cells'''
    visible = re.compile('\S')

    @staticmethod
    def preprocess(nb, resources):
        nb.cells = [cell for cell in nb.cells
                    if re.search(RemoveEmpty.visible, cell['source'])]
        if not nb.cells:
            raise Exception('No content cells after RemoveEmpty!')
        return nb, resources


class IgnoreTag(Preprocessor):
    '''Ignore Cells with #ignore tag in the beginning'''
    @staticmethod
    def preprocess(nb, resources):
        nb.cells = [cell for cell in nb.cells
                    if not cell['source'].startswith('#ignore')]
        if not nb.cells:
            raise Exception('No content cells after IgnoreTag!')
        return nb, resources


pres = [('IPYNB_SUBCELLS', SubCells),
        ('IPYNB_IGNORE', IgnoreTag),
        ('IPYNB_REMOVE_EMPTY', RemoveEmpty), ]
default_options = {'IPYNB_REMOVE_EMPTY': True,
                   'IPYNB_IGNORE': True,
                   'IPYNB_SUBCELLS': True, }


def config_pres(setting):
    '''Configuration of preprocess
    Precedence: Metadata > SubCells > IgnoreTag = RemoveEmpty
    Refresh preprocessor options by setting'''
    Metadata.md = markdown.Markdown(**setting['MARKDOWN'])
    preprocessors = [Metadata]
    options = default_options.copy()
    for key in options.keys():
        if key in setting:
            options[key] = setting[key]
    for opt, pre in pres:
        if options[opt]:
            preprocessors.append(pre)
    return preprocessors
