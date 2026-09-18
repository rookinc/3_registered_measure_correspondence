# Finite-rule irrational-frequency witness 002

## Result

Audit pass:

    True

Use the finite deterministic substitution

    A -> AB
    B -> A.

Its integer substitution matrix is

    [1 1]
    [1 0].

No probability or irrational constant appears in the rule.

The matrix has Perron root

    phi = (1+sqrt(5))/2.

Starting from A, the registered history grows without bound.

Its asymptotic symbol frequencies are

    f_A = (sqrt(5)-1)/2

and

    f_B = (3-sqrt(5))/2.

Both are irrational.

## Meaning

Audit 001 excluded deterministic dynamics on a fixed finite global state
space because such dynamics become eventually periodic.

Audit 002 shows the escape:

    finite rule
      !=
    fixed finite global state.

A finite alphabet and finite integer update law can generate an unbounded
registered history carrying an irrational invariant frequency.

## Boundary

This is a mechanism-class witness.

The Fibonacci substitution is not claimed to be native Thalean dynamics.

It does not yet derive the Program-02 EPR weights.

No Born rule or probability transition is inserted.

## Next gate

Test whether the Program-02 sqrt(5) weights can be reconstructed from a
minimal composite of this generated irrational measure and a balanced binary
receipt.

Such a result would be a candidate construction witness, not yet native
provenance.
