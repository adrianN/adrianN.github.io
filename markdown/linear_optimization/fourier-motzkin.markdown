% Solving Linear Programs 
% Adrian Neumann (adrian_neumann@gmx.de)

Recall from the introduction that a linear program is defined by a linear objective function $f(x) = c_1x_1+c_2x_2+\ldots+c_nx_n$ and a set of constraints $a_{i1}x_1+a_{i2}x2+a_{in}x_n \le b_i$ for $1\le i\le m$. For reasons that will become clear in a few paragraphs (and even clearer in the next part of this series), I will write the variables as a column vector $\vec x=(x_1,\ldots, x_n)^\text{T}$, where I use the superscript $T$ to indicate transposition so that I can write column vectors in the rows of this text.

When we treat the variables as a vector like this, it makes sense to call the number of variables the *dimension* of the LP. I will call vectors that satisfy all constraints *feasible*. If there is no such vector, the problem is *infeasible*.

### Solving 1D Linear Programs by combining constraints

Solving 1-dimensional LPs is trivial. We have just one variable $x$. The cost function either becomes bigger as $x$ increases or smaller, so we immediately now whether we're looking for the biggest $x$ that satisfies the constraints or the smallest. The set of feasible $x$ is then the intersection of the rays defined be the constraints. For example

$$\begin{aligned}
\min & 3x \\
\text{s.t.} & x\ge 3 \\
	& x\ge 5 \\
	& x\le 7
\end{aligned}$$

The constant before the $x$ in the cost function is positive, so in order to minimize the objective value we need to minimize $x$. The constraints can be simplified to $7 \ge x \ge 5 \ge 3 \rightarrow x\in [5,7]$ and thus the optimal value is $x=5$.

### Solving 2D Linear Programs by Eye-Balling

In two dimensions we can use a very similar strategy. The cost function still tells us in which direction to move $\vec x$ and the intersection of the constraints gives us a feasible region. We use a graphical approach to see the set of feasible values for $x$. 

The constraints define halfplanes in the 2D space. If you write an equals sign instead of $\le$ (or $\ge$), you get an equation for a line. The inequality is valid for all points on one side of the line. Which side depends on the weights on the left side (more precisely, on the direction defined by the vector $\vec a=(a_{i1},\ldots,a_{in})$) and whether it's a $\le$ or a $\ge$. The feasible region of the problem, i.e. all the points that satisfy all constraints, is then the intersection of all the halfplanes.

The cost function defines a line parameterized by $\vec x$ (i.e. the line with cost $f(x)$). If $x$ lies within the feasible region we get a feasible
solution. The cost vector $c$ is orthogonal to the line defined by $f$. The goal is to shift the line as far in negative $c$
direction as possible without leaving the feasible region. Take for example the following LP

![Fig:graphSolutionEx An example for a graphical solution of an LP.
The optimal solution is (3,2)](./images/graphSolutionEx.png "Fig:graphSolutionEx")

$$\begin{aligned}
\min & x+y\\
s.t. &2x+y\geq 8\\
	 &2x+3y\geq 12\end{aligned}$$

The cost vector is $c=(1,1)$ and the two constraints define two half-planes. For every value $z$ of the cost function, we have a line $x+y=z$. See figure
[Fig:graphSolutionEx]. We want to find the smallest value of $z$ such that $(x,y)$ is a feasible solution. So we start with some arbitrary $(x,y)$ in the feasible region (picking it is the eye-balling step) and then gradually move it in $-c$ direction (i.e. we subtract small multiples of $c$). Once we find that we can't move our solution any further without leaving the feasible region, we have reached the optimum.

A somewhat weaker operation than picking a feasible *solution* to LP is picking an objective value $z$ and finding out whether this objective value can be achieved.

