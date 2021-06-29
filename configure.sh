#!/usr/bin/env bash

# This script installs mauveContigOrderer and bazam so that they can be called from command line
# usage: configure.sh path_folder bazam_path mauve_path

# make folder (that will be added to the path)
mkdir $1
export PATH=$PATH:$1
# add scripts to run bazam and mauve
sudo echo "java -jar $2 \$@" > $1/bazam && sudo chmod 775 $1/bazam &&\
sudo echo "java -Xmx500m -cp $3 org.gel.mauve.contigs.ContigOrderer \$@" > $1/mauveContigOrderer &&\
sudo chmod 775 $1/mauveContigOrderer &&\
echo "--- Installation completed successfully ---"