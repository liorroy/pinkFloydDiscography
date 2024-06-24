import os  # to interact with the operating system (the .txt file's directory)
import re  # for regular expressions - not used right now
import sys  # for command-line arguments

def load_discography(directory):
    """Gets a directory where 'Pink_Floyd_DB.TXT' is located and loads the discography data into a nested dictionary
    by reading line by line in the text file.

    Args:
        directory (str): the directory where 'Pink_Floyd_DB.TXT' is located

    Returns:
        discography_dict (dict): a nested dictionary where each key is an album name, it's value is a dictionary
        containing the album's name, release_year and a List containing all songs in it
        (each song is dict with its own details)

        example data from 'Pink_Floyd_DB.TXT':
            #The Piper At The Gates Of Dawn::1967
            *Lucifer Sam::Syd Barrett::03:07::Lucifer Sam, Siam cat
            Always sitting by your side
            Always by your side
            ...
            That cat's something I can't explain
            *Matilda mother::Syd Barrett::03:07::There was a king who ruled the land
            His majesty was in command
            With silver eyes the scarlet eagle
            ...
            Let's go into the other room and make them work.
            #A Saucerful of Secrets::1968
            *Let There Be More Light::Waters::05:38::Far, far, far away - way
            People heard him say - say
            ...
        As you can see: line starts with '#" -> new album, '*" -> new song, the rest -> new line in a songs lyrics
       output:
            {
            'The Piper At The Gates Of Dawn': {
                'album_name': 'The Piper At The Gates Of Dawn',
                'release_year': '1967',
                'songs_list': [
                    {
                        'song_name': 'Lucifer Sam',
                        'song_writer': 'Syd Barrett',
                        'song_length': '03:07',
                        'song_lyrics': "Lucifer Sam, Siam cat\nAlways sitting by your side\nAlways by your side That cat's ...
                    },
                    {
                        'song_name': 'Matilda mother',
                        'song_writer': 'Syd Barrett',
                        'song_length': '03:07',
                        'song_lyrics': "There was a king who ruled the land\nHis majesty was in command ...
                    }, ...
                ]
            }, ...
    """
    discography_dict = {}
    current_album_dict = None  # a dictionary for each new album we read
    if not os.path.isdir(directory):
        print("Directory", directory, "not a directory in file system")
        return None
    file_path = os.path.join(directory, 'Pink_Floyd_DB copy.TXT')  # (directory + '/Pink_Floyd_DB.TXT')
    if not os.path.isfile(file_path):
        print("File", os.path.split(file_path)[1], "isn't a file in", directory)
        return None
    if os.path.getsize(file_path) == 0:
        print("File", file_path, "is completely empty")
        return None
    try:
        with (open(file_path, 'r') as file):
            for line in file:
                line = line.strip()  # remove extra whitespaces and newlines '\n' from each line str
                if line.startswith('#'):  # new album
                    album_details = line.split('::')  # = line[1:].split('::') ['#The Piper At The Gates Of Dawn', '1967']
                    album_name = album_details[0][1:]  # Remove '#' from start (index 0) of each new album line
                    release_year = album_details[1]
                    current_album_dict = {  # init new album dict (the values are dicts in discography_dict)
                        "album_name": album_name,
                        "release_year": release_year,
                        "songs_list": []  # a list of dict (each song is a dictionary)
                    }  # {'album_name': 'The Piper At The Gates Of Dawn', 'release_year': '1967', 'songs_list': []}
                    # outer key-> album name, value-> dict with all the album's details
                    discography_dict[album_name] = current_album_dict
                elif line.startswith('*') and current_album_dict:  # new song (current_album_dict not null)
                    song_details = line.split('::')  # ['*Lucifer Sam', 'Syd Barrett', '03:07', 'Lucifer Sam, Siam cat']
                    song_name = song_details[0][1:]  # Remove '*'
                    song_writer = song_details[1]
                    song_length = song_details[2]
                    song_lyrics = song_details[3:]  # ['Lucifer Sam, Siam cat']
                    if len(song_lyrics) > 0:  # usually equal to 1
                        song_lyrics = ''.join(song_lyrics)  # -> Lucifer Sam, Siam cat
                    current_song_dict = {
                        "song_name": song_name,
                        "song_writer": song_writer,
                        "song_length": song_length,
                        "song_lyrics": song_lyrics
                    }
                    # add the new song dict to the songs list (each song is a dictionary) under the current album
                    discography_dict[current_album_dict.get("album_name")]["songs_list"].append(current_song_dict)
                elif current_album_dict and current_song_dict: # new song lyric line
                    lyrics_up_to_this_line_in__dict = discography_dict[current_album_dict.get("album_name")]["songs_list"][-1]['song_lyrics']
                    # add the current line (a String) to the current song's lyrics String
                    discography_dict[current_album_dict.get("album_name")]["songs_list"][-1][
                        'song_lyrics'] = lyrics_up_to_this_line_in__dict + "\n" + line
                    # + "\n" + -> I want to print out the lyrics line by line and not in one paragraph
    except OSError as e:
        print(e)
        return None

    return discography_dict

