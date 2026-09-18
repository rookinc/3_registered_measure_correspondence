# Bounded residual frequency witness 006

## Result

Audit005 supplies the canonical algebraic class measure

    mu = (5+sqrt(5))/10.

Use the deterministic residual rule

    r_0 = 0

and on each registered attempt

    t = r_n + mu.

If

    t >= 1,

emit a favored receipt and retain

    r_(n+1) = t - 1.

Otherwise emit an unfavored receipt and retain

    r_(n+1) = t.

Exactly,

    N_fav(n) = floor(n mu)

and

    r_n = n mu - floor(n mu).

Therefore

    0 <= r_n < 1

and

    |N_fav(n)/n - mu| < 1/n.

Hence the registered frequency converges exactly to the imported algebraic
measure.

No stochastic transition probability is used.

No random input is used.

## Binary split

Toggle one parity bit inside each correlation class.

Then the two favored subreceipts differ in count by at most one, as do the
two unfavored subreceipts.

Their limiting frequencies are

    mu/2
      =
    1/4 + sqrt(5)/20

and

    (1-mu)/2
      =
    1/4 - sqrt(5)/20.

These are exactly the Program-02 nontrivial binary algebraic weights.

## Structural meaning

The bridge requires only

    addition
      -> boundary crossing
      -> integer receipt
      -> retained residual.

The rule is finitely specified.

The residual remains bounded.

Because mu is irrational, the exact residual orbit is infinite and the
receipt history is not eventually periodic.

## Boundary

This is a correspondence mechanism witness.

It does not yet prove that native Thalean registration implements this
accumulator.

It does not derive local spacelike outcome production.

It does not assume the Born rule.

## Next gate

Ask whether native registered mechanics already contains:

    additive accumulation
    normalized closure boundary
    integer receipt emission
    retained bounded residual.

If those primitives are already native, bind them to the Audit005 algebraic
measure rather than introducing a new frequency law.
