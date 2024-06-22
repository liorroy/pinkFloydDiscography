import os  # to interact with the operating system (walking through directories to parse the YAML files)
import re  # for regular expressions - not used right now
import sys  # for command-line arguments


def load_discography(directory):
    """Gets a directory where 'Pink_Floyd_DB.TXT' is located and loads the discography data into a dictionary:

    We create a nested dictionary structure to store the discography data:

    The main dictionary uses album names as keys
    Each album has 'year' and 'songs' keys
    Each song is a dictionary with 'title', 'artists', 'duration', and 'lyrics' keys


    We open and read the file line by line, parsing each line and adding the data to our structure.


        Finally, we return the parsed discography.


        Parses the text file and structures the data into a dictionary with album names as keys and album details as values.
    Each album contains its title, year, and a list of songs.
    Each song is a dictionary containing its title, writer, length, and lyrics.

    Various functions are implemented to handle the different tasks from the menu:
    list_albums(discography)
    list_songs_in_album(discography, album_name)
    get_song_length(discography, song_name)
    get_song_lyrics(discography, song_name)
    get_album_by_song(discography, song_name)
    search_songs_by_name(discography, word)
    search_songs_by_lyrics(discography, word)
    Menu Loop:

    A loop to display the menu and handle user input, invoking the appropriate function based on the user's choice.

        We do not parse the data in the file, we just read it line by line.


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
            'title': 'The Piper At The Gates Of Dawn',
            'year': '1967',
            'songs': [
                {
                    'title': 'Lucifer Sam',
                    'writer': 'Syd Barrett',
                    'length': '03:07',
                    'lyrics': "Lucifer Sam, Siam cat Always sitting by your side Always by your side That cat's something I can't explain Ginger, Ginger you're a witch You're the left side He's the right side Oh, no! That cat's something I can't explain Lucifer go to sea Be a hip cat, be a ship's cat Somewhere, anywhere That cat's something I can't explain At night prowling sifting sand Hiding around on the ground He'll be found when you're around That cat's something I can't explain"
                }
            ]
        }
        }

        dict_keys(['The Piper At The Gates Of Dawn', 'A Saucerful of Secrets', 'More', 'Division Bell', 'The Wall', 'Dark side of the moon', 'Wish you were here', 'Animals'])

        print(discography.get('The Piper At The Gates Of Dawn'))
        print('\n')
        {'year': '1967', 'songs': [{'title': 'Lucifer Sam', 'artists': ['Syd Barrett'], 'duration': '03:07', 'lyrics': 'Lucifer Sam, Siam cat'}, {'title': 'Matilda mother', 'artists': [
        'Syd Barrett'], 'duration': '03:07', 'lyrics': 'There was a king who ruled the land'}, {'title': 'Flaming', 'artists': ['Syd Barrett'], 'duration': '02:45', 'lyrics': 'Alone in
        the clouds all blue'}, {'title': 'The Gnome', 'artists': ['Syd Barrett'], 'duration': '02:13', 'lyrics': 'I want to tell you a story'}, {'title': 'Chapter 24', 'artists': ['Syd
        Barrett'], 'duration': '03:41', 'lyrics': 'A movement is accomplished in six stages'}, {'title': 'Scarecrow', 'artists': ['Syd Barrett'], 'duration': '02:10', 'lyrics': 'The bla
        ck and green scarecrow as everyone knows'}, {'title': 'Astronomy Domine', 'artists': ['Syd Barrett'], 'duration': '04:12', 'lyrics': 'Lime and limpid green, a second scene'}, {'
        title': 'Take Up Thy Stethoscope and Walk', 'artists': ['Waters'], 'duration': '03:06', 'lyrics': 'Doctor doctor!'}, {'title': 'Interstellar Overdrive', 'artists': ['Barrett', '
        Waters', 'Wright', 'Mason'], 'duration': '09:41', 'lyrics': 'Instrumental'}, {'title': 'Bike', 'artists': ['Syd Barrett'], 'duration': '03:22', 'lyrics': "I've got a bike, you c
        an ride it if you like."}]}

        Album: The Piper At The Gates Of Dawn (1967)
          - Lucifer Sam by Syd Barrett (03:07)
          - Matilda mother by Syd Barrett (03:07)
          - Flaming by Syd Barrett (02:45)
          - The Gnome by Syd Barrett (02:13)
          - Chapter 24 by Syd Barrett (03:41)
          - Scarecrow by Syd Barrett (02:10)
          - Astronomy Domine by Syd Barrett (04:12)
          - Take Up Thy Stethoscope and Walk by Waters (03:06)
          - Interstellar Overdrive by Barrett, Waters, Wright, Mason (09:41)
          - Bike by Syd Barrett (03:22)
    Args:
        directory (str): directory where 'Pink_Floyd_DB.TXT' is located

    Returns:
        discog (dict): nested dictionary with data from 'Pink_Floyd_DB.TXT', each key is an album, the value is a dictionary
        with it's details (release year) and a list of the songs in it

                            # {'album_name': 'The Piper At The Gates Of Dawn', 'release_year': '1967',
                    # 'songs_list': [{'song_name': 'Lucifer Sam', 'song_writer': 'Syd Barrett', 'song_length': '03:07', 'song_lyrics': 'Lucifer Sam, Siam cat'}]}

                    # {'album_name': 'The Piper At The Gates Of Dawn', 'release_year': '1967',
                    # 'songs_list': [{'song_name': 'Lucifer Sam', 'song_writer': 'Syd Barrett', 'song_length': '03:07', 'song_lyrics': 'Lucifer Sam, Siam cat'},
                    # {'song_name': 'Matilda mother', 'song_writer': 'Syd Barrett', 'song_length': '03:07', 'song_lyrics': 'There was a king who ruled the land'}]}
    """
    discography_dict = {}
    current_album_dict = None  # a dictionary for each album we parse

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
            print("opened the file\n")
            # print(file.read())
            # print(file.read().splitlines())
            # print(file.readlines())

            for line in file:
                print("\nNEW LINE\n")
                line = line.strip()  # remove extra whitespaces and newlines '\n' from each line str

                if line.startswith('#'):  # new album
                    album_details = line.split('::')  # = line[1:].split('::') ['#The Piper At The Gates Of Dawn', '1967']
                    album_name = album_details[0][1:]  # Remove '#' from start (index 0) of each new album line
                    release_year = album_details[1]

                    # init new album dict (the values are dicts in discography_dict)
                    current_album_dict = {
                        "album_name": album_name,
                        "release_year": release_year,
                        "songs_list": []  # a list of dict (each song is a dictionary)
                    }  # {'album_name': 'The Piper At The Gates Of Dawn', 'release_year': '1967', 'songs_list': []}
                    print(album_details)
                    print(album_name, ",", release_year)
                    print(current_album_dict.items())

                    # key-> album name, value-> dict with all the album's details
                    discography_dict[album_name] = current_album_dict

                    print(album_name, "= CURRENT ALBUM NAME = ", current_album_dict.get("album_name"), "=",
                          discography_dict[album_name]["album_name"], "=",
                          discography_dict[current_album_dict.get("album_name")]["album_name"])  # print(discography_dict)
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
                    }  # {'song_name': 'Matilda mother', 'song_writer': 'Syd Barrett', 'song_length': '03:07', 'song_lyrics': 'There was a king who ruled the land'}
                    print(song_details)
                    print(current_song_dict)
                    print(current_album_dict)
                    # add the new song dict to the songs list (a list of dicts for each song) under the current album
                    discography_dict[current_album_dict.get("album_name")]["songs_list"].append(current_song_dict)
                elif current_album_dict and current_song_dict: # new song lyric line
                    lyrics_up_to_this_line_in__dict = discography_dict[current_album_dict.get("album_name")]["songs_list"][-1]['song_lyrics']
                    # add the current line (a String) to the current song's lyrics String (with a whitespace " "
                    discography_dict[current_album_dict.get("album_name")]["songs_list"][-1][
                        'song_lyrics'] = lyrics_up_to_this_line_in__dict + "\n" + line
                    # + "\n" + -> I want to print out the lyrics line by line and not in one paragraph
    except OSError as e:
        print(e)
        return None

    return discography_dict

