FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]
# make tzdata non interactive
ENV DEBIAN_FRONTEND=noninteractive  
# prokka
ENV export PERL5LIB=$CONDA_PREFIX/lib/perl5/site_perl/5.22.0/ 
# mauve/bazam
ENV mauve=/root/downloads/mauve/Mauve.jar 
ENV bazam=/root/downloads/bazam.jar 
ENV MERQURY=/root/merqury-1.3 
ENV PATH=$PATH:/root/meryl-1.3/bin:/root/merqury-1.3 
# krakendb
ENV kraken_db=/root/kraken_db

# --- early preparation
RUN cd root &&\
# INSIDE ~
apt update &&\
apt install -y git &&\
apt install -y python3 &&\
apt install -y python3-pip &&\
apt install -y g++ &&\
apt install -y wget &&\
apt install -y nano

# --- install ANACONDA
RUN cd root && \
mkdir downloads &&\
cd downloads &&\
# INSIDE downloads
# miniconda (download, install, init)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh &&\
bash miniconda.sh -b -p $HOME/miniconda &&\
eval "$(/root/miniconda/bin/conda shell.bash hook)" &&\
echo 'eval "$(/root/miniconda/bin/conda shell.bash hook)"' >> ~/.bashrc

# --- install bam/samtools
RUN cd root && \
apt install -y cmake libjsoncpp-dev samtools bamtools 

# --- install BRACKEN
RUN cd root && \
mkdir git &&\
cd git &&\
# INSIDE git
git clone 'https://github.com/jenniferlu717/Bracken.git' &&\
cd Bracken &&\
# inside git/Bracken
bash install_bracken.sh &&\
ln -s `pwd`/bracken /usr/local/bin/bracken &&\
ln -s `pwd`/bracken-build /usr/local/bin/bracken-build 

# --- install BWA
RUN cd root && \
# inside ~
apt install -y bwa

# --- install KRAKEN2
RUN cd root && eval "$(/root/miniconda/bin/conda shell.bash hook)" &&\
conda install -y -c bioconda kraken2  


# --- install MAUVE 
RUN cd root && \
cd downloads &&\
wget -O Mauve.tar.gz 'darlinglab.org/mauve/snapshots/2015/2015-02-13/linux-x64/mauve_linux_snapshot_2015-02-13.tar.gz' &&\
tar -xvf Mauve.tar.gz --one-top-level=mauve --strip-components 1 &&\
rm Mauve.tar.gz 


# --- install JAVA
RUN cd root && \
apt install -y default-jre 

# --- install PROKKA
RUN cd root && eval "$(/root/miniconda/bin/conda shell.bash hook)" &&\
apt install -y libdatetime-perl libxml-simple-perl libdigest-md5-perl git default-jre bioperl &&\
conda install -y -c conda-forge -c bioconda -c defaults prokka 

# --- install TRIMMOMATIC
RUN cd root && \
apt install -y trimmomatic 

# --- install FASTQC
RUN cd root && \
apt install -y fastqc 

# --- install BAZAM
RUN cd root && \
cd downloads &&\
# inside downloads
wget https://github.com/ssadedin/bazam/releases/download/1.0.1/bazam.jar -O bazam.jar 


# --- install QUAST
RUN cd root && \
pip3 install quast &&\
ln -s /root/miniconda/bin/quast.py /root/miniconda/bin/quast

# --- install checkM
RUN cd root && \
pip3 install checkm-genome &&\
cd downloads &&\
# inside downloads
wget 'https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz' -O checkm_db.tar.gz &&\
tar -xvf checkm_db.tar.gz --one-top-level=checkm_db --strip-components 1 &&\
checkm data setRoot checkm_db &&\
rm checkm_db.tar.gz 

# --- install WGA-LP
RUN cd root && \
cd git &&\ 
git clone 'https://github.com/redsnic/WGA-LP.git' 


# --- install R
RUN cd root && \
apt-get install -y software-properties-common && apt update &&\
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 &&\
add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran40/' &&\
apt update &&\
apt install -y r-base &&\
echo -e 'install.packages("argparse")\ninstall.packages("ggplot2")\ninstall.packages("scales")\ninstall.packages("tidyverse")\nq()' | R --no-save 


# --- install merqury
RUN cd root && \
bash git/WGA-LP/other_scripts/install_merqury.sh &&\
rm *.tar.* 

# --- configure WGA-LP
RUN cd root && \
cd git/WGA-LP &&\
# inside git/WGA-LP
# configure bazam and mauve
mauve=/root/downloads/mauve/Mauve.jar &&\
bazam=/root/downloads/bazam.jar &&\
echo "java -jar $bazam \$@" > /usr/local/bin/bazam &&\
chmod 775 /usr/local/bin/bazam &&\
echo "java -Xmx500m -cp $mauve org.gel.mauve.contigs.ContigOrderer \$@" > /usr/local/bin/mauveContigOrderer &&\
chmod 775 /usr/local/bin/mauveContigOrderer &&\
# install WGA-LP
pip3 install . &&\
# add wgalp.py to the path
chmod 775 /root/git/WGA-LP/wgalp.py &&\
ln -s /root/git/WGA-LP/wgalp.py /usr/local/bin/wgalp 


# --- donwload and setup kraken_db
# if you want to download the mini-kraken package directly uncomment the following:
#
RUN cd root && \
wget 'ftp://ftp.ccb.jhu.edu/pub/data/kraken2_dbs/old/minikraken2_v1_8GB_201904.tgz' -O minikraken2_db.tgz &&\
tar -xvf minikraken2_db.tgz --one-top-level=kraken_db --strip-components 1 
#
# this line is used to instead to copy the db from the build folder, consider editing it
# COPY kraken_db /root/kraken_db

VOLUME /root/shared

# docker commands:
# docker build -t wgalp:0.1 .
# docker run -v /your/path/to/data:/root/shared -itd wgalp:0.1 --name wgalp
# docker exec -it wgalp /bin/bash






