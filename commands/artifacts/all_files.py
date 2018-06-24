from os import listdir
from os.path import join
from commands.utils.local_cache import LocalCache
from commands.utils.resolve_data_source import resolve_data_source

from .types import FileList


@LocalCache
def all_files(source_marker) -> FileList:
    path, parser_class, selector, features_extractor = resolve_data_source(source_marker)
    return [
        join(path, file)
        for file in listdir(path)
        if selector(file)
    ]
