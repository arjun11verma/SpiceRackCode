#include "SpiceDriver.h"

SpiceDriver::SpiceDriver() {
    this->spiceMotor = new Stepper(stepsPerRevolution, 14, 12, 13, 15);
    this->spiceMotor->setSpeed(60);
    currentPosition = OREGANO;
}

SpiceDriver::~SpiceDriver() {
    delete this->spiceMotor;
}

void SpiceDriver::changePosition(short newPosition) {
    this->spiceMotor->step((this->currentPosition - newPosition) * stepsPerPosition);
}