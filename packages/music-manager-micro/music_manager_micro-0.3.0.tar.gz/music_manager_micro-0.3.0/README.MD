# MusicManager

Build a list of media files from a root directory

# Usage

First time usage should use the execute function. This will return the python list of entries containing tuples in the form

```
[
(mtime:float,path:str),
...
]
```

```python
from music_manager_micro.music_manager import MusicManager as MM
library = 'my_library'
media_dir = '/media/music'
manager = MM(library,media_dir)
music_list = manager.execute()
```

Since the program stores the result in a sqlite DB in

```
$HOME/.config/MusicManagerMicro/<library_name>
```

We can retrieve the data quickly without re-scanning the directory. We only need to execute when the process running this application is set to check for new files.

Get an existing list

```python
from music_manager_micro.music_manager import MusicManager as MM
library = 'my_library'
media_dir = '/media/music'
manager = MM(library,media_dir)
music_list = mm.get_list()
```

# Features

-   Default searches for .mp3 and .flac files
-   Supports absolute and relative root directory

# Maintenance

-   Remove .cache/MusicManagerMicro directory to safely clear all library data, or individual libraries
-   Safely backup .cache/MusicManagerMicro directory if wanted to preserve cache data

# Notes

-   Library name is intended for internal filesystem use so should only contain characters acceptable for a folder name A-Z, a-z, \_, -.

# Build

```bash
python -m build
python -m twine upload dist/*
```
