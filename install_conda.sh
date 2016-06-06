os=MacOSX

MINICONDA_URL=http://repo.continuum.io/miniconda
MINICONDA_FILE=Miniconda3-latest-${os}-x86_64.sh
wget ${MINICONDA_URL}/${MINICONDA_FILE}
bash $MINICONDA_FILE -b -p '$HOME/miniconda'
ls $HOME/miniconda
export PATH=$HOME/miniconda/bin:$PATH
hash -r
conda config --set always_yes yes --set changeps1 no
