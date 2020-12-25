from collections import defaultdict, namedtuple
import subprocess
import os
import re
from email.utils import parsedate_to_datetime
import datetime
import xml.etree.ElementTree as ET
import sys

def readDates(filename):
    """ git blame the input file and parse out the dates. returns a list of date strings"""
    done = subprocess.run(["git", "blame", filename], capture_output=True)
    dates = []
    date_pattern = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
    for i,blameline in enumerate(done.stdout.decode('utf-8').split("\n")):
        match = date_pattern.search(blameline)
        if match is not None:
            dates.append(match.group())
        else:
            dates.append(None)
    return dates

def readLinks(filename,dates):
    """ Read all the links from the linkfile and add them to a list. 
    """
    links = []
    with open(filename,'r') as linkFile:
        def addLink(links,items,dates,lineNumbers):
            """ the items arg contains all the lines for a link.
                finds the last date where one of the lines was changed,
                munges the tags
                adds the link object to links
            """
            if items:
                changedate = min(dates[j] for j in lineNumbers)
                assert(len(items) >= 2)
                while len(items) < 4:
                    items.append("")
                items[2] = [x.strip() for x in items[2].split(",")]
                links.append(Link._make(items + [changedate]))

        items = []
        lineNumbers = []
        for i,line in enumerate(linkFile):
            # go over the lines in the file, collect them until a link
            # description is complete and then add it to the links list
            line = line.strip()
            if not line or line == "---":
                addLink(links,items,dates,lineNumbers)
                items=[]
                lineNumbers=[]
            else:
                items.append(line)
                lineNumbers.append(i)
        addLink(links,items,dates,lineNumbers)
    return links

def linksByDate(links):
    """ group the links by date """
    bydate = defaultdict(list)
    for link in links:
        linkdate = datetime.datetime.fromisoformat(link.date) 
        bydate[linkdate].append(link)
    return bydate


def findNewLinks(links, generated_time):
    """ get the links that are newer than generated_time """
    new_links = []
    for link in links:
        linkdate = datetime.datetime.fromisoformat(link.date) 
        if generated_time is None or linkdate > generated_time:
            new_links.append(link)
    return new_links

def parseRss():
    """ parse feed.rss """
    with open("feed.rss",'r') as rssFile:
        s = rssFile.read()
        tree = ET.fromstring(s)
        return s, tree

def currentTimeStr():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %T %z")

def updateRssTimeGenerated(root):
    for item in root.iter('lastBuildDate'):
        item.text = currentTimeStr()

def addLink(root, singleLink):
    """ add a link to the rss tree """
    channel = root.find("channel")
    today = currentTimeStr()
    item = ET.SubElement(channel, "item")
    title = ET.SubElement(item, "title")
    title.text = "Link: " + singleLink.text
    link = ET.SubElement(item, "link")
    link.text = singleLink.url
    pubDate = ET.SubElement(item, "pubDate")
    pubDate.text = today
    description = ET.SubElement(item, "description")
    if singleLink.descr:
        description.text = singleLink.descr
    else:
        description.text = "This link has no description. It is tagged as " + ",".join(singleLink.tagStr)

def addLinks(root, links):
    """ add multiple links to the rss tree """
    channel = root.find("channel")
    today = currentTimeStr()
    item = ET.SubElement(channel, "item")
    title = ET.SubElement(item, "title")
    title.text = "New Links"
    link = ET.SubElement(item, "link")
    link.text = "https://adriann.github.io/links_list.html"
    pubDate = ET.SubElement(item, "pubDate")
    pubDate.text = today

    desc = "<ul>"
    for link in links:
        desc += "<li>"
        desc += "<a href=\""+link.url+"\">"+link.text+"</a>"
        if link.descr:
            desc += ": "+link.descr
        desc += "</li>"

    desc += "</ul>"

    description = ET.SubElement(item, "description")
    description.text = desc


Link = namedtuple('Link', ['text', 'url', 'tagStr', 'descr', 'date'])

filename = sys.argv[1]

done = subprocess.run(["git", "log", "--pretty='%aD'", "-n 1", "--",  "links*.html"], capture_output=True)
generated_timestamp = done.stdout.decode('utf-8') #os.path.getmtime("markdown/links_list.markdown")
generated_time = parsedate_to_datetime(generated_timestamp)
filename_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
if  filename_timestamp <= generated_time:
    print("Nothing to do, exiting")
    sys.exit(0)

dates = readDates(filename)
links = readLinks(filename,dates)
new_links = findNewLinks(links, generated_time)
rssText, root = parseRss()
filtered_new_links = []
for link in new_links:
    if link.url not in rssText or input(f"{link.text} already in rss. Duplicate y/n?") == 'y':
        filtered_new_links.append(link)
new_links = filtered_new_links

if len(new_links)>1:
    addLinks(root, new_links)
elif len(new_links) == 1:
    addLink(root, new_links[0])

updateRssTimeGenerated(root)

bydate = linksByDate(links)
with open("feed.rss","w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8" ?> \n')
    f.write(ET.tostring(root, encoding="unicode"))

with open("markdown/links_list.markdown", "w") as out:
    preamble = "#Links\n"
    out.write(preamble)
    for date,linkList in sorted(bydate.items(), reverse=True):
        out.write(f"##{date.strftime('%Y-%m-%d')}\n\n")
        for link in sorted(linkList, key = lambda x : x.text):
            out.write(f"* [{link.text}]({link.url})")
            if link.descr:
                out.write(f": {link.descr}\n")
            else:
                out.write("\n")
        out.write("\n\n")

links_by_category = defaultdict(list)
for link in links:
    for tag in link.tagStr:
        links_by_category[tag].append(link)

with open("markdown/links_by_category.markdown", "w") as out:
    preamble = "#Links by Category\n"
    out.write(preamble)
    out.write("\n")
    letters = sorted(list({k[0].upper() for k in links_by_category.keys()}))
    for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if l in letters:
            out.write(f"[{l}](#{l}) ")
        else:
            out.write(f"{l} ")
    out.write("\n")
    letter_idx = -1
    for key in sorted(links_by_category.keys()):
        out.write(f"\n##{key}")
        if letter_idx <= 0 or key[0].upper() != letters[letter_idx]:
            letter_idx += 1
            out.write(" {#"+letters[letter_idx]+"}\n")
        else:
            out.write("\n")
        for link in sorted(links_by_category[key]):
            if link.descr:
                out.write(f"* [{link.text}]({link.url}): {link.descr}\n")
            else:
                out.write(f"* [{link.text}]({link.url})\n")
