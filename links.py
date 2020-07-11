import sys
from collections import namedtuple
from collections import defaultdict
import subprocess
import re

Link = namedtuple('Link', ['text', 'url', 'tagStr', 'descr', 'date'])

filename = sys.argv[1]
done = subprocess.run(["git", "blame", filename], capture_output=True)
dates = []
date_pattern = re.compile('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
for i,blameline in enumerate(done.stdout.decode('utf-8').split("\n")):
    match = date_pattern.search(blameline)
    if match is not None:
        dates.append(match.group())
    else:
        dates.append(None)

links = []
with open(sys.argv[1],'r') as linkFile:
    def addLink(links,items,dates):
        if items:
            changedate = min(dates[j] for j in lineNumbers)
            print(items, changedate)
            assert(len(items) >= 2)
            while len(items) < 4:
                items.append("")
            items[2] = [x.strip() for x in items[2].split(",")]
            links.append(Link._make(items + [changedate]))

    items = []
    lineNumbers = []
    for i,line in enumerate(linkFile):
        line = line.strip()
        if not line or line == "---":
            addLink(links,items,dates)
            items=[]
            lineNumbers=[]
        else:
            items.append(line)
            lineNumbers.append(i)
    addLink(links,items,dates)
    items=[]
    lineNumbers=[]

with open("markdown/links_list.markdown", "w") as out:
    preamble = "#Links\n"
    out.write(preamble)
    bydate = defaultdict(list)
    for link in links:
        bydate[link.date].append(link)
    for date,linkList in sorted(bydate.items(), reverse=True):
        out.write(f"##{link.date}\n\n")
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
