# REDsym

REDsym uses existing metadata saved by Whatmanager2 (https://github.com/karamanolev/WhatManager2) to create a symlinked mirror directory.

It uses the ReleaseInfo2.txt files to extract: artists names, album name, year, codec, Catalogue number... and create the mirrored structure.

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

##Running the script

	$python3 redsym.py update

