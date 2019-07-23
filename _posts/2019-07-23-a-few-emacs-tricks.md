---
layout: post
title: A Few Emacs Tricks
highlight: yes
---

Here are some Emacs Lisp stuff I have in my configuration, which others may find
useful.  I don't want to publish them on MELPA, because I have no intention
to maintain them.  They probably contain bugs, haven't been tested thoroughly
etc.  Feel free to grab them if they fit your needs, but don't complain if they
don't work!

### Automatically reload the browser when editing HTML

When I do web programming in HTML/CSS/JS, I like to have a browser to test my
changes quickly.  Switching to the browser and refreshing it got old rather
quickly, so I scripted it.

[`reload-browser.el`][] provides a function which reloads multiple browser
windows.  The first time you call it, it turns your cursor into a box, asking
you to click in the window you want to reload.  After that, calling the function
again will reload the window you selected.  You can even select multiple windows
(e.g., Firefox and Chrome) if you pass a numeric prefix argument.  With a
keybinding to save the current buffer and reload all browser windows, I don't
need a more fancy setup.

Behind the scenes it simply calls `xdotool` to do the heavy lifting.  It's
mostly straightforward, but it turns out that Chromium requires to be in focus
to be reloaded, whereas Firefox does not, so the script has to handle that as
well.

### One sentence per line for editing shared LaTeX

I usually write text with `auto-fill-mode`, which wraps lines at 80 characters
so the result is readable in any text editor.  When writing papers in LaTeX
though, I want to keep one sentence per line, as it makes reviewing the diffs
and handling conflicts much easier when working with other people.  Of course, I
want my editor to fill that way automatically.

[`ospl.el`][] redefines `auto-fill-function` to break after a sentence, and
provides an `ospl-paragraph` function which refills the current paragraph to one
sentence per line.  The trick here is to detect where sentences end so you can
insert newlines.  Emacs can recognize sentences by looking for a colon, but note
that abbreviated acronyms also end by colons ("e.g.", "i.e.").  The best way to
handle this unambiguously is to use a double space after a sentence, and a
single space after other colons (see the variable `sentence-end-double-space`).

Unfortunately, not everyone has recognized that the double space is the superior
form, so `ospl` assumes you use a single space, and avoids breaking after common
acronyms, which makes it slightly more complex than it should be.

### Preview definitions when editing assembly

Lately I've been dabbling in 6502 assembly, and when navigating code, I often
found the need to look at the definition for the label under point.  So I wrote
an xref backend for assembly ([`xref-asm.el`][]), so that I could jump to the
definition and back using the standard keybindings.  But for most labels, I
didn't really need to jump to the definition, I only needed to see a couple of
lines at or below the label, so I could remember what it was doing.

So I wrote [`xref-posframe.el`][], another package which *previews* the
definition using `posframe`.  Posframe lets you create one-shot Emacs frames
without window decorations, which is more convenient and configurable than
overlays for displaying stuff on top of the current buffer, but still fast
enough to be usable.  With xref-posframe, I can preview a definition in one
key:

<video autoplay loop>
  <source src="/img/posts/xref-asm.webm" type="video/webm">
</video>

Pressing the key a second time, I can even jump to the definition.

And it works everywhere xref is supported, not just for assembly.

### Highlight TODO keywords

This one is pretty simple.  I want keywords in comments like `TODO:` and
`FIXME:` to use a custom font, so I can see them pop out at me, screaming to be
fixed.  This can be done by adding keywords to font lock:

```emacs-lisp
(defun add-watchwords ()
  "Add TODO: words to font-lock keywords."
  (font-lock-add-keywords
   nil '(("\\(\\<TODO\\|\\<FIXME\\|\\<HACK\\|@.+\\):"
          1 font-lock-warning-face t))))
(add-hook 'prog-mode-hook #'add-watchwords)
```

![Rust snippet with a TODO keyword in a comment highlighted in bold](/img/posts/todo-highlight.png)

This method has one drawback: it highlights these words *anywhere* they appear
in a programming buffer, even outside of comments.  There are complex packages
that do this in a more robust way, making sure to only highlight these words in
comments.  I don't think these are worth the added complexity.  For me, 99.99%
of the time the method above works fine.  When there is a false positive, I just
ignore it.

Lately I've been using more descriptive keywords like `@Correctness:` or
`@Optimize:`, so I've added a wildcard at the end to handle all words between
"`@`" and "`:`".  Even then, false positives are not an issue.