To do so, we can add a new constraint, namely $f(x) \le z$. This constraint adds another half-plane that constraints the feasible region. If this makes the feasible region empty, there is no solution with at objective value at most $z$. If the feasible region still contains more than one point, then we can decrease $z$ a little more. We have reached the optimal $z$ if the feasible region contains only one point. Now, if we had a method to check whether a feasible region is empty or not, this would give us an algorithm to solve linear programs with $O(\log (z_{\text{opt}}))$ many evaluations of the feasibility algorithm.

### Fourier-Motzkin Elimination

Now that we know how to solve 1D LPs rigorously and 2D LPs with a graphical method, let us try to find a method that works for arbitrary dimensions. As we already can solve low-dimensional LPs, it makes sense to try and get there via dimensionality reduction.

Fourier-Motzkin elimination is a method to reduce the dimension of an LP by one without changing feasibility. If we keep reducing the dimension one by one, we eventually reach the 1D case, where we can test feasibility easily. The objective value is disregarded by this method, we only care about feasibility. By adding an additional constraint as described above we can transform the optimization problem to a feasibility problem. In an exercise you will show how to reconstruct an optimal solution.

The method works by rearranging the constraints to solve for one variable and then introducing enough new constraints to make the variable unnecessary. As an example we will use this 2D LP.

$$
\begin{aligned}
\text{max} & y \\
\text{s.t.} &  2x + 7y &\le 28 \\
            &  4x - 2y  &\ge 20 \\
            &  x   + y  & \ge 6\\
            &          y  &\ge 0
\end{aligned}            
$$

**Exercise**: Draw the feasible region for this LP.

We want to eliminate $y$. So first we rearrange all constraints to have just $y$ on the left side. We get

$$\begin{aligned}
y & \le  4 - 2x/7\\
y &\le -10 + 2x\\
y &\ge 6 - x\\
y &\ge 0
\end{aligned}$$

Now we can combine the constraints where $y\le \ldots$ with the constraints where $y\ge \ldots$. As we have two of each, we get four constraints.

$$
\begin{aligned}
4 - 2x/7 &\ge y \ge 6 - x \\
4 - 2x/7 &\ge y \ge 0\\
-10 + 2x &\ge y \ge 6 - x \\
-10 + 2x &\ge y \ge 0
\end{aligned}
$$

We can simplify to 

$$  5x/7 \ge 2  \quad 2x/7 \le 4 \quad 3x \ge 16  \quad 2x \ge 10 $$

which further simplifies to

$$  x \ge 14/5 \quad x \le 14 \quad x \ge 16/3 \quad x \ge 5 $$

and lastly

$$   \max(14/5,16/3,5) \le x \le \min(14). $$

If you did the exercise above correctly, you will see that projecting the feasible region down to the $x$ axis leaves you with the interval $5\le x \le 14$. Note that the simplification we did to the constraints after eliminating $y$ was in fact the procedure to eliminate $x$. A 0-dimensional LP has no variables, just a bunch of inequalities involving numbers and the feasibility check is just some calculation.

**Exercise**: Instead of $y$, eliminate $x$. Does your result match your picture?

In general Fourier-Motzkin elimination works as follows:

1. Pick a variable $y$ to eliminate.
2. Rearrange all constraints to have only $y$ on the left side. You get three kinds on inequalities:
    1. Inequalities that don't contain $y$
    2. Inequalities that bound $y$ from above.
    3. Inequalities that bound $y$ from below.
3. Keep type 1 inequalities.
4. For each type 2 inequality, take all type 3 inequalities and write down the combined inequality.

**Exercise**: Use Fourier-Motzkin Elimination to find not just the optimal objective value, but also the optimal solution.

Let's try to prove that Fourier-Motzkin Elimination is correct, that is, it reduces the dimension by one, without changing satisfiability. Let us first define the projection of a set of vectors. Since we can choose the order of our variables without changing the problem, it suffices to deal with the case where we drop the last coordinate of each vector.

