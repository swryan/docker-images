This repository contains a collection of [Docker](https://www.docker.com/) image definitions that allow you to quickly create an environment for working with OpenMDAO and related application libraries.

### Packages
  
In the packages associated with this repository, you will find some pre-built images.

To get up and running with an OpenMDAO development environment, for example, you could do the following:
```
docker run --name openmdao ghcr.io/swryan/docker-images:openmdao-dev &
```
This will pull the image from the GitHub Container Registry (ghcr) and run it, creating a container that you can attach to with:
```
docker exec -it openmdao /bin/bash
```

### Docker Desktop

If you use [Docker Desktop](https://docs.docker.com/desktop/), you can just pull down the image with:
```
docker pull ghcr.io/swryan/docker-images:openmdao-dev
```
and then work with the downloaded image within that application. 

Note that the default shell when attaching to a container is `sh` and you will want to run a `bash` shell to access the pre-built Python environment.

### Build from Dockerfile

You may also build an image yourself from the associated Dockerfile found in this repository.  

If you have access to [SNOPT](https://ccom.ucsd.edu/~optimizers/solvers/snopt/) for example, 
you may want to copy one of the `-snopt` image definitions to your computer, populate the `snopt-src` directory and build an image with SNOPT support.
