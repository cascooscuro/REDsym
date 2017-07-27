#!/usr/bin/python3
#coding: utf8

import os
import re
import ujson
from collections import defaultdict
from ftfy import fix_text
import MySQLdb
import REDsym.util
import REDsym.settings


rootdir_wcd = REDsym.settings.rootdir_wcd
rootdir_red = REDsym.settings.rootdir_red
redsym_dir = REDsym.settings.redsym_dir
DB_NAME = REDsym.settings.DB_NAME
DB_USER = REDsym.settings.DB_USER
DB_PASS = REDsym.settings.DB_PASS


# for future reference wcd vs red

release_type_table = {
			8 : 19,
			22 : 18,
			23 : 17
			}
release_type_word = {
			1 : "Album",
			3 : "Soundtrack",
			5 : "EP",
			6 : "Anthology",
			7 : "Compilation",
			8 : "DJ Mix",
			9 : "Single",
			11 : "Live Album",
			13 : "Remix",
			14 : "Bootleg",
			15 : "Interview",
			16 : "Mixtape",
			21 : "Unknown",
			22 : "Concert Recording",
			23 : "Demo"
			}

musicInfo_group_type_table = {
			1 : "artists",
			2 : "with",
			3 : "remixedBy",
			4 : "composers",
			5 : "conductor",
			6 : "dj",
			7 : "producer"
			}

torrent_table = {
			"id" : "TorrentId"
			}
group_table = {
			"id" : "TorrentGroupId"
			}

artist_table = {
			"id" : "ArtistId"
			}

