# Workshop held at MIFOBIO 2018

## Getting Started

These instructions will get you running on your local machine all exercises done at mifobio.

### Prerequisites

You need to install `git`, `docker` and `omero insight`

### Installing Git

> *Git* is a [free and open source](http://git-scm.com/about/free-and-open-source) distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

Choose one of the following options.
- [Instructions for *Windows*](https://git-scm.com/download/win)
- [Instructions for *Mac*](https://git-scm.com/download/mac)
- [Instructions for *Linux*](https://git-scm.com/download/linux)

**You can use *Git* now.**

### Installing Docker
> [*Docker*](https://www.docker.com) is a tool designed to make it easier to create, deploy, and run applications by using containers.

Choose one of the following options.
- [Instructions for *Windows*](https://docs.docker.com/docker-for-windows/install/)
- [Instructions for *Mac*](https://docs.docker.com/docker-for-mac/install/)
- [Instructions for *Linux - CentOS*](https://docs.docker.com/install/linux/docker-ce/centos/)
- [Instructions for *Linux - Debian*](https://docs.docker.com/install/linux/docker-ce/debian/)
- [Instructions for *Linux - Fedora*](https://docs.docker.com/install/linux/docker-ce/fedora/)
- [Instructions for *Linux - Ubuntu*](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

**You can use *Docker* now.**

### Installing OMERO Insight
> *OMERO.insight* is a client to upload, view and download data from any personal computer.

You can download your omero client according to your operating system in this [page](https://www.openmicroscopy.org/omero/downloads/)

**The next steps are done with a ubuntu 16.04 LTS.**

## Clone workshop repository

Copy and paste these instructions on a terminal:

```shell
cd ~
git clone https://github.com/MontpellierRessourcesImagerie/jupyter-workshop-mifobio-2018.git
cd jupyter-workshop-mifobio2018
```

## Run an omero container

To run OMERO simply do:

```shell
docker volume create --name omero-db
docker volume create --name omero-data
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres postgres
docker run -d --name omero-server --link postgres:db -e CONFIG_omero_db_user=postgres -e CONFIG_omero_db_pass=postgres -e CONFIG_omero_db_name=postgres -e ROOTPASS=omero-root-password -v omero-data:/OMERO -p 4063:4063 -p 4064:4064 openmicroscopy/omero-server:latest
docker run -d --name omero-web --link omero-server:omero -p 4080:4080 openmicroscopy/omero-web-standalone:latest
```

It will launch all services : PostgreSQL server, OMERO.server and OMERO.web.
All data needed for postgres database are saved inside **omero-db** and all data needed for server are saved inside **omero-data**.

To connect to the server with the OMERO.web client, go to [https://localhost](https://localhost:4080).
Default admin credentials are `root` and `omero-root-password`.

To connect to the server with the OMERO Insight client use `localhost` as a server address and `4064` (by default) for the port.

## Import Images to OMERO with OMERO.Insight client

You can follow these instructions on this [page](https://help.openmicroscopy.org/importing-data-5.html) to import image data onto the OMERO server.   
The goal is to import images located inside jupyter-workshop-mifobio-2018/exercises/images/PK-10B-pl1 and jupyter-workshop-mifobio-2018/exercises/images/PK-11B-pl1 directories. You can visualize an example as below onto the omero web.
![](capture_omero-web.png?raw=true)

## Run a jupyter container

To run a jupyter notebook, i use a slightly modified version of a dockerfile given by [**ome**](https://github.com/ome/training-notebooks).
To run jupyter notebook simply do:

```shell
#create workshop-mifobio2018 image
docker build -t workshop-mifobio2018 .
#run workshop-mifobio2018 image
docker run -it --net host -p 8888:8888 -v `*path_to_exercises_folder*`:/home/jovyan/mifobio_2018/exercises workshop-mifobio2018
```

All update/new notebooks in exercises are will save in your local directory `path_to_exercises_folder`

#### Docker commands

- `docker ps` — Lists running containers. Some useful flags include: `-a` / `-all` for all containers (default shows just running) and `—-quiet` /`-q` to list just their ids (useful for when you want to get all the containers).
- `docker pull` — Most of your images will be created on top of a base image from the Docker Hub registry. Docker Hub contains many pre-built images that you can pull and try without needing to define and configure your own. To download a particular image, or set of images (i.e., a repository), use `docker pull`.
- `docker build` — The `docker build` command builds Docker images from a Dockerfile and a “context”. A build’s context is the set of files located in the specified PATH or URL. Use the `-t` flag to label the image, for example `docker build -t my_container` . with the . at the end signalling to build using the currently directory.
- `docker run` — Run a docker container based on an image, you can follow this on with other commands, such as `-it bash` to then run bash from within the container. Also see Top 10 options for `docker run — a` quick reference guide for the CLI command. `docker run my_image -it bash`
- `docker logs` — Use this command to display the logs of a container, you must specify a container and can use flags, such as `--follow` to follow the output in the logs of using the program. `docker logs --follow my_container`
- `docker volume ls` — This lists the volumes, which are the preferred mechanism for persisting data generated by and used by Docker containers.
- `docker rm` — Removes one or more containers. `docker rm my_container`
- `docker rmi` — Removes one or more images. `docker rmi my_image`
- `docker stop` — Stops one or more containers. `docker stop my_container` stops one container, while `docker stop $(docker ps -a -q)` stops all running containers. A more direct way is to use `docker kill my_container`, which does not attempt to shut down the process gracefully first.
