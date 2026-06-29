#pragma once
#include <string>

// to_text -- strip all HTML tags from html and return plain text.
//
// Rules:
//   - Tags are delimited by '<' and '>'.  Everything between them is the tag.
//   - Tag names are case-insensitive: <B> and <b> produce the same result.
//   - Closing tags start with '/': </b> is the closing form of <b>.
//   - <br>  (open form only) is replaced with a newline character ('\n').
//   - <p>   (open form only) is replaced with two newlines ("\n\n").
//   - All other tags -- known (<b>, <i>, <u>) or unknown -- are stripped silently.
//   - Malformed tags (a '<' with no matching '>') are treated as literal text.
//
// Example:
//   to_text("<b>hello</b> world")   -> "hello world"
//   to_text("a<br>b")               -> "a\nb"
//   to_text("<p>paragraph")         -> "\n\nparagraph"
std::string to_text(const std::string& html);

// count_tag -- return the number of OPENING occurrences of tag_name in html.
//
// Rules:
//   - Only open tags are counted; </b> is not counted when tag_name is "b".
//   - Tag name comparison is case-insensitive: <B> and <b> both count for "b".
//   - Malformed tags (no closing '>') are not counted.
//
// Example:
//   count_tag("<b>hi</b><B>there</B>", "b")  -> 2
//   count_tag("<b>hi</b>", "B")               -> 1   (case-insensitive)
//   count_tag("<span>hi</span>", "b")         -> 0
int count_tag(const std::string& html, const std::string& tag_name);
