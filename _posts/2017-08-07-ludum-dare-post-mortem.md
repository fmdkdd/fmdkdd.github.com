---
layout: post
title: Ludum Dare 39 Post-Mortem
---

![Bright Plateau screenshot](/img/projects/ld39.png)

So, [Merwan][] and I made another game for [Ludum Dare][].  It had been two
years since our last entry, [You Are The Münster](/yatm) (*YATM* henceforth),
which we had a really great time making.  Ever since, we have been meaning to
get together for another round, but never managed to align our schedules until
now.

You can play *Bright Plateau* [right here](/ld39).  The rest of this post is a
recollection of the 72 hours we spent making it, and may contain minor spoilers.

### Day 0: Warming-up

In our timezone, the theme is announced at 3AM, in the night from Friday to
Saturday.  Merwan arrived Friday evening and, after we exchanged pleasantries,
we spent a few hours throwing ideas at each other, talking about games we liked,
why we liked them, what we thought they were lacking.  I remember talking about
simulations and tycoons.  These genres would come up again later.

We went through the list of candidate themes, which at the
time [was](https://ldjam.com/events/ludum-dare/39/theme/4):

> - Signal lost
> - Parallel worlds
> - Moving fortress
> - Running out of power
> - You are alone
> - Start with nothing
> - Machines
> - Running out of space
> - On / Off
> - Connections
> - Protect it
> - You are not the main character
> - 1 vs 100
> - It spreads
> - Different perspective
> - 1 HP

We liked "Moving Fortress", "Parallel Worlds", "Running out of space", "On /
Off", "Connections"; I remember discussing "You are not the main character" and
concluding it was a dead-end, on the basis that any mechanism we could find
would make the player-controlled character *the* main character for the player
in the end.  We felt pretty good about "Running out of space" winning, but we
did not cast our votes, as we didn't even have accounts to the new site at the
time.

We then checked out a few of the top games from the last Ludum Dare for
inspiration:

![LD38 top games](/img/posts/ld38.png)

Out of these six games, we played: *Honey Home*, *The Deep*, *Super Kaiju Dunk
City* and *Snowed In*.  *Little Lands* looked awesome, but was Windows only, so
we skipped it.  For each game, we tried to understand its appeal, how they used
the theme to good effect, and summarized what we liked/disliked.

I showed Merwan another LD game I had stumbled upon
prior: [Twin Condition](https://jackrugile.com/twin-condition/).  I really liked
the clean aesthetic, and the fact that you had to play both part of the levels
differently, but at the same time:

![Twin Condition screenshot](/img/posts/twin-conditions.png)

I also showed him [this prototype](http://rezoner.net/labs/spacesim.io/client/)
by rezoner, the author of [Playground.js](http://playgroundjs.com/) (among other
nice things); I liked the effectiveness and look of the low-resolution 3D
graphics:

![Rezoner space prototype screenshot](/img/posts/spacesim-proto.png)

Though it was not obvious to us at the time, in retrospect you can find
influences from all of these sources in the final game.

Then it was already 1AM.  For our previous LD, we stayed up until the theme had
been announced, started scribbling game ideas on paper, and went to bed only
after we had nothing further to write down.  This time though, we elected to
start off with a good night's sleep and to find out the theme in the morning.

### Finding a game idea

We woke up at around 9AM to discover the winning theme:

> Running out of power

Well, we quickly skirted that one the night before, as it hadn't inspired
anything to us.  But now the choice had been made.  We started throwing ideas:

![paper with game ideas for the theme](/img/posts/ld39-ideas.png)

We quickly gravitated to the idea in lower right: "Puzzle based around the power
grid".  Although at first it was much more elaborate than what we have now.

I remember pushing for a tycoon-like: there would be houses and plants to
consume power, and you would buy and put power generators on the map to supply
them.  The power consumers would have different consumption profiles: plants
would need a lot of power with low downtime, while houses would be consume
mostly in the day, but less at night.  The consumption would not be fixed, but
could vary from house to house.  The generators would *also* produce a varying
amount of power, depending on environmental conditions (wind for wind turbine,
sunlight for solar panels), maintenance, efficiency...  You earn money by
providing power to consumers.  Maybe this money would have been your score,
maybe it would have allowed you to upgrade your generators.  You can make out
some of that on the doodles above.

With our previous game, we had learned that it was quite tempting to aim for a
much larger game than we had the (time) budget to build.  In *YATM*, we had
planned for a large world with four areas, each guarded by a boss that would
be designed around the item kept in its area.  In the end, we only had two
areas, and zero boss.

This time around, we agreed to focus our design in order to have a game that
would feel whole.  Merwan argued that we could make the simulation, but would
have no idea whether it's fun until we have something working and running.  By
then, what if it's not?  Maybe we wouldn't have the time to throw it and design
another game.  He pushed for simpler rules; less simulation, more puzzle.  What
if instead of houses and plants, we had only houses?  What if, instead of money,
you would have a simple goal: power all the houses?  What if, instead of a
varying power distribution, we had only a binary state: on and off?

We thought about how that would work.  You would put generators on the map to
supply houses.  Each generator would supply power to all the houses in an area
around it, but it would also have a fixed distribution in time.  So, for
instance, the solar panel would power all the houses in a disc around it, but it
would have a 50/50 distribution over 24 hours: 100% in daylight, 0% at night.

We tried to play with the idea in our heads.  Would that be easy to understand?
How would you play the game?  How would you visualize the constraint of
validating the power distribution over time?  It turned out that the time
distribution was equivalent to a distribution in another spatial dimension.  So,
instead of placing generators on a plane, you were really placing them in space.
But how would that work, exactly?  Placing objects in space on a 2D screen is
not the easy to grasp, even when accustomed.  Maybe display the time dimension
below, like in [Shenzhen I/O](http://www.zachtronics.com/shenzhen-io/).

![Shenzhen I/O screenshot]()

Merwan suggested to simplify, again.  What if, instead of 24 slices of a day, we
had only two: one slice for the day, one for the night.  Then, we could show the
grid in the day, have a little sun floating in the sky, and you would pick up
the sun and drag to the right to see the grid at night.  At night, the coverage
of the generators would change, and to solve the puzzle you would have to solve
day and night simultaneously.  We felt that would make for an interesting game:
simple coverage alone would be quickly boring, but solving coverage with two
slightly different sets of constraints?  A tricky twist!

I pushed for having the day and night side-by-side, as I felt that going back
and forth between the day and night would make playing unnecessarily
frustrating.  Merwan argued that it might be difficult to explain to players the
sudden split between day and night.  But then again, finding out that you could
drag the sun away would not necessarily be more intuitive.  And having the day
and night portions side-by-side would probably be easiest to get right.  We
thought about potential ways to present this to the player, but did not find a
satisfying solution, and elected to review this once we had the game running.
In the end, we never reviewed it: the night levels are introduced without any
explanation, but so far no player has complained about not understanding that
they have to light all the houses on both sides to solve the level.

### Paper prototype

We took this idea for a spin.  What should the coverage for the generators be?
Again, we went for the simplest thing we could think of: the solar panel would
power a straight line, and the wind turbine would power its immediate neighbors
(in the final game, we did it the other way around, as it felt more natural
while playing).  I cut small lines and crosses out of paper, and drew a few
levels to get started:

![paper prototype photo]()

The number represent the amount of houses you have to power.  Each generator
provides 1 unit of power to each tile it covers, so you have to use multiple
generators to supply power to tiles with 2 or more houses.  In designing these
levels, I went for the simplest non-trivial configurations of lines and crosses
I could find, then simply numbered *some* of the tiles covered by the shapes.

Numbering all the tiles would have given away the placement of the generators,
and would have over-constrained the solution.  Solving the levels would have
been easy and boring.  By not giving away too much information, you leave
the player guessing.  By not over-constraining the level, you also let the
player solve the levels in different ways, and that makes it more interesting.
Although, you should try to make sure there are no *trivial* solutions that you
didn't think of.

I handed these levels to Merwan, and he tried to solve them.  He got one very
quickly, and got stumped on another one.  "Are you sure there is a solution?" he
asked.  "I think so" I replied, and I thought: this is challenging, he looks
like he is having fun!  Then I double-checked, and as it turned out, my level
had no solution.  When I fixed it, he solved it quite easily.  I then made
another one, this time making sure it had a solution, and one that was not too
obvious.  He solved it in around 1 minute.  At this point, we agreed that the
process of solving the levels was interesting enough to go forward with this
idea.

We had not resolved the rules of the night portion of the levels, however.  We
started by reducing the coverage of wind turbines and solar panels by half.
Now, we had to somehow overcome this power disparity between night and day.  We
thought about adding a third power generator that would work only at night.
What would be its coverage area?  We thought of a battery that would spread
power to neighboring houses.  Maybe we could charge the battery in the day, and
depending on the amount of charge, it would power that many houses?  But how
would we decide *which* houses would be powered by the battery: it the battery
has one unit of power, but two neighboring houses, which one is powered?  And
more importantly, how to communicate that rule to the player?  Maybe the battery
gives power to all the neighboring houses, regardless of its charge.  But then,
it would make the day and night levels feel unconnected: you solve the day
portion, then go to the night portion, put a battery or two, and you are done.
We wanted to have a real interplay between the day and night portions: you would
have to go back and forth to satisfy the constraints on both sides.  Maybe, the
battery would need to be powered in the day?  That could work.  However, we did
not design any level with the battery, as we weren't sure about how it would
work, and if it would be interesting enough.

It was already 4PM, so we elected to start coding rather than to keep designing
in the dark.  Maybe better ideas would come once we had something in our hands.

### Day 2:

INVENTORY

### Designing the levels


[Merwan]: https://merwanachibet.net
[Ludum Dare]: https://ldjam.com
[Shenzhen I/O]:
