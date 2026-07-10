// Pattern Toolkit -- legacy reference material, NOT graded, do not submit.
//
// Two free functions, each assembling a report as one big string. The
// inventory report was copy-pasted from the sales report to save time, and
// the two have already started to drift apart -- see if you can spot the
// bug before reading the README.
//
// History, as it really happened:
//   make_sales_report() shipped first. Someone later noticed the footer had
//   a typo ("--- End of Reprot ---") and fixed it in place.
//   make_inventory_report() was copy-pasted from the sales report BEFORE
//   that fix landed, so it still carries the typo today. Nobody has
//   noticed, because the two functions are never compared side by side --
//   there is no single "footer" anyone can look at.

#include <string>

std::string make_sales_report() {
    std::string report;
    report += "=== Sales Report ===\n";
    report += "Total Sales: $1000\n";
    report += "--- End of Report ---\n"; // typo fixed here
    return report;
}

std::string make_inventory_report() {
    std::string report;
    report += "=== Inventory Report ===\n";
    report += "Items In Stock: 42\n";
    report += "--- End of Reprot ---\n"; // <-- desync bug: typo never fixed
    return report;
}
