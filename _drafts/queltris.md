---
layout: post
title: QUELTRIS
---

(TODO: Ask Merwan for pics of scrapbook)

(Focus on design decisions)

theme: sacrifice

mechanism: match-3 (playing puyopuyo vs tetris)

brainstorm visuals, find well
Merwan suggests pushing people down the well.

Great idea!

Match-3 with push instead of swap?

Make a prototype.  It's not fun.

Fun: we can feel if it isn't there, but how do we measure it, and more
importantly, how do we improve the mechanism?

Few decisions: 7 columns to push.  All decisions are the same => boring.

Doubt and uncertainty.

We look at other games, what makes them tick.

Tetris, PuyoPuyo, Hexic, Clash of Heroes, Puzzle quest, 10,000,000, Labyrinth

We try to expand pushing to sides: 10,000,000, Labyrinth

But ultimately, moving one piece at a time is uninteresting.  See PuyoPuyo,
Tetris: you get a couple of colors, or tetraminoes.

Feeling we have exhausted the search space, Merwan suggests we rotate instead of
push.

I implement rotation in 2 hours.  The mechanism itself is already fun, even if
we are just matching 3+ horizontal lines.  That's a good sign.

Now we can move in 4 directions: why match only lines?  We hit on the idea of
matching "runes": patterns of colors.  The god requires a few patterns, when you
match them they change, and so on.

Initially we envision large patterns: letters, shapes around 4x5 or 6x6.

But smaller patterns are more satisyfing: large patterns require more moves
before a match; with smaller patterns you can have more match in less time =>
better gratification.

Trying it out.  Great feel.  The simple change in mechanism opens up many
gameplay possibilities:

- overlap match
- multi-pattern match
- combos
- chains

Same tension as match-3: build order from disorder.

Why not change patterns?  Playtesting revealed that it was good to learn how to
find patterns, but when these changes it was confusing: I was always looking for
the previous patterns.

This is also why we chose tetraminoes: they are familiar.  I tried with another
4-cells in 3x2 pattern:

oo.
o.o

After a while I could find it in the soup, but the familiarity helps getting
into the game quicker.

Timer adds a failure state, and forces you to become better at finding patterns
and planning your path.
