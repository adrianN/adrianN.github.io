% Linear Programs and Polyhedra 
% Adrian Neumann (adrian_neumann@gmx.de)

In the previous section we saw how the feasible region of a linear program is constructed as the intersection of a number of halfplanes, one for each constraint. Using this insight we developed a graphical approach for solving 2D LPs. Together with Fourier-Motzkin elimination as a means for reducing the dimensionality of an LP, this gave us a general method for solving linear programs.

Unfortunately Fourier-Motzkin produces a rather large number of constraints, so it is unsuited for solving problems with many variables. 

In this section I will talk more about the properties of the feasible region. With more knowledge about the feasible region, we'll eventually be able to understand a very popular method for solving linear programs, the Simplex Method.

Let us start by introducing some notation and some terms. 

Already in the last part we started writing the variables $x_1,\ldots, x_n$ as a column vector $\vec x$ and the constants $a_{ij}$ as a row vector $\vec a_i$. We did the same with the cost function, writing the weights for each variable as a row vector $\vec c$. This way we could use the dot product instead of writing sums explicitly. 

$$ \vec a_i \cdot \vec x = a_{i1}x_1+\ldots+a_{in}x_n$$

The constraints can be written using a matrix vector product. We write the $a_{ji}$ in a matrix $A$ like so

$$
A=\left(\begin{aligned}
a_{11} & a_{12} & \ldots & a_{1n}\\
a_{21} & \ldots \\
\vdots & \\
a_{m1} & \ldots & & a_{mn} \end{aligned}\right)
$$

Note that the rows of $A$ are simply the vectors $\vec a_i$.

Now we can write the constraints simply as $Ax\le b$, where $b$ is a column vector of the $b_j$. Summarizing we get the general form of a linear program:

$$\begin{aligned}
\text{minimize:}& \vec c \cdot \vec x \\
\text{subject to:} & A \cdot \vec x \le \vec b\end{aligned}$$

Note that it really doesn't matter whether we use $\le$ or $\ge$. Just multiplying by $-1$ switches a constraint around without changing it.

<div class="block">**Def** A *polyhedron* is a set in $\text{R}^n$ whose
members obey a set of linear inequalities

$$\{x\in \text{R}^n | Ax \geq b\} \qquad A\in \text{R}^{m\times n},\ b\in \text{R}^m$$

If the region is bounded (i.e. it has a finite volume) it can also be
called *polytope*. We say $n$ is the *dimensionality* of the polyhedron.
</div>

I already used the word *halfspace* without giving a formal definition. Let us remedy this.

<div class="block">**Def** Let $a,x\in \text{R}^n$, $a\neq 0$.

1.  $\{x|ax=b\}$ is a *hyperplane* (a line in 2D)
2.  $\{x|ax\geq b\}$ is a *halfspace* (halfplane in 2D)
</div>

With this definition we can say that a polyhedron is an
intersection of a bunch of halfspaces.

### Corners of Polyhedra

A corner of a $n$-dimensional polyhedron is, intuitively, a point where $n$ edges meet. I will give a bunch of different definitions and them prove them to be equal.

The simplest definition uses a line. A corner of a polyhedron is a point $p$ in the polyhedron where we can find a line that touches the polyhedron only at $p$.

<div class="block">**Def** Let $P$ be a polyhedron. A vector $x\in P$ is a
*vertex* of P if $\exists \vec c\in \text{R}^n$ s.t. $cx < cy$ for all 
$y\in P, y \neq x$; that is, $x$ is the minimal point for some cost
vector $c$ (the unique optimal solution for some LP with the feasible set
P). See figure [Fig:vertex]

![[Fig:vertex] A vertex $x$ is the optimal solution for a cost vector
$c$](./images/vertex.png "Fig:vertex")
</div>

