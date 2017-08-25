# REDsym

REDsym uses existing metadata saved by Whatmanager2 (https://github.com/karamanolev/WhatManager2) to create a symlinked mirror directory.

It uses the ReleaseInfo2.txt files to extract: artists names, album name, year, codec, Catalogue number... and create the mirrored structure.

REDsym does not modify or delete any of the source files or folders to be symlinked.  

It turns this structure:

```
$ tree ~/WM2/12345/album/
.
│── ABC.mp3
└── DEF.mp3
```

into this structure:

```
$ tree ~/redsym/
.
├── The Doors
	├── (1967) The Doors (40th Anniversary Edition)  (WPCR-12716)  [FLAC]
	├── (1971) L.A. Woman (40th Anniversary Edition)  (WPCR-12721)  [MP3] 
	├── (1971) L.A. Woman (5.1 Surround 24-88.2)  (CAPP 75011 SA)  [FLAC]
	├── (1971) L.A. Woman (62612-9)  [FLAC] 
	└── (1971) L.A. Woman (62612-9)  [MP3] 
├── The Dream Syndicate
├── The Drift
└── [...etc...]
```

## Tested with

 - Python 3.4
 - Linux (Ubuntu 14.04)
 - Gazelle trackers metadata (RED, WCD)

## Requires

 - python-ftfy (to fix encoding issues)
 - mysql
 - A filesystem that supports os.symlink


## Configuration
Configure folders, mysql database name/user/pass in "settings.py".

## Running the script

	$python3 redsym.py update

## Docker

### Network

Create network used for inter-container communication between the database container and the application container:

```
sudo docker network create --internal redsym
```

### Database container

Create a volume to store MariaDB's persistent data:

```
sudo docker volume create redsym-mariadb-data
```

Create the database container:

```
sudo docker run --rm -d \
	--name redsym-mariadb \
	--network redsym \
	--mount type=volume,src=redsym-mariadb-data,dst=/var/lib/mysql \
	-e MYSQL_RANDOM_ROOT_PASSWORD=yes \
	-e MYSQL_DATABASE=REDsym \
	-e MYSQL_USER=redsym \
	-e MYSQL_PASSWORD=redsym \
	mariadb:10.2 \
	--character-set-server=utf8mb4 \
	--collation-server=utf8mb4_unicode_ci
```

### Application container

Build image based on Dockerfile found in the current directory: `sudo docker build --tag redsym .`

Copy the `settings.py` file, e.g. `mkdir conf && cp REDsym/settings.py conf/` and edit it. Set `DB_HOST = 'redsym-mariadb'`, this is the name of the MariaDB container. For example:

```
rootdir_wcd = ''

rootdir_red = '/mnt/music-dl/'

redsym_dir = '/mnt/music-lib/'

DB_HOST = 'redsym-mariadb'
DB_NAME = 'REDsym'
DB_USER = 'redsym'
DB_PASS = 'redsym
```

Run an instance of REDsym based on the image we built:

```
sudo docker run --rm -it \
	--name redsym \
	--network redsym \
	--mount type=bind,src=/mnt/music-dl/,dst=/mnt/music-dl/,readonly \
	--mount type=bind,src=/mnt/music-lib/,dst=/mnt/music-lib/ \
	--mount type=bind,src=$(pwd)/conf/settings.py,dst=/srv/redsym/REDsym/settings.py,readonly \
	redsym
```

This runs `python3 /srv/redsym/redsym.py update`, as seen on the last line of the Dockerfile.
