import os, sys, imp

config = imp.load_source('config', '../src/config.py')
pathname = os.getcwd()

os.system('make html')
os.system('make latex')
os.system('make htmlhelp')
os.chdir(pathname + '/build/latex/')
os.system('pdflatex "%s Benutzerhandbuch.tex"' % config.APP_NAME)
os.system('pdflatex "%s Entwicklerhandbuch.tex"' % config.APP_NAME)

