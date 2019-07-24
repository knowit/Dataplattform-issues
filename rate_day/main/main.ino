#include <WiFi.h>
#include <HTTPClient.h>

const int pin_r = 4;
const int pin_g = 16;
const int pin_b = 17;
const int pin_btn1 = 5;
const int pin_btn2 = 18;

const char* ssid = "";
const char* password = "";
const char* url = "...com/test/dataplattform_ingest/DayRatingType";
const char* ingest_api_key = "";

void setup() {
    Serial.begin(115200);
    delay(20);

    pinMode(pin_r, OUTPUT);
    pinMode(pin_g, OUTPUT);
    pinMode(pin_b, OUTPUT);
    pinMode(pin_btn1, INPUT);
    pinMode(pin_btn2, INPUT);

    Serial.println("Startup");
    Serial.print("URL: ");
    Serial.println(url);
    Serial.print("Connecting to ");
    Serial.println(ssid);
    Serial.print("Password: ");
    Serial.println(password);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        digitalWrite(pin_b, HIGH);
        delay(250);
        digitalWrite(pin_b, LOW);
        delay(250);
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(pin_g, HIGH);
    delay(1000);
    digitalWrite(pin_g, LOW);
}

void loop() {
    int btn1 = digitalRead(pin_btn1);
    int btn2 = digitalRead(pin_btn2);
    if (btn1 | btn2) {
        if (WiFi.status() == WL_CONNECTED) {
            digitalWrite(pin_r, LOW);
            digitalWrite(pin_b, HIGH);
            HTTPClient http;
            http.begin(url);
            http.addHeader("Content-Type", "application/json");
            http.addHeader("x-api-key", ingest_api_key);

            String post = "{\"button\": ";
            if (btn1) {
                post += "-1 ";
            } else if (btn2) {
                post += "1 ";
            }
            post += "\"}";
            Serial.println(post);
            int response = http.POST(post);
            digitalWrite(pin_b, LOW);
            if (response >= 200 && response < 300) {
                digitalWrite(pin_g, HIGH);
                Serial.println(response);
                Serial.println(http.getString());
            } else {
                digitalWrite(pin_r, HIGH);
                Serial.print("Error on POST: ");
                Serial.println(response);
                Serial.println(http.getString());
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

