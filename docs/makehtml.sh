cd generated
ipython nbconvert --to rst ../*.ipynb # run from ./docs/generated
cd ../source
ipython nbconvert --to rst ../*.ipynb # run from ./docs/generated
cd ..
make html