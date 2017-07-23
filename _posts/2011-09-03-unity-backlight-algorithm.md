---
layout: post
title: Unity backlight color algorithm
highlight: yes
---

With the release of Ubuntu 11.04, the new [Unity][] interface was
introduced to users.  While it has its issues, I have been satisfied
with it overall.  I find it cleaner than the Gnome 2 default bottom
panel, and I can quickly launch any application or find recent files
without leaving the keyboard.

Ever since I began using it however, one detail caught my attention:
the colored backlight behind applications icons.

![Unity backlight zoom](/img/posts/unity.png)

### Backlight color

Notice how every icon has a square with rounded corners behind it?
This square is colored for currently open applications.  This is the
backlight.

First, notice the backlight color is not constant: Emacs has a rich
purple matching its icon, while the Firefox icon has an orange
backlight, but a deeper orange than Update Manager (the box with the
orange arrow).  Thus, the backlight color seems to match the icon
contents.  But how exactly is the color determined?

### Algorithm hypothesis

Initially, we might guess that the backlight algorithm picks the
icon's most abundant color.  It is a good fit for the icons of Emacs,
Firefox and Empathy (the two blue heads).  However, it falls flat when
considering the Update Manager icon, as the orange arrow is smaller
than the beige box, but the backlight color is orange and not beige.
This is also demonstrated by GIMP's icon.  Our hypothesis is not far
from the truth however.

The catch is, we did not define what "most abundant color" meant.
Should we scan the icon and keep a count of each pixel color,
returning the most frequent color?  That could lead to surprising
results when considering high resolution icons with gradients. Our
eyes might easily differentiate between the blue globe and the humping
fire fox around it, but such an algorithm would not.  Individual RGBA
values are all the algorithm considers, but humans look at the whole
picture at once and see continents, a tail, a paw, ears and a muzzle.
There are algorithms for detecting image features, but they are far
too complex for the task at hand.  In fact, the actual algorithm is
quite simple.

### The code

Diving into the [source code][code] for Unity, we find the relevant function
in the `LauncherIcon` class, named `ColorForIcon`.  Here is
the entire function:

{% highlight c++ %}
void LauncherIcon::ColorForIcon (GdkPixbuf *pixbuf,
                                 nux::Color &background,
                                 nux::Color &glow)
{
  unsigned int width = gdk_pixbuf_get_width (pixbuf);
  unsigned int height = gdk_pixbuf_get_height (pixbuf);
  unsigned int row_bytes = gdk_pixbuf_get_rowstride (pixbuf);

  long int rtotal = 0, gtotal = 0, btotal = 0;
  float total = 0.0f;


  guchar *img = gdk_pixbuf_get_pixels (pixbuf);

  for (unsigned int i = 0; i < width; i++)
  {
    for (unsigned int j = 0; j < height; j++)
    {
      guchar *pixels = img + ( j * row_bytes + i * 4);
      guchar r = *(pixels + 0);
      guchar g = *(pixels + 1);
      guchar b = *(pixels + 2);
      guchar a = *(pixels + 3);

      float saturation = (MAX (r, MAX (g, b)) - MIN (r, MIN (g, b))) / 255.0f;
      float relevance = .1 + .9 * (a / 255.0f) * saturation;

      rtotal += (guchar) (r * relevance);
      gtotal += (guchar) (g * relevance);
      btotal += (guchar) (b * relevance);

      total += relevance * 255;
    }
  }

  float r, g, b, h, s, v;
  r = rtotal / total;
  g = gtotal / total;
  b = btotal / total;

  nux::RGBtoHSV (r, g, b, h, s, v);

  if (s > .15f)
    s = 0.65f;
  v = 0.90f;

  nux::HSVtoRGB (r, g, b, h, s, v);
  background = nux::Color (r, g, b);

  v = 1.0f;
  nux::HSVtoRGB (r, g, b, h, s, v);
  glow = nux::Color (r, g, b);
}
{% endhighlight %}

The code is rather straightforward.  Even without GDK experience, the
calls are self-explanatory.  The backlight color is close to a mean of
each pixel's color, except each color channel is weighted by a
`relevance` factor before contributing to the icon total.  The
relevance of each pixel is proportional to its saturation and alpha
value.  This explains the orange backlight for Update Manager: even
though the beige box is larger, the orange arrow is more saturated,
weighting more than beige in the backlight total.  Thus the result is
more orange than beige, but not quite the same backlight color as for
the Firefox icon, which has more saturated orange pixels.

Finally, there is also some saturation normalization:

{% highlight c++ %}
if (s > .15f)
    s = 0.65f;
  v = 0.90f;
{% endhighlight %}

Every backlight color that is saturated enough will be normalized to
65%.  I guess this is done in order to achieve a more unified feel, and
to avoid highly-saturated backlight colors.

[Unity]: http://unity.ubuntu.com/
[code]: http://bazaar.launchpad.net/~ubuntu-branches/ubuntu/natty/unity/natty/view/head:/src/LauncherIcon.cpp#L223