### Insert screenshots into Org documents

I take a lot of notes on what I'm working on in Org.  Whenever I'm working on
something that can be visualized, I prefer to include screenshots as they are
often more helpful in conveying what's going on.  To reduce the friction of
taking the screenshot, cropping it, and inserting the link into the Org file,
I've written a bit of Elisp to do it for me:

```emacs-lisp
(defun insert-screenshot (file-name)
  "Save screenshot to FILE-NAME and insert an Org link at point.

This calls the `import' from ImageMagick to take the screenshot,
and `optipng' to reduce the file size if the program is present."
  (interactive "FSave to file: ")
  ;; Get absolute path
  (let ((file (expand-file-name file-name)))
    ;; Create the directory if necessary
    (make-directory (file-name-directory file) 'parents)
    ;; Still, make sure to signal if the screenshot was in fact not created
    (unless (= 0 (call-process "import" nil nil nil file))
      (user-error "`import' failed to create screenshot %s" file))
    (if (executable-find "optipng")
        (start-process "optipng" nil "optipng" file))
    (insert
     ;; A link relative to the buffer where it is inserted is more portable
     (format "[[file:%s]]"
             (file-relative-name file
                                 (file-name-directory buffer-file-name))))
    (when (eq major-mode 'org-mode)
      (org-redisplay-inline-images))))
```

This snippet asks for a filename, then calls `import` to select just the area I
want to screenshot, saves it and then insert an org-format image link at point.
In org-mode, it redisplays inline images so I can see the result right away.  If
`optipng` is installed, it even compresses the screenshot to save space.

### Insert, delete or change delimiters

In Spacemacs and Vim, there's a nifty way to quickly surround a part of text
with quotes, braces, and other delimiters.  When I went back to vanilla Emacs,
adding quotes by hand seemed tedious.

[`delimiter.el`][] solves this.  It's very straightforward: `delimiter-surround`
will prompt for a delimiter char and surround the current region with it.  If no
region is active, it surrounds the current sexp.  So in two quick key presses, I
can quote a word.  Some delimiters go in pairs, so giving an opening brace "`{`"
will use the matching closing brace "`}`" as closing delimiter.

There is also `delimiter-change` to change an existing delimiter pair to
something else, and `delimiter-delete` which is self-explanatory.

Note that the deletion is purposefully *not* clever: if you have nested
delimiters, it will just delete the ones closest to point, so in the following
situation (the caret `|` marks point):

```
(he|re (is) a list)
```

invoking `M-x delimiter-delete ( RET` will yield:
```
he|re (is a list)
```

where one may expect to eat the outermost parens:
```
he|re (is) a list
```

If you want clever behavior, you should look elsewhere.

### Auto-revert without the lag

Just yesterday I wanted to explore the assembly output of GCC for some simple C
file.  I opened two windows: one with the C code, and one with the output
assembly.  I put the latter in `auto-revert-mode` so I could quickly see the
result after recompilation.

Turns out, `auto-revert-mode` had some weird lag on my machine, where it could
take a few seconds to revert the buffer so I could see the result.  Opening a
terminal with `watch -n 0.1 cat a.s` was better.

I wrote a small minor mode that reverts the buffer after getting change events
from `inotify`, and it was constantly instantaneous.

Later, I checked out the source to `auto-revert-mode`, and found that it does
more or less the same as my minor mode, using `filenotify` watchers first, and
falling back on polling if filenotify isn't supported or fails.  Yet, it can
still take seconds to refresh whereas my minor mode just works.

If you have the same issue with `auto-revert-mode`, you may want to try
[`inotify-revert.el`][].





[`reload-browser.el`]: https://github.com/fmdkdd/dotfiles/blob/master/emacs/.emacs.d/elisp/reload-browser.el
[`ospl.el`]: https://github.com/fmdkdd/dotfiles/blob/master/emacs/.emacs.d/elisp/ospl.el
[`xref-asm.el`]: https://github.com/fmdkdd/dotfiles/blob/master/emacs/.emacs.d/elisp/xref-asm.el
[`xref-posframe.el`]: https://github.com/fmdkdd/dotfiles/blob/master/emacs/.emacs.d/elisp/xref-posframe.el
[`delimiter.el`]: https://github.com/fmdkdd/dotfiles/blob/master/emacs/.emacs.d/elisp/delimiter.el
[`inotify-revert.el`]: https://github.com/fmdkdd/dotfiles/blob/master/emacs/.emacs.d/elisp/inotify-revert.el
