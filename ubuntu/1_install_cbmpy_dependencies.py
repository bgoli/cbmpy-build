# Detect all MetaToolKit depencies on Ubuntu and create a custom script to install them.
# Tested on Ubuntu 14.04, 16.04
# Author Brett G. Olivier (bgoli@users.sourceforge.net)
# (C) All rights reserved, Brett G. Olivier, Amsterdam 2016.

import os, subprocess, itertools, stat

UBUNTU = CONDA = False
try:
    print(os.sys.argv)
    arg = os.sys.argv[1]
except:
    arg = 'UBUNTU'
if arg == 'UBUNTU':
    UBUNTU = True
elif arg == 'CONDA':
    CONDA = True
else:
    print('\nPlease call script with CONDA as argument for Anaconda install script, defaulting to UBUNTU')
    UBUNTU = True

res = {'Required' : {},\
       'Optional' : {}
       }

# First lets check for some Python essentials
reqcnt = itertools.count(1,1)
optcnt = itertools.count(1,1)
# this should just be there for any sane python build environment
if UBUNTU:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install build-essential g++ gfortran python python-dev'
if CONDA:
    res['Required'][reqcnt.next()] = 'conda update -y conda # if this is the only required package ignore it'
try:
    import pip
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-pip'
try:
    import numpy
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-numpy'
try:
    import sympy
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-sympy'
try:
    import xlrd
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-xlrd'
try:
    import xlwt
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-xlwt'
try:
    import matplotlib
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-matplotlib'
try:
    import PyQt4
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-qt4'
    elif CONDA:
        res['Required'][reqcnt.next()] = 'conda install -y pyqt=4.11.4'
try:
    import Bio
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-biopython'
    elif CONDA:
        res['Required'][reqcnt.next()] = 'conda install -y biopython'
try:
    import nose
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-nose'
try:
    import docx
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -EH pip install docx'    
    elif CONDA:
        res['Required'][reqcnt.next()] = 'pip install docx'    
try:
    import libsbml
    if libsbml.LIBSBML_VERSION < 51201:
        print('\nPlease update to the latest version of libSBML.\n')
        raise ImportError
except ImportError:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install libxml2 libxml2-dev libxslt-dev zlib1g zlib1g-dev bzip2 libbz2-dev'
        res['Required'][reqcnt.next()] = 'sudo -EH pip install --upgrade python-libsbml'
    elif CONDA:
        res['Required'][reqcnt.next()] = 'conda install -c SBMLTeam -y python-libsbml'
try:
    import cbmpy
except:
    if UBUNTU:
        res['Required'][reqcnt.next()] = 'sudo -EH pip install --upgrade cbmpy'
        res['Required'][reqcnt.next()] = 'sudo python -c "import cbmpy"'
    if CONDA:
        res['Required'][reqcnt.next()] = 'pip install cbmpy'
        res['Required'][reqcnt.next()] = 'python -c "import cbmpy"'
try:
    out = subprocess.call(['java', '-version'])
except (OSError):
    if UBUNTU or CONDA:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install default-jre'

try:
    out = subprocess.call(['perl', '-v'])
except (OSError):
    if UBUNTU or CONDA:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install perl'
p_script = """\
my $rc = 0;
$rc = eval
{
  require XML::Parser;
  XML::Parser->import();
  1;
};
if ($rc){
    exit 0
    } else {
    exit 1
    }
"""
try:
    PF = file('_test.pl', 'w')
    PF.write(p_script)
    PF.close()
    out = int(subprocess.call(['perl', '_test.pl']))
    if out:
        raise OSError
except (OSError):
    if UBUNTU or CONDA:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install libxml-parser-perl'
try:
    out = subprocess.call(['blastall'])
except (OSError):
    if UBUNTU or CONDA:
        res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install blast2'

# Optional/recommended
# https://github.com/bgoli/cbmpy-glpk
if UBUNTU:
    res['Optional'][optcnt.next()] = 'sudo apt-get -y install git cython libxml2-dev libxslt-dev'
try:
    import IPython
except ImportError:
    if UBUNTU:
        res['Optional'][optcnt.next()] = 'sudo -E apt-get -y install ipython ipython-notebook'
try:
    import suds
except ImportError:
    if UBUNTU:
        res['Optional'][optcnt.next()] = 'sudo -E apt-get -y install python-suds'
    elif CONDA:
        res['Optional'][optcnt.next()] = 'pip install suds'
try:
    import flask
except ImportError:
    if UBUNTU:
        res['Optional'][optcnt.next()] = 'sudo -E apt-get -y install python-flask'

if UBUNTU or CONDA:
    bash_script="""\
    while true; do
        read -p "Do you wish to install *{}* MetaToolkit dependencies? [y/n]: " yn
        case $yn in
            [Yy]* ) echo "Installing ..."; break;;
            [Nn]* ) exit;;
            * ) echo "Please enter y/n.";;
        esac
    done
    
    """
    
    bash_script="""\
    
    # {}
    
    """
    
    output = '#!/bin/sh\n\n'
    output += '#MetaToolkit: Ubuntu system requirements check\n'
    output += '#=============================================\n\n'
    
    REQUIRE_USER_INPUT = False
    
    for r in res:
        if len(res[r]) > 0:
            if REQUIRE_USER_INPUT:
                output += bash_script.format(r)
            output += '#{}\n#{}\n\n'.format(r, '-'*len(r))
            resk = list(res[r])
            resk.sort()
            for k in resk:
                if k != None:
                    output += '{}\n'.format(res[r][k])
            output += '\n'
    output += 'exit\n\n'
    fname = 'metatoolkit_install_dependencies.sh'
    F = file(fname, 'w')
    F.write(output)
    F.close()
    os.chmod(fname, stat.S_IRWXU)
    
    print('')
    print(output)
    print('\n\nInstall script (shown above) saved as file: {}\nplease examine it carefully and run. Alternatively install individual dependencies manually').format(fname)
