Counting Subgraphs in Streams
=============================

![](pictures/stream.jpg "CC-BY-NC 'Streaming' by Flickr user Dru!")

Suppose you have a very large graph, for example a protein-protein interaction graph for some complicated synthesis pathway. To draw conclusions from such a wealth of data, it is typically helpful to look for certain patterns, or subgraphs. 

Finding, or indeed even counting, small sized subgraphs in a large graph seems to be a very hard problem: The number of candidate positions against which you need to match your subgraph explodes com&shy;bi&shy;na&shy;to&shy;ri&shy;cal&shy;ly. The situation is even more hopeless if the data doesn't fit into main memory anymore.

To address the problem of working with graphs that don't fit into RAM the streaming model was introduced. Here the algorithm has a very limited amount of storage, say O($\log n$) bits, and the in&shy;put is pre&shy;sent&shy;ed as a stream of edges. The algorithm is only allowed to make a small number of passes over the data.

Only few problems can be solved exactly in this model, but often it is possible to find good approximation algorithms. In this post we will have a look at how to count triangles in the streaming model. Very similar techniques can be used to count arbitrary constant size subgraphs.[^2]

Triangle counting already is a relevant problem in itself. It has applications for example in community detection in graphs. There the clustering coefficient, i.e. how many of a node's neighbours are adjacent to each other (and thus form triangles), plays a central role. Indeed there are several papers [^3] on counting triangles using MapReduce as a way to tackle the large networks we face today. The streaming algorithm I'll present here is a simple alternative to this.

<!-- more -->

The Algorithm
-------------

This algorithm is from a paper by Jowhari and Ghodsi [^1]. It is extremely simple. We need a source of sufficiently independent random bits, say an explicit polynomial generator of degree 12. That is a polynomial $p$ over some sufficiently large field with random coefficients. The random numbers are then $p(1),p(2),\ldots$ and we use their binary representation for a stream of random numbers $b[1],\ldots, b[n]$, with $b[i] \in \{-1,1\}$. Note that we can encode this generator using only a logarithmic number of bits for the coefficients.

As we see the edges $(u,v),(x,y),\ldots$ we sum up $b[u]b[v]$, that is the algorithm computes

$$Z = \sum_{(u,v)\in E} b[u]b[v]$$

The output is then

$$\frac{1}{6} Z^3.$$

That's it. Algorithm over. This might seem too simple to be correct, but it actually works. Observe that we output

$$\frac 16 \sum_{(u,v), (w,x), (y,z) \in E} b[u]b[v]b[w]b[x]b[y]b[z]$$

Since $b[u]^k$ is zero in expectation for odd $k$, only terms with even powers count (in expectation) in this sum.[^4] Hence only if $u=z$, $v=w$, and $x=y$ we count this term. This is exactly true if the three edges form a triangle! Of course we over count, since there are $3*2*1=6$ permutations of the three edges and they all occur in the sum, but we simply divide by six and get the right thing.

Unfortunately this is only true in expectation, the actual value can differ quite a bit. But it is not too difficult to bound the variance of $Z$ and hence get a good estimate of how often we need to run this with fresh random variables to get a good estimate. Have a look at the paper to get the actual numbers. In the streaming model we can simply run these instances in parallel.

In did a few experiments and it seems like the high independence that we require in the analysis is actually not so important for random graphs. My results indicate that a normal linear congruential generator already provides sufficient randomness to get good estimates, so the algorithm is really trivial to implement.


[^1]: Jowhari, Ghodsi: [New Streaming Algorithms for Counting Triangles in Graphs](http://sina.sharif.ac.ir/~ghodsi/papers/jowhari-cocoon2005.pdf)
[^2]: Kane, Mehlhorn, Sauerwald, Sun: [Counting Arbitrary Subgraphs in Data Streams](http://www.mpi-inf.mpg.de/~hsun/SGC12.pdf)
[^3]: Suri, Vassilvitskii: Counting Triangles and the Curse of the Last Reducer,  
      Pagh, Tsourarakis: Colorful triangle counting and a mapreduce implementation
[^4]: If you ask yourself why we can take the expectation of the individual $b[u]$, even though they appear in a product, this is because they are sufficiently independent. For the expectation calculation six-way independent random numbers would be sufficient (there are six terms in the product), but for the variance calculation that I don't show here we need $E(Z)^2$, hence 12-way independence.