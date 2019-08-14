# Event-knapp
Denne mappen inneholder oppsettet for feedback-knappen som kan brukes til å gi
en negativ/nøytral/positiv rating for et event.


Koden for ESP32 ligger i ```main/main.ino```. For å kjøre koden må du:
* Installere tooling for ESP32 (f.eks som tillegg til Arduino IDE)
    * OBS: Noen versjoner av Arduino IDE har breaking bugs, men har hatt flaks med 1.8.5
* Endre variabler i ```main/main.ino```:
    * ```ssid``` skal være ssid til WiFiet du bruker
    * ```password``` skal være passordet til WiFiet
    * ```url``` skal være ```HTTPS```-urlen til ingest API endepunktet
        * URLen burde se ut som ```https://[...].execute-api.[...].amazonaws.com/prod/dataplattform_ingest/EventRatingType```
    * ```ingest_api_key``` skal være en gyldig API-nøkkel til ingest APIet
* Kompiler og last opp til ESP32 over USB

Mikrokontrolleren sender informasjon om hva den holder på med over serial, så det burde
være greit å finne ut av hvor ting går galt hvis noe ikke fungerer.

