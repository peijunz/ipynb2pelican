from nbconvert.preprocessors import Preprocessor

class Metadata(Preprocessor):
    '''Extract Metadata from first cell. '''
    data={}
    @staticmethod
    def meta_line(line):
        if ':' in line:
            key, val = line.split(': ', 1)
            key=key.strip().lower()
            val.strip()
            if key:
                Metadata.data[key]=val
            return True
        else:
            return False
    @staticmethod
    def meta_cell(cell):
        lines=cell.split('\n')
        if lines[0].startswith('# '):
            lines[0]='title: ' + lines[0][2:]
        lines=[l.lstrip("+ ") for l in lines]
        for l in lines:
            if not Metadata.meta_line(l):
                data={}
                return False
        return True
    @staticmethod
    def preprocess(nb, resources):
        Metadata.data=dict()
        if Metadata.meta_cell(nb.cells[0]['source']):
            nb.cells = nb.cells[1:]
        return nb, resources
class SubCells(Preprocessor):
    """A preprocessor to select a slice of the cells of a notebook
    The subcell function is executed after Metadata preprocessor, so
    0th Cell is the first cell after MetaCell
    Read start and end from the metacell like:
    + subcells: [5, 10]
    """
    start = 0
    end = None
    @staticmethod
    def preprocess(nb, resources):
        # Get start/end from subcells metadata
        if 'subcells' in Metadata.data:
            SubCells.start, SubCells.end=eval(Metadata.data['subcells'])
        tmp=nb.cells[SubCells.start:SubCells.end]
        if tmp:
            nb.cells = tmp
        else:
            #print(SubCells.start, SubCells.end, tmp)
            raise Exception('Wrong Slicing Range!')
        return nb, resources

class RemoveEmpty(Preprocessor):
    '''Remove Empty Cells
    Tested'''
    @staticmethod
    def preprocess(nb, resources):
        nb.cells=list(
            filter(lambda c:bool(c['source']), nb.cells)
        )
        return nb, resources

class IgnoreTag(Preprocessor):
    '''Ignore Cells with #ignore tag in the beginning
    Tested'''
    @staticmethod
    def preprocess(nb, resources):
        nb.cells=list(
            filter(
                lambda cell: not (cell['source'].startswith('#ignore')),
                nb.cells
                )
        )
        return nb, resources

# Below is the configuration process
class Preprocess:
    # Precedence: Metadata > SubCells > IgnoreTag = RemoveEmpty
    pres=[('IPYNB_SUBCELLS', SubCells),
          ('IPYNB_IGNORE', IgnoreTag),
          ('IPYNB_REMOVE_EMPTY', RemoveEmpty),]
    options={'IPYNB_REMOVE_EMPTY': True,
                 'IPYNB_IGNORE': True,
                 'IPYNB_SUBCELLS': True,}
    enabled_prepros=[Metadata]

def config_pres(setting):
    ''''''
    # Refresh preprocessor options by setting
    for key in Preprocess.options.keys():
        if key in setting:
            Preprocess.options[key]=setting[key]
    for opt, pre in Preprocess.pres:
        if Preprocess.options[opt]:
            Preprocess.enabled_prepros.append(pre)
    return Preprocess.enabled_prepros
if __name__=="__main__":
    import doctest
    
