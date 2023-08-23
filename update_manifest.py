import os, json, collections
from datetime import datetime

def update_manifest():
       
    errors = []
    
    # Specify the path to the JSON file
    json_path = "song-manifest.json"

    try:
        # Open the JSON file in read mode
        with open(json_path, "r") as json_file:
            # Load the JSON data into a Python dictionary
            data = json.load(json_file)

    except FileNotFoundError:
        print(f"File '{json_path}' not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error while parsing JSON: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
        
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
    
    for filename in list(os.listdir('old-format-charts')):
        # check correct file type
        if filename[-4:] != '.pdf':
            errors.append(f'{filename} is not a pdf file, please use .pdf format')
            continue
        
        # check correct filename format
        if len(filename.split(' - ')) != 2:
            errors.append(f'{filename} is not the correct format, please use [title] - [artist].pdf')
            continue
        
        if filename[:-4] in charts:
            os.remove(os.path.join('old-format-charts', filename))
        else:
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
        details = {'title': title, 'artist': artist}
        print()
        print(f'Need new info for {filename}')
        while True:
            try:
                year = int(input('Year of release: '))
                if not 1000 <= year <= datetime.now().year+1:
                    print("That probably isn't the year you meant")
                    continue
                details['release-year'] = year
                break
            except ValueError:
                print('Invalid input')
        
        while True:
            try:
                is_christmas = input('Is a Christmas song (y/N): ')
                assert not is_christmas or is_christmas in 'ynYN'
                details['christmas'] = bool(is_christmas and is_christmas in 'yY')
                break
            except ValueError:
                print('Need to enter y or n')
        
        while True:
            try:
                is_halloween = input('Is a Halloween song (y/N): ')
                assert not is_halloween or is_halloween in 'ynYN'
                details['halloween'] = bool(is_halloween and is_halloween in 'yY')
                break
            except ValueError:
                print('Need to enter y or n')
        
        while True:
            try:
                is_musical_theatre = input('Is a musical theatre song (y/N): ')
                assert not is_musical_theatre or is_musical_theatre in 'ynYN'
                details['musical'] = bool(is_musical_theatre and is_musical_theatre in 'yY')
                break
            except ValueError:
                print('Need to enter y or n')
        
        data.append(details)

    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def write_song_list():
    json_path = "song-manifest.json"

    try:
        # Open the JSON file in read mode
        with open(json_path, "r") as json_file:
            # Load the JSON data into a Python dictionary
            data = json.load(json_file)
    
    except FileNotFoundError:
        print(f"File '{json_path}' not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error while parsing JSON: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    
    song_categories = collections.defaultdict(list)
    
    for details in data:
        title = details['title'] + ' - ' + details['artist']
        if details['christmas']:
            song_categories['Christmas'].append(title)
        elif details['halloween']:
            song_categories['Halloween'].append(title)
        elif details['musical']:
            song_categories['Musicals'].append(title)
        else:
            year = details['release-year']
            song_categories[f'{10*(year//10)}s'].append(title)
        
    lines = [
        '# The Fever Bandeoke - Song List',
        ''
    ]
    
    for category in sorted([c for c in song_categories if c not in ['Christmas', 'Halloween', 'Musicals']])+['Christmas', 'Halloween', 'Musicals']:
        songs = sorted(song_categories[category])
        if not songs:
            continue
        lines += [f'## {category}', '']
        lines += [song+'\\' for song in songs[:-1]]+[songs[-1]]+['']
    
    with open('song-list.md', 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    update_manifest()
    write_song_list()