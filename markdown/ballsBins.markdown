One Rule to Distribute them All
===============================

![Share... the load](pictures/sam.jpg "Copyright probably with New Line Cinema")

Suppose you are a poor orkish messenger and have $n$ rings to distribute to the $n$ elven-kings under the sky. Of course each is supposed to get their own, but you're lazy and the nasty elves all look the same anyway.

Due to your extensive experience with ~~chaos~~ randomization you quickly see that throwing rings at elves randomly is in expectation just as good. The number of rings for each elf is distributed as $\mbox{Bin}(n,1/n)$, so the expectation is one. You might also know that binomial random variables are pretty strongly concentrated around their expectation and you don't think the dependencies between the elves will change anything about that. 

Your boss however would like some more arguments why your approach is good enough. Let's try to compute the maximum number of rings any elf will get.

The knowledgeable reader probably recognizes this as a classical balls-into-bins settings with all the immediate applications to scheduling, hashing, and so forth. From here I will use the more standard nomenclature.

<!--more-->

Counting Bins
-------------

This seems like a difficult problem to tackle, but it turns out we can use the first moment method[^1] on appropriately defined random variables.

As it is so often the case, 'appropriately' defining things gets you half way to a solution. The first moment method allows us to show that a random variable will be zero asymptotically almost surely. In our application we want to show that there will be no bins with a large number of balls, so let's define $X\_k$ to count the number of bins who have $k$ or more rings. 

As we already observed the number of balls is binomially distributed, so it is not so difficult to bound the probability that a bin contains more than $k$. To make things easier, we will use the Poisson approximation[^2] and cheat a little with the constant factors involved.
$$\mbox{Pr}(\mbox{elf has }\geq k \mbox{ rings})= \mbox{Pr}(\mbox{Bin}(n,1/n)\geq k) \leq n \mbox{Pr}(\mbox{Pois}(1) = k) =n e^{-1} \cdot \frac{1}{k!}\approx ne^{-1} \cdot 2^{-k \log k} \approx e^{\log n - k \log k}$$

We used Stirling to approximate $k! \approx 2^{k\log k}$. By defining an indicator for every bin we see that the expectation is just $\mathbb{E}(X\_k) \leq e^{2\log n - k \log k}$. Clearly this expectation goes to zero for 
$$
k \geq \frac{c\log n}{\log \log n}
$$
for some suitable $c$, depending on the exact values of the constants in the exponent.

Remarks
-------

Our sloppy calculations show that the number of bins with more than $O(\log n/\log \log n)$ balls is zero a.a.s., and hence the maximum load is sublogarithmic with high probability. The interested reader might want to show, using a variance calculation, that this bound is tight. Not bad for such a simple algorithm! If you're feeling adventurous, you can try the exercise at the end of this blog post to see how much a simple twist can improve the algorithm. Perhaps I'll write a bit about that in a different post.

You might be a little disappointed at how slowly the expectation goes to zero, but rest assured that this is just a symptom of our weak tools. After all we used nothing more advanced than Markov's inequality! It is entirely possible (and indeed a common textbook example) to derive much stronger bounds by applying Chernoff-type bounds on a series of appropriately conditioned Poisson random variables, see for example chapter 5 of the excellent book [Probability and Computing](http://books.google.com/books/about/Probability\_and\_computing.html?id=0bAYl6d7hvkC) by Mitzenmacher and Upfal.

Exercise
--------

Intuitively you could do a little better by distributing the rings in rounds. In each round you pick two elves and give a ring to the elf who currently has fewer. Can you still compute the maximum number of rings a single elf will get?

[^1]: Recently discussed in relation to [triangles in random graphs](http://zufallstee.blogspot.com/2011/10/triangles-in-random-graphs.html).
[^2]: I told you the Poisson distribution is useful [in this post](http://zufallstee.blogspot.com/2011/10/poisson-distribution.html)