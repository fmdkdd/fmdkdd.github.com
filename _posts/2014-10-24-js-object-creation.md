---
layout: post
title: The Many Ways to Build Objects in JavaScript
---

In JavaScript, the dominant pattern to declare objects is to write a
constructor function and append each method to its `prototype`
property.  To create an instance of the object, one must then use the
`new` keyword on a call to the constructor function.

{% highlight js %}
function Set() {
  this.items = [];
}

Set.prototype.add = function(e) { this.items.push(e); }
Set.prototype.size = function() { return this.items.length; }
{% endhighlight %}

Here `Set` is the constructor function; in its body, `this` is a
reference to a newly-created object that will be returned after a call
to the constructor with the `new` keyword.  By convention, constructor
functions begin with a capital.

{% highlight js %}
var s = new Set();
s.add(1);
s.size() // 1
{% endhighlight %}

Note that `Set` is just a regular function, i.e. we can call it
without the `new` keyword.  Though usually it is not what you want,
since `Set` will return `undefined` and will bind `this` to the global
object in the absence of a caller.

{% highlight js %}
var s = Set();
s.add(1); // error: s is undefined
this.items; // [] -- Global objects is polluted
{% endhighlight %}

The `new` keyword applied to the `Set` function has the following
effect:

1. An empty object `o` is created.
2. The `[[Proto]]` property of `o` is bound to `Set.prototype`.  In
   other words, the prototype of `o` is set to `Set.prototype`.
3. The function `Set` is called with `o` is bound to `this`.
4. When the function returns, it returns `o` instead of `undefined`.

That is why methods of the object must be attached to the
`Set.prototype` object: it is the prototype of every instance of
`Set`.

I always found this pattern verbose and confusing.  The `new` keyword
was made to be familiar for Java programmers, but there is no mention
of classes, only prototypes.  In fact, it can be misleading to relate
to Java, since the receiver of a method is not bound statically in
JavaScript.

{% highlight js %}
var s = new Set();
s.add(1);
var add = s.add;    // Aliasing the method
add(2);             // error: `this.items` is undefined
{% endhighlight %}

The call to `add(2)` has no explicit caller, so `this` is bound to the
global object, which does have an `items` object.

Also, functions have a unique `prototype` property that is
unfortunately not the same thing as the `[[Proto]]` property that
every object -- including functions -- have.

Languages that compile to JavaScript, like CoffeeScript, TypeScript,
Dart and even the next version of EcmaScript all provide syntactic
sugar to hide this pattern.

Luckily, there are alternatives to this pattern in vanilla JS.  By not
trying to mimic class-based languages, but harnessing the simplicity
of the prototype model, one finds flexible and terse ways to create
objects.

### Object factories

JavaScript has objects literals, which are great for building
singleton objects.

{% highlight js %}
var bag = {
  items: [],

  add: function(e) { this.items.push(e); },
  size: function() { return this.items.length; },
};

bag.add(1);
bag.size(); // 1
{% endhighlight %}

Attributes and methods are now just properties of the same object.
In this respect, this form is more regular than the first pattern.

What if we want another instance of this object?  In other
prototype-based languages, we would just clone the first one; in
JavaScript, there’s no built-in clone function.  Instead, we can
create a factory function.

{% highlight js %}
function mkSet() {
  return {
    items: [],

    add: function(e) { this.items.push(e); },
    size: function() { return this.items.length; },
  };
}

var s1 = mkSet();
var s2 = mkSet();
s1.add(1);
s2.size(); // 0
{% endhighlight %}

The `mkSet` function puts out new objects of identical initial state.
Compared to the previous example, we have lost a bit of flexibility.
The bag was usable right away, but here we must call the factory to
create a new object before beginning to use it.

This form also has another downside: the methods are recreated
separately for each object.  The `add` method of `s1` and `s2` are not
the same.  Not only if this wasteful, but leaves us no way of adding
or altering methods for all objects of the same factory.

### Sharing behavior with prototypes

We can correct the latter defect by putting the methods in a separate
`setProto` object.  Then, in the factory method we must set the
`[[Proto]]` property to this `setProto` object.

{% highlight js %}
var setProto = {
  add: function(e) { this.items.push(e); },
  size: function() { return this.items.length; },
};