def print_all_songs_in_album(discography, the_album):
    if the_album in discography.keys():
        the_albums_songs_list = discography[the_album]["songs_list"]
        # List of dicts, every song is a dict with the keys: "song_name" "song_writer" "song_length" "song_lyrics"

        # print(the_albums_songs_list)

        # for song in the_albums_songs_list:
        #     print("\t-", song["song_name"])
        #
        # for i in range(len(the_albums_songs_list)):
        #     print("\t", str(i) + ".", dict(the_albums_songs_list[i]).get("song_name"))
        #
        # index = 0
        # for song in the_albums_songs_list:
        #     print("\t-", str(index) + ")", the_albums_songs_list[index]["song_name"])
        #     index = index + 1
        #
        # indexi = 0
        # for song in the_albums_songs_list:
        #     print("\t-", str(indexi) + "-", song["song_name"])
        #     indexi = indexi + 1
        #
        # for songIndex, song in enumerate(the_albums_songs_list):
        #     print((songIndex + 1), song["song_name"], song["song_length"])
        #
        # for songi, song in enumerate(the_albums_songs_list, start= 1):
        #     print(songi, song["song_name"], song["song_length"])

        if isinstance(the_albums_songs_list, list) and len(the_albums_songs_list) > 0:
            print("\nAll songs in Pink Floyd's", the_album + ":\n")
            for song_number, song in enumerate(the_albums_songs_list, start= 1):
                # start= 1 -> List indexes start at 0 for the first song
                print("\n\t", str(song_number) + '.', song["song_name"])
        else:
            print("\n", the_album, "doesn't have any songs in the discography, please chose a different album")
    else:
        print("\n", the_album, "isn't an album in the discography, please try again")

