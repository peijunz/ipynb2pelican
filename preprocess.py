from nbconvert.preprocessors import Preprocessor
class RemoveEmptyCells(Preprocessor):
    '''Remove Empty Cells'''
    def preprocess(self, nb, resources):
        nb.cells=list(
            filter(lambda c:bool(c['source']), nb.cells)
        )
        return nb, resources

class FirstCellMeta(Preprocessor):
    '''Get metadata'''
    data=dict()
    def setmeta(self, cell):
        keys={"title", "date", "category", "tags", "slug", "author"}
        lines=cell.split('\n')
        if lines[0].startswith('# '):
            lines[0]='title: ' + lines[0][2:]
        lines=[l.strip("+ ") for l in lines]
        for l in lines:
            if ': ' in l:
                key, val=l.split(': ', 1)
                key=key.strip().lower()
                val.strip()
                if key in keys:
                    FirstCellMeta.data[key]=val
        return
    def preprocess(self, nb, resources):
        FirstCellMeta.data=dict()
        self.setmeta(nb.cells[0]['source'])
        nb.cells = nb.cells[1:]
        return nb, resources
