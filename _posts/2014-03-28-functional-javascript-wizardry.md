---
layout: post
title: Functional JavaScript Wizardry
highlight: yes
---

Since EcmaScript 5, JavaScript has gotten nice collection functions
like `Array.map`, `Array.forEach`, `Array.filter` and the
[usual suspects][iterators].  However, they can be a bit clunky to use
when dealing with objects.  Look at the following piece of code:

{% highlight js %}
[" fun", " ction ", "  al"].map(function(str) { return str.trim(); })
                           .join("");
//=> 'functional'
{% endhighlight %}

I map over an array of strings, trim each string, then join the
resulting array of trimmed strings.  Except it’s a bit too verbose for
my tastes.  I would like to write (and read) this instead:

{% highlight js %}
[" fun", " ction ", "  al"].map(trim).join("");
{% endhighlight %}

The straightforward way to do that is to define the anonymous wrapper
function that calls `trim` beforehand:

{% highlight js %}
var trim = function(str) { return str.trim(); };
[" fun", " ction ", "  al"].map(trim).join("");
//=> 'functional'
{% endhighlight %}

Okay.  Except that I don’t want to call just `trim`, I might call any
function on `Array`, or `Object`, or any custom created object for
that matter.  And I certainly don’t want to write stupid wrapper
functions each time.

The `trim` function already has a name: `String.prototype.trim`.  But
unfortunately, I cannot just write the following:

{% highlight js %}
[" fun", " ction ", "  al"].map(String.prototype.trim).join("");
// TypeError: String.prototype.trim called on null or undefined
{% endhighlight %}

Because here `map` will call `trim` on each string in the array, but
without any context object (a value for `this`).  Instead, I would
like `map` to pass each string _as_ the context object to `trim`, in
turn.  We could redefine a custom version of `map` that works that
way, but there’s a simpler solution.

### Abstracting wrappers

What we really need is a function that transforms method calls into
function calls.  We need a function `m2f` to transform `o.m(args)`
calls into `f(o, args)` calls, where `f = m2f(o.m)`.  Easy enough
in JavaScript (bar the ugliness of dealing with the arguments special
object):

{% highlight js %}
function m2f(fun) {
  return function(/* args */) {
    var args = [].slice.apply(arguments);
    return fun.apply(args.shift(), args);
  };
}

var trim = m2f(String.prototype.trim);
[" fun", " ction ", "  al"].map(trim).join("");
//=> 'functional'
{% endhighlight %}

Good!  Now I can use `m2f` on any “method”, and get back a more
flexible function.  For instance, I can use `map` on any “array-like”
objects like strings, the special `arguments` object, `NodeList` and
so on:

{% highlight js %}
var map = m2f([].map); // Saving a few chars over `Array.prototype.map`
var up = m2f(String.prototype.toUpperCase);
map("abc", up)
// [ 'A', 'B', 'C' ]

map({0: 'albatros', 1: 'albatros', length: 2}, up);
// [ 'ALBATROS', 'ALBATROS' ]

function(){ return map(arguments, up) }(1, 2, 'abc', 'z')
// [ '1', '2', 'ABC', 'Z' ]
{% endhighlight %}

And of course, I can use `m2f` on any method, not just `map`.  Here I
populate an `array` object with functions from `Array.prototype` that
work on any array-like object:

{% highlight js %}
var array = {};
function isFunction(x) { return typeof x === 'function'; }
var names = Object.getOwnPropertyNames(Array.prototype);
names.forEach(function(name) {
  if (isFunction(Array.prototype[name]))
    array[name] = m2f(Array.prototype[name]);
})

array
// { join: [Function],
//   pop: [Function],
//   ... }

array.slice([0,1,2], -1)
//=> [ 2 ]
{% endhighlight %}

This replicates the Mozilla-specific “Array generics” extension.  This
extension is [not available][V8] in V8-powered environment like
nodejs.

