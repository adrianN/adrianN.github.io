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

Note that it really doesn't matter whether we use $\le$ or $\ge$. Just multiplying by $-1$ switches it around.

<div class="block">**Def** A *polyhedron* is a set in $\text{R}^n$ whose
members obey a set of linear inequalities
$$\{x\in \text{R}^n | Ax \geq b\} \qquad A\in \text{R}^{m\times n},\ b\in \text{R}^m$$ If
the region is bounded (i.e. it has a finite volume) it can also be
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

<div class="block">**Def** Let $P$ be a polyhedron. A vector $x\in P$ is a
*vertex* of P if $\exists \vec c\in \text{R}^n$ s.t. $cx < cy$ for all 
$y\in P, y \neq x$; that is, $x$ is the minimal point for some cost
vector $c$ (the unique optimal solution for some LP with the feasible set
P). See figure [Fig:vertex]

![[Fig:vertex] A vertex $x$ is the optimal solution for a cost vector
$c$](./images/vertex.png "Fig:vertex")
</div>

<div class="block">**Def**  An *extreme point* of a polyhedron P
is a vector $x\in P$ s.t. $x$ is not a convex combination of any two
vectors $y,z\in P$ different from $x$.
</div>

Example: In 2D we can always select the two adjacent corners of a point
$x$ on the edge of $P$ if and only if $x$ is not a corner. Then $x$ will be on the
line between the two corners.

<div class="block">**Def** Let $P$ be a polyhedron that
is defined by some linear inequalities $a_i$: $P=\{x|a_ix\geq b_i\}$.
We’ll say that the $i$-th constraint is *active* at a point $x$ if we
have equality: $a_ix = b_i$
</div>

The constraints define the edges of polyhedron. If a point is on an
edge that constraint is active. Intuitively it must be a corner if it
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
