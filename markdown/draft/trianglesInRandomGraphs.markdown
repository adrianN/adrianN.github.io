Suppose we construct a graph on \\(n\\) vertices by including every edge with some probability \\(p:=p(n)\\). Clearly, if \\(p\\) is too small, say \\(n\^{-3}\\), there won't be any edges at all with high probability. How large do we have to choose \\(p\\) until the first triangle appears with high probability as \\(n\\) grows large?

The First Moment Method
-----------------------

It is not difficult to compute the expected number of triangles in our graph. There are \\(\\left(n \\atop 3\\right)\\) triples of nodes that can possibly form a triangle, and for each the necessary edges are present with probability \\(p\^3\\). Hence we have
\\[
\\mathbb{E}[\\triangle] = \\left(n \\atop 3\\right) p\^3 = \\Theta(n\^3)p\^3,
\\]
where we implicitly defined \\(\\triangle = \\sum Y\_{u,v,w}\\) with \\(Y\_{u,v,w} = 1\\) if the three nodes form a triangle.

What does the expectation tell us about the probability that there exists at least one triangle? We know by Markov's inequality 
\\[
\\text{Pr}[X\\geq 1] \\leq \\mathbb{E}(X),
\\]
for non-negative random variables. Hence if the expected number of triangles tends to zero, there will be no triangles asymptotically almost surely (a.a.s), i.e. the probability goes to 1 as \\(n\\) goes to infinity. According to our above calculations this happens for \\(p=o(n\^{-1})\\).

This line of probabilistic argument is often called the *First Moment Method*, because it relies on calculation the expectation -- the first moment -- of a random variable.

Can we use the same argument to show that there are triangles for \\(p=\\omega(n\^{-1})\\)? Unfortunately Markov isn't strong enough for that. Consider for example the random variable \\(X\\) with \\(\\text{Pr}[X=0]=1-n\^{-1}\\) and \\(\\text{Pr}[X=n\^2] = n\^{-1}\\). Its expectation tends to infinity, but it is zero a.a.s.!

The Second Moment Method
------------------------

Intuitively the number of triangles shouldn't be as badly behaved as the above \\(X\\). We can check this intuition by calculating the variance -- the second moment. By an application of Chebychev's inequality we can then bound the probability that there are no triangles. If a random variable \\(X\\) is zero, we have \\(|X-\\mathbb{E}[X]|=\\mathbb{E}[X]\\) and hence by Chebychev
\\[
 \\text{Pr}[X=0] \\leq \\text{Pr}(|X-\\mathbb{E}[X]|=\\mathbb{E}[X]) \\leq \\text{Pr}(|X-\\mathbb{E}[X]|\\geq \\mathbb{E}[X]) \\leq \\frac{\\text{Var}[X]}{\\mathbb{E}[X]\^2}.
\\]
 
Typically the variance is much harder to calculate than the expectation, because it is not linear. This is also true in our case, but it is still manageable. The trick is not to simplify too early.
\\[
\\begin{align\*}
  \\text{Var}[\\triangle] &= \\mathbb{E}[\\triangle\^2] - (\\mathbb{E}[\\triangle])\^2 \\\\
    &= \\mathbb{E}\\left[\\left(\\sum\_{u,v,w} Y\_{uvw}\\right)\^2\\right] - \\left(\\sum\_{u,v,w} \\mathbb{E}[Y\_{uvw}]\\right)\^2 \\\\
    &= \\mathbb{E}\\left[\\sum\_{(u,v,w),(x,y,z)} Y\_{uvw}Y\_{xyz}\\right] - \\sum\_{(u,v,w),(x,y,z)} \\mathbb{E}[Y\_{uvw}]\\mathbb{E}[Y\_{xyz}] \\\\
    &= \\sum\_{(u,v,w),(x,y,z)} \\mathbb{E}[Y\_{uvw}Y\_{xyz}] - \\mathbb{E}[Y\_{uvw}]\\mathbb{E}[Y\_{xyz}].
\\end{align\*}
\\]
Note how we didn't plug in the value for \\(\\mathbb{E}[\\triangle]\^2\\), even though we know it. This allows us to put \\(\\mathbb{E}[Y\_{uvw}Y\_{xyz}] - \\mathbb{E}[Y\_{uvw}]\\mathbb{E}[Y\_{xyz}]\\) under a big sum. These terms cancel if the variables are independent. Of course this isn't always the case: if we know that \\(a,b,c\\) form a triangle, this makes it more likely \\(a,b,d\\) also forms a triangle. The probability that both \\(a,b,c\\) and \\(a,b,d\\) form a triangle is \\(p\^5\\) because five edges must be present. Of course for some terms of the sum \\((u,v,w) = (x,y,z)\\). As these are the only terms that don't cancel, the sum simplifies to
\\[
\\begin{align\*}
  \\text{Var}[\\triangle] &= \\sum\_{u,v,w}  \\mathbb{E}[Y\_{uvw}] - \\mathbb{E}[Y\_{uvw}]\^2 + \\sum\_{(u,v,w),(u,v,x)} \\mathbb{E}[Y\_{uvw}Y\_{uvx}] - \\mathbb{E}[Y\_{uvw}]\\mathbb{E}[Y\_{uvx}] \\\\
    &= \\sum\_{u,v,w} p\^3-p\^6 + \\sum\_{(u,v,w),(u,v,x)} p\^5-p\^6 \\\\
    &= \\left({n \\atop 3}\\right) (p\^3-p\^6) + \\left({n \\atop 4}\\right) (p\^5-p\^6) = \\Theta(n\^4) (p\^5-p\^6)
\\end{align\*}
\\]

Now you can easily verify yourself that indeed for \\(p=\\omega(n\^{-1})\\) there will be triangles asymptotically almost surely.

Thresholds
----------

As we've seen triangles appear at a pretty sharp boundary for \\(p\\). By having a closer look at the variance you can see that we won't have just one or two triangles for slightly larger \\(p\\), but in fact there will be lots. We say the number of triangles exhibits a *threshold behaviour*. This is a surprisingly common phenomenon is many random processes. For example in random graphs the appearance of any fixed size subgraph, the size of the largest component, \\(k\\)-connectivity etc. all have such a threshold. In many cases this also holds if you change the random graph model, for example to preferential attachment graphs, that supposedly better model real world networks like the web graph.

Closely related to the connectivity of random graphs is the process that determines at which temperature your marmalade changes from liquid to semi-solid, i.e. the temperature where gelatine strands become long enough to stabilise the mixture. This is studied under the term percolation theory. The Wikipedia article on [percolation thresholds](http://en.wikipedia.org/wiki/Percolation_threshold) has some pretty pictures.