# def print_song_length1(discography, the_song): # Lucifer Sam
    # all_songs_list = []  # list with all song names
    # for key in discography:
    #     the_albums_songs_list = discography[key]["songs_list"]
    #     for song in the_albums_songs_list:
    #         all_songs_list.append(song["song_name"])
    # print(all_songs_list)

    # dict with key -> song name , value -> song length
    # all_songs_length = {}  # list with all song names
    # for key in discography:
    #     the_keys_song_list = discography[key]["songs_list"]
    #     for song in the_keys_song_list:
    #         all_songs_length[song["song_name"]] = song["song_length"]
    #         print(song["song_name"], " ", song["song_length"])
    # print(len(all_songs_length),"\n")
    # print(all_songs_length.keys(),"\n")
    # print(all_songs_length.items(),"\n")
    # print(all_songs_length,"\n")
    # print(all_songs_length.get("Pigs On The Wing (Part One)"),"\n\n\n\n\n\nNOW WITH LYRICS:")


    #
    # all_songs_length_and_lyrics = {}  # nested dict with key -> song name , value -> list with 2 elements = [length, lyrics]
    # for key in discography:
    #     the_keys_song_list = discography[key]["songs_list"]
    #     for song in the_keys_song_list:
    #         all_songs_length_and_lyrics[song["song_name"]] = [song["song_length"], song["song_lyrics"]]
    #         print(song["song_name"], " ", song["song_length"])
    #         print(song["song_name"], " ", song["song_lyrics"])
    #
    # for key in all_songs_length_and_lyrics:
    #     print(key, "-> Length:", all_songs_length_and_lyrics[key][0], "-> LYRICS:", str(all_songs_length_and_lyrics[key][1]))
    # print(len(all_songs_length_and_lyrics), "\n")
    # print(all_songs_length_and_lyrics.keys(), "\n")
    # print(all_songs_length_and_lyrics.items(), "\n")
    # print(all_songs_length_and_lyrics, "\n")
    # print(all_songs_length_and_lyrics.get("Pigs On The Wing (Part One)"), "\n")
    # print(all_songs_length_and_lyrics.get("Lucifer Sam")[1])

    # {
    #     "song_name": song_name,
    #     "song_writer": song_writer,
    #     "song_length": song_length,
    #     "song_lyrics": song_lyrics
    # }

    # print(len(all_songs_in_discography))
        # the_albums_songs_list = discography[the_album]["songs_list"] # the_albums_songs_list[index]["song_name"]
        # all_songs_in_discography.append(discography[key]["songs_list"]["song_name"])

    # if the_song in all_songs_in_discography:
    #     print("")
    # else:
    #     print("\n", the_song, "couldn't be found in the discography, please try again")
#
# def print_song_length(all_songs_length_and_lyrics, the_song):
#     if the_song in all_songs_length_and_lyrics:
#         print("\tThe length of the song-", the_song,  "is:", all_songs_length_and_lyrics.get(the_song)[0], "minutes")
#     else:
#         print("\n", the_song, "doesn't exist in the discography, please try again")
#
# def print_song_lyrics(all_songs_length_and_lyrics, the_song):
#     if the_song in all_songs_length_and_lyrics:
#         print("\nThe lyrics of the song-", the_song + ":\n\n" + all_songs_length_and_lyrics.get(the_song)[1])
#     else:
#         print("\n", the_song, "doesn't exist in the discography, please try again")


