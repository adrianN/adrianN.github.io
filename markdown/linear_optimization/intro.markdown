% Introduction
% Adrian Neumann (adrian_neumann@gmx.de)

Although it's called "Programming", Linear Programming has little to do with what you'd call programming today. The term dates back to a time where programming had more to with filling out tables than writing code.

Let me first hit you with the formal definition. In Linear Programming we have a number of real variables $x_1, \ldots, x_n$, and some linear value function $f(x_1, \ldots, x_n)$ we want to maximize (or minimize). The interesting part is the set of constraints on the variables we need to satisfy (otherwise optimizing $f$ would be trivial). The constraints are a set of $m$ linear inequalities 

$$a_{j1}x_1 + \ldots + a_{jn} x_n \leq b_j \qquad a_{ij},b_i \in \mbox{R}$$

for $1\leq j\leq m$.

Now this likely seems difficult to you and you can't see any obvious applications. Good. This way you can feel very smart once you understand it. Let's proceed with an examples.

In the Diet Problem we want to find a cheap diet, say for the military. [This is one of the original applications of Linear Programming.](http://www.jstor.org/stable/25061369) and dates back to the first half of the twentieth century.

Let's introduce a mathematical model of a diet. We have $i$ types of food and each foodstuff has $m$ different features, e.g. calories, price, different vitamins, etc. A diet, that is, a solution to our problem, consists of $x_i$ (kilograms) of food $i$ (say per month). The $x_i$ are the variables we want to find.

We want to optimize the price of our diet, so our objective function is the sum of the amount of food $i$, $x_i$, times the cost, cost($i$), for $i=1,\ldots, n$. This is a linear function, because we don't multiply two or more variables with each other. The cost of food $i$ is not a variable, it's just a number.

The cheapest diet is a starvation diet where you don't eat anything, but of course we want a diet that is cheap and nutritious, so we need to constrain our solution. To do so we can introduce a number of constraints. Things like 

* our diet must have at least 2000 calories a day
* our diet must have at least the recommended amount of each vitamin
* our diet must have at most the safe amount of salt

As you can easily see these are all linear constraints, since for example the calories of each food in our diet simply add up. Since we have a linear cost function and a set of linear constraints, our model is in the form of a linear program. Using a piece of software called an LP solver we can find an optimal solution, that is a diet that is as cheap as possible while not violating any of our nutritiousness constraints. I will later explain how these programs work.

One has to be somewhat careful in designing these constraints, otherwise the solutions one gets can be amusingly impractical. The article I linked at the beginning contains a funny anecdote about this.

Note that we implicitly assumed that we can have any real number as the amount of food we eat. This is bad because we might get a solution where we have to eat negative amounts of some food (Too many calories in your diet? Just try this one trick and eat negative amounts of butter!). We can fix this with additional constraints $x_i \ge 0$. Another problem is that some foods are not easily divided into small parts. It's hard to eat 0.213kg of bananas a day without wasting some bananas. We'd like to have integer values for some of the $x_i$. This can not be expressed with additional linear constraints[^1] and you'll see later on that imposing integrality constraints on our solution makes the problem a lot harder. 

But note that dropping some constraints, notably integrality constraints, can only improve the cost of the optimal solution. So a solution with fractional variables can be used as a lower bound for the optimal cost. This is an extremely useful insight if you want to prove bounds on the quality of some approximation algorithm you just came up with. Fractional solutions can also be a good start for finding true solution to your problem, for example by rounding.

Solving a fractional LP and then rounding is often an easy way to get an approximate solution to a problem that is hard to solve exactly. But of course it's not the only way. The field of approximation algorithms tries to find approximate solutions, typically for NP-complete problems. It also contains hardness results. Some problems are not only hard to solve exactly, they're *also* hard to approximately solve. This is interesting because it gives us a more nuanced view of the difficulty of hard problems. The typical CS undergraduate will stop after a NP-completeness proof, because NP-complete problems are a) all hard and b) all about the same, after all once you can solve one, you can solve them all. Approximation theory reveals a whole world of nuance between different NP-complete problems.

Let's see an example of a simple approximation algorithm.

Suppose we have $n$ jobs that take times $w_1 \ldots w_n$ to complete and two machines that can work of them. We want to assign the jobs to the machines such that the total running time is minimized. This problem is NP-complete (reduction e.g. Knapsack). Let's try a heuristic solution and see how good it performs. The natural approach is assigning the first job to the first machine and then assigning the $i+1$-th job to the machines that has less work among the first $i$ jobs. Note that this algorithm doesn't need to know all the jobs before hand, it can handle jobs as they come in. This is sometimes a very desirable property of an algorithm. Algorithms of this kind are called *online algorithms*.

How does a schedule such computed compare to the optimal schedule that might use arbitrarily clever algorithms and advance knowledge of all jobs? Every sensible algorithm is at least within a factor of two of the optimal schedule. Since we only have two machines we can’t do more than two units of work concurrently. The heuristic I described above is however better. It takes at most $3/2$ the time of an optimal schedule. We say it's a $3/2$ approximation.

The proof is easy: Let $w_{max}$ be the size of the maximal job and let $W$ be the total amount of work we have to do. No schedule can be faster than $w_{max}$. Hence the time $\mbox{opt}$ an optimal schedule takes can be bounded as $\mbox{opt} \geq \max (w_{max}, W/2)$. Consider the situation before the last job is assigned. The size of the already assigned jobs is $W-w_n$ so the less loaded machine (wlog 2) has a load at most $(W-w_n)/2$. Assuming machine 2 determines the total length, the algorithm produces a schedule of length

$$\frac{(W-w_n)}{2} + w_n \leq W/2+w_n/2 \leq \mbox{opt} + \mbox{opt}/2$$

Click here to proceed to the next part, the Simplex Method (coming soon)  
[Click here to go back to the index](../linear_optimization.html)



[^1]: unless P=NP, I guess...
