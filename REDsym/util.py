#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 tw=79 et :

import sys
import os
import os.path
import REDsym.bigtable 


def filenamefy(value):
    value_fix_char = value.replace('/', '-')
    value_fix_dot = value_fix_char.lstrip('.')
    value_valid = value_fix_dot[0:254]
    return value_valid


def audio_dir_filename_wcd_wm2(dir):
    db = REDsym.bigtable.DBase()


    audio_info_wm2 = db.get_meta_from_dir_WCD(dir)


    if audio_info_wm2['year'] !='':
        album_name = '(' +  str(audio_info_wm2['year']) + ') '  + audio_info_wm2['name']
    else:
        album_name = audio_info_wm2['name']
    
    if audio_info_wm2['remasterTitle'] !='':
        album_name = album_name + ' (' +  audio_info_wm2['remasterTitle'] + ') '
   
    if audio_info_wm2['remasterCatalogueNumber'] !='':
        album_name = album_name + ' (' +  audio_info_wm2['remasterCatalogueNumber'] + ') '

    album_name = album_name + ' [' + audio_info_wm2['format'] + ']'

    
    #detect classical or jazz
    if any("classical" in s for s in audio_info_wm2['tags']):
        classical = 1
    else:
        classical = 0

    if any("jazz" in s for s in audio_info_wm2['tags']):
        jazz = 1
    else:
        jazz = 0


    if len(audio_info_wm2['musicInfo'].values()) == 1:
        for key, value in audio_info_wm2['musicInfo'].items():
                if len(value)==1:
                    artist_name = ','.join(value)
                elif len(value)==2:
                    artist_name = ', '.join(value)
                elif len(value)==3:
                    artist_name = ', '.join(value)
                elif classical ==1 :
                    artist_name = 'Various Classical Artists'
                elif jazz ==1 :
                    artist_name = 'Various Jazz Artists'
                else:
                    artist_name = 'Various Artists'
    elif classical:
        if 'composers' in audio_info_wm2['musicInfo']:
                if len(audio_info_wm2['musicInfo']['composers'])==1:
                    artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
                elif len(audio_info_wm2['musicInfo']['composers'])==2:
                    artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
                elif len(audio_info_wm2['musicInfo']['composers'])==3:
                    artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
                else:
                    artist_name = 'Various Classical Artists'
        elif 'artists' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['artists'])==1:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            elif len(audio_info_wm2['musicInfo']['artists'])==2:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            elif len(audio_info_wm2['musicInfo']['artists'])==3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            else:
                artist_name = 'Various Classical Artists'

        elif 'conductor' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['conductor'])==1:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['conductor'])
            elif len(audio_info_wm2['musicInfo']['conductor'])==2:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['conductor'])
            elif len(audio_info_wm2['musicInfo']['conductor'])==3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['conductor'])
            else:
                artist_name = 'Various Classical Artists'



    elif 'artists' not in audio_info_wm2['musicInfo']:
        for key, value in audio_info_wm2['musicInfo'].items():
            if value:
                artist_name = ', '.join(value)
    
    elif jazz:
        if 'artists' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['artists'])==1:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            elif len(audio_info_wm2['musicInfo']['artists'])==2:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            elif len(audio_info_wm2['musicInfo']['artists'])==3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            else:
                artist_name = 'Various Jazz Artists'
        elif 'with' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['with'])==1:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['with'])
            elif len(audio_info_wm2['musicInfo']['with'])==2:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['with'])
            elif len(audio_info_wm2['musicInfo']['with'])==3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['with'])
            else:
                artist_name = 'Various Jazz Artists'

    elif 'artists' in audio_info_wm2['musicInfo']:
        if len(audio_info_wm2['musicInfo']['artists'])==1:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
        elif len(audio_info_wm2['musicInfo']['artists'])==2:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
        elif len(audio_info_wm2['musicInfo']['artists'])==3:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
        else:
            artist_name = 'Various Artists'
    elif 'composers' in audio_info_wm2['musicInfo']:
        if len(audio_info_wm2['musicInfo']['composers'])==1:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
        elif len(audio_info_wm2['musicInfo']['composers'])==2:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
        elif len(audio_info_wm2['musicInfo']['composers'])==3:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
        else:
            artist_name = 'Various Artists'

    return (artist_name, album_name)


