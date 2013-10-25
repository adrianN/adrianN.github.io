![Who are these people?](http://2.bp.blogspot.com/-oeJ9uuHN0Jg/Tpl5q1qLeEI/AAAAAAAAAAw/mFjrC7qLH1k/s1600/teaparty.jpg "Art by Arthur Rackham")

As a computer scientist, I am of course highly familiar with the local party scene. Regular party-goers will probably have noticed that there are at least two kinds of parties: those where large cliques of people that know each other form and those where everybody knows the host but nobody else.

Clearly the host can influence which type of party he creates by inviting a clever combination of people. Is it possible to avoid creating either type of party, that is, can a host invite people such that there is neither a large group of mutual friends nor a large group of mutual strangers?

<!--more-->

A lemma on edge colourings
--------------------------

We can model the party as an edge-coloured complete graph. The vertices are the guests and an edge is red if they know each other and blue otherwise. Then the problem can be reformulated as

> Is it possible to colour the edges of the complete graph \\(K\_n\\) with red and blue such that there is no monochromatic clique of size \\(k\\)?

Intuitively it gets harder to avoid monochromatic cliques as the graph becomes larger. For example it is not difficult to show that it is possible to avoid a monochromatic triangle in a \\(K\_5\\) (by colouring it like [this](http://upload.wikimedia.org/wikipedia/commons/9/98/RamseyTheory_K5_no_mono_K3.svg)), however we are forced to create a triangle in a \\(K_6\\). It is of course possible to show this by enumerating all possible edge colourings, but that takes [rather long](http://upload.wikimedia.org/wikipedia/commons/e/ef/Friends_strangers_graph.gif). A more elegant proof goes like this:

Fix an arbitrary vertex \\(v\_1\\). It has five incident edges, at least three of which must have the same colour, say red. Let \\(v\_i,v\_j,v\_k\\) be the other endpoints of the red edges. If any of the edges \\(\\{v\_i,v\_j\\}\\), \\(\\{v\_i,v\_k\\}\\), \\(\\{v\_j,v\_k\\}\\) is red, we obtain a red triangle with \\(v\_1\\). Otherwise \\(v\_i,v\_j,v\_k\\) form a blue triangle.

An upper bound
--------------

The example from the last section provides strong evidence that our intuition is correct and it is indeed not possible to avoid monochromatic cliques if the party becomes too large. Let's try to find an upper bound on the required size. The idea is to construct the graph by glueing together smaller graphs in which a (slightly smaller) monochromatic clique must exist. This shows that a finite number of guests suffices to force a clique and from the proof we can then deduce an upper bound.

To make this easier, we do a slight generalisation and allow different sizes for the cliques, depending on their colour. We want to avoid red cliques of size \\(k\\) and blue cliques of size \\(\\ell\\).

We show by induction over \\(k+\ell\\) that there is an integer \\(P(k,\ell)\\) such that at any party with \\(P(k,\ell)\\) people, at least \\(k\\) know each other, or \\(\ell\\) do not know each other. Due to the example in the last section, we can set \\(P(k,\ell)=6\\) for \\(k+\ell\leq 3\\).

For the induction step, assume that \\(P(k-1,\ell)\\) and \\(P(k,\ell-1)\\) exist. We will prove the claim for \\(P(k,\ell) := P(k-1,\ell)+P(k,\ell-1)\\). Consider an arbitrary coloring of the complete graph on \\(P(k,\ell)\\) vertices. Fix a vertex \\(v\\), and let \\(R\\) and \\(B\\) be the sets of vertices that are connected to \\(v\\) via a red, respectively blue, edge. Clearly, \\(P(k,\ell) = |R|+|B|+1\\).

By the definition of \\(R\\), \\(B\\), and \\(P(k,\ell)\\), either \\(|B| \geq P(k, \ell-1)\\) or \\(|R| \geq P(k-1, \ell)\\) (as otherwise \\(|R|+|B|\leq P(k,\ell)-2\\), a contradiction). W.l.o.g. let \\(|B|\geq P(k,\ell-1)\\). If the subgraph induced by the vertices of \\(B\\) contains a red clique of size \\(k\\) we are done, otherwise by the induction hypothesis this graph must contain a blue clique of size \\(\ell-1\\), which together with \\(v\\) forms a blue clique of size \\(\ell\\). 

Let \\(R(k,\ell)\\) be the minimal number of vertices such that the graph contains either a monochromatic \\(K\_k\\)$ or a monochromatic \\(K\_\ell\\). It is not hard to see that the above inductive argument gives  an upper bound for \\(R(k,\ell)\\) of about \\(2\^{k+\ell}\\) (using \\(P(k,\ell)=8=2^3\\) for \\(k+\ell\leq 3\\) as the induction base). For the symmetric case \\(k=\ell\\) this gives \\(R(k,k)\leq 4^k\\); this is best known up to subexponential terms (as far as I know).

A lower bound
-------------

The upper bound of \\(4^k\\) that we derived in the last section is ridiculously huge. For \\(k=3\\) we know that the true value is 6, yet our bound gives us 64! Maybe we should try deriving a lower bound.

For a lower bound we must show that for graphs of size less than some \\(n_0\\) we can colour the edges without creating monochromatic cliques of size \\(k\\). It is completely unclear how to find such a colouring without enumerating them all.

Before we start thinking too hard, let's try a random colouring. Maybe we're lucky. 

What's the probability that the edges of a \\(k\\)-clique all have the same colour? There are \\(\\left(k \\atop 2\\right)\\) edges and only two of the possible colourings are forbidden, so the probability to get a bad colouring is only
\\[
	2\^{1-\\left(k \\atop 2\\right)}.
\\]
There are \\(\\left(n \\atop k\\right)\\) possible subgraphs of size \\(k\\) and hence by a union bound the probability that there is one that isn't properly coloured is
\\[
	\\frac{\\left(n \\atop k\\right)}{2\^{\\left(k \\atop 2\\right)-1}}.
\\]
Clearly, if \\(n\\) is small enough such that this fraction is smaller than 1, with positive probability no forbidden subgraph exists. But that implies the existence of a good colouring. 

We can use the simple approximation \\(\\left(n \\atop k\\right) \leq n\^k\\) to conclude that for \\(n\leq 2\^{k/2}\\) the corresponding graph can be colouring without a monochromatic clique of size \\(k\\). Again this bound is the best known, up to subexponential terms.

Remarks
-------

The questions we considered in this post fall under the category of [Ramsey theory](http://en.wikipedia.org/wiki/Ramsey_theory). There are many similar questions one can ask about order in sufficiently large structures. However, in most cases it is very difficult to give exact values or even to prove tight bounds.

The minimal size of a graph such that it must contain a monochromatic clique is called the Ramsey number. It doesn't seem too difficult to find an exact value, at least for smallish \\(k\\). After all we just need to try all colourings. However very little is known about the Ramsey numbers, mainly because nobody knows a significantly more clever way to compute them than to try out all colourings and there are way too many. Already \\(R(5)\\) is unknown, and it is very unlikely that we'll ever find out \\(R(6)\\). The Wikipedia has this nice quote by Joel Spencer on the topic:

> Erdős asks us to imagine an alien force, vastly more powerful than us, landing on Earth and demanding the value of R(5) or they will destroy our planet. In that case, he claims, we should marshal all our computers and all our mathematicians and attempt to find the value. But suppose, instead, that they ask for R(6). In that case, he believes, we should attempt to destroy the aliens.

Given that we know \\(102 \leq R(6) \leq 165\\), I would first let Bruce Willis or Will Smith guess before I launch my nukes.
