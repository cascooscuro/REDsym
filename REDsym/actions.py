#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 tw=79 et :
#

import os.path
import regex
from ftfy import fix_text
import REDsym.bigtable 
import REDsym.util
import REDsym.settings


rootdir_wcd = REDsym.settings.rootdir_wcd
rootdir_red = REDsym.settings.rootdir_red
redsym_dir = REDsym.settings.redsym_dir

def update_wm2():

    db = REDsym.bigtable.DBase()


    (new_dir_folders_only_music, deleted_dir_folders) = REDsym.bigtable.update_bigtable()

    print ("##### START symlinking #####")
    print ("There are: ", len(new_dir_folders_only_music),  " new folders to symlink\n" )
    print ("There are: ", len(deleted_dir_folders),  " symlinks to delete\n" )
    
    for deleted_dir_folder in deleted_dir_folders:
        
        if rootdir_wcd in deleted_dir_folder:
            symlink = db.get_symlink_WCD_from_dir(deleted_dir_folder)
            if symlink:
                db.delete_symlink_WCD(symlink)
                os.remove(symlink) 

        
        if rootdir_red in deleted_dir_folder:
            symlink = db.get_symlink_RED_from_dir(deleted_dir_folder)
            if symlink:
                db.delete_symlink_RED(symlink)
                os.remove(symlink) 


    for new_dir_folder in new_dir_folders_only_music:        
        if rootdir_wcd in new_dir_folder:
            
            audio_info_wm2 = db.get_meta_from_dir_WCD(new_dir_folder)
            (artist_name, album_name) = REDsym.util.audio_dir_filename_wcd_wm2(new_dir_folder)
            artist_name_valid = REDsym.util.filenamefy(artist_name)
            album_name_valid = REDsym.util.filenamefy(album_name)

            if not os.path.exists(redsym_dir+artist_name_valid ):
                os.makedirs(redsym_dir + artist_name_valid )

            
            new_album_path_folder = REDsym.util.get_music_dir (new_dir_folder)
            source = os.path.join(new_dir_folder, new_album_path_folder)
            target =os.path.join(redsym_dir , artist_name_valid , album_name_valid)
            
            print ("symink '%s' -> '%s" % (fix_text(source), target ))

            if os.path.exists(target):
                target = target + ' ID: ' +  str(audio_info_wm2['TorrentId'])
            
            try:
                os.symlink(source, target)
                db.insert_symlink_WCD(new_dir_folder, target)
            except FileExistsError:
                print ("symkink exists  '%s' -> '%s" % (fix_text(source), target ))


        if rootdir_red in new_dir_folder:
                        
            audio_info_wm2 = db.get_meta_from_dir_RED(new_dir_folder)
            (artist_name, album_name) = REDsym.util.audio_dir_filename_red_wm2(new_dir_folder)
            artist_name_valid = REDsym.util.filenamefy(artist_name)
            album_name_valid = REDsym.util.filenamefy(album_name)

            if not os.path.exists(redsym_dir+artist_name_valid ):
                os.makedirs(redsym_dir+ artist_name_valid )
            
            new_album_path_folder = REDsym.util.get_music_dir (new_dir_folder)
            source = os.path.join(new_dir_folder, new_album_path_folder)
            target =os.path.join(redsym_dir , artist_name_valid , album_name_valid)
            print ("symlink '%s' -> '%s" % (fix_text(source), target ))

            if os.path.exists(target):
                target = target + ' ID: ' +  str(audio_info_wm2['TorrentId'])
            try:
                os.symlink(source, target)
                db.insert_symlink_RED(new_dir_folder, target)
            except FileExistsError:
                print ("symkink exists  '%s' -> '%s" % (fix_text(source), target ))


