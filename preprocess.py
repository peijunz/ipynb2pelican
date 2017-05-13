from nbconvert.preprocessors import Preprocessor
import re
import ast
import markdown


class Metadata(Preprocessor):
    '''Extract Metadata from first cell. '''
    data = {}
    md = None

    @staticmethod
    def meta_cell(cell):
        '''Process the first cell'''
        lines = cell.split('\n')
        if lines[0].startswith('# '):
            lines[0] = 'title: ' + lines[0][2:]
        lines = [l.lstrip("+ ") for l in lines]
        for line in lines:
            if ':' not in line:
                data = {}
                return False
            key, val = line.split(':', 1)
            key = key.strip().lower()
            val = val.strip()
            if key:
                Metadata.data[key] = val
            else:
                return False
        return True

    @staticmethod
    def preprocess(nb, resources):
        '''Process the notebook to extract metadata'''
        Metadata.data = {}
        if Metadata.meta_cell(nb.cells[0]['source']):
            nb.cells = nb.cells[1:]
            if not nb.cells:
                raise Exception('No content cells after metadata extraction!')
        else:
            raise Exception('Failure in metadata extraction!')
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
                    if re.match(RemoveEmpty.visible, cell['source'])]
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
