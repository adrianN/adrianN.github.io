![Les poisson, les poisson, how I love les poisson](http://3.bp.blogspot.com/-42hFqlHoTIE/ToSJpKL8tmI/AAAAAAAAAAU/A9WRkbhdgHE/s1600/les_poisson.jpg)

At least once a day I open the [Wikipedia article](http://en.wikipedia.org/wiki/Poisson_Distribution) about the Poisson distribution. It has to be the most unintuitive discrete distribution that you *want* to use because of its nice properties. The Wikipedia introduces it as

> The Poisson distribution is a discrete probability distribution that expresses the probability of a given number of events occurring in a fixed interval of time and/or space if these events occur with a known average rate and independently of the time since the last event.

I at least have no idea what that is supposed to mean. A much better introduction, at least for computer scientists who do similar things like me, would be

> The Poisson distribution \\(\\text{Po}(np)\\) is the limit of the Binomial distribution, \\(\\text{B}(n,p)\\), as \\(n\\) goes to infinity, if \\(p\cdot n\\) is reasonably small.

<!--more-->

The motivation to have such a distribution is clear. For binomially distributed \\(X\\) we have
\\[
P(X=k) = \\left({n \\atop k} \\right) p\^k(1-p)\^{n-k},
\\]
and those binomial coefficients are rather cumbersome to handle, especially for large \\(n\\).

Let's see how the binomial distribution behaves as \\(n\\) grows large. We get
\\[
\\begin{align\*}
P(X=k) &= \\left({n \\atop k} \\right) p\^k(1-p)\^{n-k}\\\\
	&= n! / (n-k)!k! p\^k(1-p)\^{n-k}\\\\
	&\\leq  n\^k/k! p\^k e\^{-pn-pk}\\\\
	&\\leq (np)^k e^{-np}/k!,
\\end{align\*}
\\]
where both bounds are pretty good as long as \\(k\\) is not too large, say \\(o(\\sqrt n)\\). As it turns out, for \\(np = \\Theta(1)\\), this is a probability distribution, namely the Poisson distribution. This can be easily verified, if one recalls that
\\[e\^c = \\sum\_{j=0}\^\\infty \\frac{c^j}{j!}.\\]
(I'm not sure that this would not also work for non-constant \\(np\\)). We need to show that the sum over the whole probability space is 1. With the above equation in mind, this is quickly done:
\\[
\\sum\_{k=0}\^\\infty \\frac{c\^ke\^{c}}{k!} = e\^{-c} \\sum\_{k=0}\^\\infty \\frac{c\^k}{k!} = 1.
\\]

I claimed that the one actually wants to work with the Poisson distribution as opposed to the binomial distribution. This is because its probabilities behave much nicer inside sums. Take for example the calculation of the expected value and suppose we don't know that it probably behaves like the binomial distribution and can thus guess \\(\\mathbb{E}(X)=c\\).
\\[
\\begin{align\*}
\\mathbb{E}(X) &= \\sum\_{k=0}\^\\infty kP(X=k)\\\\
	&= \\sum\_{k=0}\^\\infty k\\frac{c\^ke\^{-c}}{k!} \\\\
	&= ce\^{-c} \\sum\_{k=1}\^\\infty \\frac{c\^{k-1}}{(k-1)!}\\\\
	&= ce\^{-c}e\^{c} = c.
\\end{align\*}
\\]
Very easy, as long as one remembers the series for \\(e\^c\\). There are also useful results about the concentration of Poisson distributed variables, similar to the exponential bounds for Binomial variables.

Unfortunately things like \\(P(X\\geq k)\\) or even \\(P(|X-Y| \\geq k)\\) are still tricky. As far as I know it's not even possible to neatly approximate that using integrals -- everything becomes non-analytic and all you get are some functions that are important enough to get their own name, but don't help at all for your problem at hand.