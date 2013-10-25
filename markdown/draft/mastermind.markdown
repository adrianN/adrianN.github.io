![The classic game](http://2.bp.blogspot.com/-Puv_X8hqLis/TqHCdRGJz6I/AAAAAAAAAA8/Fl6nYPDZHs4/s1600/mastermind_owlpacino_scaled.jpg" "Picture BY-ND by Flickr user owlpacino")

We already considered a [guessing game](http://zufallstee.blogspot.com/2011/09/guessing-games-art-by-arthur-rackham.html) on this blog, in which Alice asks queries of the form "is the number in this set" and receives yes/no answers.

In this post, we will play a restricted version of the popular game Mastermind. In Mastermind Carole thinks of a secret string of four coloured pins. Alice can query strings and learns the number of matching pins (differentiated between the pins that are correct and in the correct position and the pins that are merely contained in the secret string).

Mastermind has been extensively studied in combinatorics. Already in '77 Knuth showed that Alice can always win in at most 5 moves. Here we want to find asymptotics for the game when Carole chooses a string of length \\(n\\).

To make things easier for our calculation, we will restrict the game to binary strings. Also, Alice only learns the Hamming distance (that is the number of differences) between her string and Carole's string. Alice is computationally unbounded, the only important metric is the number of queries she needs to guess Carole's string.

The naive algorithm is testing each bit of Carole's string sequentially, by querying strings of the form `0000`, `1000`, `0100`, etc. This takes \\(n\\) queries for bitstrings of length \\(n\\) -- essentially we do a binary search for Carole's string. However the algorithm doesn't seem to be very efficient, it appears that Mastermind is easier than the yes/no game. After all we get much more information with each query.

Can we find Carole's string with less than \\(n\\) queries?

<!-- more -->

It turns out that it *is* possible to gather enough information quickly. Disappointingly the strategy is not very useful if we take the computation time into account that Alice needs to produce the secret string.

#### A Randomized Strategy

In Knuth's algorithm, Alice always queries the string that eliminates the largest number of possible secret strings. This is straightforward to implement by using a brute force approach (we're com&shy;pu&shy;ta&shy;tionally un&shy;bound&shy;ed), however the analysis becomes tricky.

Luckily Alice has a very simple randomized strategy that succeeds with high probability. Without thinking she queries random strings and stores the string and its Hamming distance to the secret string. Intuitively a random string is not much worse at eliminating possible solutions than the optimal string.

We have collected enough information when there is only one possible solution left. Let the the secret string be \\(s\\), and let the query string be \\(q\\). Let us try to find the probability that a fixed impostor-string \\(i\\) is not excluded by querying \\(q\\), i.&nbsp;e. \\(s\\) and \\(i\\) have the same Hamming distance from \\(q\\).

![The same distance](http://4.bp.blogspot.com/-Kchx9EeOuNI/TqKCjhR1AJI/AAAAAAAAABI/IX3glZqN_c0/s1600/mastermind.png)

Suppose \\(s\\) and \\(i\\) differ in \\(d\\) positions. How many query strings are there that don't discern between the two? For \\(q\\) to have the same distance from both, only the positions matter where \\(s\\) and \\(i\\) disagree -- where they agree the bits of \\(q\\) contribute the same thing to the Hamming distance. So \\(n-d\\) positions of \\(q\\) are completely arbitrary. In the remaining positions we need to make sure half the bits agree with \\(s\\) and the other half agrees with \\(i\\). Clearly this is only possible if \\(d\\) is even. Already after the first query we've excluded all impostors that have an odd distance from \\(s\\). Pretty neat. 

For even \\(d\\) we get
\\[\\text{Pr}[i \\text{ survives}] = \\frac{\\left({{d}\\atop{d/2}}\\right) \\cdot 2\^{n-d}}{2\^{n}} = \\left({{d}\\atop{d/2}}\\right) \\cdot 2\^{-d}.\\]
Using Stirling's approximation on the factorials it is straightforward to show that this is essentially
\\[\\sqrt{\\frac{2}{\\pi d}}.\\]

We want to show that after a sufficiently large number of samples \\(t\\), the probability that there is an impostor string left tends to zero. By a simple union bound it suffices to show
\\[ \\sum\_d \\left({{n}\\atop{d}}\\right) \\cdot \\left(\\frac{2}{\\pi d}\\right)\^{t/2} \\rightarrow 0.\\]

Let's try to bound the individual summands. We do a case distinction. First consider the case where \\(d \\leq n/(\\log n)\^3\\). By Stirling's formula we can bound 
\\[\\left({{n}\\atop{d}}\\right) \\leq \\left(\\frac{en}{d}\\right)\^d,\\]
and thus the summands are no larger than
\\[2\^{t/2\cdot (2d/t \\cdot \\log (en/d)- \\log(\\pi d/2))}.\\]
By plugging in the extreme values, 2 and \\(n/(\\log n)\^3\\), for \\(d\\) and setting \\(t\geq 4n/\\log n\\) we get
\\[2d/t\\cdot \\log (en/d) - \\log (\\pi d/2) \\leq \\frac{1}{2(\\log n)\^2} \\log (en/2) - \\log \pi \\leq -3/2,\\]
for sufficiently large \\(n\\) and thus the exponent can be bounded from above by \\(-3t/4\\).

Hopefully we can also derive such a bound in the case where \\(n/(\\log n)\^3 \\leq d \\leq n\\). In this case we bound the binomial coefficient rather crudely by \\(2\^n\\). Then the summands are not larger than
\\[2\^{t/2\\cdot (2n/t - \\log (\\pi d/2))}.\\]
Bounding \\(\\pi d/2\\) by \\(n/(\\log n)\^3\\) and setting \\(t\geq 4n/\\log n\\) we get
\\begin{align\*}
\\frac{2n}{t} - \\log {\\pi d}{2} & \\leq \\frac{\\log n}{2} - \\log (n/(\\log n)\^3) \\
& = \\frac{\\log n}{2} - \\log n + 3 \\log \\log n \\
& = 3 \\log \\log n - \\frac{\\log n}{2}.
\\end{align\*}
Again this is smaller than \\(-3/2\\) for sufficiently large \\(n\\) and we can bound the summands by \\(2\^{-3t/4}\\) in this case too.

Now we can easily bound the whole sum for \\(t\\geq 4n/\\log n\\)
\\begin{align\*}
\\sum\_{d} \\left({{n}\\atop{d}}\\right) \\cdot \\left(\\frac{2}{\\pi d}\\right)\^{t/2} &\\leq \\sum\_d 2\^{-3t/4} \\
& = n2\^{-3t/4},\\
\\end{align*}
and this goes to zero rather quickly.

Hence a sublinear number of queries suffices to narrow down the solution space to a single candidate. An information theoretic argument shows that this is optimal. We get \\(\\log n\\) bits in every query and the secret string has \\(n\\) bits, proof by handwave.

#### Remarks

We've shown that after \\(O(n/\\log n)\\) queries we've collected enough information to exclude all but one possible solutions. We can then find the remaining solution by brute force. Unfortunately we can't improve much on that method: Checking whether there is a valid solution given \\(k\\) queries and answers is [NP-complete](http://arxiv.org/abs/cs.CC/0512049).

Optimizing functions (like the Hamming distance from a fixed string) using only the answers from an oracle is studied under the name "Blackbox Complexity". The applications are mainly in the analysis of evolutionary and genetic algorithms. In theory algorithms base their decisions solely on the evaluation of a problem specific fitness function. Blackbox complexity tries to prove lower and upper bounds or the running time of these algorithms for different function classes. Currently only very simple functions are tractable mathematically.

The analysis of Mastermind I presented here is from a [FOGA '11 paper by Doerr et al.](http://arxiv.org/abs/1012.0952) A slightly different take on the problem that some might find easier to follow can be found in Anil and Wiegand "Black-box Search by Elimination of Fitness Functions".