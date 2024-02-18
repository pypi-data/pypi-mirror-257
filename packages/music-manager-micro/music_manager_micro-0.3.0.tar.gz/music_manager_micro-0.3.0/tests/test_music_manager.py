"""Test cases for MusicManager"""
from src.music_manager_micro.music_manager import MusicManager as mm

LIBRARY_NAME = '###TESTABC###'
music_manager = mm(LIBRARY_NAME, "tests/multi_sample")
music_manager.reset_library()
# music_manager.default_root_dir = '.cache/'
music_manager.DEBUG = False

# Tests the collation of music files in a root directory


def test_getfiles():
    '''test file search'''
    root_dir = 'tests/multi_sample'
    l = music_manager.get_files_from_folder(root_dir)
    assert len(l) == 2
    assert l[0] == 'tests/multi_sample/2.mp3'
    assert l[1] == 'tests/multi_sample/1.mp3'

# Tests a music file can generate a valid string representation


def test_build_entry():
    '''test single entry formatting'''
    root_dir = 'tests/multi_sample'
    l = music_manager.get_files_from_folder(root_dir)
    e = music_manager.build_entry(l[0])
    assert e[0] == 1690570765.6394708
    assert e[1] == 'tests/multi_sample/2.mp3'

# Tests that a root directory can generate a list of valid strings


def test_build_list():
    '''full build of a directory'''
    root_dir = 'tests/multi_sample'
    e = music_manager.build_list(root_dir)
    assert e[0][0] == 1690570765.6394708
    assert e[1][1] == 'tests/multi_sample/1.mp3'


def test_empty_folder():
    '''no files present'''
    root_dir = 'tests/empty_folder'
    e = music_manager.build_list(root_dir)
    assert len(e) == 0


def test_execute():
    '''test full process'''
    l = music_manager.execute()
    assert len(l) == 2
    l = music_manager.get_list()
    assert len(l) == 2


def test_get_list():
    '''test returning values without running'''
    l = music_manager.get_list()
    assert len(l) == 2
