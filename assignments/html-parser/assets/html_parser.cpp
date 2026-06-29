#include "html_parser.hpp"
#include <cctype>

// Helper: return a lowercase copy of s.
static std::string to_lower(const std::string& s) {
    std::string r = s;
    for (char& c : r) {
        c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    }
    return r;
}

std::string to_text(const std::string& html) {
    std::string result;
    std::size_t i = 0;
    while (i < html.size()) {
        if (html[i] == '<') {
            // TODO: find the matching '>'
            // TODO: extract and lowercase the tag name
            // TODO: if the tag is "br" -> append '\n'
            //        if the tag is "p"  -> append "\n\n"
            //        otherwise           -> strip silently
            // TODO: handle malformed tags (no '>') as literal text
            ++i;  // placeholder: remove this and implement the logic above
        } else {
            result += html[i++];
        }
    }
    return result;
}

int count_tag(const std::string& html, const std::string& tag_name) {
    // TODO: scan html for open tags matching tag_name (case-insensitive)
    // TODO: return the count of opening (non-closing) occurrences
    return 0;  // placeholder
}
