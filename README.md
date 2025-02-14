This repository contains a collection of [Docker](https://www.docker.com/) image definitions that allow you to quickly create an environment for working with OpenMDAO and related tools.  You can substitute the [podman](https://podman.io) command for `docker` in the following examples if you prefer that tool.

## Packages

In the packages associated with this repository, you will find some pre-built images.

To get up and running with an OpenMDAO development environment, for example, you could do the following:
```
docker run --name openmdao ghcr.io/swryan/docker-images:openmdao-dev &
```
This will pull the image from the GitHub Container Registry (ghcr) and run it, creating a container that you can attach to with:
```
docker exec -it openmdao /bin/bash
```

## Docker Desktop

If you use [Docker Desktop](https://docs.docker.com/desktop/) or [podman desktop](https://podman-desktop.io/), you can just pull down the image with:
```
docker pull ghcr.io/swryan/docker-images:openmdao-dev
```
and then work with the downloaded image within that application.

Note that the default shell when attaching to a container in Docker Desktop is `sh` and you will want to run a `bash` shell to access the pre-built Python environment.

## Build from Dockerfile

You may also build an image yourself from the associated Dockerfile found in this repository.

If you have access to [SNOPT](https://ccom.ucsd.edu/~optimizers/solvers/snopt/) for example,
you may want to copy one of the `-snopt` image definitions to your computer, populate the `snopt-src` directory and build an image with SNOPT support.

## Integrate with host environment

When you get a shell prompt into a container, you will start in an empty `work` directory.  You can map this directory to
a directory on the host machine to make your working files available both inside and outside of the container.  This is
done via the `-v` option on the command line as seen below (or in the desktop UI).

```
# make sure the host directory is writable by docker
chmod 777 `pwd`/work

# run container, mappping host directory to the work directory in the container
docker run --name omdev -v `pwd`/work:/home/omdao/work:rw -it openmdao-dev &

# when working in the container's 'work' directory, files will be accessible on the host as well
docker exec -it omdev /bin/bash
```

Each image contains the `google-chrome` browser for viewing OpenMAO reports. To make use of this feature, you need to
set the `DISPLAY` environment variable in the container.

On the host:
```
~/dev/docker-images$ env | grep DISPLAY
DISPLAY=172.21.192.1:0.0
```
In the container:
```
(mdaowork) omdao@dbf0cc234e32:~/work$ export DISPLAY=172.21.192.1:0.0
(mdaowork) omdao@dbf0cc234e32:~/work$ openmdao n2 ~/OpenMDAO/openmdao/test_suite/scripts/circle_opt.py
```
