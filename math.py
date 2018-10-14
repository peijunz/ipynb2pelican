# Copied from pelican-ipynb project
class Mathjax:
    '''Math script toolkit'''
    script = """\
<script type="text/javascript">if (!document.getElementById('mathjaxscript_pelican_#%@#$@#')) {
    var mathjaxscript = document.createElement('script');
    mathjaxscript.id = 'mathjaxscript_pelican_#%@#$@#';
    mathjaxscript.type = 'text/javascript';
    mathjaxscript.src = 'MATHJAX_CDN';
    mathjaxscript.src += 'MATHJAX_CONFIG';
    mathjaxscript[(window.opera ? "innerHTML" : "text")] =
        "MathJax.Hub.Config({" +
        "    config: ['MMLorHTML.js']," +
        "    TeX: { extensions: ['AMSmath.js','AMSsymbols.js','noErrors.js','noUndefined.js'], equationNumbers: { autoNumber: 'AMS' } }," +
        "    jax: ['input/TeX','input/MathML','output/HTML-CSS']," +
        "    extensions: ['tex2jax.js','mml2jax.js','MathMenu.js','MathZoom.js']," +
        "    displayAlign: 'center'," +
        "    displayIndent: '0em'," +
        "    showMathMenu: true," +
        "    tex2jax: { " +
        "        inlineMath: [ ['$','$'] ], " +
        "        displayMath: [ ['$$','$$'] ]," +
        "        processEscapes: true," +
        "        processEnvironments: true," +
        "        preview: 'TeX'," +
        "    }, " +
        "    'HTML-CSS': { " +
        " linebreaks: { automatic: true, width: '95% container' }, " +
        "    } " +
        "}); ";
    (document.body || document.getElementsByTagName('head')[0]).appendChild(mathjaxscript);
}
</script>
"""
    cdn = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js'
    conf = '?config=TeX-AMS-MML_HTMLorMML'
    cached = False

    @staticmethod
    def config(setting):
        '''Return configured mathjax script'''
        if not Mathjax.cached:
            if "MATHJAX_CDN" in setting and setting["MATHJAX_CDN"]:
                Mathjax.cdn = setting["MATHJAX_CDN"]
            Mathjax.script = Mathjax.script.replace("MATHJAX_CDN", Mathjax.cdn)
            if "MATHJAX_CONFIG" in setting and setting["MATHJAX_CONFIG"]:
                Mathjax.conf = setting["MATHJAX_CONFIG"]
            Mathjax.script = Mathjax.script.replace("MATHJAX_CONFIG", Mathjax.conf)
            cached_mathjax = True
        return Mathjax.script