**Definition** Let $\vec x = (x_1, \ldots, x_n)$ be a vector. Then $\pi(\vec x) = (x_1,\ldots,x_{n-1})$ is the projection of $x$ on the first $n-1$ coordinates. For a set of vectors $S$, let $\pi(S) = \{\pi(x) | x \in S \}$ be the set where we apply $\pi$ on every element.

It is easy to see that for any non-empty set $S$, $\pi(S)$ is also non-empty. So if $S$ is the feasible set of our linear program, projecting it down doesn't change feasibility. So far so good. Unfortunately we don't have the feasible region given as a point set, it's given by the inequalities. Hence we need to use Fourier Motzkin elimination instead of just dropping a coordinate. Next we will show that Fourier Motzkin elimination indeed computes the projection.

**Proof** Let $S$ be the feasible region of our LP, and let $Q$ be the feasible region of the LP after we remove the last variable $x_n$ via Fourier Motzkin Elimination. We show $Q=\pi(S)$. We do so by proving mutual inclusion, that is $\pi(x)\in Q \Rightarrow \pi(x) \in \pi(S)$ and $\pi(x) \in \pi(S) \Rightarrow \pi(x) \in \pi(Q)$

1. $\pi(x) \in \pi(S) \Rightarrow \pi(x) \in Q$. That means we
    have a point $\pi(x)$ in $\pi(S)$ and we want to find a
    $\pi(x)$ in $Q$ that corresponds to it. In $S$ the vector
    $x$ has another component, so let us write in a slight abuse of notation
    $x = (\pi(x),x_n)$. We don’t know $x_n$ (and there are in general many $x\in S$ that get mapped to $\pi(x)$) but we
    know that it had to satisfy the constraints. 

    There are three kinds of constraints in our LP after we rearrange the inequalities to have $x_n$ only on the left hand side, as explained above. Type 1 constraints don't contain $x_n$ and hence have no influence on $x_n$, so if $x$ satisfies them $\pi(x)$ also satisfies them. For type 2 and type 3 inequalities, we know that there is an $x_n$ that satisfies *all* of them.

    We constructed $Q$ by combining type 2 and type 3 constraints. Let $T_2$ be the r.h.s. of the tightest type 2 constraint, that is, the constraint where the right hand side evaluates to the smallest number when we plug in $\pi(x) = x_1,\ldots,x_{n-1}$, and similarly let $T_3$ be the r.h.s. of the tightest type 3 constraint. Note that then $T_3 \le T_2$ is the tightest constraint for $\pi(x)$ that we have in $Q$. Since $x_n$ satisfies all constraints, we know $T_3 \le x_n \le T_2$ and hence $T_3 \le T_2$. Thus $\pi(x)$ satisfies the constraints for $Q$ and hence $\pi(x) \in Q$.

2. $\pi(x)\in Q \Rightarrow \pi(x) \in \pi(S)$. For this direction also we have to choose $x_n$ so that $x=(\pi(x),x_n)$ satisfies the constraints for $S$. As in the other direction let $T_2$ be the r.h.s. of the tightest type 2 constraint, and let $T_3$ be the r.h.s. of the tightest type 3 constraint. Then we can simply choose any $x_n \in [T_3, T_2]$. This interval can't be empty, because we have the constraint $T_3 \le T_2$ in our constraint set for $Q$ and $\pi(x)$ satisfies all of those constraints.

And this concludes our proof.

So with Fourier Motzkin elimination we have a method of checking feasibility for Linear Programs: Eliminate dimensions until no variables remain and do the math to see whether each inequality is satisfied. Together with your method for transforming optimization to repeated feasibility, we can now solve Linear Programming. Unfortunately Fourier Motzkin Elimination gets pretty expensive for large dimensions as you'll see in the next exercise.

**Exercise** What's the runtime of an $n$-step Fourier Motzkin Elimination? Hint: How many constraints do you introduce in each step?

Next part coming soon  
[Click here to go back to the index](../linear_optimization.html)