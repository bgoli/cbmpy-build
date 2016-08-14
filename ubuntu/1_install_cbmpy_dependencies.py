# Detect all MetaToolKit depencies on Ubuntu and create a custom script to install them.
# Tested on Ubuntu 14.04, 16.04
# Author Brett G. Olivier (bgoli@users.sourceforge.net)
# (C) All rights reserved, Brett G. Olivier, Amsterdam 2016.

import os, subprocess, itertools, stat

res = {'Required' : {},\
       'Optional' : {}
       }

# First lets check for some Python essentials

reqcnt = itertools.count(1,1)
optcnt = itertools.count(1,1)

# this should just be there for any sane python build environment
res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install build-essential g++ gfortran python python-dev'
try:
    import pip
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-pip'
# try:
    # import setuptools
# except ImportError:
    # res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-setuptools'
try:
    import numpy
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-numpy'
try:
    import sympy
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-sympy'
try:
    import xlrd
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-xlrd'
try:
    import xlwt
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-xlwt'
try:
    import matplotlib
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-matplotlib'
try:
    import PyQt4
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-qt4'
try:
    import Bio
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-biopython'
try:
    import nose
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install python-nose'    
try:
    import libsbml
    if libsbml.LIBSBML_VERSION < 51201:
        raise ImportError
except ImportError:
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install libxml2 libxml2-dev libxslt-dev zlib1g zlib1g-dev bzip2 libbz2-dev'
    res['Required'][reqcnt.next()] = 'sudo -EH pip install --upgrade python-libsbml'
try:
    import cbmpy
except:
    res['Required'][reqcnt.next()] = 'sudo -E easy_install --upgrade cbmpy'
try:
    out = subprocess.call(['java', '-version'])
except (OSError):
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install default-jre'
try:
    out = subprocess.call(['perl', '-v'])
except (OSError):
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
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install libxml-parser-perl'
try:
    out = subprocess.call(['blastall'])
except (OSError):
    res['Required'][reqcnt.next()] = 'sudo -E apt-get -y install blast2'


# Optional/recommended
try:
    import IPython
except ImportError:
    res['Optional'][optcnt.next()] = 'sudo -E apt-get -y install ipython ipython-notebook'
try:
    import suds
except ImportError:
    res['Optional'][optcnt.next()] = 'sudo -E apt-get -y install python-suds'
try:
    import flask
except ImportError:
    res['Optional'][optcnt.next()] = 'sudo -E apt-get -y install python-flask'

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
