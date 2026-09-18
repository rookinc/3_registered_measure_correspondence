# Native spectral quadratic register 005

## Result

For every binary analyzer pair define

    O = A tensor B.

Because the local observables are reflections,

    O^2 = I.

Therefore

    Q+ = (I+O)/2
    Q- = (I-O)/2

are complete orthogonal projectors.

Using

    Gamma = Tr(P_odd O),

their canonical source weights are

    Tr(P_odd Q+) = (1+Gamma)/2

and

    Tr(P_odd Q-) = (1-Gamma)/2.

Orienting the labels by sign(Gamma) gives

    q_fav   = (1+|Gamma|)/2
    q_unfav = (1-|Gamma|)/2.

For

    |Gamma| = 1/sqrt(5),

these are exactly

    (5+sqrt(5))/10

and

    (5-sqrt(5))/10.

Because

    P_odd = |psi><psi|,

and Q is an orthogonal projector,

    Tr(P_odd Q)
      =
    ||Q psi||^2.

Thus the two masses are intrinsic squared component norms of a complete
orthogonal register.

No cross outcomes are discarded.

No outcome postselection occurs.

## Relation to Audit003

The Fibonacci pair-square witness reproduces these same two masses.

It is therefore a useful finite-rule model of the quadratic structure, but it
is not needed to derive the native masses themselves.

The native quadratic register already exists in the Program-02 operator
algebra.

## Remaining problem

The open correspondence question is now narrower:

    canonical spectral quadratic weight
      ?->
    long-run registered empirical frequency.

That is the next Program-03 gate.
