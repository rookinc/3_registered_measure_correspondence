# Contextual multiplexing 016

## Result

Give each Bell setting context

    00
    01
    10
    11

its own complete registration state.

The global register is

    S_00 x S_01 x S_10 x S_11.

When context c occurs, advance only S_c.

Transitions belonging to different contexts therefore commute.

For any global schedule, if context c has occurred

    m_c

times, its state is exactly the same as the standalone c registrar after
m_c steps.

Hence every receipt cell obeys

    |N_ab^c - m_c w_ab^c| < 1

and

    |N_ab^c/m_c - w_ab^c| < 1/m_c.

This is independent of how the four contexts are interleaved.

If every context is sampled infinitely often, every conditional receipt table
converges to its Program-02 algebraic table.

The conditional local marginals converge to one half.

The context correlations obey

    |Ehat_c-Gamma_c| < 2/m_c.

Therefore the frozen CHSH statistic obeys

    |Shat-S|
      <
    2(1/m00 + 1/m01 + 1/m10 + 1/m11)

and converges to

    1 + 3/sqrt(5).

## Critical boundary

This is a joint contextual registration theorem.

The setting pair (x,y) selects which joint registrar advances.

This does not assign preexisting local answers

    A0,A1,B0,B1.

It also does not yet prove that Alice's individual output is generated using
only x or that Bob's individual output is generated using only y.

No spacelike-local outcome-generation theorem is claimed.

The next gate is therefore causal/operational realization, not statistical
multiplexing.