def create_DB():

	
	TABLES_RED = {}
	
	TABLES_RED['Artists_RED'] = (
		"CREATE TABLE `Artists_RED` ("
		"  `ArtistId` int(11),"
		"  `name` varchar(2048),"
		"  `notificationsEnabled` TINYINT(1),"
		"  `image` varchar(2048),"
		"  `hasBookmarked` TINYINT(1),"
		"  `body` TEXT,"
		"  `vanityHouse` TINYINT(1),"
		"  `statistics` varchar(2048),"
		"  `Parsed` TINYINT(1) DEFAULT  '0',"
		"  PRIMARY KEY (`ArtistId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	TABLES_RED['AlbumsArtists_RED'] = (
		"CREATE TABLE `AlbumsArtists_RED` ("
		"  `ArtistId` int(11) NOT NULL,"
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  `musicInfo` varchar(191),"
		"  UNIQUE KEY `AlbumsArtists_TOTALindex_RED` (`ArtistId`, `TorrentGroupId`, `musicInfo`), KEY AlbumsArtists_indexGroupId_RED (`TorrentGroupId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	
	TABLES_RED['AlbumsTorrents_RED'] = (
		"CREATE TABLE `AlbumsTorrents_RED` ("
		"  `TorrentId` int(11) NOT NULL,"
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  `media` varchar(255),"
		"  `format` varchar(255),"
		"  `encoding` varchar(255),"
		"  `remasterYear` varchar(255),"
		"  `remastered` varchar(255),"
		"  `remasterTitle` varchar(255),"
		"  `remasterRecordLabel` varchar(255),"
		"  `scene` TINYINT(1),"
		"  `hasLog` TINYINT(1),"
		"  `hasCue` TINYINT(1),"
		"  `logScore` int(6),"
		"  `fileCount` int(6),"
		"  `freeTorrent`  TINYINT(1),"
		"  `size` bigint(12),"
		"  `time` varchar(255),"
		"  `hasFile` bigint(12),"
		"  `description` text,"
		"  `leechers` int(6),"
		"  `seeders` int(6),"
		"  `snatched` int(10),"
		"  `reported` TINYINT(1),"
		"  `infoHash` varchar(191),"
		"  `fileAlbumImage` varchar(255),"
		"  `pathAlbumImage` varchar(255),"
		"  `hasSnatched` TINYINT(1),"
		"  `hasUploaded` TINYINT(1),"
		"  `fileList`  mediumtext,"
		"  `filePath` varchar(255),"
		"  `dir` varchar(191),"
		"  `album_path` varchar(255),"
		"  `datafolder` varchar(255),"
		"  `userId` varchar(255),"
		"  `username` varchar(255),"
		"  `remasterCatalogueNumber` varchar(255),"
		"  PRIMARY KEY (`TorrentId`), UNIQUE KEY `AlbumsTorrents_index_RED` (`TorrentGroupId`, `TorrentId`), KEY AlbumsTorrents_hash_RED (`infoHash`), KEY AlbumsTorrents_hasSnatched_RED (`hasSnatched`), KEY AlbumsTorrents_dir_RED (`dir`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	
	TABLES_RED['AlbumsTorrents_RED_linked'] = (
		"CREATE TABLE `AlbumsTorrents_RED_linked` ("
		" `id` MEDIUMINT NOT NULL AUTO_INCREMENT,"
		"  `dir` varchar(512),"
		"  `symlink` varchar(512),"
		"  PRIMARY KEY (`id`)"
		") ENGINE=InnoDB CHARSET utf8mb4")

	
	TABLES_RED['Albums_RED'] = (
		"CREATE TABLE `Albums_RED` ("
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  `name` varchar(255),"
		"  `wikiBody` text,"
		"  `wikiImage` varchar(255),"
		"  `year` int(4),"
		"  `recordLabel` varchar(255),"
		"  `catalogueNumber` varchar(255),"
		"  `releaseType` tinyint(2),"
		"  `isBookmarked` tinyint(1),"
		"  `time` varchar(255),"
		"  `vanityHouse` tinyint(1),"
		"  `categoryId` tinyint(2),"
		"  `categoryName` varchar(255),"
		"  PRIMARY KEY (`TorrentGroupId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	TABLES_RED['AlbumsTags_RED'] = (
		"CREATE TABLE `AlbumsTags_RED` ("
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  `tags` varchar(191),"
		"  UNIQUE KEY `AlbumsTags_index_RED` (`TorrentGroupId`, `tags`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	TABLES_RED['Collages_RED'] = (
		"CREATE TABLE `Collages_RED` ("
		"  `CollageId` int(11) NOT NULL,"
		"  `CollageName` varchar(2048),"
		"  `CollageDescription` TEXT,"
		"  `CollageDeleted` TINYINT(1),"
		"  `CollageCategoryID` TINYINT(2),"
		"  `CollageCategoryName` varchar(2048),"        
		"  `CollageLocked` TINYINT(1),"
		"  `CollagehasBookmarked` TINYINT(1),"
		"  `CollagehasSubscriberCount` int(10),"
		"  `ParsedCollage` TINYINT(1) DEFAULT  '0',"
		"  PRIMARY KEY (`CollageId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")

	TABLES_RED['CollageAlbum_RED'] = (
		"CREATE TABLE `CollageAlbum_RED` ("
		"  `CollageId` int(11) NOT NULL,"
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  UNIQUE KEY `CollageAlbum_TOTALindex_RED` (`CollageId`, `TorrentGroupId`), KEY Collage_TorrentGroupId_RED (`TorrentGroupId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	




	TABLES_WCD = {}
	
	TABLES_WCD['Artists_WCD'] = (
		"CREATE TABLE `Artists_WCD` ("
		"  `ArtistId` int(11),"
		"  `name` varchar(2048),"
		"  `notificationsEnabled` TINYINT(1),"
		"  `image` varchar(2048),"
		"  `hasBookmarked` TINYINT(1),"
		"  `body` TEXT,"
		"  `vanityHouse` TINYINT(1),"
		"  `statistics` varchar(2048),"
		"  `Parsed` TINYINT(1) DEFAULT  '0',"
		"  PRIMARY KEY (`ArtistId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	TABLES_WCD['AlbumsArtists_WCD'] = (
		"CREATE TABLE `AlbumsArtists_WCD` ("
		"  `ArtistId` int(11) NOT NULL,"
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  `musicInfo` varchar(191),"
		"  UNIQUE KEY `AlbumsArtists_TOTALindex_WCD` (`ArtistId`, `TorrentGroupId`, `musicInfo`), KEY AlbumsArtists_indexGroupId_WCD (`TorrentGroupId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	
	TABLES_WCD['AlbumsTorrents_WCD'] = (
		"CREATE TABLE `AlbumsTorrents_WCD` ("
		"  `TorrentId` int(11) NOT NULL,"
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  `media` varchar(255),"
		"  `format` varchar(255),"
		"  `encoding` varchar(255),"
		"  `remasterYear` varchar(255),"
		"  `remastered` varchar(255),"
		"  `remasterTitle` varchar(255),"
		"  `remasterRecordLabel` varchar(255),"
		"  `scene` TINYINT(1),"
		"  `hasLog` TINYINT(1),"
		"  `hasCue` TINYINT(1),"
		"  `logScore` int(6),"
		"  `fileCount` int(6),"
		"  `freeTorrent`  TINYINT(1),"
		"  `size` bigint(12),"
		"  `time` varchar(255),"
		"  `hasFile` bigint(12),"
		"  `description` text,"
		"  `leechers` int(6),"
		"  `seeders` int(6),"
		"  `snatched` int(10),"
		"  `reported` TINYINT(1),"
		"  `infoHash` varchar(191),"
		"  `fileAlbumImage` varchar(255),"
		"  `pathAlbumImage` varchar(255),"
		"  `hasSnatched` TINYINT(1),"
		"  `hasUploaded` TINYINT(1),"
		"  `fileList`  mediumtext,"
		"  `filePath` varchar(255),"
		"  `dir` varchar(191),"
		"  `album_path` varchar(255),"
		"  `datafolder` varchar(255),"
		"  `userId` varchar(255),"
		"  `username` varchar(255),"
		"  `remasterCatalogueNumber` varchar(255),"
		"  PRIMARY KEY (`TorrentId`), UNIQUE KEY `AlbumsTorrents_index_WCD` (`TorrentGroupId`, `TorrentId`), KEY AlbumsTorrents_hash_WCD (`infoHash`), KEY AlbumsTorrents_hasSnatched_WCD (`hasSnatched`), KEY AlbumsTorrents_dir_WCD (`dir`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	
	TABLES_WCD['AlbumsTorrents_WCD_linked'] = (
		"CREATE TABLE `AlbumsTorrents_WCD_linked` ("
		" `id` MEDIUMINT NOT NULL AUTO_INCREMENT,"
		"  `dir` varchar(512),"
		"  `symlink` varchar(512),"
		"  PRIMARY KEY (`id`)"
		") ENGINE=InnoDB CHARSET utf8mb4")

	TABLES_WCD['Albums_WCD'] = (
		"CREATE TABLE `Albums_WCD` ("
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  `name` varchar(255),"
		"  `wikiBody` text,"
		"  `wikiImage` varchar(255),"
		"  `year` int(4),"
		"  `recordLabel` varchar(255),"
		"  `catalogueNumber` varchar(255),"
		"  `releaseType` tinyint(2),"
		"  `isBookmarked` tinyint(1),"
		"  `time` varchar(255),"
		"  `vanityHouse` tinyint(1),"
		"  `categoryId` tinyint(2),"
		"  `categoryName` varchar(255),"
		"  PRIMARY KEY (`TorrentGroupId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	TABLES_WCD['AlbumsTags_WCD'] = (
		"CREATE TABLE `AlbumsTags_WCD` ("
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  `tags` varchar(191),"
		"  UNIQUE KEY `AlbumsTags_index_WCD` (`TorrentGroupId`, `tags`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
	TABLES_WCD['Collages_WCD'] = (
		"CREATE TABLE `Collages_WCD` ("
		"  `CollageId` int(11) NOT NULL,"
		"  `CollageName` varchar(2048),"
		"  `CollageDescription` TEXT,"
		"  `CollageDeleted` TINYINT(1),"
		"  `CollageCategoryID` TINYINT(2),"
		"  `CollageCategoryName` varchar(2048),"        
		"  `CollageLocked` TINYINT(1),"
		"  `CollagehasBookmarked` TINYINT(1),"
		"  `CollagehasSubscriberCount` int(10),"
		"  `ParsedCollage` TINYINT(1) DEFAULT  '0',"
		"  PRIMARY KEY (`CollageId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")

	TABLES_WCD['CollageAlbum_WCD'] = (
		"CREATE TABLE `CollageAlbum_WCD` ("
		"  `CollageId` int(11) NOT NULL,"
		"  `TorrentGroupId` int(11) NOT NULL,"
		"  UNIQUE KEY `CollageAlbum_TOTALindex_WCD` (`CollageId`, `TorrentGroupId`), KEY Collage_TorrentGroupId_WCD (`TorrentGroupId`)"
		") ENGINE=InnoDB CHARSET utf8mb4")
	
   
	indexdb = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, host='127.0.0.1', db=DB_NAME, charset='utf8mb4', use_unicode=True)
	indexdbc = indexdb.cursor()
	indexdbc.execute("""set session transaction isolation level READ COMMITTED""")

	list_of_tables = [TABLES_WCD, TABLES_RED ]
	
	try:
		indexdb.database = DB_NAME    
	except MySQLdb.Error as e:
		try:
			print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
		except IndexError:
			print ("MySQL Error: %s" % str(e))
		
	for TABLES 	in list_of_tables:
		for name, ddl in TABLES.items():
			
			try:
				#print("Creating table {}: " + (str(create_DB)))
				indexdbc.execute(ddl)
			except MySQLdb.Error as  e:
				if e.args[0]!= 1050:
					print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))


	indexdb.commit()
	indexdbc.close()
	indexdb.close()

class DBase:

	dsn = ("127.0.0.1",DB_USER,DB_PASS,DB_NAME)

	def __init__(self):
		self.conn = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, host='127.0.0.1', db=DB_NAME, charset='utf8mb4', use_unicode=True)
		self.cur = self.conn.cursor()

	def __enter__(self):
		return DBase()

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.conn:
			self.conn.close()



	def get_wm2_dir_RED(self):

		sql = 'SELECT dir FROM AlbumsTorrents_RED WHERE 1'
		self.cur.execute(sql)
		groupid_select_RED=[r[0] for r in self.cur.fetchall()]

		return  groupid_select_RED

	def get_wm2_dir_WCD(self):
		sql = 'SELECT dir FROM AlbumsTorrents_WCD WHERE 1'
		self.cur.execute(sql)
		groupid_select_WCD=[r[0] for r in self.cur.fetchall()]


		return groupid_select_WCD



	def get_meta_from_dir_WCD(self, dir ):
		sql ="SELECT at.format, at.remasterYear, at.remastered, at.remasterTitle, at.dir, at.filePath, at.remasterCatalogueNumber, at.fileList, a.name, a.year, at.TorrentGroupId, at.TorrentId FROM AlbumsTorrents_WCD AS at JOIN Albums_WCD AS a ON at.TorrentGroupId=a.TorrentGroupId WHERE dir = %s"

		self.cur.execute(sql, (dir,))

		row = self.cur.fetchall()

		filelist = re.split(r'\{\{\{[0-9]+\}\}\}\|+|\{\{\{[0-9]+\}\}\}+', row[0][7] )
		filelist_no_empty_items = list(filter(None, filelist))

		groupid_select_meta_album={'format': row[0][0], 'remasterYear': row[0][1], 'remastered': row[0][1], 'remasterTitle': row[0][3], 'dir': row[0][4], 'filePath': row[0][5], 'remasterCatalogueNumber': row[0][6], 'fileList': filelist_no_empty_items, 'name': row[0][8], 'year': row[0][9], 'TorrentGroupId': row[0][10], 'TorrentId': row[0][11]}

		sql ="SELECT  aa.musicInfo, ar.name FROM AlbumsArtists_WCD AS aa JOIN  Artists_WCD AS ar ON aa.ArtistId=ar.ArtistId WHERE aa.TorrentGroupId = %s"
		groupid = groupid_select_meta_album.get('TorrentGroupId')
		self.cur.execute(sql, (groupid,) )
		groupid_select_meta_artist=[r for r in self.cur.fetchall()]

		#from list of tuples to dict

		artistname_by_musicinfo = defaultdict(list)
		for  musicinfo, name in groupid_select_meta_artist:
			artistname_by_musicinfo[musicinfo].append(name)
		
		groupid_select_meta_album['musicInfo'] = dict(artistname_by_musicinfo)


		sql ="SELECT  tags FROM AlbumsTags_WCD  WHERE TorrentGroupId = %s"
		self.cur.execute(sql, (groupid,) )
		groupid_select_meta_tags=[r[0] for r in self.cur.fetchall()]

		groupid_select_meta_album['tags'] =  groupid_select_meta_tags                     
		
		return (groupid_select_meta_album )


	


	def get_meta_from_dir_RED(self, dir ):
		sql ="SELECT at.format, at.remasterYear, at.remastered, at.remasterTitle, at.dir, at.filePath, at.remasterCatalogueNumber, at.fileList, a.name, a.year, at.TorrentGroupId, at.TorrentId FROM AlbumsTorrents_RED AS at JOIN Albums_RED AS a ON at.TorrentGroupId=a.TorrentGroupId WHERE dir = %s"

		self.cur.execute(sql, (dir,))

		row = self.cur.fetchall() 
		filelist = re.split(r'\{\{\{[0-9]+\}\}\}\|+|\{\{\{[0-9]+\}\}\}+', row[0][7] )
		filelist_no_empty_items = list(filter(None, filelist))

		groupid_select_meta_album={'format': row[0][0], 'remasterYear': row[0][1], 'remastered': row[0][1], 'remasterTitle': row[0][3], 'dir': row[0][4], 'filePath': row[0][5], 'remasterCatalogueNumber': row[0][6], 'fileList': filelist_no_empty_items, 'name': row[0][8], 'year': row[0][9], 'TorrentGroupId': row[0][10], 'TorrentId': row[0][11]}

		sql ="SELECT  aa.musicInfo, ar.name FROM AlbumsArtists_RED AS aa JOIN  Artists_RED AS ar ON aa.ArtistId=ar.ArtistId WHERE aa.TorrentGroupId = %s"
		groupid = groupid_select_meta_album.get('TorrentGroupId')
		self.cur.execute(sql, (groupid,) )
		groupid_select_meta_artist=[r for r in self.cur.fetchall()]

		#from list of tuples to dict


		artistname_by_musicinfo = defaultdict(list)
		for  musicinfo, name in groupid_select_meta_artist:
			artistname_by_musicinfo[musicinfo].append(name)
		
		groupid_select_meta_album['musicInfo'] = dict(artistname_by_musicinfo)


		sql ="SELECT  tags FROM AlbumsTags_RED  WHERE TorrentGroupId = %s"
		self.cur.execute(sql, (groupid,) )
		groupid_select_meta_tags=[r[0] for r in self.cur.fetchall()]

		groupid_select_meta_album['tags'] =  groupid_select_meta_tags                     
		
		return (groupid_select_meta_album )




	def delete_torrent_WCD(self, torrentid, dir, album_path):
		#search for group id, dir folder or album_path

		if torrentid:

			sql = "SELECT TorrentGroupId FROM AlbumsTorrents_WCD WHERE TorrentId=%s"
			self.cur.execute(sql, (torrentid,))
			groupid_select=[r[0] for r in self.cur.fetchall()]
			if groupid_select != []:
				groupid = groupid_select[0]
			else:
				print ("orphaned torrentid=", torrentid,  "no group id associated")


			sql = "DELETE FROM AlbumsTorrents_WCD WHERE TorrentId=%s" 
			self.cur.execute(sql, (torrentid,))
			self.conn.commit()

			if groupid:
				sql = "SELECT TorrentId FROM AlbumsTorrents_WCD WHERE TorrentGroupId=%s"
				self.cur.execute(sql, (groupid,))
				torrentid_select=[r[0] for r in self.cur.fetchall()]
				if torrentid_select == []:
					sql1 = "DELETE FROM AlbumsArtists_WCD WHERE TorrentGroupId=%s" 
					sql2 = "DELETE FROM AlbumsTags_WCD WHERE TorrentGroupId=%s" 
					sql3 = "DELETE FROM Albums_WCD WHERE TorrentGroupId=%s" 
					self.cur.execute(sql1, (groupid,))
					self.cur.execute(sql2, (groupid,))
					self.cur.execute(sql3, (groupid,))
					self.conn.commit()


		if dir:
			sql = "SELECT TorrentGroupId FROM AlbumsTorrents_WCD WHERE dir=%s"
			self.cur.execute(sql, (dir,))
			groupid_select=[r[0] for r in self.cur.fetchall()]
			if groupid_select != []:
				groupid = groupid_select[0]
			else:
				print ("orphaned torrent=", dir,  "no group id associated")


			sql = "DELETE FROM AlbumsTorrents_WCD WHERE dir=%s" 
			self.cur.execute(sql, (dir,))
			self.conn.commit()
			if groupid:
				sql = "SELECT TorrentId FROM AlbumsTorrents_WCD WHERE TorrentGroupId=%s" 
				self.cur.execute(sql, (groupid,))
				torrentid_select=[r[0] for r in self.cur.fetchall()]
				if torrentid_select == []:
					sql1 = "DELETE FROM AlbumsArtists_WCD WHERE TorrentGroupId=%s" 
					sql2 = "DELETE FROM AlbumsTags_WCD WHERE TorrentGroupId=%s" 
					sql3 = "DELETE FROM Albums_WCD WHERE TorrentGroupId=%s" 
					self.cur.execute(sql1, (groupid,))
					self.cur.execute(sql2, (groupid,))
					self.cur.execute(sql3, (groupid,))
					self.conn.commit()


		if album_path:
			sql = "SELECT TorrentGroupId FROM AlbumsTorrents_WCD WHERE album_path=%s"
			self.cur.execute(sql, (album_path,))
			groupid_select=[r[0] for r in self.cur.fetchall()]
			if groupid_select != []:
				groupid = groupid_select[0]
			else:
				print ("orphaned torrent=", album_path,  "no group id associated")


			sql = "DELETE FROM AlbumsTorrents_WCD WHERE album_path=%s" 
			self.cur.execute(sql, (album_path,))
			self.conn.commit()

			if groupid:
				sql = "SELECT TorrentId FROM AlbumsTorrents_WCD WHERE TorrentGroupId=%s" 
				self.cur.execute(sql, (groupid,))
				torrentid_select=[r[0] for r in self.cur.fetchall()]
				if torrentid_select == []:
					sql1 = "DELETE FROM AlbumsArtists_WCD WHERE TorrentGroupId=%s" 
					sql2 = "DELETE FROM AlbumsTags_WCD WHERE TorrentGroupId=%s" 
					sql3 = "DELETE FROM Albums_WCD WHERE TorrentGroupId=%s" 
					self.cur.execute(sql1, (groupid,))
					self.cur.execute(sql2, (groupid,))
					self.cur.execute(sql3, (groupid,))
					self.conn.commit()


		return self.cur.lastrowid


	def delete_torrent_RED(self, torrentid, dir, album_path):

		if torrentid:

			sql = "SELECT TorrentGroupId FROM AlbumsTorrents_RED WHERE TorrentId=%s"
			self.cur.execute(sql, (torrentid,))
			groupid_select=[r[0] for r in self.cur.fetchall()]
			if groupid_select != []:
				groupid = groupid_select[0]
			else:
				print ("orphaned torrent=", torrentid,  "no group id associated")


			sql = "DELETE FROM AlbumsTorrents_RED WHERE TorrentId=%s" 
			self.cur.execute(sql, (torrentid,))
			self.conn.commit()

			if groupid:
				sql = "SELECT TorrentId FROM AlbumsTorrents_RED WHERE TorrentGroupId=%s"
				self.cur.execute(sql, (groupid,))
				torrentid_select=[r[0] for r in self.cur.fetchall()]
				if torrentid_select == []:
					sql1 = "DELETE FROM AlbumsArtists_RED WHERE TorrentGroupId=%s" 
					sql2 = "DELETE FROM AlbumsTags_RED WHERE TorrentGroupId=%s" 
					sql3 = "DELETE FROM Albums_RED WHERE TorrentGroupId=%s" 
					self.cur.execute(sql1, (groupid,))
					self.cur.execute(sql2, (groupid,))
					self.cur.execute(sql3, (groupid,))
					self.conn.commit()

		if dir:
			sql = "SELECT TorrentGroupId FROM AlbumsTorrents_RED WHERE dir=%s"
			self.cur.execute(sql, (dir,))
			groupid_select=[r[0] for r in self.cur.fetchall()]
			if groupid_select != []:
				groupid = groupid_select[0]
			else:
				print ("orphaned torrent=", dir,  "no group id associated")


			sql = "DELETE FROM AlbumsTorrents_RED WHERE dir=%s"
			self.cur.execute(sql, (dir,))
			self.conn.commit()
			if groupid:
				sql = "SELECT TorrentId FROM AlbumsTorrents_RED WHERE TorrentGroupId=%s" 
				self.cur.execute(sql, (groupid,))
				torrentid_select=[r[0] for r in self.cur.fetchall()]
				if torrentid_select == []:
					sql1 = "DELETE FROM AlbumsArtists_RED WHERE TorrentGroupId=%s" 
					sql2 = "DELETE FROM AlbumsTags_RED WHERE TorrentGroupId=%s" 
					sql3 = "DELETE FROM Albums_RED WHERE TorrentGroupId=%s" 
					self.cur.execute(sql1, (groupid,))
					self.cur.execute(sql2, (groupid,))
					self.cur.execute(sql3, (groupid,))
					self.conn.commit()


		if album_path:
			sql = "SELECT TorrentGroupId FROM AlbumsTorrents_RED WHERE album_path=%s"
			self.cur.execute(sql, (album_path,))
			groupid_select=[r[0] for r in self.cur.fetchall()]
			if groupid_select != []:
				groupid = groupid_select[0]
			else:
				print ("orphaned torrent=", album_path,  "no group id associated")


			sql = "DELETE FROM AlbumsTorrents_RED WHERE album_path=%s"
			self.cur.execute(sql, (album_path,))
			self.conn.commit()
			if groupid:
				sql = "SELECT TorrentId FROM AlbumsTorrents_RED WHERE TorrentGroupId=%s" 
				self.cur.execute(sql, (groupid,))
				torrentid_select=[r[0] for r in self.cur.fetchall()]
				if torrentid_select == []:
					sql1 = "DELETE FROM AlbumsArtists_RED WHERE TorrentGroupId=%s" 
					sql2 = "DELETE FROM AlbumsTags_RED WHERE TorrentGroupId=%s" 
					sql3 = "DELETE FROM Albums_RED WHERE TorrentGroupId=%s" 
					self.cur.execute(sql1, (groupid,))
					self.cur.execute(sql2, (groupid,))
					self.cur.execute(sql3, (groupid,))
					self.conn.commit()

		return self.cur.lastrowid


	def insert_album_WCD(self, info_dict):
		

		#fix id for TorrentId and groupId
		info_dict['torrent']['TorrentId'] = info_dict['torrent'].pop('id')
		info_dict['group']['TorrentGroupId'] = info_dict['group'].pop('id')

		placeholders_torrent = ', '.join(['%s'] * (len(info_dict['torrent']) +1))
		columns_torrent  = ', '.join(list(info_dict['torrent'].keys()) + ['TorrentGroupId'])
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ('AlbumsTorrents_WCD', columns_torrent, placeholders_torrent)
		self.cur.execute(sql, list(info_dict['torrent'].values()) + [info_dict['group']['TorrentGroupId']])

		
		#then with group tags
		values_group_tags = [ (info_dict['group']['TorrentGroupId'], x) for x in info_dict['group']['tags'] ]
		placeholders_group_tags = '%s, %s'
		columns_group_tags = 'TorrentGroupId, tags'
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ("AlbumsTags_WCD", columns_group_tags, placeholders_group_tags)
		self.cur.executemany(sql, values_group_tags )


		values_group_tags = [ (tuple_list[0], dict['id'], info_dict['group']['TorrentGroupId'])  for tuple_list in info_dict['group']['musicInfo'].items() for dict in tuple_list[1]  ]
		placeholders_group_tags = '%s, %s , %s'
		columns_group_tags = 'musicInfo, ArtistId, TorrentGroupId'
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ("AlbumsArtists_WCD", columns_group_tags, placeholders_group_tags)
		self.cur.executemany(sql, values_group_tags )


		#then with artists
		values_artists = [ (dict['id'], dict['name'])  for tuple_list in info_dict['group']['musicInfo'].items() for dict in tuple_list[1]  ]
		placeholders_artists = '%s, %s'
		columns_artists = 'ArtistId, name'
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ("Artists_WCD", columns_artists, placeholders_artists)
		self.cur.executemany(sql, values_artists )

		#then with group
		del info_dict['group']['tags']
		del info_dict['group']['musicInfo']
		placeholders_group = ', '.join(['%s'] * (len(info_dict['group']) ))
		columns_group  = ', '.join(info_dict['group'].keys())
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ('Albums_WCD', columns_group, placeholders_group)
		self.cur.execute(sql, list(info_dict['group'].values() ))
		self.conn.commit()
		return self.cur.lastrowid

	def insert_album_RED(self, info_dict):
		

		#fix id for TorrentId and groupId
		info_dict['torrent']['TorrentId'] = info_dict['torrent'].pop('id')
		info_dict['group']['TorrentGroupId'] = info_dict['group'].pop('id')

		placeholders_torrent = ', '.join(['%s'] * (len(info_dict['torrent']) +1))
		columns_torrent  = ', '.join(list(info_dict['torrent'].keys()) + ['TorrentGroupId'])
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ('AlbumsTorrents_RED', columns_torrent, placeholders_torrent)
		self.cur.execute(sql, list(info_dict['torrent'].values()) + [info_dict['group']['TorrentGroupId']])
		
		#then with group tags
		values_group_tags = [ (info_dict['group']['TorrentGroupId'], x) for x in info_dict['group']['tags'] ]
		placeholders_group_tags = '%s, %s'
		columns_group_tags = 'TorrentGroupId, tags'
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ("AlbumsTags_RED", columns_group_tags, placeholders_group_tags)
		self.cur.executemany(sql, values_group_tags )


		values_group_tags = [ (tuple_list[0], dict['id'], info_dict['group']['TorrentGroupId'])  for tuple_list in info_dict['group']['musicInfo'].items() for dict in tuple_list[1]  ]
		placeholders_group_tags = '%s, %s , %s'
		columns_group_tags = 'musicInfo, ArtistId, TorrentGroupId'
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ("AlbumsArtists_RED", columns_group_tags, placeholders_group_tags)
		self.cur.executemany(sql, values_group_tags )


		#then with artists
		values_artists = [ (dict['id'], dict['name'])  for tuple_list in info_dict['group']['musicInfo'].items() for dict in tuple_list[1]  ]
		placeholders_artists = '%s, %s'
		columns_artists = 'ArtistId, name'
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ("Artists_RED", columns_artists, placeholders_artists)
		self.cur.executemany(sql, values_artists )

		#then with group
		del info_dict['group']['tags']
		del info_dict['group']['musicInfo']
		placeholders_group = ', '.join(['%s'] * (len(info_dict['group']) ))
		columns_group  = ', '.join(info_dict['group'].keys())
		sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s )" % ('Albums_RED', columns_group, placeholders_group)
		self.cur.execute(sql, list(info_dict['group'].values()) )
		self.conn.commit()
		return self.cur.lastrowid


	def insert_symlink_WCD(self, dir, symlink):


		sql = "INSERT IGNORE INTO AlbumsTorrents_WCD_linked (dir, symlink)  VALUES ( %s, %s )"
		self.cur.execute(sql, (dir, symlink))
		self.conn.commit()
		return self.cur.lastrowid
	
	def insert_symlink_RED(self, dir, symlink):


		sql = "INSERT IGNORE INTO AlbumsTorrents_RED_linked (dir, symlink)  VALUES ( %s, %s )"
		self.cur.execute(sql,(dir, symlink))
		self.conn.commit()
		return self.cur.lastrowid

		

	def delete_symlink_WCD(self, symlink):
		sql = "DELETE FROM AlbumsTorrents_WCD_linked WHERE symlink=%s" 
		self.cur.execute(sql, (symlink,))
		self.conn.commit()
		return self.cur.lastrowid

	def delete_symlink_RED(self, symlink):
		sql = "DELETE FROM AlbumsTorrents_RED_linked WHERE symlink=%s" 
		self.cur.execute(sql, (symlink,))
		self.conn.commit()
		return self.cur.lastrowid




	def get_symlink_WCD_from_dir(self, dir):

		sql = "SELECT symlink FROM AlbumsTorrents_WCD_linked WHERE dir=%s"
		self.cur.execute(sql, (dir,))
		groupid_select=[r[0] for r in self.cur.fetchall()]
		if groupid_select != []:	
			groupid = groupid_select[0]
			return groupid
		else:
			print ("can't find simlink in DB for:",dir, "can't delete it")
			return False

	def get_symlink_RED_from_dir(self, dir):

		sql = "SELECT symlink FROM AlbumsTorrents_RED_linked WHERE dir=%s"
		self.cur.execute(sql, (dir,))
		groupid_select=[r[0] for r in self.cur.fetchall()]
		if groupid_select != []:

			groupid = groupid_select[0]
			return groupid
		else:
			print ("can't find simlink in DB for:",dir, "can't delete it")
			return False


def get_size(start_path):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	return total_size


def get_new_dir_folders_wcd():
	count = 0
	current_album_path_list = []
	db = DBase()
	print ("Getting new folders from WCD path")
	database_dir_list = db.get_wm2_dir_WCD()

	for rootdir in [ rootdir_wcd]:
		for subdir, dirs, files in os.walk(rootdir):

			for file in files:
				size_folder = get_size(subdir)
				if file == 'ReleaseInfo2.txt' and size_folder > 10000000 and REDsym.util.get_music_dir (subdir):
					count += 1
					current_album_path_list.append( subdir)


	new_dir_folders = list(set(current_album_path_list).difference(database_dir_list))

	return new_dir_folders

def get_deleted_dir_folders_wcd():
	count = 0
	current_album_path_list = []
	db = DBase()
	print ("Getting deleted folders from WCD path")
	database_dir_list = db.get_wm2_dir_WCD()

	for rootdir in [ rootdir_wcd]:
		for subdir, dirs, files in os.walk(rootdir):

			for file in files:
				size_folder = get_size(subdir)
				if file == 'ReleaseInfo2.txt' and size_folder > 10000000:
					count += 1
					current_album_path_list.append( subdir)


	deleted_dir_folders = list(set(database_dir_list).difference(current_album_path_list))

	return deleted_dir_folders



def get_new_dir_folders_red():
	count = 0
	current_album_path_list = []
	db = DBase()
	print ("Getting new folders from RED path")
	database_dir_list = db.get_wm2_dir_RED()

	for rootdir in [ rootdir_red]:
		for subdir, dirs, files in os.walk(rootdir):

			for file in files:
				size_folder = get_size(subdir)
				if file == 'ReleaseInfo2.txt' and size_folder > 10000000 and REDsym.util.get_music_dir (subdir) :
					count += 1
					current_album_path_list.append( subdir)


	new_dir_folders = list(set(current_album_path_list).difference(database_dir_list))

	return new_dir_folders

def get_deleted_dir_folders_red():
	count = 0
	current_album_path_list = []
	db = DBase()
	print ("Getting deleted folders from RED path")
	database_dir_list = db.get_wm2_dir_RED()

	for rootdir in [ rootdir_red]:
		for subdir, dirs, files in os.walk(rootdir):

			for file in files:
				size_folder = get_size(subdir)
				if file == 'ReleaseInfo2.txt' and size_folder > 10000000:
					count += 1
					current_album_path_list.append( subdir)


	deleted_dir_folders = list(set(database_dir_list).difference(current_album_path_list))

	return deleted_dir_folders



def update_bigtable():

	create_DB()
	db = DBase()



	new_dir_folders_wcd = get_new_dir_folders_wcd()
	deleted_dir_folders_wcd = get_deleted_dir_folders_wcd()
	new_dir_folders_red = get_new_dir_folders_red()
	deleted_dir_folders_red = get_deleted_dir_folders_red()

	
	new_dir_folders = new_dir_folders_wcd + new_dir_folders_red
	deleted_dir_folders = deleted_dir_folders_wcd + deleted_dir_folders_red


	new_dir_folders_only_music =[]
	print ("##### START Database update #####")
	print ("There are: ", len(new_dir_folders),  " new folders to update in DB\n" )
	print ("There are: ", len(deleted_dir_folders),  " folders to delete in DB\n" )
	

	for rootdir in new_dir_folders:
		for subdir, dirs, files in os.walk(rootdir):

			for file in files:


				size_folder = get_size(subdir)
				if file == 'ReleaseInfo2.txt' and size_folder > 10000000:

					with open(os.path.join(subdir,file), 'r') as ReleaseInfo:
						info_dict = ujson.loads(ReleaseInfo.read())
					info_dict['torrent']['dir'] = subdir
					#subdir is /media/silvhd/pth/wm2/2222/ 



					if  not info_dict['torrent']['filePath']:
						datapath = subdir
						datafolder = subdir
					else:

						datafolder = [name for name in os.listdir(info_dict['torrent']['dir']) if os.path.isdir(os.path.join(info_dict['torrent']['dir'], name))][0]
						datapath =  os.path.join(info_dict['torrent']['dir'], datafolder)
						#datapath is /media/silvhd/pth/wm2/2222/artist-album/
						#datafolder is artist-album 

					if REDsym.util.is_surrogate_escaped(datapath): 
						datapath_fix = REDsym.util.remove_surrogate_escaping(datapath)
						datafolder_fix = REDsym.util.remove_surrogate_escaping(datafolder)
					else:
						datapath_fix = datapath
						datafolder_fix = datafolder
					
					info_dict['torrent']['album_path'] = datapath_fix
					info_dict['torrent']['datafolder'] = datafolder_fix
					
					info_dict['group']['name'] = fix_text(info_dict['group']['name'])
					info_dict['group']['wikiBody'] = fix_text(info_dict['group']['wikiBody'])
					info_dict['torrent']['description'] = fix_text(info_dict['torrent']['description'])

					
					if not info_dict['group']['categoryName'] == 'Music':
						#print ("Handling album '%s'" % (fix_text(datapath)))
						#print ("Not a 'Music' release, skipping.")
						break
					if not REDsym.util.get_music_dir (subdir):
						#print ("Handling album '%s'" % (fix_text(datapath)))
						#print ("no media files, skipping")
						break
					
					if rootdir_wcd in rootdir:
						db.insert_album_WCD(info_dict)
						new_dir_folders_only_music.append (subdir)
						#print ("Handling  WCD album '%s'" % (datapath_fix))

					if rootdir_red in rootdir:
						db.insert_album_RED(info_dict)
						new_dir_folders_only_music.append (subdir)
						#print ("Handling  RED album '%s'" % (datapath_fix))
	
	for dir in deleted_dir_folders:
		if rootdir_wcd in dir:
			db.delete_torrent_WCD(False, dir, False)
		if rootdir_red in dir:
			db.delete_torrent_RED(False, dir, False)
	return (new_dir_folders_only_music, deleted_dir_folders)


		