Corners are interesting for optimization because the converse is also kind of true, at least for bounded polyhedra. For any cost vector $c$, we can find a vertex $x$ of the (bounded) polyhedron such that $cx \le cy$ for all points $y$ in the polyhedron. There is no strict inequality here because the line defined by $c$ might be parallel to one of the edges of the polyhedron. If the polyhedron is not bounded, there are some $c$ such that for any point $y$ there is a point $y'$ such that $cy' < cy$, that is, the optimal value for this cost vector is unbounded. These are of course the cost vectors that define a line that doesn't leave the polyhedron. 

However, we need some more definitions and theorems before we can prove the above statement.


<div class="block">**Def**  An *extreme point* of a polyhedron P
is a vector $x\in P$ s.t. $x$ is not a convex combination of any two
distinct vectors $y,z\in P$ different from $x$.
</div>

Convex combinations of two points $x,y$ are all points $z$ for which the equation $\lambda x + (1-\lambda) y = z$ has a solution for $\lambda$ in $[0,1]$. Geometrically, the points $z$ lie on a line between $x$ and $y$. You can also take the convex combinations of more than two points. The principle is the same though, you add all the points, scaling each one with a non-negative scaling factor $\lambda_i$. The combination is convex if the $\lambda_i$ sum to 1. 

Example: In 2D we can always select the two adjacent corners of a point
$x$ on the edge of $P$ if and only if $x$ is not a corner. Then $x$ will be on the
line between the two corners.

<div class="block">**Def** Let $P$ be a polyhedron that
is defined by some linear inequalities $a_i$: $P=\{x|a_ix\geq b_i\}$.
We’ll say that the $i$-th constraint is *active* at a point $x$ if we
have equality: $a_ix = b_i$
</div>

The constraints define the edges of polyhedron. If a point is on an
edge that constraint is active. Intuitively the point must be a corner if it
lies on the intersection of $n$ edges.

<div class="block"> **Def** Let $P\in \text{R}^n$ be a polyhedron in
standard form and let $x^{*}\in \text{R}^n$. The vector $x^{*}$ is a *basic
solution* if at $x^*$ all equality constraints are active and there are $n$ active constraints that are linearly independent. See
solution $A$ in figure [Fig:bsfVSbs] for an example of a basic solution. If a basic solution is also feasible, we call it a *basic feasible solution* (b.f.s.). See the point $B$ in figure [Fig:bsfVSbs] for an example of
a basic feasible solution.

![[Fig:bsfVSbs] Some LP. Solution $A$ is a basic solution. Solution $B$ is a basic
feasible solution.](./images/basicVsBasicFeasible.png "Fig:bsfVSbs")
</div>

A polyhedron with fever than $n$ constraints never has a basic solution.

Now we want to prove that the three definitions are all equivalent to each other.

<div class="block"> **Theorem** Let $P$ be a polyhedron and $x\in P$. The following
statements are equivalent

1.  $x$ is a vertex
2.  $x$ is an extreme point
3.  $x$ is a basic feasible solution
</div>

<div class="block">
**Proof**

We show 1.) $\Rightarrow$ 2.) $\Rightarrow$ 3.) $\Rightarrow$ 1.).

-   $x$ is a vertex $\Rightarrow$ $x$ is an extreme point: Proof by contraposition. 

    Assume the existence of $y,z \in P$ both different from $x$ such that $x$ is a linear combination of $y$ and $z$, i.e. $x= \lambda y + (1-\lambda )z$. Since $x$ is a linear combination of two vectors, it's not an extreme point. We show that it is also not a vertex.

    From the definition of vertex we know that some cost vector $c$ should exist such that $c x < c w$, for all $w\in P$, that is $x$ is optimal w.r.t. $c$. Together with the assumption $x= \lambda y + (1-\lambda )z$ this leads to a contradiction.

    $$\begin{aligned}
    cx &= \lambda cy +(1-\lambda)cz\\
       &> \lambda cx + (1-\lambda)cx = cx && \text{since }cx< cy, cx< cz\\\end{aligned}$$

