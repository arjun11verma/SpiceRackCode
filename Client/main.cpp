#include <Arduino.h>
#include "SpeechSocket.h"

#define packet_size_int 8
#define MICROPHONE_PIN A0

size_t packet_size;
int packet_idx;
int packet_int[packet_size_int];
uint8_t active_spice;
SpeechSocket* speech_sock;

void setup() {
  Serial.begin(9600);
  Serial.println("Serial begun!");

  speech_sock = new SpeechSocket();
  packet_size = packet_size_int * sizeof(int);
  packet_idx = 0;
}

void loop() {
  packet_int[packet_idx] = analogRead(MICROPHONE_PIN);
  packet_idx++;

  if (packet_idx == packet_size_int) {
    speech_sock->sendBuffer(packet_int, packet_size);
    packet_idx = 0;
  }

  active_spice = speech_sock->readSpice();
  if (active_spice != -1) {
    Serial.print("Data recieved: ");
    Serial.print(active_spice);
    Serial.println();
  }
}