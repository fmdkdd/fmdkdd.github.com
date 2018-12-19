---
layout: post
title: Ludum Dare 43 Post-Mortem
---

<!-- TODO: Ask Merwan for pics of scrapbook -->

![Queltris](/img/posts/ld43-cover.png)

We made another game for the latest Ludum Dare game jam.  It's called QUELTRIS,
and you can play it [right here](https://0xc0de.fr/ld43).

In this post I want to describe the game design process: how we came up with the
idea, how the initial idea wasn't fun at all, and how we turned that around to
find something that worked.

### The idea
The theme this time was *Sacrifices must be made*.  We started by brainstorming
around that theme, trying to find an interesting setting and a game idea that
would fit.  We took the theme rather literally and quickly gravitated around the
idea of an Aztec god asking you to sacrifice pawns.

On the game side, I suggested to do a match-3 (aka Bejeweled).  Probably in part
because we had been playing PuyoPuyo vs. Tetris the night before, but also
because I though we could more easily nail the game design in 72 hours.  In
[Münster][], not only the game was *much shorter* than envisioned, but the
gameplay felt wonky due to falling short on time.  For [Bright Plateau][] we did
manage to make a decent-sized game (for a Ludum Dare), but as I designed the
levels the last day, we didn't know how fun the game would end up being until a
few hours before the deadline.  This time, we focused on getting to a good
gameplay first.

bejeweled pic

Of course, we didn't want to just do a Bejeweled clone, so we sketched some
ideas on how to iterate on the formula in an original way: using a different
swap mechanism, changing the grid...  I recalled QbQbQb, a game where you put
pieces around a planet.  Another one: that first-person Tetris game that has you
looking down the well in 3D as a tetramino.

sketchbook pics / QbQbQb / FPS Tetris

Trying to sketch how a circle grid would work for us, Merwan has an idea: what
if we had a round, bottomless well, and the player would push pieces so that
they fell in the abyss?  We both instantly love that idea: it's a simple
mechanism (push) that goes perfectly with the theme (sacrifice).

Now, at this point we don't know if it's a game or not.  We had a good idea, but
needed to see it in motion.  I start making a playable prototype while Merwan
begins working on the visuals.

### The prototype
At 21:19 on the first day we had a playable prototype:

<video controls>
  <source src="/img/posts/ld43-push-proto.webm" type="video/webm">
</video>

The player moves the white triangle at the top between columns, and can push the
current column down to match lines of the same color.  Every move consumes blood
from the gauge, while making matches fills it back.  When the gauge is empty,
you lose.

The first thing to note is that it is nearly a complete game.  In that sense,
our focus on prototyping was a success.  Adding a little polish here and there,
and we could have submitted it!  Needless to say, we felt pretty good about our
progress.

Except for one thing: the game wasn't fun.  *At all*.

In the video above I'm just pressing buttons at random, without thinking about
whether my move will make a match.  I don't need to: most moves *will* make a
match.  Since we are moving a whole column down, 7 pieces change position,
making 7 places for a potential match.  As I keep pressing the down button, I
make many matches, just at random.  The game does not challenge me, so I'm not
*engaging* with the game.  It's just not fun.

The blood gauge was actually an addition I made after finding out that the push
mechanism was simply not enough.  Adding the gauge was supposed to force the
player to consider each move, but as matches were easily made, the balance was
still off.

We were in a crisis.  We had a good idea, or a least we *thought* we did, but it
wasn't fun.  How could we salvage it?

### Finding the fun
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

<video controls>
  <source src="/img/posts/ld43-rotate-proto.webm" type="video/webm">
</video>

Now we can move in 4 directions: why match only lines?  We hit on the idea of
matching "runes": patterns of colors.  The god requires a few patterns, when you
match them they change, and so on.

Initially we envision large patterns: letters, shapes around 4x5 or 6x6.

But smaller patterns are more satisyfing: large patterns require more moves
before a match; with smaller patterns you can have more match in less time =>
better gratification.

Trying it out.  Great feel.  The simple change in mechanism opens up many
gameplay possibilities:

<video controls>
  <source src="/img/posts/ld43-combos.webm" type="video/webm">
</video>

- overlap match
- multi-pattern match
- combos
- chains

<video style="width: 200px" controls loop>
  <source src="/img/posts/ld43-overlap.webm" type="video/webm">
</video>

<video style="width: 200px" controls loop>
  <source src="/img/posts/ld43-multi-pattern.webm" type="video/webm">
</video>

<video style="width: 200px" controls loop>
  <source src="/img/posts/ld43-combos2.webm" type="video/webm">
</video>

<video style="width: 200px" controls loop>
  <source src="/img/posts/ld43-chain.webm" type="video/webm">
</video>

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

[Münster]: /yatm
[Bright Plateau]: /ld39
