#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Incrementor for Sublime Text 3
Created on 25-Sep-2014 by Sanchit Karve
A Sublime Text 3 Plugin that can generate a sequence of numbers and letters using search and replace.

Ported to ST3 from Incrementor for ST2 created on 10-Jul-2012 by eBookArchitects
https://github.com/eBookArchitects/Incrementor
"""
import sublime
import sublime_plugin
import re
from functools import partial
from types import GeneratorType


class IncrementorCommand(sublime_plugin.TextCommand):
    """"""
    def window(self):
        """"""
        return self.view.window()

    def match_gen(self, regex):
        """"""
        position = 0
        while True:
            region = self.view.find(regex, position)
            if region:
                yield region
                if region.size() > 1:
                    position = region.end() - 1
                else:
                    position = region.end()
            else:
                break

    def make_alpha_step(self, start='a', step=1, repeat_after='z'):
        """"""
        # optional repeat_after argument specifies the limit of the incrementation.
        # after the limit is reached, return to the start value and resume incrementing
        num = start
        while True:
            yield num
            # No validation here. Use carefully.
            num = chr(ord(num) + step)
            # return to start value if we're past repeat_after
            if repeat_after:
                if step < 0:
                    if num < repeat_after:
                        num = start
                else:
                    if num > repeat_after:
                        num = start

    def make_step(self, start=1, step=1, repeat_after=None):
        """"""
        # optional repeat_after argument specifies the limit of the incrementation.
        # after the limit is reached, return to the start value and resume incrementing
        num = start
        while True:
            yield num
            num = num + step
            if repeat_after:  # return to start value if we're past repeat_after
                if step < 0:
                    if num < repeat_after:
                        num = start
                else:
                    if num > repeat_after:
                        num = start

    def inc_replace(self, pattern_list, match):
        """"""
        replace_string = ''
        for i in range(len(pattern_list)):
            if isinstance(pattern_list[i], GeneratorType):
                replace_string = replace_string + str(next(pattern_list[i]))
            else:
                replace_string = replace_string + match.expand(pattern_list[i])
        return replace_string

    def parse_replace(self, replace):
        """"""
        replace_list = re.split(r'(\\[iaA]\(.+?\)|\\[iaA])', replace)
        replace_list[:] = [item for item in replace_list if item != '']
        for i in range(len(replace_list)):
            if replace_list[i] == '\\i':
                replace_list[i] = self.make_step()
            elif replace_list[i] == '\\a':
                replace_list[i] = self.make_alpha_step(start='a', repeat_after='z')
            elif replace_list[i] == '\\A':
                replace_list[i] = self.make_alpha_step(start='A', repeat_after='Z')
            elif re.match(r'^\\[i]\(.+?\)$', replace_list[i]):
                arg_list = [int(num) for num in re.split(r'\\i|\(|,| |\)', replace_list[i]) if num != '']
                if len(arg_list) == 3:
                    replace_list[i] = self.make_step(start=arg_list[0], step=arg_list[1], repeat_after=arg_list[2])
                elif len(arg_list) == 2:
                    replace_list[i] = self.make_step(start=arg_list[0], step=arg_list[1])
                else:
                    replace_list[i] = self.make_step(start=arg_list[0])

        return replace_list

    def run(self, edit, regex_to_find, replace_matches_with):
        """"""
        positiveMatch = []

        def regionSort(thisList):
            """"""
            for region in thisList:
                currentBegin = region.begin()
                currentEnd = region.end()
                if currentBegin > currentEnd:
                    region = sublime.Region(currentEnd, currentBegin)

            return sorted(thisList, key=lambda region: region.begin())

        startRegions = self.view.get_regions('Incrementor')
        startRegions = regionSort(startRegions)
        view = self.view
        reFind = re.compile(regex_to_find)
        myReplace = self.parse_replace(replace_matches_with)

        if startRegions and replace_matches_with:
            # Check if regions are in the given selections.
            positiveMatch = []
            # Create list of non-empty regions.
            nEmptyRegions = [sRegion for sRegion in startRegions if not sRegion.empty()]

        # If there is at least one empty region proceed to check in matches are in region.
        if len(nEmptyRegions) == 0:
            positiveMatch = self.match_gen(regex_to_find)
            for match in positiveMatch:
                myString = view.substr(match)
                newString = reFind.sub(partial(self.inc_replace, myReplace), myString)
                view.replace(edit, match, newString)
        else:
            adjust = 0
            for sRegion in startRegions:
                matchRegions = self.match_gen(regex_to_find)
                if adjust:
                    newBeg = sRegion.begin() + adjust
                    newEnd = sRegion.end() + adjust
                    sRegion = sublime.Region(newBeg, newEnd)
                for mRegion in matchRegions:
                    if sRegion.contains(mRegion):
                        myString = view.substr(mRegion)
                        newString = reFind.sub(partial(self.inc_replace, myReplace), myString)
                        view.erase(edit, mRegion)
                        charLen = view.insert(edit, mRegion.begin(), newString)
                        adjustment = charLen - mRegion.size()
                        adjust = adjust + adjustment
                        newEnd = sRegion.end() + adjustment
                        sRegion = sublime.Region(sRegion.begin(), newEnd)
        for match in positiveMatch:
            myString = view.substr(match)
            newString = reFind.sub(partial(self.inc_replace, myReplace), myString)
            view.replace(edit, match, newString)
        view.erase_regions('Incrementor')


class IncrementorHighlight:
    """Highlights regions or regular expression matches."""

    def __init__(self, view):
        """"""
        self.view = view

    def run(self, match=None, startRegions=None):
        """"""
        view = self.view
        if startRegions and match:
            matchRegions = view.find_all(match)
            # Check if regions are in the given selections.
            positiveMatch = []
            # Create list of non-empty regions.
            nEmptyRegions = [sRegion for sRegion in startRegions if not sRegion.empty()]
            # If there is at least one empty region proceed to check in matches are in region.
            if len(nEmptyRegions) == 0:
                positiveMatch = matchRegions
            else:
                for mRegion in matchRegions:
                    for sRegion in startRegions:
                        if sRegion.contains(mRegion):
                            positiveMatch.append(mRegion)

            view.add_regions('Incrementor', positiveMatch, 'comment', '', sublime.DRAW_OUTLINED)
        else:
            view.erase_regions('Incrementor')


class IncrementorPromptCommand(sublime_plugin.WindowCommand):
    """Prompts for find and replace strings."""

    def highlighter(self, regex=None):
        highlighter = IncrementorHighlight(view=self.window.active_view())
        if regex:
            highlighter.run(match=regex, startRegions=self.selected_regions)
        else:
            highlighter.run()

    def show_find_panel(self):
        self.window.show_input_panel('Find (w/ RegEx) :', '', on_done=self.find_callback_on_done, on_change=self.highlighter, on_cancel=self.highlighter)

    def find_callback_on_done(self, find):
        self.regex_to_find = find
        self.show_replace_panel()

    def show_replace_panel(self):
        self.window.show_input_panel('Replace (w/o RegEx) :', '', on_done=self.replace_callback_on_done, on_cancel=self.highlighter, on_change=None)

    def replace_callback_on_done(self, replace):
        self.replace_matches_with = replace
        # Call IncrementorCommand to actually make the replacements
        self.window.active_view().run_command('incrementor', {'regex_to_find': self.regex_to_find, 'replace_matches_with': self.replace_matches_with})

    def run(self):
        """"""
        self.window.active_view().erase_regions('Incrementor')
        self.selected_regions = []
        for selection in self.window.active_view().sel():
            region = sublime.Region(selection.end(), selection.begin())
            self.selected_regions.append(region)
        self.show_find_panel()
