http://www.flickr.com/photos/dolmansaxlil/4667065009/

In the [last post]() we discussed Cuckoo Hashing as an efficient way to implement dictionaries, that is mappings from keys to values. However, sometimes it is difficult to find hash functions for your keys that are both efficiently computable and provide a "random" distribution over their values.

For this reason the C++ Standard Template Library doesn't use hashing for their map implementation but provides a map that just assumes an order on the keys. The map is then implemented using balanced trees. This way we need logarithmic time for all operations with less strong assumptions about our keys. In fact, if push comes to shove all object can be ordered according to their position in memory.

Keeping trees balanced is a rather tricky business, as everyone who tried implementing their own [Red-Black Trees]() knows. Once again we can find a simpler method that uses randomization.

<--more-->

Skip lists, introduced  are conceptually very easy. We start with an ordered linked lists of elements. Now we extend the list to two dimensions. For every element we start flipping a coin. As long as the coin comes up heads we copy the element to the next level. This way we build a tower of copies above every element. Every copy has four links: One to the copies on the next higher, respectively lower level and one to its predecessor and successor on its own level. Note that every level still is an ordered linked list.

Finding an element in this two dimensional structure is not hard. We start at the topmost layer and go right until the next element is too large, then we go downwards. Once we're at the lowest level we either encounter the element as we go right, or it is not contained in the skip list.

Once we can find elements it is of course possible to insert new elements too. Just find the right position in the lowest list and start building the random tower, updating all links on the higher levels too.

This is already everything that you need to know to implement your own version of skip lists.

####Analysis

As usual the randomization shifts the difficulty from the implementation to the analysis side. In this post we will analyze skip lists a little more thoroughly than what is usually done in an algorithms class.

#####Memory

#####Time

####Uses

Skip lists are quite popular for implementing ordered sets, priority queues and dictionaries, especially for concurrent applications. The popular key-value store [Redis](http://redis.io) uses skip lists, and there is a skip list implementation in `java.util.concurrent`. Skip lists prove to be more scalable in concurrent settings than alternative data structures[^1]

For those who really like their trees, fear not, randomization can help you too. Seidel et al. introduced randomized search trees[^2] that provide virtually the same performance guarantees.

####References

[^0]: [Skip Lists: A Probabilistic Alternative to Balanced Trees](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.85.9211&rep=rep1&type=pdf) (PDF)
[^1]: [Skiplist-based concurrent priority queues ](http://ieeexplore.ieee.org/xpl/freeabs\_all.jsp?arnumber=845994)
[^2]: [Randomized Search Trees](http://www.google.de/url?sa=t&rct=j&q=randomized+search+trees&source=web&cd=2&ved=0CDIQFjAB&url=http%3A%2F%2Fpeople.ischool.berkeley.edu%2F%257Earagon%2Fpubs%2Frst89.pdf&ei=V5nSTvn6M-\_b4QThrYk\_&usg=AFQjCNG8nooKQXe6-AOq7Ute-cqotaL-gg&cad=rja)