-   extreme point $\Rightarrow$ bsf. Proof by contraposition.

    Suppose $x$ is not a basic feasible solution. Then $x$ is either not feasible, or not a basic solution. If it's not feasible, then it can't be an extreme point. Hence we can assume $x\in P$ and it's not a basic solution.

    Let $B$ be a matrix of active constraints at $x$ and $C$ the matrix of the inactive constraints such that $Bx=d$, $Cx>f$. Since $x$ is not a bfs the matrix $B$ doesn't have full rank and hence its kernel is nonempty. So we can find some vector in the kernel:

    $$\exists \delta \in \text{R}^n, \delta \neq 0:\ B\delta =0$$

    With $\delta$ we define two vectors:

    $$y=x-\epsilon \delta \quad z = x+\epsilon \delta$$

    Note that $x=(z+y)/2$. That means that $x$ is not an extreme point
    if $z,y \in P$, because $x$ is a convex combination of the two.
    Consider

    $$Bz = B(x+\epsilon \delta) = Bx + \epsilon B\delta = Bx$$

    Since $B\delta = 0$ the active constraints are still active. For the
    inactive constraints we have some slack before we leave the
    polyhedron. If we choose $\epsilon$ small enough we’re still
    within. It suffices to choose $\epsilon$ such that

    $$\forall i: \epsilon |c_i z| < c_i x - f_i\qquad \vec c_i\in C,\ f_i \in \vec f$$

    That is, we make epsilon small enough such that we don't violate the tightest of the constraints in $C$. 

    Hence $z$ (and analogous $y$) are still in the polyhedron and $x$ is
    not an extreme point.

-   bfs $\Rightarrow$ vertex: Suppose $x$ is a bfs. We construct a cost
    vector for which $b$ is the unique optimal solution.

    Let $B$ be the matrix of active constraints s.t. $Bx=b$. Let $c$ be the sum of the $n$ rows of $B$. We know the objective value for $x$ w.r.t. $c$. It’s $c x = \sum b_i$.

    Because $B$ has rank $n$, $x$ is the unique solution to $Bx=b$. For all $y\in P$ that are different from $x$, $By > b$, hence $x$ is the optimal point for the cost vector $c$. Therefore $x$ is a vertex.
</div>

### The shape of polyhedra

So far we've shown that the extreme points of a polyhedron, i.e. its corners, are also vertices, that is, optimal solutions for *some* cost vector. However, we want to be able to say that for *every* cost vector we can find an optimal solution that is also an extreme point.

In this section we'll learn that polyhedra are so called *convex sets* and, for bounded polyhedra, every point inside the set can be expressed as a linear combination of the extreme points. Recall that a vector $x$ is a linear combinations of some vectors $y_1,\ldots, y_n$ if you can find constants $\lambda_1,\ldots, \lambda_n$ such that $x=\sum_i \lambda_i y_i$, or in vector notation $x=\lambda \cdot y$.

<div class="block"> **Def** A subset $S\subseteq R^n$ is called *convex* if for any to points $x,y\in S$ the line connecting $x$ and $y$ is also in $S$. That is

$$\forall \lambda \in [0,1], \forall x,y\in S: \lambda x + (1-\lambda)y \in S$$
</div>

<div class="block"> **Theorem** Polyhedra are convex sets.
</div>

<div class="block"> **Proof** This follows directly from the definition. Recall that we defined a polyhedron as the set of points 

$$\{x\in \text{R}^n | Ax \geq b\}$$

for some matrix A. Since matrix multiplication is linear we have for some $y_1,y_2$ from $P$ that

$$A\cdot (\lambda y_1 + (1-\lambda) y_2) \ge \lambda b + (1-\lambda) b = b$$
</div>

Note that the notion of convex combination can be extended to sets of more than two points trivially. It is a simple exercise to show that this doesn't change what it means to be a convex set. I will just use it.

<div class="block">**Def** The *convex hull* of a set of vectors $X=x_1,\ldots, x_n$ is the set

$$\text{CH}(X)=\bigcup_{\sum \lambda_i=1} \left\{\sum_{i=1}^n \lambda_i x_i\right\}$$

That is, the convex hull is the union of all convex combinations that can be formed from the vectors in $X$.
</div>

