import sublime_plugin
import sublime
import re
from .tailwind import tailwind_classes

class tailwindCompletions(sublime_plugin.EventListener):
    def __init__(self):
        classes = re.findall(
            r"\.((?:[a-z]*\\:)*[a-z0-9-]*)(?::[a-z0-9-]*)*\s*\{(.[^}]*)\}",
            tailwind_classes
        )

        self.class_completions = []
        for [the_class, the_attribute] in classes:
            self.class_completions.append(("%s \t%s" % (
                get_class(the_class), get_attribute(the_attribute)
            ),
            get_class(the_class)
        ))

    def on_query_completions(self, view, prefix, locations):
        if view.match_selector(locations[0], "text.html string.quoted"):

            if len(prefix) <= 0:
                return

            # Cursor is inside a quoted attribute
            # Now check if we are inside the class attribute

            # max search size
            LIMIT  = 100

            # place search cursor one word back
            cursor = locations[0] - len(prefix) - 1

            # dont start with negative value
            start  = max(0, cursor - LIMIT - len(prefix))

            # get part of buffer
            line   = view.substr(sublime.Region(start, cursor))

            # split attributes
            parts  = line.split('=')

            # is the last typed attribute a class attribute?
            if len(parts) > 1 and parts[-2].strip().endswith("class"):
                return self.class_completions
            else:
                return []
        elif view.match_selector(locations[0], "text.html meta.tag - text.html punctuation.definition.tag.begin"):
            # Cursor is in a tag, but not inside an attribute, i.e. <div {here}>
            return []

        else:
            return []


def get_class(c):
    return c.replace('\:', ':')

def get_attribute(a):
    return a[:30]
