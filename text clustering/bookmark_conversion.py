import json

def bookmarksToUrls(profile_name, unsorted_folder_name="other"):
    path = r'C:\Users\MichaelE\AppData\Local\Google\Chrome\User Data\\'
    path += profile_name
    path += '\Bookmarks'

    with open(path) as json_file:
        bookmarks = json.loads(json_file.read())

    unsorted = bookmarks["roots"][unsorted_folder_name]
    unsorted_urls = [bookmark["url"] for bookmark in unsorted["children"]]
    return unsorted_urls
