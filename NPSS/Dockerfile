# Define image with OpenMDAO and NPSS

FROM oraclelinux:8

SHELL ["/bin/bash", "-c"]

COPY Miniforge3-Linux-x86_64.sh Miniforge3-Linux-x86_64.sh

# Install Miniforge
RUN bash Miniforge3-Linux-x86_64.sh -b ;\
    rm Miniforge3-Linux-x86_64.sh ;\
    export PATH=$HOME/miniforge3/bin:$PATH ;\
    conda init bash

COPY NPSSv32_src NPSSv32_src

COPY server.py server.py

# Create conda environment
RUN source $HOME/miniforge3/etc/profile.d/conda.sh ;\
    conda create -n mdaowork python=3.12 'numpy<2' scipy cython swig -q -y ;\
    conda activate mdaowork ;\
    conda install git gxx gfortran make cmake unix-ar ncurses sigcpp-2.0 libblas liblapack -q -y ;\
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
# RUN source $HOME/miniforge3/etc/profile.d/conda.sh ;\
#     conda activate mdaowork ;\
#     cd NPSSv32_src ;\
#     source buildNPSS.sh

# Make script  to run server 
RUN echo "source /root/miniforge3/etc/profile.d/conda.sh" >> /run_server.sh ;\
    echo "conda activate mdaowork" >> /run_server.sh ;\
    echo "source /NPSSv32_src/dev/npss.env.sh" >> /run_server.sh ;\
    echo "python /server.py" >> /run_server.sh

ENTRYPOINT ["/bin/bash", "/run_server.sh"]
