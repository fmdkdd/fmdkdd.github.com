Fundamental tension of speaker vs listener dynamic.  Both want to minimize
effort when communicating, without loss of information.

When writing code, we often feel that "it can be made simpler".  We feel that if
we could design our own language, we could express intention exactly without the
ceremony or repetition caused by the language we are using (the *accidental
complexity*).

It is true.  There is a minimal way to state precisely the information, and we
know that from Shanon's information theory.  If you have only two states, you
only need one bit.  If you have 256 states, you only need 8 bits.

You can even use Hamming encoding to get a guaranteed minimal alphabet.

Of course it's not a simple when designing human interfaces.  Natural language,
for instance, is not terse.  There is redundancy; many combinations of letters
do not correspond to any recognized word.  The signal-to-noise ratio is less
than 1.  But the noise here acts as a correction code.  If few words begin with
'q', then when I hear them over an imperfect medium (like a phone, or a loud
bar), I can fill in the missing letters.  Context helps as well.  Natural
languages have also evolved due to natural constraints like the shape of
sound-emitting apparatus, our vocal chords, mouth and tongue, but also from the
constraints of the receiving end: our ears, and how our brain processes its
signals.

The constraints for code are a bit different.  You usually have a non-noisy
communication channel: every symbol of code is perfectly restituted to the
reader.  But our brains are easily fooled: in code you want to avoid
misreadings.  Like, no-one would think of having both a `mimimum` and a
`minimum` global variable, as the former will too easily be mistaken for the
latter.  You thus *want* redundancy.

But more importantly, even if it is feasible to design a minimal language for
your domain, you want to leave some room for change.

Related to "the wrong abstraction" blog post.  It's when you refactor in such a
way that you cannot express all your domain concerns.

What I did recently for the Z80 gen is a good example of overfitting, or
premature refactoring.

In the end, it all boils down to designing your language.  A DSL is obviously a
language, but an API is a language as well.

Cue Lisp, Forth, which make this easier.
