#include <Stepper.h>

#define stepsPerRevolution 400

#define stepsPerPosition 150 // for now this is just (400 * gearRatio) / 8 which about equals 150 

enum SpicePositions {
    OREGANO = 0,
    BASIL = 1,
    ROSEMARY = 2,
    PARSLEY = 3,
    GARLIC = 4,
    ONION = 5,
    PAPRIKA = 6,
    CUMIN = 7
};

class SpiceDriver {
public:
    SpiceDriver();
    ~SpiceDriver();
    void changePosition(short newPosition);
private:
    Stepper* spiceMotor;
    short currentPosition;
};