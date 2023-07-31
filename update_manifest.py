import os, json

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
            errors.append(f'{filename} is not a markdown file, please use .md format')
            continue
        
        # check correct filename format
        if len(filename.split(' - ')) != 2:
            errors.append(f'{filename} is not the correct format, please use [title] - [artist].md')
            continue
        
        charts.add(filename[:-5])
    
    both_present = charts & lyrics
    
    bad_data = set()
    for i, details in enumerate(data):
        warnings = []
        filename = details['title'] + ' - ' + details['artist']
        if details['title'] not in charts:
            warnings.append(f'Chart not found for {filename}')
        if details['title'] not in lyrics:
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
                details['release-year'] = int(input('Year of release: '))
                break
            except ValueError:
                print('Invalid input')
        
        while True:
            try:
                is_christmas = input('Is a Christmas song (y/N): ')
                assert not is_christmas or is_christmas in 'ynYN'
                details['christmas'] = is_christmas in 'yY'
                break
            except ValueError:
                print('Need to enter y or n')
        
        while True:
            try:
                is_halloween = input('Is a Halloween song (y/N): ')
                assert not is_halloween or is_halloween in 'ynYN'
                details['halloween'] = is_halloween in 'yY'
                break
            except ValueError:
                print('Need to enter y or n')
        
        while True:
            try:
                is_musical_theatre = input('Is a musical theatre song (y/N): ')
                assert not is_musical_theatre or is_musical_theatre in 'ynYN'
                details['musical'] = is_musical_theatre in 'yY'
                break
            except ValueError:
                print('Need to enter y or n')
        
        data.append(details)

    with open(json_path, "w") as json_file:
        json.dump(data, json_file)

if __name__ == '__main__':
    update_manifest()