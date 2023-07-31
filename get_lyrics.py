import os, json
from azapi import AZlyrics

def get_lyrics():
       
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
    
    while True:
        
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
        
        need_lyrics = charts - lyrics
        
        if not need_lyrics:
            break
        
        for filename in need_lyrics:
            print(filename)
            title, artist = filename.split(' - ')
            api = AZlyrics()
            api.artist = artist
            api.title = title
            try:
                lyrics = api.getLyrics(save=False)
            except IndexError:
                continue
            if not lyrics:
                continue
            try:
                with open(os.path.join('raw-lyrics', filename+'.md'), 'w') as f:
                    f.write(lyrics)
            except TypeError:
                continue

if __name__ == '__main__':
    get_lyrics()