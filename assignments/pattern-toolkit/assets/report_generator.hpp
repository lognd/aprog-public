// Pattern Toolkit -- Part 3: the Template Method pattern.
//
// ReportGenerator owns the algorithm skeleton: generate() assembles a report
// by calling header(), then body(), then footer(), in that fixed order.
// Subclasses fill in the header() and body() steps; the footer is shared by
// every report and lives in the base class. Subclasses never call generate()
// themselves -- the base class calls their hooks ("don't call us, we'll call
// you").
//
// Rules:
//   - Do not use `new`, `delete`, or `throw` anywhere in this file.
//   - Do not modify the signatures below.
#pragma once

#include <string>

namespace pt {

// Base class holding the report-building skeleton. generate() is the fixed
// algorithm; header() and body() are the customization hooks.
class ReportGenerator {
public:
    virtual ~ReportGenerator() = default;

    // The template method. Assembles the report as header() + body() +
    // footer(), in that exact order. Do not override this.
    std::string generate() const {
        // TODO
        return "";
    }

protected:
    // Customization hooks. Each subclass provides its own header and body.
    virtual std::string header() const = 0;
    virtual std::string body() const = 0;

    // Shared footer, identical for every report. Returns
    // "--- End of Report ---\n".
    std::string footer() const {
        // TODO
        return "";
    }
};

// A sales report. header() returns "=== Sales Report ===\n" and body()
// returns "Total Sales: $1000\n".
class SalesReport : public ReportGenerator {
protected:
    std::string header() const override {
        // TODO
        return "";
    }

    std::string body() const override {
        // TODO
        return "";
    }
};

// An inventory report. header() returns "=== Inventory Report ===\n" and
// body() returns "Items In Stock: 42\n".
class InventoryReport : public ReportGenerator {
protected:
    std::string header() const override {
        // TODO
        return "";
    }

    std::string body() const override {
        // TODO
        return "";
    }
};

} // namespace pt
