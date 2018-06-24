from os.path import basename
from commands.utils.local_cache import LocalCache
from commands.utils.resolve_data_source import resolve_data_source

from .types import FileList
from .parsed_data import parsed_data
from .deduplicated_files import deduplicated_files


@LocalCache
def unintersected_files(source_marker: str) -> FileList:
    deduplicated_files_list = deduplicated_files(source_marker)
    path, parser_class, selector, features_extractor = resolve_data_source(source_marker)

    unitersected = []
    previous_key = None
    for filename in sorted(deduplicated_files_list):
        data = parsed_data(source_marker, filename)
        features = features_extractor(basename(filename))
        key = '{year}.{day}'.format(**features)
        ut = data.get('ut', transposed=True)[0]

        if key != previous_key or len(unitersected) == 0:
            previous_key = key
            unitersected.append((filename, ut[0], ut[-1]))
            continue

        if ut[0] <= unitersected[-1][1] <= ut[-1] or ut[0] <= unitersected[-1][1] <= ut[-1]:
            unitersected.pop()
        else:
            unitersected.append((filename, ut[0], ut[-1]))

    return unitersected
