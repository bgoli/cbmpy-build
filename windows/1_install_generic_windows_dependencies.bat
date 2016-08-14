@ECHO OFF
easy_install numpy scipy matplotlib
easy_install xlrd xlwt sympy biopython
easy_install libsbml ipython
easy_install install --upgrade cbmpy

echo  Don't forget Qt4 if you don't have it already (import PyQt4)
echo .
echo http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x64.exe