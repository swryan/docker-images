# This Docker File is for use by NASA Developers of OpenMDAO, Dymos, and Aviary
# This file contains SNOPT, a proprietary software code, and cannot be distributed outside of NASA

FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

# Install updates
RUN apt-get update -y && apt-get -y install wget git pip gfortran libblas-dev liblapack-dev
    # texlive-latex-base texlive-latex-extra \
    # texlive-latex-recommended texlive-pictures

# Install Miniforge which gives us access to conda
# from https://github.com/conda-forge/miniforge
RUN wget -O Miniforge3.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" ;\
    bash Miniforge3.sh -b ;\
    rm Miniforge3.sh ;\
    export PATH=$HOME/miniforge3/bin:$PATH ;\
    conda init bash

# Create the conda environment
RUN . "$HOME/miniforge3/etc/profile.d/conda.sh" ;\
    conda create -n mdaowork python=3.12 'numpy<2' scipy cython swig -y ;\
    conda activate mdaowork ;\
    conda install matplotlib -y ;\
    conda install mpi4py petsc4py -y ;\
    conda install graphviz -y ;\
    pip install pyparsing psutil objgraph plotly pyxdsm pydot

# Copy SNOPT source code into the container
COPY ./snopt-src ./snopt-src

# Install PyOptSparse into the conda environment
RUN . "$HOME/miniforge3/etc/profile.d/conda.sh" ;\
    conda activate mdaowork ;\
    pip install git+https://github.com/openmdao/build_pyoptsparse ;\
    build_pyoptsparse -s ./snopt-src -v

# Clone the OpenMDAO, Dymos, and Aviary repositories into the container
RUN mkdir /OMDAO
RUN git clone https://github.com/OpenMDAO/OpenMDAO.git /OMDAO/OpenMDAO
RUN git clone https://github.com/OpenMDAO/dymos.git /OMDAO/Dymos
RUN git clone https://github.com/OpenMDAO/Aviary.git /OMDAO/Aviary

# Install OpenMDAO, Dymos, and Aviary into the conda environment in developer mode
RUN . "$HOME/miniforge3/etc/profile.d/conda.sh" ;\
    conda activate mdaowork ;\
    pip install -e '/OMDAO/OpenMDAO[all]' ;\
    pip install -e '/OMDAO/Dymos[all]' ;\
    pip install -e '/OMDAO/Aviary[test]'

# Modify the Bashrc file
RUN echo "## Always activate mdaowork environment on startup ##" >> ~/.bashrc ;\
    echo "conda activate mdaowork" >> ~/.bashrc ;\
    echo "" >> ~/.bashrc ;\
    echo "## OpenMPI settings" >> ~/.bashrc ;\
    echo "export OMPI_MCA_rmaps_base_oversubscribe=1" >> ~/.bashrc ;\
    echo "export OMPI_MCA_btl=^openib" >> ~/.bashrc ;\
    echo "" >> ~/.bashrc ;\
    echo "## Required for some newer MPI / libfabric instances" >> ~/.bashrc ;\
    echo "export RDMAV_FORK_SAFE=true" >> ~/.bashrc ;\
    echo "" >> ~/.bashrc ;\
    echo "## Always cd into OMDAO folder when bash starts ##" >> ~/.bashrc ;\
    echo "cd /OMDAO" >> ~/.bashrc ;\
    echo "" >> ~/.bashrc
