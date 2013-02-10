import inspect
import re

from markdown.extensions.headerid import slugify

from wiki.models import page_types as types


# A dictionary for reverse lookup of page type by the short name
# So, given "course-quiz", find the CourseQuiz object etc
page_types = {}
for name, obj in inspect.getmembers(types):
    if inspect.isclass(obj):
        # Because it returns a tuple. There is probably a better way of doing it but issubclass() doesn't work so don't try it
        if obj.__bases__ == (types.PageType,):
            page_types[obj.short_name] = obj()

page_type_choices = tuple([(name, obj.long_name) for name, obj in page_types.iteritems()])


def get_section_start_end(lines, anchor_name):
    # Strip the underscore + number if there is one
    section_name = re.match('[^_]*', anchor_name).group()

    # If there's an underscore + a number at the end of the slug
    section_number_match = re.match('[^_]*_(\d+)', anchor_name)
    if section_number_match:
        section_number = int(section_number_match.group(1))
    else:
        section_number = 0

    # Start going through the lines, one by one, looking for perfect headers
    in_code_block = False
    num_found = 0
    last_depth = 5
    start = 0
    end = len(lines)
    looking_for_end = False

    # Set up some regular expressions
    code_block_re = re.compile('[~`]{3,}')
    header_re = re.compile('(#{1,5}) ?(.+)')

    for line_number, line in enumerate(lines):
        # Ignore headers inside code blocks
        code_block_match = code_block_re.match(line)
        if code_block_match:
            in_code_block = not in_code_block

        if in_code_block:
            continue

        header_match = header_re.match(line)
        if header_match:
            # Figure out the depth (needed to determine the end of the section)
            header_depth = len(header_match.group(1))
            if header_depth <= last_depth and looking_for_end:
                end = line_number
                looking_for_end = False

            # Save the name of the section here
            header = unicode(header_match.group(2))
            if slugify(header, '-') == section_name:
                # This is a potential header!
                if num_found == section_number:
                    # This is the right one. Start looking for the end
                    looking_for_end = True
                    start = line_number
                    last_depth = header_depth

                num_found += 1

    return (start, end)
