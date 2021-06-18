# INSTALL mrequry

# run this script in your home directory

# ---- prerequisito (meryl)

wget https://github.com/marbl/meryl/releases/download/v1.3/meryl-1.3.Linux-amd64.tar.xz
tar -xJf meryl-1.3.Linux-amd64.tar.xz
# sostituire con cartella opportuna il percorso
export PATH=$HOME/meryl-1.3/bin:$PATH
# test
meryl
# aggiungi al PATH
echo 'export PATH=$HOME/meryl-1.3/bin:$PATH' >> ~/.bashrc

# ---- merqury

wget https://github.com/marbl/merqury/archive/v1.3.tar.gz
tar -zxvf v1.3.tar.gz
cd merqury-1.3
# create MERQURY variable (adattare i path)
export MERQURY=$HOME/merqury-1.3
echo 'export MERQURY=$HOME/merqury-1.3' >> ~/.bashrc
# test 
Rscript $MERQURY/plot/plot_spectra_cn.R --help
 
# IF THERE ARE ERRORS RUNNING R (because of missing package)
# --- run
# R
# install.packages("nameoftheproblematicpackage") # if there are more packaages, repeat this command with all required names
# q() # say no to the prompt to save your workspace
