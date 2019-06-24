#include <WiFi.h>
#include <HTTPClient.h>

const int pin_r = 4;
const int pin_g = 16;
const int pin_b = 17;
const int pin_btn = 5;
const int pin_btn2 = 18;

const char* ssid = "ssid";
const char* password = "pin";
const char* url = "";

// the setup function runs once when you press reset or power the board
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

    // initialize digital pin ledPin as an output.
    pinMode(pin_r, OUTPUT);
    pinMode(pin_g, OUTPUT);
    pinMode(pin_b, OUTPUT);
    pinMode(pin_btn, INPUT);
    pinMode(pin_btn2, INPUT);
}

// the loop function runs over and over again forever
void loop() {
    int btn_state = digitalRead(pin_btn);
    //Serial.print("Button: ");
    //Serial.println(btn_state);
    if (btn_state == HIGH) {
        if (WiFi.status() == WL_CONNECTED) {
            digitalWrite(pin_r, LOW);
            digitalWrite(pin_b, HIGH);
            HTTPClient http;
            http.begin(url);
            http.addHeader("Content-Type", "application/json");

            int response = http.POST("{}");
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
