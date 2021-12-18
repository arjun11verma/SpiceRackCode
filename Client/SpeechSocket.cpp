#include "SpeechSocket.h"

SpeechSocket::SpeechSocket() {
    WiFi.begin(SSID, password);
    while((WiFi.status()) != WL_CONNECTED) {
      Serial.println("Not connected!");
      delay(1000);
    }

    String ip = WiFi.localIP().toString();
    Serial.printf("[SETUP] WiFi Connected %s\n", ip.c_str());

    this->tcp_socket = new WiFiClient();
    if (this->tcp_socket->connect(SERVER_IP, SERVER_PORT)) {
      Serial.println("Socket connected!");
    }
}

SpeechSocket::~SpeechSocket() {

}

void SpeechSocket::sendBuffer(int *buffer, int len) {
    this->tcp_socket->write_P((const char*) buffer, len);
}

uint8_t SpeechSocket::readSpice() {
  return this->tcp_socket->read();
}