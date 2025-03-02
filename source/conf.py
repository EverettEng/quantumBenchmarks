# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os 
import sys

sys.path.insert(0, os.path.abspath('/home/everett/SERS_project/'))

import construct_benchmarks.bqskit_benchmarks
import construct_benchmarks.qiskit_benchmarks
import bqskit_comp.compile
import predetermined.compile

project = 'quantumBenchmarks'
copyright = '2025, Everett Eng'
author = 'Everett Eng'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_rtd_theme"]

html_theme = "sphinx_rtd_theme"

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
