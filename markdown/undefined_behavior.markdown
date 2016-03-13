% Undefined Behavior in C++
% Adrian Neumann (adrian_neumann@gmx.de)


Type Punning
------------

In a systems language like C++ you often want to interpret a value of type A as a value of type B where A and B are completely unrelated types. This is called *type punning*. 

Take for example the ever popular [Fast Inverse Square Root](https://en.wikipedia.org/wiki/Fast_inverse_square_root). The Wikipedia gives us the following code.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
float Q_rsqrt( float number )
{
    long i;
    float x2, y;
    const float threehalfs = 1.5F;

    x2 = number * 0.5F;
    y  = number;
    i  = * ( long * ) &y;                       // evil floating point bit level hacking
    i  = 0x5f3759df - ( i >> 1 );               // what the fuck? 
    y  = * ( float * ) &i;
    y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration
//  y  = y * ( threehalfs - ( x2 * y * y ) );   // 2nd iteration, this can be removed

    return y;
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We interpret a float value as integer in the "evil floating point bit level hacking" line. Similar type punning often happens when we want to interpret a stream of bytes as some structure. We try to simply cast the `char*` input stream to our structure and use the member elements to read values.

Another common way to do this is via a union.

~~~~~~~~~~~~~~~~~
union U {
    long i;
    float f;
};

U u;
u.f = number;
long number_as_int = u.i;
~~~~~~~~~~~~~~~~~

Unfortunately neither are valid C++.

Casting is invalid because of C++'s [strict aliasing rules](http://en.cppreference.com/w/cpp/language/reinterpret_cast). Basically, you mustn't cast a pointer to a different type and then dereference it (unless you cast to `char*`).

The union trick is also *not valid*, because only one member of a union can be "active". When we set `f` it becomes active and `i` is thus inactive. Reading from an inactive member results in undefined behavior. At least that's how I understand the standard. [The union trick in valid in modern C99 (but not in C89).](https://stackoverflow.com/questions/25664848/unions-and-type-punning)

Instead of this you should use `memcpy` and hope that your compiler knows how to optimize it.

~~~~~~~~~~~~~~~~~~
memcpy(&i, &y, sizeof(long));
~~~~~~~~~~~~~~~~~~

See also:

* [John Regehr on type punning](http://blog.regehr.org/archives/959)