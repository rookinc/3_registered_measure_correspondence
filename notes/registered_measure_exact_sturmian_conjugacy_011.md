# Exact Sturmian conjugacy 011

## Result

The two Program-03 frequency witnesses define exactly the same infinite
binary history.

The Fibonacci fixed word satisfies

    p_k = floor(k phi^2)

for the position of its kth B.

Under

    A -> 1
    B -> 10,

the kth B contributes the kth zero at

    z_k = p_k + k
        = floor(k(phi^2+1)).

Let

    mu    = (5+sqrt(5))/10
    alpha = 1-mu
          = (5-sqrt(5))/10.

Then

    phi^2+1 = 1/alpha,

so

    z_k = floor(k/alpha).

For the phase-aligned mechanical word,

    x_n = floor((n+1)mu)-floor(n mu).

Its zero indicator is

    1-x_n
      =
    floor((n+1)alpha)-floor(n alpha),

whose kth zero occurs at the same position

    floor(k/alpha).

Therefore the zero sets coincide for every k, and the binary histories are
identical for all time.

## Consequence

There is now one correspondence-history candidate with two exact coordinate
descriptions:

    Fibonacci substitution + finite morphism

and

    irrational rotation + carry receipt.

The remaining problem is native provenance of this single Sturmian history.