def audio_dir_filename_red_wm2(dir):
    db = REDsym.bigtable.DBase()

    audio_info_wm2 = db.get_meta_from_dir_RED(dir)


    if audio_info_wm2['year'] !='':
        album_name = '(' +  str(audio_info_wm2['year']) + ') '  + audio_info_wm2['name']
    else:
        album_name = audio_info_wm2['name']
    
    if audio_info_wm2['remasterTitle'] !='':
        album_name = album_name + ' (' +  audio_info_wm2['remasterTitle'] + ') '
   
    if audio_info_wm2['remasterCatalogueNumber'] !='':
        album_name = album_name + ' (' +  audio_info_wm2['remasterCatalogueNumber'] + ') '

    album_name = album_name + ' [' + audio_info_wm2['format'] + ']'

    
    #detect classical or jazz
    if any("classical" in s for s in audio_info_wm2['tags']):
        classical = 1
    else:
        classical = 0

    if any("jazz" in s for s in audio_info_wm2['tags']):
        jazz = 1
    else:
        jazz = 0


    if len(audio_info_wm2['musicInfo'].values()) == 1:
        for key, value in audio_info_wm2['musicInfo'].items():
                if len(value)==1:
                    artist_name = ','.join(value)
                elif len(value)==2:
                    artist_name = ', '.join(value)
                elif len(value)==3:
                    artist_name = ', '.join(value)
                elif classical ==1 :
                    artist_name = 'Various Classical Artists'
                elif jazz ==1 :
                    artist_name = 'Various Jazz Artists'
                else:
                    artist_name = 'Various Artists'
    elif classical:
        if 'composers' in audio_info_wm2['musicInfo']:
                if len(audio_info_wm2['musicInfo']['composers'])==1:
                    artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
                elif len(audio_info_wm2['musicInfo']['composers'])==2:
                    artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
                elif len(audio_info_wm2['musicInfo']['composers'])==3:
                    artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
                else:
                    artist_name = 'Various Classical Artists'
        elif 'artists' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['artists'])==1:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            elif len(audio_info_wm2['musicInfo']['artists'])==2:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            elif len(audio_info_wm2['musicInfo']['artists'])==3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            else:
                artist_name = 'Various Classical Artists'

        elif 'conductor' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['conductor'])==1:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['conductor'])
            elif len(audio_info_wm2['musicInfo']['conductor'])==2:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['conductor'])
            elif len(audio_info_wm2['musicInfo']['conductor'])==3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['conductor'])
            else:
                artist_name = 'Various Classical Artists'



    elif 'artists' not in audio_info_wm2['musicInfo']:
        for key, value in audio_info_wm2['musicInfo'].items():
            if value:
                artist_name = ', '.join(value)
    
    elif jazz:
        if 'artists' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['artists'])==1:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            elif len(audio_info_wm2['musicInfo']['artists'])==2:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            elif len(audio_info_wm2['musicInfo']['artists'])==3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            else:
                artist_name = 'Various Jazz Artists'
        elif 'with' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['with'])==1:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['with'])
            elif len(audio_info_wm2['musicInfo']['with'])==2:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['with'])
            elif len(audio_info_wm2['musicInfo']['with'])==3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['with'])
            else:
                artist_name = 'Various Jazz Artists'

    elif 'artists' in audio_info_wm2['musicInfo']:
        if len(audio_info_wm2['musicInfo']['artists'])==1:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
        elif len(audio_info_wm2['musicInfo']['artists'])==2:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
        elif len(audio_info_wm2['musicInfo']['artists'])==3:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
        else:
            artist_name = 'Various Artists'
    elif 'composers' in audio_info_wm2['musicInfo']:
        if len(audio_info_wm2['musicInfo']['composers'])==1:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
        elif len(audio_info_wm2['musicInfo']['composers'])==2:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
        elif len(audio_info_wm2['musicInfo']['composers'])==3:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
        else:
            artist_name = 'Various Artists'

    return (artist_name, album_name)


def get_music_dir(dir):
    
    def get_immediate_subdirectories(a_dir):
        return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

    
    def media_in_directory(directory):
        items = os.listdir(directory)

        newlist = []
        for names  in items:
            if names.lower().endswith(".mp3") or names.lower().endswith(".flac") or names.lower().endswith(".dts") or names.lower().endswith(".wav") or names.lower().endswith(".m4a") or names.lower().endswith(".ac3"):
                newlist.append(names)

        return len(newlist)


    def media_in_subdirs(album_path):
        newlist = []
        for root, dirs, files in os.walk(album_path):
            for file in files:
                if file.lower().endswith(".mp3") or file.lower().endswith(".flac") or file.lower().endswith(".dts") or file.lower().endswith(".wav") or file.lower().endswith(".m4a") or file.lower().endswith(".ac3"):
                 newlist.append(file)

        return len(newlist)


    
    sub_directory = get_immediate_subdirectories(dir)

    
    if len(sub_directory) == 0:

        sub_directory = ""

    else:
        sub_directory = sub_directory[0]

    if (media_in_directory(os.path.join(dir, sub_directory)) > 1) and (media_in_directory(dir) > 1):
        return ""
    elif (media_in_directory(os.path.join(dir, sub_directory)) > 1) or media_in_subdirs(os.path.join(dir, sub_directory)) :
        return sub_directory
    elif media_in_directory (dir) >1:
        return ""
    elif media_in_directory (dir) ==0:
        return False



def remove_surrogate_escaping(s, method='ignore'):
    assert method in ('ignore', 'replace'), 'invalid removal method'
    return s.encode('utf-8', method).decode('utf-8')

def is_surrogate_escaped(s):
    try:
        s.encode('utf-8')
    except UnicodeEncodeError as e:
        if e.reason == 'surrogates not allowed':
            return True
        raise
    return False

