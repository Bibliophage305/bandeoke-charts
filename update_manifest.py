import os, json, collections, datetime, uuid

JSON_PATH = "songManifest.json"
CATEGORIES_PATH = "categories.json"

def get_current_manifest():
    # Open the JSON file in read mode
    with open(JSON_PATH, "r") as json_file:
        # Load the JSON data into a Python dictionary
        data = json.load(json_file)
    return data

def get_categories():
    # Open the JSON file in read mode
    with open(CATEGORIES_PATH, "r") as json_file:
        # Load the JSON data into a Python dictionary
        data = json.load(json_file)
    return data

def write_manifest(data):
    with open(JSON_PATH, "w") as json_file:
        json.dump(sorted(data, key=lambda x:x['title']), json_file, indent=4)

def update_manifest():
    
    errors = []
    
    data = get_current_manifest()
    
    # find all songs with lyric files
    lyrics = set()
    for filename in os.listdir('raw-lyrics'):
        # check correct file type
        if filename[-3:] != '.md':
            errors.append(f'{filename} is not a markdown file, please use .md format')
            continue
        
        # check correct filename format
        if len(filename.split(' - ')) != 2:
            errors.append(f'{filename} is not the correct format, please use [song name] - [artist].md')
            continue
        
        lyrics.add(filename[:-3])
    
    # find all songs with musescore chart files
    charts = set()
    for filename in os.listdir('musescore-charts'):
        # check correct file type
        if filename[-5:] != '.mscz':
            errors.append(f'{filename} is not a musescore file, please use .mscz format')
            continue
        
        # check correct filename format
        if len(filename.split(' - ')) != 2:
            errors.append(f'{filename} is not the correct format, please use [title] - [artist].mscz')
            continue
        
        charts.add(filename[:-5])
    
    # add to charts all songs with old format chart files
    for filename in list(os.listdir('old-format-charts')):
        # check correct file type
        if filename[-4:] != '.pdf':
            errors.append(f'{filename} is not a pdf file, please use .pdf format')
            continue
        
        # check correct filename format
        if len(filename.split(' - ')) != 2:
            errors.append(f'{filename} is not the correct format, please use [title] - [artist].pdf')
            continue
        
        # if it's already there, we can delete it
        if filename[:-4] in charts:
            print(f'can now remove old format chart {filename}')
        charts.add(filename[:-4])
    
    both_present = charts & lyrics
    
    for filename in sorted(charts - both_present):
        print(f'lyrics not found for {filename}')
    
    for filename in sorted(lyrics - both_present):
        print(f'chart not found for {filename}')
    
    bad_data = set()
    for i, details in enumerate(data):
        warnings = []
        filename = details['title'] + ' - ' + details['artist']
        if filename not in charts:
            warnings.append(f'Chart not found for {filename}')
        if filename not in lyrics:
            warnings.append(f'Lyrics not found for {filename}')
        if warnings:
            print('\n'.join(warnings))
            print(f'Removing {filename} from song manifest')
            bad_data.add(i)
            print()
        else:
            both_present.remove(filename)
    
    data = [details for i, details in enumerate(data) if i not in bad_data]
    for filename in both_present:
        title, artist = filename.split(' - ')
        data.append({
            'id': str(uuid.uuid4()),
            'title': title,
            'artist': artist,
            'releaseYear': None,
            'categories': [],
            'checkedCategories': [],
        })
        
    categories = get_categories()
        
    for i, details in enumerate(data):
        if 'id' not in details:
            data[i]['id'] = str(uuid.uuid4())
        if details['releaseYear'] is None:
            while True:
                try:
                    year = int(input(f"{details['title']} - {details['artist']} year of release: "))
                    if not 1000 <= year <= datetime.datetime.now().year+1:
                        print("That probably isn't the year you meant")
                        continue
                    data[i]['releaseYear'] = year
                    break
                except ValueError:
                    print('Invalid input')
        decade_category = f"{10*(data[i]['releaseYear']//10)}s"
        if decade_category not in data[i]['categories']:
            data[i]['categories'].append(decade_category)
        for category in [c for c in categories.keys() if c not in details['checkedCategories']]:
            while True:
                try:
                    has_category = input(f"{details['title']} - {details['artist']} has category {category} (y/N): ")
                    assert not has_category or has_category in 'ynYN'
                    if bool(has_category and has_category in 'yY'):
                        data[i]['categories'].append(category)
                    data[i]['checkedCategories'].append(category)
                    break
                except ValueError:
                    print('Need to enter y or n')

    write_manifest(data)

def write_song_list():
    data = get_current_manifest()
    
    song_categories = collections.defaultdict(list)
    
    separate_categories = [c for c, v in get_categories().items() if v['separate']]
    
    for details in data:
        title = details['title'] + ' - ' + details['artist']
        for c in separate_categories:
            if c in details['categories']:
                song_categories[c].append(title)
                break
        else:
            year = details['releaseYear']
            song_categories[f'{10*(year//10)}s'].append(title)
        
    lines = [
        '# The Fever Bandeoke - Song List',
        ''
    ]
    
    for category in sorted([c for c in song_categories if c not in separate_categories])+separate_categories:
        songs = sorted(song_categories[category])
        if not songs:
            continue
        lines += [f'## {category}', '']
        lines += [song+'\\' for song in songs[:-1]]+[songs[-1]]+['']
    
    with open('songList.md', 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    update_manifest()
    write_song_list()