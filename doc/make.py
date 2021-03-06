#!/usr/bin/env python
import fileinput
import glob
import os
import shutil
import sys

def check_build():
    build_dirs = ['build', 'build/doctrees', 'build/html', 'build/latex',
                  '_static', '_templates']
    for d in build_dirs:
        try:
            os.mkdir(d)
        except OSError:
            pass

def figs():
    os.system('cd users/figures/ && python make.py')

def html():
    check_build()
    figs()
    os.system('sphinx-build -b html -d build/doctrees . build/html')

def latex():
    check_build()
    figs()
    if sys.platform != 'win32':
        # LaTeX format.
        os.system('sphinx-build -b latex -d build/doctrees . build/latex')

        # Produce pdf.
        os.chdir('build/latex')

        # Copying the makefile produced by sphinx...
        os.system('pdflatex Basemap.tex')
        os.system('pdflatex Basemap.tex')
        os.system('makeindex -s python.ist Basemap.idx')
        os.system('makeindex -s python.ist modBasemap.idx')
        os.system('pdflatex Basemap.tex')

        os.chdir('../..')
    else:
        print 'latex build has not been tested on windows'

def clean():
    shutil.rmtree('build')

def all():
    figs()
    html()
    latex()


funcd = {'figs':figs,
         'html':html,
         'latex':latex,
         'clean':clean,
         'all':all,
         }


if len(sys.argv)>1:
    for arg in sys.argv[1:]:
        func = funcd.get(arg)
        if func is None:
            raise SystemExit('Do not know how to handle %s; valid args are'%(
                    arg, funcd.keys()))
        func()
else:
    all()