def print_all_songs_in_album(discography, the_album):
    discography_lower_keys = {} # same, but the outer keys (album names) are now lowercase
    for key, value in discography.items():
        try:
            discography_lower_keys[key.lower()] = value
        except AttributeError:
            discography_lower_keys[key] = value
    the_album_lower = str(the_album).lower()
    if the_album_lower in discography_lower_keys.keys():
        the_albums_songs_list = discography_lower_keys[the_album_lower]["songs_list"]
        if isinstance(the_albums_songs_list, list) and len(the_albums_songs_list) > 0:
            print("\nAll songs in Pink Floyd's", the_album + ":\n")
            for song_number, song in enumerate(the_albums_songs_list, start=1):
                # start= 1 -> List indexes start at 0 for the first song
                print("\t", str(song_number) + '.', song["song_name"])
        else:
            print("\n", the_album, "doesn't have any songs in the discography, please chose a different album")
    else:
        print("\n", the_album, "isn't an album in the discography, please try again")

def print_Songs_album(discography, the_song, song_length, is_option_seven):
    each_song_with_its_album = {}  # dict where key -> song name , value -> album where the song is
    for key in discography:
        the_keys_song_list = discography[key]["songs_list"]
        for song in the_keys_song_list:
            each_song_with_its_album[song["song_name"]] = discography[key]["album_name"]
    if is_option_seven is False:  # choice == '5'
        result_choice_five = ("The song- " + the_song + " (" + song_length + ") " +
                              "is in Pink Floyd's album- " + each_song_with_its_album.get(the_song))
        return result_choice_five
    else:  # choice == '7' or choice == '6'
        result_choice_seven = (" (" + song_length + ") " + "\t * From the album: " +
                               str(each_song_with_its_album.get(the_song)))
        return result_choice_seven