This `m2f` function is quite handy when you are used to a functional
style of programming.  You can find it in Fogus’
[_Functional JavaScript_][funjs] under the name ‘invoker’.  However,
there is another way to define `m2f` using a powerful corner of
EcmaScript 5.1, `bind`.

### Calling and binding functions

Earlier, I said I could not just write:

{% highlight js %}
var trim = String.prototype.trim;
{% endhighlight %}

Because JavaScript methods are really just functions.  Now my `trim`
is pretty useless on its own, because it expects a context object.

{% highlight js %}
trim("  a ");
// TypeError: String.prototype.trim called on null or undefined
{% endhighlight %}

There’s a way to provide one to it, using `call`:

{% highlight js %}
trim.call("  a ");
// 'a'
{% endhighlight %}

The `call` function takes a context, some arguments, and calls the
receiver (a function) with them.

Another way to provide the context is to use the `bind` function.  As
its name implies, `bind` will return a function with the supplied
context bound to it.  Let’s see how it works:

{% highlight js %}
var trimA = trim.bind("  a ");
trimA();
// 'a'

trimA.call("b");
// 'a'
{% endhighlight %}

Whenever `trimA` is called, it will call `trim` with `"a"` as context,
even if `trimA` is supplied another context with `call`.

### Binding call

Where does that lead us?  Well, if we look at the precedent example
again,

{% highlight js %}
trim.call("  a ");
{% endhighlight %}

we see that `trim.call` is essentially the function we want.  But we’d
rather use `trim` directly, without calling `call` on it.  How to
achieve that?

Notice that `call` is itself a method call.  So we can extract it on
its own, and use it to call `trim`.  But since it’s an extracted
method, we still need to use `call` on it,

{% highlight js %}
var call = trim.call;

call(trim, "  a ");
// TypeError: object is not a function

call.call(trim, "  a ");
// 'a'
{% endhighlight %}

Since we are calling `call` on itself, the notation is a bit
overloaded, but it works.  Note that now, `trim` is just an argument;
we can put any other method in there,

{% highlight js %}
call.call([].map, "abc", up);
// [ 'A', 'B', 'C' ]
{% endhighlight %}

In fact, there’s nothing tying `call` to `trim`.  We could have
defined `call` without `trim`, by taking it on `Function.prototype`
directly,

{% highlight js %}
var call = Function.prototype.call;
{% endhighlight %}

Nevertheless, the greatest benefit of this transformation is that we
can now use `bind` to fix the first argument of `call` to a specific
function.

{% highlight js %}
var map = call.bind([].map);

map("abc", up);
// [ 'A', 'B', 'C' ]
{% endhighlight %}

And we just redefined `m2f`!

{% highlight js %}
var m2f = call.bind;
var map = m2f([].map);
// TypeError: Bind must be called on a function
{% endhighlight %}

Except it doesn’t work ... because we did not provide a context to
`bind`.  Putting it all together,

{% highlight js %}
var call = Function.prototype.call;
var bind = call.bind;
var m2f = bind.bind(call);
{% endhighlight %}

Alternatively, since `bind` is not tied to `call`, it might be clearer
to just write:

{% highlight js %}
var call = Function.prototype.call;
var bind = Function.prototype.bind;
var m2f = bind.bind(call);
{% endhighlight %}

Which finally gives this one-liner gem:

{% highlight js %}
var m2f = Function.prototype.bind.bind(Function.prototype.call);
{% endhighlight %}

A very useful tool for writing terse JavaScript.

A variant of this form was given by
[Dave Herman](https://twitter.com/littlecalculist/status/125413301965438976)
and explained by
[Erik Kronberg](https://variadic.me/posts/2013-10-22-bind-call-and-apply-in-javascript.html),
which I read thrice without really understanding what was going on.
This article is my attempt to derive this magic one-liner in a way
that makes sense for me.


[iterators]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#Iteration_methods
[funjs]: https://github.com/funjs/book-source/blob/master/chapter04.js#L59
[V8]: https://code.google.com/p/v8/issues/detail?id=308
