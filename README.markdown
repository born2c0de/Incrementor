# Sublime Text 3 Plugin: The Incrementor

A Sublime Text 3 (ST3) Plugin that can generate a sequence of numbers and alphabets using search and replace.
Ported to ST3 by Sanchit Karve from [original Incrementor implementation for ST2](https://github.com/eBookArchitects/Incrementor) by eBookArchitects.

![Example Image](http://i.imgur.com/Rfqz1nB.gif)

Example (Before):

    10. Bob
    12. Larse
    15. Billy

> Find: `[0-9]+\.`
> Replace: `\i.`

Example (After):

    1. Bob
    2. Larse
    3. Billy

You can also take start and step arguments `\i(start,step)` in parenthesis.

Example (Before):

    10. Bob
    12. Larse
    15. Billy

> Find: `[0-9]+\.`
> Replace: `\i(10,10).`

Example (After):

    10. Bob
    20. Larse
    30. Billy

The Incrementor also supports negative steps! `\i(start,-step)`

Example (Before):

    10. Bob
    12. Larse
    15. Billy

> Find: `[0-9]+\.`
> Replace: `\i(100,-10).`

Example (After):

    100. Bob
    90. Larse
    80. Billy

Lastly, The Incrementor also supports alphabet replacements `\a` for lowercase and `\A` for uppercase.

Example (Before):

    10. Bob
    12. Larse
    15. Billy

> Find: `[0-9]+\.`
> Replace: `\a.`

Example (After):

    a. Bob
    b. Larse
    c. Billy

Note that start and step are not supported for alphabet replacements.


## Using

Use the keybinding to prompt for your find and replace.

Windows: [Ctrl + Alt + Shift + H]

Linux: [Ctrl + Alt + Shift + H]

## Installing

TODO

## Todo

- Replace based on order of selection as well as their direction.
- Scroll to matching pattern like sublime's default find window.
- Allow prepending 0s to the initial number. (001, 002, 003, 004, etc.)
- Add number of replaced items in statusbar after completion.
- Add step support for alphabet replacements

## License

[Creative Commons Attribution 2.0 Generic](http://creativecommons.org/licenses/by/2.0/)
