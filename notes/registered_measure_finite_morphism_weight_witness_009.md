# Finite morphism weight witness 009

## Result

Use the finite substitution

    A -> AB
    B -> A

and the fixed binary receipt morphism

    A -> 1
    B -> 10.

No probabilities appear.

No irrational constants appear.

No algebraic fractional state is stored.

If the source frequencies are

    f_A = (sqrt(5)-1)/2
    f_B = (3-sqrt(5))/2,

then output one-frequency is

    (f_A+f_B)/(f_A+2f_B)
      =
    (5+sqrt(5))/10,

and output zero-frequency is

    f_B/(f_A+2f_B)
      =
    (5-sqrt(5))/10.

These are exactly the native spectral class masses from Audit005.

## Structural point

This gives a second correspondence mechanism class:

    finite substitution
      -> growing history
      -> finite variable-length receipt morphism
      -> irrational limiting frequency.

It does not require an explicit Q(sqrt5) fractional residual register.

The morphism has output lengths

    1
    2,

which is suggestive in light of the already-native receipt cycle-doubling
theorem.

## Boundary

The Fibonacci substitution is not yet native.

The morphism A->1, B->10 is not yet native.

The resemblance to cycle doubling is not a proof.

This remains a target-informed finite-rule witness.

## Next gate

Test whether native receipt dynamics already contain:

    a two-class transition matrix conjugate to [[1,1],[1,0]]

and

    a one-versus-two receipt expansion.

If yes, the frequency bridge may close without any continuous algebraic
phase register.
