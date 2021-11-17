# Learnings

This was a fun project. Here are some of the new tools I got a chance to explore.

## mkdocs

I'd used this a _bit_ before, but I got a chance to play around with a lot of plugins.

I also figured out how to get README.md to be the docs homepage (I didn't know that git could track simlinks), but it might be more trouble than it's worth -- links to the documentation in the README can either work in github or on the docs site, not both (because the docs site composes the links relative to `./docs/`, whereas in github, they're constructed relative to `./`)

## oauth2-server

I got a chance to use `oauth2-server` as a static file server, which was fun to figure out and configure. I'm not sure how often I'll use for this purpose though. Most of the time, documentation would either be hosted on a platform that restricts access to members of an organization, or I'd want it to be publicly available. That being said, I might use `oauth2-server` for other stuff in the future.

## hypothesis

Like `mkdocs`, I'd used `hypothesis` for a couple projects before, but I'd never used it as extensively as I have here (it's been really useful for catching edge cases).

### Unicode is wild

Here are some unicode edge cases caught by hypothesis in the `casechange` tests (that I managed to capture here)

1. `s="0Āa", n=2`
   1. This one was really tricky. It turns out that numpy was handling everything properly, and the naive solution was failing, but my tests were failing for both because python's regex module `re` is strict that `bool(re.match(r"A", Ā)) == False`.
2. `"ᴀa"`
   1. `ᴀ` is a member of a character set called Small Capital Case Latin letters. It belongs to the lowercase letters unicode category (`r"\p{Ll}"`), `"ᴀ".upper() == "ᴀ"`!!!
   2. The solution I ended up coming up with is to treat `ᴀ` as _both_ an upper-case and lower-case character, and test with it accordingly.
3. [`º`](https://en.wikipedia.org/wiki/Ordinal_indicator)
   1. This isn't actually a case-able letter, but it was showing up in some of the letter categories. I don't remember how, but I ended up managing to exclude it from the alphanumeric category without adding it to an explicit excludelist.
4. [`ß`](https://en.wikipedia.org/wiki/%C3%9F)
   1. This is in the category of latin letters (`\p{Alphabetic}` and `\p{Script=Latin}`), but `"ß".upper() == "SS"`, which is really confusing because it adds an extra character.
   2. The solution: to explicitly exclude it from the alphanumerics

### New poetry version

The preview version of poetry has better support for splitting dependencies the way that `setuptools` encourages (`docs` vs `test` vs `lint` etc.)
