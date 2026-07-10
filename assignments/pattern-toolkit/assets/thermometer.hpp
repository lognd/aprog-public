// Pattern Toolkit -- Part 2: the Observer pattern.
//
// A Thermometer is a subject. Observers register themselves with it; when
// the temperature changes, the thermometer notifies every attached observer
// in the order they attached. Observers are held as non-owning pointers --
// the thermometer never allocates or frees them.
//
// Rules:
//   - Do not use `new`, `delete`, or `throw` anywhere in this file.
//   - Do not modify the signatures below.
#pragma once

#include <vector>

namespace pt {

// Interface implemented by anything that wants to react to temperature
// changes. on_temperature is called once per set_temperature() on the
// subject the observer is attached to.
class Observer {
public:
    virtual ~Observer() = default;
    virtual void on_temperature(double temp) = 0;
};

// The subject. Holds non-owning pointers to attached observers and notifies
// them, in attach order, every time the temperature is set.
class Thermometer {
public:
    // Registers o to receive future notifications. o is not owned.
    void attach(Observer* o) {
        // TODO
        (void)o;
    }

    // Removes o so it receives no further notifications. Does nothing if o
    // was never attached.
    void detach(Observer* o) {
        // TODO
        (void)o;
    }

    // Records the new temperature and notifies every attached observer, in
    // attach order, by calling on_temperature(temp).
    void set_temperature(double temp) {
        // TODO
        (void)temp;
    }

private:
    std::vector<Observer*> observers_;
};

// Counts how many times the temperature it was notified with was strictly
// greater than a threshold set at construction.
class HighAlarm : public Observer {
public:
    explicit HighAlarm(double threshold) : threshold_(threshold), count_(0) {}

    void on_temperature(double temp) override {
        // TODO
        (void)temp;
    }

    // Number of notifications whose value exceeded the threshold.
    int count() const {
        // TODO
        return 0;
    }

private:
    double threshold_;
    int count_;
};

// Records every temperature value it is notified with, in order.
class TemperatureLog : public Observer {
public:
    void on_temperature(double temp) override {
        // TODO
        (void)temp;
    }

    // All temperatures received so far, in the order they arrived.
    const std::vector<double>& values() const {
        // TODO
        return values_;
    }

private:
    std::vector<double> values_;
};

} // namespace pt
