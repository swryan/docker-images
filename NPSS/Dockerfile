# Define image with OpenMDAO and NPSS

# FROM ubuntu:20.04
FROM debian:bookworm

SHELL ["/bin/bash", "-c"]

# Install system dependencies
RUN apt-get update -y && apt-get install \
    wget git apt-utils build-essential pkg-config  openjdk-17-jre \
    g++-multilib gcc-multilib gfortran-multilib sigc++ libsigc++ \
    liblapack-dev libblas-dev libopenblas-dev libncurses-dev libxkbcommon-dev \
    libnss3 libnspr4 libgbm1 libasound2 python3-pip cython3 python-is-python3 -y

# Install Miniforge
RUN wget -q -O Miniforge3.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" ;\
    bash Miniforge3.sh -b ;\
    rm Miniforge3.sh ;\
    export PATH=$HOME/miniforge3/bin:$PATH ;\
    conda init bash

COPY NPSSv32_src NPSSv32_src

COPY server.py server.py

# Create conda environment
RUN source $HOME/miniforge3/etc/profile.d/conda.sh ;\
    conda create -n mdaowork python=3.12 'numpy<2' scipy cython swig -q -y ;\
    conda activate mdaowork ;\
    conda install protobuf grpcio grpcio-tools -q -y ;\
    #
    # Install OpenMDAO
    #
    git clone https://github.com/OpenMDAO/OpenMDAO.git ;\
    python -m pip install -e 'OpenMDAO[test]' ;\
    #
    # Install Aviary
    #
    git clone https://github.com/OpenMDAO/Aviary.git ;\
    python -m pip install -e 'Aviary' ;\
    #
    # Install Philote
    #
    git clone https://github.com/chrislupp/Philote-Python.git ;\
    cd Philote-Python ;\
    git submodule init ;\
    git submodule update ;\
    python -m pip install -e . ;\
    #
    conda info ;\
    conda list

# build NPSS
RUN source $HOME/miniforge3/etc/profile.d/conda.sh ;\
    conda activate mdaowork ;\
    cd NPSSv32_src ;\
    source buildNPSS.sh

# Make script  to run server
RUN echo "source /root/miniforge3/etc/profile.d/conda.sh" >> /run_server.sh ;\
    echo "conda activate mdaowork" >> /run_server.sh ;\
    echo "" >> /run_server.sh ;\
    echo "cd /NPSSv32_src/dev/" >> /run_server.sh ;\
    echo "./npssenv" >> /run_server.sh ;\
    echo "source ./npss.env.sh" >> /run_server.sh ;\
    echo "" >> /run_server.sh ;\
    echo "cd /" >> /run_server.sh ;\
    echo "python server.py" >> /run_server.sh

# Set up a work directory that can be shared with the host operating system
WORKDIR /work

ENTRYPOINT ["/bin/bash", "/run_server.sh"]