def menu(discography):
    while True:  # show menu until user quits
        print("\nMenu:")
        print("""
            #1\t List all Pink Floyd's albums
            #2\t List all songs in an album
            #3\t Lookup a song's length (enter the exact song name)
            #4\t Lookup a song's lyrics (enter the exact song name)
            #5\t Lookup a song's album (enter the exact song name)
            #6\t Find a song by part of it's name (or a part of the name)
            #7\t Find a song by a lyric (returns all songs that contain that lyric)
            #8\t Quit 
            """)
        choice = input("Choose an option: ")
        if choice == '1':
            print("The", len(discography.keys()), "albums in Pink Floyd's discography:\n")
            for key in discography:
                print("\t-", key, "(" + discography[key]["release_year"] + ")")  # discography.get(key)["release_year"]
        elif choice == '2':
            the_album = input("Enter the album name: ").strip()
            print_all_songs_in_album(discography, the_album)
        elif choice in ['3', '4', '5', '7']:
            all_songs_length_and_lyrics = {}
            # nested dict with key -> song name , value -> list with 2 elements = [length, lyrics]
            for key in discography:
                the_keys_song_list = discography[key]["songs_list"]
                for song in the_keys_song_list:
                    all_songs_length_and_lyrics[song["song_name"]] = [song["song_length"], song["song_lyrics"]]
            if choice != '7':
                the_song = input("Enter the songs name: ").strip()
                if the_song not in all_songs_length_and_lyrics:
                    print("\n", the_song, "isn't a song in the discography, please try again")
                else:  # the song exists in the discography
                    if choice == '3':
                        print("\n\tThe length of the song-", the_song, "is:",
                              all_songs_length_and_lyrics.get(the_song)[0], "minutes")
                    elif choice == '4':
                        print("\nThe lyrics for the song-",
                              the_song + ":\n\n" + all_songs_length_and_lyrics.get(the_song)[1])
                    elif choice == '5':
                        print("\n\t",
                              print_Songs_album(discography, the_song, all_songs_length_and_lyrics.get(the_song)[0], False))
            else:  # choice == '7':
                all_songs_and_lyrics = {}  # dict with key -> song name , value -> it's lyrics
                for key in discography:
                    the_keys_song_list = discography[key]["songs_list"]
                    for song in the_keys_song_list:
                        all_songs_and_lyrics[song["song_name"]] = song["song_lyrics"]
                the_lyric = input("Enter the Lyric from the song you're looking for: ").strip()
                matched_songs = []
                the_lyric_lower = the_lyric.lower()
                for key in all_songs_and_lyrics:
                    if the_lyric_lower in all_songs_and_lyrics.get(key).lower():
                        matched_songs.append(key)
                if len(matched_songs) == 0:
                    print("\nNo Pink Floyd song contains the Lyric-", "'" + the_lyric + "'", ",Please try again.")
                elif len(matched_songs) == 1:
                    print("\nThe song that contains the Lyric", "'" + the_lyric + "'", "is:")
                    print("\t-", matched_songs[0],
                          print_Songs_album(discography, matched_songs[0], all_songs_length_and_lyrics.get(matched_songs[0])[0], True))  # discography.get(key)["release_year"]
                else:
                    print("\nHere are all of the songs that contain the Lyric", "'" + the_lyric + "':\n")
                    for song in matched_songs:
                        print("\t-", song,
                              print_Songs_album(discography, song, all_songs_length_and_lyrics.get(song)[0], True))
        elif choice == '6':  # Find a song by part of it's name
            all_songs_length = {}  # dict with key -> song name , value -> length
            for key in discography:
                the_keys_song_list = discography[key]["songs_list"]
                for song in the_keys_song_list:
                    all_songs_length[song["song_name"]] = song["song_length"]
            the_song_name = input("Enter the name (or a part of it) of the song you're looking for: ").strip()
            the_song_name_lower = the_song_name.lower()
            matched_songs = []
            for key in all_songs_length:
                if re.search(the_song_name_lower, key.lower()) is not None:
                    matched_songs.append(key)
            if len(matched_songs) == 0:
                print("\nNo Pink Floyd song name contains -", "'" + the_song_name + "'", ",Please try again.")
            elif len(matched_songs) == 1:
                print("\nThe song who's name contains-", "'" + the_song_name + "'", "is:")
                print("\t-", matched_songs[0],
                      print_Songs_album(discography, matched_songs[0], all_songs_length.get(matched_songs[0]), True))
            else:
                print("\nHere are all of the songs that name contains-", "'" + the_song_name + "':\n")
                for song in matched_songs:
                    print("\t-", song,
                          print_Songs_album(discography, song, all_songs_length.get(song), True))
        elif choice in ['8', 'q', 'Q']:
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    db_directory = "/Users/Study/Downloads"  # default directory where 'Pink_Floyd_DB.TXT' is located
    if len(sys.argv) > 1:
        directory = sys.argv[1]  # e.g: python3 pink_floyd.py /Users/Study/Downloads
    discography = load_discography(db_directory)
    if not (isinstance(discography, dict)):
        print("Error: please check the 'Pink_Floyd_DB.TXT' file")
    else:
        menu(discography)