#include <Arduino.h>

#include <ESP8266WiFi.h>

#include <WiFiClient.h>

#define SSID "Samsung Galaxy A71 5G 5868"
#define password "jaanjaan"

#define CLIENT_PORT 4210

#define SERVER_PORT 4209
#define SERVER_IP "192.168.174.56"

class SpeechSocket {
public:
    SpeechSocket();
    ~SpeechSocket();
    void sendBuffer(int* buffer, int len);
    uint8_t readSpice();
private:
    WiFiClient* tcp_socket;
};