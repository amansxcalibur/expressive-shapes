# Morph: Shape-to-Shape Bezier Morphing

This module implements smooth morphing between two `RoundedPolygon` shapes. The core
entry point is `Morph.match()`, which takes two polygons and produces a list of matched
cubic Bezier pairs. These pairs can then be interpolated at any progress `t` (0.0 to 1.0)
via `Morph.as_cubics()` to produce intermediate shapes.

The algorithm is very similar to that of Android's Kotlin `androidx.graphics.shapes.Morph`.

## Key Invariant

All cutting/splitting operations in this pipeline are **subdivisions**, not deformations.
When a cubic Bezier is split at some parameter `t`, the two resulting cubics trace the
**exact same path** as the original. The shapes are geometrically identical before and
after — they just have more pieces. This is what allows the final pair count to exceed
both input shapes' cubic counts while preserving their outlines exactly.

---

## Walkthrough of `match()` with a concrete example

Let's morph an **equilateral triangle** (Shape 1) into a **square** (Shape 2), both centered at origin, roughly unit-sized.

---

### Step 1: Measure the polygons (`measure_polygon`)

Each polygon's cubic segments are measured by **arc length**, and each segment gets a
progress range `[start, end]` normalized to `[0.0, 1.0]`. Progress is purely based on
how far along the perimeter a point is — progress 0.5 means 50% of the way around.

**Shape 1 (Triangle) — `measured1`:**

Assume 3 edges with some rounding cubics at corners. For simplicity, say 6 cubics (each corner has a rounding curve + a straight edge):

```
Cubic 0: corner rounding at A    progress [0.000, 0.050]
Cubic 1: edge A→B                progress [0.050, 0.383]
Cubic 2: corner rounding at B    progress [0.383, 0.433]
Cubic 3: edge B→C                progress [0.433, 0.717]
Cubic 4: corner rounding at C    progress [0.717, 0.767]
Cubic 5: edge C→A                progress [0.767, 1.000]
```

Corner features are assigned a progress value at the **midpoint** of their rounding
cubic's progress range (see `measure_features`). This gives each corner a single
progress value representing "where on the perimeter this corner lives," used for
mapping calculations only — the actual corner cubics are preserved.

```
Corner A: progress = midpoint(0.000, 0.050) = 0.025
Corner B: progress = midpoint(0.383, 0.433) = 0.408
Corner C: progress = midpoint(0.717, 0.767) = 0.742
```

**Shape 2 (Square) — `measured2`:**

8 cubics (4 corner roundings + 4 edges):

```
Cubic 0: corner rounding at P    progress [0.000, 0.040]
Cubic 1: edge P→Q                progress [0.040, 0.290]
Cubic 2: corner rounding at Q    progress [0.290, 0.330]
Cubic 3: edge Q→R                progress [0.330, 0.540]
Cubic 4: corner rounding at R    progress [0.540, 0.580]
Cubic 5: edge R→S                progress [0.580, 0.790]
Cubic 6: corner rounding at S    progress [0.790, 0.830]
Cubic 7: edge S→P                progress [0.830, 1.000]
```

Corner features:

```
Corner P: progress = 0.020
Corner Q: progress = 0.310
Corner R: progress = 0.560
Corner S: progress = 0.810
```

---

### Step 2: Corner-to-corner mapping via `do_mapping`

Only **corner** features are extracted from each shape:

```
corners1 = [A(0.025), B(0.408), C(0.742)]
corners2 = [P(0.020), Q(0.310), R(0.560), S(0.810)]
```

`do_mapping` computes all 3x4 = 12 pairwise **spatial distances** using
`feature_dist_squared`. Each corner's representative point is the midpoint of its
first curve's start and last curve's end (`feature_representative_point`). Cross-concavity
pairs (convex corner vs concave corner) are rejected with `inf` distance.

The remaining candidates are sorted closest-first:

```
Sorted candidates (closest first):
1. (A, P)  dist=0.02    <- closest pair
2. (B, Q)  dist=0.15
3. (C, R)  dist=0.18
4. (C, S)  dist=0.40
5. (B, R)  dist=0.55
6. (A, Q)  dist=0.70
...etc
```

