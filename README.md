# Pelican Plugin for Jupyter Notebooks using MetaCell

This plugin provides markup for Jupyter/IPython notebooks in pelican, so `.ipynb` files are recognized as a valid filetype for an article. 

The plugin is simple and powerful:

+ The css of jupyter will not be taken into outputs. 
+ Math in ipynb is supported
+ Great solution for metadata
+ You can change `preprocessor.py` and use your own preprocessors
+ Change `pres` in [precessors.py]() to enable `#ignore` filter

## MetaCell

Idea of MetaCell:

> All metadata should be stored at the first cell of ipynb. 

MetaCell is the biggest difference from [pelican-ipynb](https://github.com/danielfrg/pelican-ipynb). With MetaCell, there is NO need to create another metadata file, or edit ipynb externally. 

The block below is a template metadata cell

```
# This is title
+ date: 2020-02-22
+ tags: [hello, world]
```

Thanks to the markdown capability of ipynb, MetaCell willl be shown like the following:

### This is title
+ date: 2020-02-22
+ tags: [hello, world]

So, MetaCell itself will even enhance the readability of your notebooks! 
> Hint: In jupyter notebook, press `Esc+M` will switch selected cell to markdown mode. 

## Dependency
+ pelican
+ nbconvert
+ jupyter
+ ipython

## Installation
Download this repo and put all the .py files it into an ipynb directory into your plugins directory.

In the `pelicanconf.py`
```
MARKUP = ('md', 'ipynb')

PLUGIN_PATH = 'pelican-plugins'
PLUGINS = ['pelican-plugins']
```
## TODO
+ More strict MetaCell Check
+ Summary Generation? Using nbconvert and covert it to markdown as summary?
+ Fix the inperfect environment support?

## Acknowledgement
Thanks to [pelican-ipynb](https://github.com/danielfrg/pelican-ipynb)! From reading the code of the project, I have learned how to write a similiar plugin with my own ideas.