function mkSet() {
  return {
    __proto__: setProto,
    items: [],
  };
}

var s1 = mkSet();
var s2 = mkSet();
s1.add(1);
s2.size(); // 0
{% endhighlight %}

This way, all objects created by the factory `mkSet` share the same
methods.  We can easily extend the functionality of all sets by
appending methods to `setProto`.

{% highlight js %}
setProto.clear = function(e) { this.items.length = 0; };
{% endhighlight %}

Note that we did not correct the first defect: we must still use the
factory to begin using sets.  However, we essentially recreated the
first pattern: `mkSet()` does what `new Set()` did, and `setProto` is
`Set.prototype`.  It is less verbose, but now the methods and
constructor are separate entities, which makes even less sense.  As a
result `setProto`, is not a usable object on its own.  We would like
to reunite the two.

### Reuniting prototype and constructor

Since the constructor is just a function, why not put it inside the
prototype object itself?

{% highlight js %}
var Set = {
  new: function() {
    return {
      __proto__: Set,
      items: [],
    };
  },

  add: function(e) { this.items.push(e); },
  size: function() { return this.items.length; },
};

var s1 = Set.new();
var s2 = Set.new();
s1.add(1);
s2.size(); // 0
{% endhighlight %}

`Set` is still the prototype object, but the constructor is part of
its definition.  Calling `Set.new()` creates new objects inheriting
from `Set`.  In fact, `new` is a method of all `Set` objects.

{% highlight js %}
s1.new(); // Exactly the same as Set.new()
{% endhighlight %}

While this is unusual for class-based languages like Java, where
constructors are special methods, here we see they are just regular
functions that return new objects.

There is a bit of redundancy there, namely the `Set` in the line
`__proto__: Set`.  Since we will call the constructor with
`Set.new()`, why not use `this` instead?

{% highlight js %}
var Set = {
  new: function() {
    return {
      __proto__: this,
      items: [],
    };
  },

  ...
};

var s1 = Set.new();
{% endhighlight %}

Now `Set.new()` and `s1.new()` are no longer equivalent.  The latter
create an object that have `s1` as prototype, not `Set`.  This means
that we can specialize objects in branches, not only as a whole.

{% highlight js %}
var s1 = Set.new();
var s2 = Set.new();
var s11 = s1.new();

Set.clear = function(e) { this.items.length = 0; };
s1.forEach = function(f) { this.items.forEach(fn); };
{% endhighlight %}

Here, `s1`, `s2` and `s11` all have the `clear` method, but only `s1`
and `s11` have `forEach`.

### Prototypes as default objects

We should try to correct the first defect.  As it stands, the only
method that makes sense to call on `Set` is `new`.  Why not make `Set`
a fully functional instance of itself?

{% highlight js %}
var set = {
  new: function() {
    ...
  },

  ...
}.new();

set.add(1);
var s2 = set.new();
{% endhighlight %}

Just by calling `new()` on the object defining the `set` prototype, we
are giving it an `items` array.  Somehow we lost the direct reference
to the original prototype, but it does not matter since all `set`
objects will be derived from `set` itself (and we can still access it
from `set.__proto__`).

### Cloning is just another method

Finally, when creating objects we might want to make a deep copy of
an existing copy -- not start from a fresh state.  This can be
achieved by adding a `clone` method that defines the deep cloning of
each attribute.  It also binds `[[Proto]]` of course.

{% highlight js %}
var set = {
  ...

  clone: function() {
    return {
      __proto__: this,
      items: new Array(this.items),
    };
  },

  ...
}.new();

set.add(1);
var s1 = set.clone();
s1.size(); // 1
{% endhighlight %}

Here `s1` begins as an identical copy of `set`, but not sharing the
reference to the `items` array.  If we want shallow cloning, we can
just use `Object.create(set)`.  And if we want to branch, we can call
`set.new`.  We also can use `set` right away as a set.  All objects
derived from `set` will inherit from changes made to their prototype,
which allow to specialize and extend their behavior as befit.

This last form is not only more flexible than the dominant pattern of
the first example, it is more terse and regular.  But more
importantly, it illustrates the orthogonality of the core concepts of
JavaScript: object literals, first-class functions and prototypes.
