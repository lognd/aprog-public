// Pattern Toolkit -- legacy reference material, NOT graded, do not submit.
//
// This is the thermometer before anyone thought to make the reactions
// pluggable. It started as "print the temperature," and every later
// requirement got bolted directly onto set_temperature() instead of being
// pulled out into its own object.
//
// History, as it really happened:
//   Sprint 1: set_temperature just printed the value to the console.
//   Sprint 2: ops wanted a log of every reading, so a std::vector<double>
//             got added and appended to inline.
//   Sprint 3: safety wanted an alarm above a threshold, so a counter and an
//             if-statement got added inline too.
//   Sprint 4 (never shipped): "marketing wants SMS alerts too, add param??
//             another bool??" -- see the TODO below. Every new reaction
//             means editing this one function and widening its signature
//             or its member list again.

#include <iostream>
#include <vector>

class ThermometerV1 {
public:
    explicit ThermometerV1(double alarm_threshold)
        : alarm_threshold_(alarm_threshold), alarm_count_(0) {}

    // TODO: marketing wants SMS alerts too, add param?? another bool??
    // TODO: ops also asked for a "quiet hours" flag that suppresses the
    //       console print but keeps logging and alarms. Where does that
    //       go -- another parameter? Another member?
    void set_temperature(double temp) {
        // Sprint 1: print to console.
        std::cout << "Temperature reading: " << temp << "\n";

        // Sprint 2: append to the log vector.
        log_.push_back(temp);

        // Sprint 3: check the alarm threshold, hardcoded inline.
        if (temp > alarm_threshold_) {
            ++alarm_count_;
            std::cout << "ALARM: temperature exceeded threshold!\n";
        }

        // Every future reaction (SMS, email, dashboard push, quiet hours)
        // has to be wedged into this function too, and every reaction has
        // to know about the other reactions' side effects to test it in
        // isolation -- there is no way to add or remove a reaction without
        // editing this function.
    }

    const std::vector<double>& log() const { return log_; }
    int alarm_count() const { return alarm_count_; }

private:
    double alarm_threshold_;
    int alarm_count_;
    std::vector<double> log_;
};