def menu(discography):
    choice = ''
    # while choice != '1.'

    while True:
        print("\nMain Menu:")
        print("""
            #1\t List all Pink Floyd's albums
            #2\t List all songs in an album
            #3\t Lookup a song's length
            #4\t Lookup a song's lyrics
            #5\t Lookup a song's album
            #6\t Lookup song's by name 
            #7\t Lookup song's by Lyric (get all songs that contain a lyric)
            #8\t Quit 
            """)

        # in 3. 4. look for exact song name
        # in 6. 7. letter size doesn't matter (e.g time will return the same as input - Time, if Time is in the db),\
        # and also find half words, e.g "ti" will find the song time

        # print("\nMain Menu:")
        # print("1. List of albums")
        # print("2. List of songs in the album")
        # print("3. Getting the length of the song")
        # print("4. Getting song lyrics")
        # print("5. In which album is the song")
        # print("6. Searching for a song by name")
        # print("7. Searching for a song by lyrics")
        # print("8. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            # print(f"\nthe keys: {discography.keys()}\n")
            print("The",  len(discography.keys()), "albums in Pink Floyd's discography:\n")
            for key in discography:
                print("\t-", key)
            # break
        elif choice == '2':
            the_album = input("Enter the album name: ").strip()
            print_all_songs_in_album(discography, the_album)
        elif choice in ['3', '4']:

            all_songs_length_and_lyrics = {}  # nested dict with key -> song name , value -> list with 2 elements = [length, lyrics]
            for key in discography:
                the_keys_song_list = discography[key]["songs_list"]
                for song in the_keys_song_list:
                    all_songs_length_and_lyrics[song["song_name"]] = [song["song_length"], song["song_lyrics"]]

            the_song = input("Enter the songs name: ").strip()
            if the_song not in all_songs_length_and_lyrics:
                print("\n", the_song, "doesn't exist in the discography, please try again")
            else:
                if choice == '3':
                    print("\n\tThe length of the song-", the_song, "is:", all_songs_length_and_lyrics.get(the_song)[0],
                          "minutes")
                elif choice == '4':
                    print("\nThe lyrics for the song-",
                          the_song + ":\n\n" + all_songs_length_and_lyrics.get(the_song)[1])
        # elif choice == '5':

            # if choice == '3':
            #     the_song = input("Enter the songs name: ").strip()
            #     print_song_length(all_songs_length_and_lyrics, the_song)
            # elif choice == '4':
            #     the_song = input("Enter the songs name to lookup it's lyrics: ").strip()
            #     print_song_lyrics(all_songs_length_and_lyrics, the_song)
            # break
        # elif choice == '2':
        #     album_name = input("Enter the album name: ")
        #     songs = list_songs_in_album(discography, album_name)
        #     if songs:
        #         for song in songs:
        #             print(song)
        #     else:
        #         print("Album not found.")
        elif choice in ['8', 'q', 'Q']:
            break
        else:
            print("Invalid option. Please try again.")





# cd /Users/Shared/PyCharm\ projects/pinkFloydDiscography/ #
if __name__ == '__main__':

    db_directory = "/Users/Study/Downloads"  # default directory where 'Pink_Floyd_DB.TXT' is located
    if len(sys.argv) > 1:
        directory = sys.argv[1]  # e.g:  python3 main.py /Users/Study/Downloads

    discography = load_discography(db_directory)
    # if isinstance(discography, dict):
    #     print("IT DICT")
    menu(discography)

    # if discography is not None:
    #     print(f"\nthe keys: {discography.keys()}\n")
    #     print("All albums in Pink Floyd's discography:\n")
    #     for key in discography:
    #         print("\t-",key)
    # menu()


    # print("\n\n\n\n\n\tThe FINAL returned dict:"'\n', discography.keys(), '\n\n\n', discography.items(),
    #       '\n\n\n',
    #       discography, '\n\n\n\n\n\nFhe first album:', discography.get("The Piper At The Gates Of Dawn"),
    #       '\n\n\n', discography.get("The Piper At The Gates Of Dawn!", "MISSING KEY!"),
    #       '\n\n\n', discography["The Piper At The Gates Of Dawn"], '\n\n\n\n\n\nFhe last (eigth) album:',
    #       discography.get("Animals"))
    # # print(f"\nthe keys: {data.keys()}\n")
    # # print(data.get('The Piper At The Gates Of Dawn'))
    # # print("done")
