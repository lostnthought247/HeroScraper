from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request
import re

# Collects & parses info from root URL
root_url = 'https://heroichub.com/'
req = Request(root_url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urlopen(req).read()
soup = BeautifulSoup(resp, 'html.parser')

# Sets up all the lists for add links, sublinks, and forum links
all_links = []
forum_links = []
all_sub_links = []
final_links = []


batman = 0
supergirl = 0
wonderwoman = 0
aquaman = 0
wolverine = 0
superman = 0

# Collects, parses, and finds links on a given page
def get_initial_link_list(soup):
    for link in soup.find_all('a'):
        all_links.append(link.get('href'))


    for link in all_links:
        if str(link)[0:12] == "./viewforum.":
            url = root_url + str(link).split("&")[0][1:]
            forum_links.append(url)

    for link in forum_links:
        get_sub_links(link)

    for link in all_sub_links:
        get_final_links(link)


# Collects, parses, and finds links on link found in initial page
def get_sub_links(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urlopen(req).read()
    soup = BeautifulSoup(resp, 'html.parser')

    # Tries to search keyword "permissions" to only add non-restricted links to sublink list
    if "permissions" not in str(soup):
        for link in soup.find_all('a'):
            if "/viewforum." in str(link):
                print("sublink: ", link)
                all_sub_links.append(root_url + str(link.get('href')).split('&')[0][2:])

# Grabs all the discussion board links
def get_final_links(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urlopen(req).read()
    soup = BeautifulSoup(resp, 'html.parser')

    if "to view this forum" not in str(soup):
        for link in soup.find_all('a'):
            if "viewtopic" in str(link):
                print("Final_Link: ", link)
                final_links.append(root_url + str(link.get('href')))

# Reviews text on discussion boards for keyword matches to hero names
def count_super_hero(url):
    global superman
    global batman
    global supergirl
    global wonderwoman
    global aquaman
    global wolverine


    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urlopen(req).read()
    soup = BeautifulSoup(resp, 'html.parser')
    text = soup.get_text()
    text = text.lower()
    text = text.splitlines()

    for line in text:
        if " superman " in line:
            superman += 1
            print("+1 superman")
            print(line)
        if " batman " in line:
            batman += 1
            print("+1 batman")
            print(line)
        if " supergirl " in line:
            supergirl += 1
            print("+1 supergirl")
            print(line)
        if " aquaman " in line:
            aquaman += 1
            print("+1 aquaman")
            print(line)
        if " wolverine " in line:
            wolverine += 1
            print("+1 wolverine")
            print(line)
        if " wonder woman " in line or " wonderwoman " in line:
            wolverine += 1
            print("+1 wolverine")
            print(line)


    return (superman, batman, supergirl, aquaman, wolverine)

# Runs the main script() and prints final counts
get_initial_link_list(soup)
n = 1
for link in final_links:
    print('Revieiwng Page Number:', n)
    n += 1
    count_super_hero(link)

print("Superman Refs:" , superman)
print("Batman Refs:" , batman)
print("Supergirl Refs:" , supergirl)
print("Wonder Woman Refs:" , wonderwoman)
print("Aquaman Refs:" , aquaman)
print("Wolverine Refs:" , wolverine)
