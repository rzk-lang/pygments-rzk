# Rzk syntax highlighting in MkDocs

A path-algebra example, highlighted by
[`pygments-rzk`](https://github.com/rzk-lang/pygments-rzk):

```rzk
#lang rzk-1

#section path-algebra

#variable A : U
#variables x y z : A

-- Paths are symmetric, so we can reverse x =_A y to y =_A x.
#define rev uses (A x y)
  (p : x = y)       -- A path from x to y in A.
  : y = x           -- The reversal will be defined by path induction on p.
  := idJ(A, x, \y' p' -> y' = x, refl, y, p)

-- Path composition (concatenation) by induction on the second path.
#define concat
  (p : x = y)       -- A path from x to y in A.
  (q : y = z)       -- A path from y to z in A.
  : (x = z)         -- The concatenated path x = y = z.
  := idJ(A, y, \z' q' -> (x = z'), p, z, q)

#end path-algebra
```