`MappingHelper.add_mapping` is called for each candidate in order. It greedily inserts
pairs while enforcing three constraints:
- **No reuse:** each feature can only be mapped once
- **No crowding:** pairs whose progress values are too close to existing anchors are rejected
- **No crossings:** new pairs must not violate the circular ordering of existing pairs
  (i.e., the mapping must be monotonic around the perimeter)

Result:

```
mapping_pairs = [(0.025, 0.020), (0.408, 0.310), (0.742, 0.560)]
```

Meaning: Triangle corner A <-> Square corner P, B <-> Q, C <-> R. Square corner S is
unmatched — that's fine, 3 pairs is enough to define the mapping.

---

### Step 3: Build `DoubleMapper` and compute `poly2_cut_point`

```python
double_mapper = DoubleMapper((0.025, 0.020), (0.408, 0.310), (0.742, 0.560))
```

The `DoubleMapper` creates a **piecewise-linear circular mapping** between the two
shapes' progress spaces. The corner pairs serve as anchor points; everything between
them is linearly interpolated. It can map in both directions:
- `map(x)`: Shape 1 progress -> Shape 2 progress
- `map_back(x)`: Shape 2 progress -> Shape 1 progress

Three segments (wrapping around):

```
Segment 0: Shape1 [0.025 -> 0.408] <-> Shape2 [0.020 -> 0.310]  (sizes: 0.383, 0.290)
Segment 1: Shape1 [0.408 -> 0.742] <-> Shape2 [0.310 -> 0.560]  (sizes: 0.334, 0.250)
Segment 2: Shape1 [0.742 -> 0.025] <-> Shape2 [0.560 -> 0.020]  (sizes: 0.283, 0.460)  <- wraps
```

Now: `poly2_cut_point = double_mapper.map(0.0)`

This asks: **"Where on Shape 2's perimeter does Shape 1's starting point (progress 0.0) correspond?"**

Progress 0.0 on Shape 1 is NOT a corner — it falls in the wrap-around segment
(Segment 2: `0.742 -> 0.025`). The DoubleMapper **linearly interpolates** within that
segment, which is why the result is generally not on a cubic boundary:

```
segment_size_x = (0.025 - 0.742) % 1.0 = 0.283
segment_size_y = (0.020 - 0.560) % 1.0 = 0.460
position_in_segment = ((0.0 - 0.742) % 1.0) / 0.283
                    = 0.258 / 0.283 = 0.912

result = (0.560 + 0.460 * 0.912) % 1.0
       = (0.560 + 0.4195) % 1.0
       = (0.9795) % 1.0
       = 0.9795
```

So **`poly2_cut_point = 0.9795`**. This falls inside the square's Cubic 7 (edge S->P, `[0.830, 1.000]`).

---

### Step 4: `cut_and_shift(0.9795)` on Shape 2

Shape 2 needs to "start" at the point corresponding to Shape 1's progress 0.0. Since
`poly2_cut_point = 0.9795` lands in the middle of Cubic 7, that cubic must be **split**
(the cut point almost never falls exactly on a cubic boundary — see Step 3 for why).

The cubic gets split:

```
Cubic 7a: S->M  progress [0.830, 0.9795]   (first part)
Cubic 7b: M->P  progress [0.9795, 1.000]   (second part)
```

Where M is a point on edge S->P about 88% along it (very close to P).

Then the polygon is **rotated** so it starts at M, and all progress values are shifted:

```
bs2 (after cut_and_shift):

Cubic 0: M->P             progress [0.000, 0.0205]    <- was 7b, shifted
Cubic 1: corner at P      progress [0.0205, 0.0605]   <- was cubic 0
Cubic 2: edge P->Q        progress [0.0605, 0.3105]   <- was cubic 1
Cubic 3: corner at Q      progress [0.3105, 0.3505]   <- was cubic 2
Cubic 4: edge Q->R        progress [0.3505, 0.5605]   <- was cubic 3
Cubic 5: corner at R      progress [0.5605, 0.6005]   <- was cubic 4
Cubic 6: edge R->S        progress [0.6005, 0.8105]   <- was cubic 5
Cubic 7: corner at S      progress [0.8105, 0.8505]   <- was cubic 6
Cubic 8: S->M             progress [0.8505, 1.000]    <- was 7a
```

Shape 2 now has 9 cubics (one was split) and starts at M — which corresponds to
Shape 1's progress 0.0 through the mapping. **bs1 (Shape 1) is unchanged.**

