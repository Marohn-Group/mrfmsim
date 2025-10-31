# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath("../../mrfmsim"))
sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'mrfmsim'
# copyright = '2023 - 2025, Peter Sun'
author = 'Peter Sun'
release = '0.4.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    # 'nbsphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = []


# -- custom directive for rst -----------------------------------------------------

from docutils.parsers.rst import Directive
from docutils import nodes
import mrfmsim.experiment

class GroupDirective(Directive):
    """Discover all experiments in a group and output their string representation."""

    has_content = True
    required_arguments = 1
    optional_arguments = 0

    def run(self):

        name_list = self.arguments[0].split(".") # e.g. mrfmsim.experiment.exptgroup
        exptgroup = getattr(mrfmsim.experiment, name_list[-1])
        node_out = []
        for expt in exptgroup.experiments:
            child_node = nodes.literal_block(text=str(exptgroup.experiments[expt]))
            node = nodes.list_item(
                "", nodes.strong(text=f"{expt}"), child_node
            )
            # the bullet_list doesn't do anything but create an indentation
            list_node = nodes.bullet_list("", node)
            node_out.append(list_node)

        return node_out


class ExperimentDirective(Directive):
    """Output experiment string representation."""

    has_content = True
    required_arguments = 1
    optional_arguments = 0

    def run(self):

        name_list = self.arguments[0].split(".") # e.g. mrfmsim.experiment.expt
        expt = getattr(mrfmsim.experiment, name_list[-1])

        child_node = nodes.literal_block(text=str(expt))
        # the bullet_list doesn't do anything but create an indentation
        list_node = nodes.bullet_list("", child_node)
        return [list_node]


def setup(app):
    app.add_directive("group", GroupDirective)
    app.add_directive("experiment", ExperimentDirective)
