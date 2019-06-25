#include <WiFi.h>
#include <HTTPClient.h>

const int pin_r = 4;
const int pin_g = 16;
const int pin_b = 17;
const int pin_btn1 = 5;
const int pin_btn2 = 18;
const int pin_btn3 = 19;

const char* ssid = "ssid";
const char* password = "pwd";
const char* url = "";

const char* post1 = "{\"button\": -1}";
const char* post2 = "{\"button\": 0 }";
const char* post3 = "{\"button\": 1 }";

void setup() {
    Serial.begin(115200);
    delay(20);

    Serial.println("Startup");
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    pinMode(pin_r, OUTPUT);
    pinMode(pin_g, OUTPUT);
    pinMode(pin_b, OUTPUT);
    pinMode(pin_btn1, INPUT);
    pinMode(pin_btn2, INPUT);
    pinMode(pin_btn3, INPUT);
}

void loop() {
    int btn1 = digitalRead(pin_btn1);
    int btn2 = digitalRead(pin_btn2);
    int btn3 = digitalRead(pin_btn3);
    if (btn1 | btn2 | btn3) {
        if (WiFi.status() == WL_CONNECTED) {
            digitalWrite(pin_r, LOW);
            digitalWrite(pin_b, HIGH);
            HTTPClient http;
            http.begin(url);
            http.addHeader("Content-Type", "application/json");

            int response = 0;
            if (btn1) {
                response = http.POST(post1);
            }
            else if (btn2) {
                response = http.POST(post2);
            }
            else if (btn3) {
                response = http.POST(post3);
            }
            digitalWrite(pin_b, LOW);
            if (response > 0) {
                digitalWrite(pin_g, HIGH);
                Serial.println(response);
                Serial.println(http.getString());
            } else {
                digitalWrite(pin_r, HIGH);
                Serial.print("Error on POST: ");
                Serial.println(response);
            }
            http.end();
            delay(1000);
            digitalWrite(pin_r, LOW);
            digitalWrite(pin_g, LOW);
        } else {
            digitalWrite(pin_r, HIGH);
            Serial.println("Error: not connected to WiFi");
            delay(1000);
            digitalWrite(pin_r, LOW);
        }
    }
}
