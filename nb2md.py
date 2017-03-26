#!/usr/bin/python3
import json
from nbconvert import export_markdown
import os
def ipynb2md(fname):
    export_markdown(fname)
def setmetadata(fname, meta):
    '''Extract Metadata from the first ipython notebook cell
    and return the ipynb json object
    
    Args:
    fname   filename of ipynb
    meta    + True, write metadata only
            + None, write metadata if specified that do not convert
            + False, Prepare for markdown output

    Example contents for the cell:
    # This is the first title
    + title: This title will overwrite the first title
    + Author: Peijun Zhu
    + date: 2020-02-02
    + tags: [test, helloworld]
    '''
    ipynb_file = open(fname)
    ipynb=json.load(ipynb_file)
    ipynb_file.close()
    firstcell=ipynb['cells'][0]['source'].copy()
    keys={"mode", "title", "date", "category", "tags", "slug", "author"}
    if firstcell[0].startswith('# '):
        firstcell[0]='+ title: ' + firstcell[0][2:]
    firstcell=[i.strip("+ ") for i in firstcell]
    D=dict()
    for i in firstcell:
        if ': ' not in i:
            continue
        k,v=i.split(': ')
        k=k.strip()
        v=v.strip()
        if k in keys:
            D[k]=v
    if (meta is True) or ((meta is None) and ('mode' in D) and (D['mode'] != 'convert')):
        ipynb['metadata'].update(D)
        return False, ipynb
    else:
        ipynb['cells'][0]['source']=firstcell
        ipynb['cells']=list(
            filter(
                lambda c:bool(c['source'])
                , ipynb['cells']
                )
        )
        return True, ipynb
def process_ipynb(name, outpath=None, res_path=None, clean=False, meta=None):
    '''
    Two kinds of processing ipynb:
    + Write information of first cell into Metadata
    + Write information of first cell into pelican blog markdown
    
    For the first type
    '''
    print("{}\nProcessing {}...".format('-'*40, name))
    assert(name.endswith('.ipynb'))
    imgpost={'png', 'jpg', 'svg'}
    conv, ipynb=setmetadata(name, meta)
    path=os.path.split(name)
    name=path[1][:-6]
    if outpath is None:
        if path[0]:
            outpath=path[0]
        else:
            outpath='.'
    if res_path is None:
        res_path=outpath+'/images'
    else:
        res_path=outpath+'/'+res_path
    if clean:
        rmcmd="rm {0}/{2}-output* {1}/{2}.md".format(res_path, outpath, name)
        print(rmcmd)
        os.system(rmcmd)
        return
    if conv:
        tmp='.tmp-'+name+'.ipynb'
        with open(tmp, 'w') as outfile:
            json.dump(ipynb, outfile)
        md, meta=export_markdown(tmp)
        outs=meta['outputs']
        for res in outs:
            l=res.split('.')
            if l[1] in imgpost:
                imgpath=res_path+'/'+name+'-'+res
                with open(imgpath, "wb") as img_file:
                    img_file.write(outs[res])
                print('Wrote {}!'.format(imgpath))
        mdpath=outpath+'/'+name+'.md'
        with open(mdpath, "w") as md_file:
            md_file.write(
                md.replace(
                    '](output_', ']({{attach}}/{}/{}-output_'.format(os.path.split(res_path)[-1], name)
                ).lstrip()
            )
        print('Wrote {}!'.format(mdpath))
        os.remove(tmp)
    else:
        with open(outpath+'/'+name+'.ipynb', 'w') as outfile:
            json.dump(ipynb, outfile)
    return conv
if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert Jupyter Notebook to Markdown for Pelican Blog")
    parser.add_argument("files", help="Input ipynb file",
                        type=str, nargs='*')
    parser.add_argument("-o", '--out', help="Output Dir",
                        type=str, nargs='?')
    parser.add_argument("-c", '--clean', 
                        help="Remove all .md and resources files according to the files/paths specified"
                        , action="store_true")
    parser.add_argument("-m", '--write-meta', help="Write metadata only", action="store_true")
    parser.add_argument("-r", '--resource-path', help="Path for resources related to output dir", type=str, nargs='?')
    args = parser.parse_args()
    for f in args.files:
        process_ipynb(f,
                      args.out, 
                      clean=args.clean, 
                      meta=args.write_meta, 
                      res_path=args.resource_path)
