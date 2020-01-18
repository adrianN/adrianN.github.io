% Future Proof Static Websites
% Adrian Neumann (adrian_neumann@gmx.de)

I administer the website for my [Aikido Group](https://takemusu-aikido-berlin.de). As is the nature of websites for small sports clubs, it contains only static content and changes very rarely. Naturally, I used a static site generator, namely Pelican (because I know some Python).
For hosting I use [Nearly Free Speech](https://www.nearlyfreespeech.net/) because they provide exactly what I need for about thirty cents a month. All logging is disabled so that I don't have to worry about accidentally storing PII.

Everything worked fine and I got a website.

Now after a year or two where the website remained untouched I wanted to change something. Meanwhile my Python environment changed and Pelican was no longer working. I also had forgotten everything I learned about Pelican when I first set up the site.

As I don't really enjoy fiddling with software that doesn't work, I considered just taking the HTML that Pelican produced the last time it worked and editing it by hand. However, the generated code was too complicated for my very limited HTML skills and I didn't like copying around a lot of stuff to get things like a navigation menu.

The website you're currently on is made with a combination of [Pandoc](https://pandoc.org) and a bit of shell and hosted on Github Pages. This setup works well, but I don't really get a lot of benefit from using Markdown over just using plain HTML. 

So this time I simplified things a little more. All I really need is a bit of help copypasting things like the navigation into all pages. Luckily there is a POSIX tool for that: `m4`. `m4` is a Turing complete macro language that, to my knowledge, is mostly used to generate stuff it `automake`. It's actually very easy to use for simple templating (and, being Turing complete, can also be used for very complex templating).

I only use `m4` to include stuff in the header and the navigation, so for my purposes something even simpler might still work, but I don't know anything that does *just* file inclusion.

Now each page looks like this 

```
<!DOCTYPE html>
<html lang="de">

include(../macros/header)

<body>

include(../macros/nav)

<section id="content">

<p> The actual content </p>

</body>

</html>
```

With a little more `m4` macros this could be reduced to something like 

```
define(`pageContent', `
<p> The actual content </p>
')
include(../macros/page)
```

but I'm comfortable with the current amount of copypasting.

The pages are stored under `pages/pagename.htmlm4` and a script like the following translates them to proper html and puts the result in `html/pagename.html`.

```
#!/bin/bash

pushd .
cd pages
for f in `find . -name "*.htmlm4"`
do
  changeddir="${f/./../html}"
  destination="${changeddir/m4/}"
  echo "${f} -> ${destination}"
  m4 "$f" > "$destination"
done
popd
```

Then I just have to `rsync -vrz --delete html/` to my hoster and I'm done. Since I only depend on `bash`, `rsync` and `m4`, I can be quite confident that I can regenerate the website in the future. And if all else fails, the whole site is simple enough HTML that I can generate it by hand.

The full source of the website is available [on Github](https://github.com/adrianN/takemusu-aikido-berlin.de).
