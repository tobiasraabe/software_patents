# -*- coding: utf-8 -*-

# Documentation build configuration file, created by sphinx-quickstart

# This file is execfile() with the current directory set to its containing dir.

# Note that not all possible configuration values are present in this
# autogenerated file.

# All configuration values have a default; values that are commented out serve
# to show the default.

import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../..'))

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.6'

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named 'sphinx.ext.*')
# or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxcontrib.bibtex',
    'nbsphinx',
    # bug fix for https://github.com/spatialaudio/nbsphinx/issues/24
    'IPython.sphinxext.ipython_console_highlighting',
]

suppress_warnings = ['app.add_directive', 'app.add_node', 'app.add_role']

autodoc_mock_imports = [
    'bld',
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'sklearn',
]

# Boolean indicating whether to scan all found documents for autosummary
# directives, and to generate stub pages for each.
# autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Identification Strategies of Software Patents'
copyright = u'2015-, Tobias Raabe'  # noqa: A001

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.1'
# The full version, including alpha/beta/rc tags.
release = '0.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = '
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%d %B %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '**.ipynb_checkpoints']

# The reST default role (used for this markup: `text`) to use for all
# documents. default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['src.']


# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# '<project> v<release> documentation'.
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
# html_static_path = ['_static']

# If not ', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, 'Created using Sphinx' is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, '(C) Copyright ...' is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
html_file_suffix = '.html'

# Output file base name for HTML help builder.
htmlhelp_basename = 'somedoc'


# -- Options for LaTeX output -------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',
    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '11pt',
    # Remove the 'Release ...' subtitle from the LaTeX frontpage.
    'releasename': '',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': ',
    # Add options to remove blank pages
    'classoptions': ', openany, oneside',
}

# Grouping the document tree into LaTeX files. List of tuples (source start
# file, target name, title, author, documentclass [howto/manual]). Usually the
# list will only consist of one tuple for the master file.
latex_documents = [
    (
        'index',
        'documentation.tex',
        'Documentation of the Identification Strategies of Software Patents '
        'project',
        'Tobias Raabe',
        'manual',
    )
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ""

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True

# -- Options for nbsphinx -----------------------------------------------------

# Execute notebooks before conversion: 'always', 'never', 'auto' (default)
nbsphinx_execute = 'never'

# Use this kernel instead of the one stored in the notebook metadata:
# nbsphinx_kernel_name = 'python3'

# List of arguments to be passed to the kernel that executes the notebooks:
# nbsphinx_execute_arguments = [
#     '--InlineBackend.figure_formats={"png", "pdf"}'
# ]

# If True, the build process is continued even if an exception occurs:
nbsphinx_allow_errors = False

# Controls when a cell will time out (defaults to 30; use -1 for no timeout):
# nbsphinx_timeout = 60

# Default Pygments lexer for syntax highlighting in code cells:
# nbsphinx_codecell_lexer = 'ipython3'

# Width of input/output prompts used in CSS:
# nbsphinx_prompt_width = '8ex'

# If window is narrower than this, input/output prompts are on separate lines:
# nbsphinx_responsive_width = '700px'

# This is processed by Jinja2 and inserted before each notebook
# nbsphinx_prolog = r"""
# {% set docname = env.doc2path(env.docname, base='doc') %}

# .. only:: html

#     .. role:: raw-html(raw)
#         :format: html

#     .. nbinfo::

#         This page was generated from `{{ docname }}`__.
#         Interactive online version:
#         :raw-html:`<a
#             href="https://mybinder.org/v2/gh/spatialaudio/nbsphinx/{{
#             env.config.release }}?filepath={{ docname }}"><img alt="Binder
#             badge" src="https://mybinder.org/badge.svg"
#             style="vertical-align:text-bottom"></a>`

#     __ https://github.com/spatialaudio/nbsphinx/blob/
#         {{ env.config.release }}/{{ docname }}

# .. raw:: latex

#     \vfil\penalty-1\vfilneg
#     \vspace{\baselineskip}
#     \textcolor{gray}{The following section was generated from
#     \texttt{\strut{}{{ docname }}}\\[-0.5\baselineskip]
#     \noindent\rule{\textwidth}{0.4pt}}
#     \vspace{-2\baselineskip}
# """

# This is processed by Jinja2 and inserted after each notebook
# nbsphinx_epilog = r"""
# .. raw:: latex

#     \textcolor{gray}{\noindent\rule{\textwidth}{0.4pt}\\
#     \hbox{}\hfill End of
#     \texttt{\strut{}{{ env.doc2path(env.docname, base='doc') }}}}
#     \vfil\penalty-1\vfilneg
# """
