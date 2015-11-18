% Software Archeology
% Adrian Neumann (adrian_neumann@gmx.de)
% 2015-11-15

So, you work in a *[mature programming environment](http://lambda-the-ultimate.org/node/4424)* and your boss gave you the job of figuring out how an important piece of code in your company's infrastructure works. Unfortunately, the tool is about a million lines of poorly documented legacy code. What documentation you can find seems outdated. There are few tests.

In this post I will share some techniques that I found helpful in the daunting task of software archeology.

Where to Start
--------------

The first thing you should do is trying to build the software and check that it runs OK. This might be as easy as `make`, but depending on your luck you might have to hunt for the requisite dependencies in exactly the right versions and define magic environment variables to make everything work. If you have a working system somewhere, but can't get it to work on your machine, it is worthwhile to examine the binary there. You might want to check [which libraries it's linked against](http://superuser.com/questions/239590/find-libraries-a-binary-was-linked-against).

Once you have a working copy, you can start understanding the code. When faced with a huge occult code base, it's often difficult to find a spot from where to start understanding it. 

If you're looking at a runnable program, starting from its entry point is a good way. Finding that entry point might be difficult if you have multiple `main` methods. Try examining the build scripts to see which of the alternatives is used. You could also try putting `assert(false)` in the code to see which `main` is actually called.

For a library, this task is more difficult. I suggest looking at users of that library to get an idea what parts are most important. You can also try finding which functions are exported, but probably that's a huge list.

If your project is under version control, you can try finding files that are modified often. These tend to contain some crucial functionality.

Getting Around
--------------

You found a starting point and begin your archeological journey into the great unknown. If you use a sane build system and not some bundle of hand written Perl scripts, you can try generating a project file for some full featured IDE. Modern IDEs are really good at jumping around the code and telling you from where a function is used.

If that's not possible, or you don't like IDEs very much, there are a number of other tools that can be helpful. You probably already know `grep`. With some knowledge of regular expressions you can quickly get an overview of your codebase, I recommend reading its manpage. There are faster alternatives to `grep` available, like [The Silver Searcher](https://github.com/ggreer/the_silver_searcher). Unfortunately, regular expressions only get you so far.

However, there are some neat tools that actually understand your programming language. I've so far only investigated C and C++, so my advice here is somewhat limited. There are tools like `ctags` that produce an index of function and variable declarations/definitions and integrate nicely in your text editor of choice. I also found the copy-paste-detector from [PMD](http://pmd.github.io/) to be very useful.

For an overview of some of these tools (again with a strong C bias), see

* [Navigating Linux Source Code](http://www.drdobbs.com/navigating-linux-source-code/184401358)
* [Greg's source code navigation tools](http://www.lemis.com/grog/software/source-code-navigation.php) (note the Unix Beard Of Authority on the author, his advice must be really good!)
* [What tool do you use to index C/C++ code?](http://stackoverflow.com/questions/100143/what-tool-do-you-use-to-index-c-c-code)

Draw Maps
---------

It's important that you document your findings. Remember, it's only science if you write things down.

I recommend adding comments to the code where necessary (but [don't overdo it](http://stackoverflow.com/questions/143429/whats-the-least-useful-comment-youve-ever-seen)) and writing structural insights down in a wiki. Try to create a consistent narrative for a particular use case from system startup to shutdown. This provides a skeleton that you can then flesh out as you investigate other parts of the code.

Sometimes, UML diagrams can be useful. I think simpler is better, so I would recommend a simple tool like [ArgoUML](http://argouml.tigris.org/) or even [VioletUML](http://alexdp.free.fr/violetumleditor/page.php) over Enterprise Architect or the like. Something like [Inkscape](https://inkscape.org/) can also work. In my opinion, UML is best if used very informally. [All the UML you need to know](http://www.cs.bsu.edu/homepages/pvg/misc/uml/) provides a succint overview of class diagrams. Some UML tools can automatically analyze your codebase and draw diagrams for you. I've yet to see a nontrivial code base where this is helpful, but I wouldn't consider myself particularly experienced.

Write Tests
-----------

Usually, legacy code is poorly tested. Writing tests serve two purposes. First it helps you understand what's going on by giving you a possibility to test your assumptions. This alone is a good reason to write some tests as you dwelve into the code. Another important benefit is that tests allow you to refactor some code and being reasonably sure that you didn't break other parts of your [Big Ball Of Mud](http://joeyoder.com/PDFs/mud.pdf). That is of course only useful if your pointy haired boss gives you time to do any refactoring. You company probably already has a test framework of choice. Otherwise googling will reveal a number of nice unit testing frameworks for your language. As always, avoid rolling your own if possible.

Related Links
-------------

As usual, I'm not the first person to write about this. Here are some other resources that I found interesting

* [Code Spelunking](http://queue.acm.org/detail.cfm?id=945136)
* [Software Archeology](http://media.pragprog.com/articles/mar_02_archeology.pdf)
* [An Empirical Approach to Software Archeology](http://herraiz.org/papers/english/icsm05short.pdf)