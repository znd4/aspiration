# Learnings

This was a fun project. Here are some of the new tools I got a chance to explore.

## mkdocs

I'd used this a _bit_ before, but I got a chance to play around with a lot of plugins.

## hypothesis

Like `mkdocs`, I'd used `hypothesis` for a couple projects before, but I'd never used it as extensively as I have here (it's been really useful for catching edge cases).

### Edge cases

Edge cases caught by hypothesis (that I managed to capture here):

1. `s="0Āa", n=2`
   1. This one was really tricky. It turns out that numpy was handling everything properly, and the naive solution was failing, but my tests were failing for both because python's regex module `re` is strict that `bool(re.match(r"A", Ā)) == False`.

### Unicode is wild

Oof, there's a lot going on here. I finally learned what [lookahead assertions](https://stackoverflow.com/a/469951/5071232) are

### New poetry version

The preview version of poetry has better support for splitting dependencies the way that `setuptools` encourages (`docs` vs `test` vs `lint` etc.)