Intuitively the convex hull is the set you get by spanning a tight rubber band around the vectors of $X$.

We come to the central result of this section. The next theorem shows that the extreme points of a polyhedron span the whole polyhedron. This is what allows us to only look at the extreme points when looking for an optimal solution to a LP.

<div class="block">**Theorem** Let $P$ be a non-empty bounded polyhedron and let $E$ be the set of extreme points of $P$. Then $P = \text{CH}(E)$
</div>

<div class="block">**Proof**  We show both directions. First we show $\text{CH}(E) \subseteq P$. This direction is particularly easy. We already showed that polyhedra are convex sets, hence any convex combination of points from $P$ still lies in $P$.

Now we show the other direction $P \subseteq \text{CH}(E)$. To do so we show that an arbitrary point $x\in P$ can be expressed as a convex combination of extreme points. The proof of this is very similar to the proof we gave above that extreme points are basic feasible solutions.

Consider $Ax \ge b$. We rearrange the rows of $A$, $x$, and $b$ such that the first $k$ inequalities are tight. We can decompose $A$ into two matrices $B$ and $C$ such that $A=B+C$ by taking $B$ as the first $k$ rows of $A$ (and fill it with 0) and $C$ as the last $n-k$ rows of $A$ (and fill with 0 from the top).

If the rank of $B$ is $n$, then $x$ is a basic feasible solution (i.e. an extreme point by the theorem above) and we're done. Otherwise we can find some vector $y$ in the kernel of $B$, i.e. $By=0$. Since the equalities defined by $C$ are not tight, we can move $x$ by some $\epsilon_1$ in the $y$ direction without leaving the polyhedron. We chose $\epsilon_1$ such that at least one constraint of $C$ becomes tight for $x=x+\epsilon_1 y$. There also has to be an $\epsilon_2$ that takes us to a boundary in the opposite direction. Let $x_2=x-\epsilon_2 y$.

As in the previous proof $x$ can be expressed as a convex combination of $x_1$ and $x_2$. If $x_1$ and $x_2$ are extreme points, we're done. Otherwise we can repeat the same process for $x_1$ and $x_2$, only this time the rank of $B$ is one greater than before. Eventually we will reach full rank and hence a set of extreme points that can express $x$ as a convex combination.
</div>

Now that we know that every point in the polyhedron can be expressed as a convex combination of extreme points, we can use this fact to show that for *every* const vector $c$ we can find an optimal point that is also an extreme point.

<div class="block">**Corollary** Let $P$ be a non-empty bounded polyhedron. Then the LP $\text{min } cx$ such that $x\in P$ has an optimal solution that is an extreme point.
</div>

<div class="block">**Proof** Let $x^*$ be an optimal solution and let $v=cx$ be the optimal objective value. By the previous theorem we can write $x^*$ as a convex combination of extreme points

$$x^* = \sum \lambda_i y_i.$$

We want to  show that there is a $y_i$ such that $c y_i= c x^*$. We already know that $v=cx^*$ is minimal, so we know that $cy_i\geq v$ for all $i$. Since the $\lambda_i$ must sum to 1, we can conclude that for at least one $y_i$ we actually have $cy_i=v$. Otherwise can can quickly derive the following contradiction:

$$v=c x^* = c\sum \lambda_i y_i > c\sum \lambda_i x^* = \sum \lambda_i cx^* = v\sum \lambda_i = v$$

</div>

Now we have all ingredients for an algorithm. We have shown that for *every* cost vector there is an extreme point that is an optimal solution. Therefore we can find the optimal solution to a LP by enumerating extreme points. We also know that extreme points are basic feasible solutions, that is, points where the matrix of active constraints has full rank. That is, once we found one basic feasible solution we can move to another one by manipulating a matrix -- throwing out one active constraint and replacing it by a different one. This is the basic strategy of the Simplex method, that we'll discuss in the next section.

(The next section is coming when I get around to writing it.)


[Click here to go back to the index](../linear_optimization.html)
