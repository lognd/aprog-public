// media-library.hpp -- declare Book, Film, Album, and Library below.
// Do not modify the MediaItem class -- it is complete already.
#pragma once

#include <string>
#include <vector>

// ============================================================================
// MediaItem -- abstract base class shared by every catalog item.
// This class is complete. Do not modify it.
// ============================================================================
class MediaItem {
public:
    MediaItem(std::string title, int year) : title_(std::move(title)), year_(year) {}

    // A class with virtual functions needs a virtual destructor so that
    // destroying a derived object through a MediaItem reference or pointer
    // still runs the derived part of the destructor. This assignment never
    // calls `new`/`delete` on a MediaItem, but the rule holds regardless.
    virtual ~MediaItem() = default;

    // Pure virtual functions ("= 0"): every concrete media type must supply
    // its own kind() and summary(). Declaring them here with no body, and
    // marking them "= 0", makes MediaItem abstract -- it can never be
    // instantiated on its own, only through a derived class.
    virtual std::string kind() const = 0;
    virtual std::string summary() const = 0;

    // Non-virtual shared helpers. Every MediaItem, no matter its kind, is
    // read the same way.
    std::string title() const { return title_; }
    int year() const { return year_; }

protected:
    std::string title_;
    int year_;
};

// ============================================================================
// Book, Film, Album -- concrete media types.
//
// TODO: declare each class as `class X : public MediaItem`. Each needs:
//   - a constructor that takes (title, year, <its own fields>...) and passes
//     (title, year) to MediaItem's constructor via the member initializer list
//   - std::string kind() const override;
//   - std::string summary() const override;
//   - private members for its own fields
//
// Exact formats (see README "Task" section for the full spec):
//   Book::summary()   "Book: \"<title>\" (<year>) by <author>, <pages> pages"
//   Film::summary()   "Film: \"<title>\" (<year>), directed by <director>, <minutes> min"
//   Album::summary()  "Album: \"<title>\" (<year>) by <artist>, <trackCount> tracks"
//   kind() returns "Book", "Film", "Album" respectively.
// ============================================================================

// TODO: class Book : public MediaItem { ... };

// TODO: class Film : public MediaItem { ... };

// TODO: class Album : public MediaItem { ... };

// ============================================================================
// Library -- HAS-A collection of media items (composition, not inheritance).
//
// Library does not own the items it catalogs. It stores non-owning pointers,
// `const MediaItem*`, that refer to objects the caller constructed and
// continues to own. Library never allocates or frees a MediaItem -- there is
// no `new`/`delete` anywhere in this assignment. The items you add must
// outlive the Library that refers to them.
//
// TODO: declare class Library with:
//   - void add(const MediaItem& item);          -- stores &item, non-owning
//   - int count() const;                        -- number of items added
//   - std::vector<std::string> summaries() const;  -- item->summary() for each
//   - a private std::vector<const MediaItem*> member
// ============================================================================

// TODO: class Library { ... };