---

### Step 5: The Walking Algorithm

Now both shapes start at corresponding points (progress 0.0 is aligned). But they have
different numbers of cubics with different boundary positions. The walking algorithm
produces **matched pairs** by consuming cubics from both shapes in lockstep, cutting
whichever one extends further at each step.

**The comparison is always done in Shape 1's progress space.** For each step:

- **`b1a`** = end progress of current cubic on Shape 1 (already in Shape 1 space)
- **`b2a`** = end progress of current cubic on Shape 2, **converted to Shape 1 space**:
  first undo the shift (`+ poly2_cut_point`), then `map_back()` through the DoubleMapper

**Special case:** when either shape is on its **last** cubic, its end progress is forced
to `1.0` to guarantee both shapes finish together.

Initialize:

```
i1=0, i2=0
b1 = bs1.get_cubic(0)  -> Triangle Cubic 0 [0.000, 0.050]
b2 = bs2.get_cubic(0)  -> Square Cubic 0   [0.000, 0.0205]
```

**Walk Step 0:**

```
b1a = 0.050   (triangle cubic 0 ends here)
b2a = map_back((0.0205 + 0.9795) mod 1.0) = map_back(0.0) = ~0.007

min_b = 0.007  (b2 ends sooner in Shape 1 space)

-> b1a (0.050) > min_b (0.007): CUT b1 at progress 0.007
   seg1 = triangle cubic [0.000, 0.007]  (tiny sliver)
   new_b1 = remainder [0.007, 0.050]

-> b2a (0.007) ~ min_b: CONSUME b2 whole
   seg2 = square cubic [0.000, 0.0205]
   advance to next: b2 = bs2.get_cubic(1)

-> PAIR: (seg1, seg2)
```

**Walk Step 1:**

```
b1 = triangle remainder [0.007, 0.050]
b2 = square cubic 1 [0.0205, 0.0605]

b1a = 0.050
b2a = map_back((0.0605 + 0.9795) mod 1.0) = map_back(0.040) = ~0.057

min_b = 0.050  (b1 ends sooner)

-> b1a ~ min_b: CONSUME b1 whole
-> b2a (0.057) > min_b (0.050): CUT b2 at mapped progress

-> PAIR: (b1, seg2_first_half)
```

**This continues** until both shapes are exhausted. At each step:
- The cubic that "runs out" sooner (in Shape 1's progress space) is consumed
- The other is split so the boundary aligns
- A pair `(seg1, seg2)` is emitted

After all steps, you end up with something like **~12-15 pairs**, both lists having the
same count. The total pair count is roughly the **union** of both shapes' boundary
positions (at most `count1 + count2`), since every boundary from either shape needs to
exist in both.

---

### Step 6: Return and interpolation

```python
return ret  # List of (Cubic, Cubic) pairs
```

Each pair aligns a segment of the triangle with a corresponding segment of the square.
At render time, `as_cubics(matched_pairs, progress=0.5)` interpolates each pair's four
control points (p0, p1, p2, p3) 50% of the way between the two shapes, producing
a shape halfway between triangle and square.

The last cubic's end point is snapped to the first cubic's start point to ensure the
shape is always closed.

---

### Summary of data flow

```
Shape 1 (triangle)              Shape 2 (square)
     |                               |
  measure_polygon               measure_polygon
     |                               |
  6 cubics                        8 cubics
  3 corners [0.025,0.408,0.742]   4 corners [0.020,0.310,0.560,0.810]
     |                               |
     +------- do_mapping ------------+
                  |
          3 pairs: (0.025,0.020) (0.408,0.310) (0.742,0.560)
          (greedy closest-first, with ordering constraints)
                  |
            DoubleMapper
          (piecewise-linear circular mapping)
                  |
          map(0.0) = 0.9795
          (where on Shape 2 does Shape 1's start correspond?)
                  |
            cut_and_shift(0.9795) on Shape 2
                  |
              9 cubics (one edge was split)
              starts at mapped point M
                  |
     +------ walking algorithm ------+
     |                               |
  consume/cut cubics          consume/cut cubics
  in lockstep, compared in Shape 1's progress space
     |                               |
     +-------- ~12-15 pairs ---------+
                  |
          (Cubic, Cubic) list
          ready for interpolation via as_cubics()
```
