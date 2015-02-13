# Waaazap
A hackathon project.. We basically created a "happymeter", a physical device 
which allows users to input their "mood" of the day. Four expressive big buttons 
that reflects the mood of the user. Every signal are then uploaded to a backend 
webapp running in the Cloud.

We were quiet eager - so every one of us created their own web service in the Cloud..


## Technology stack

*Device:* A voting device with 4x buttons

*Cloud:* A endpoint which receives input signals from the _device_

*Client:* The web client (_Angular_) which will present the votes in a neatly manner


## The architecture

![waaazap architecture](https://github.com/Statoil/Waaazap/raw/master/waaaazap_architecture.png)


## Web projects

### Fredrik
Web input: https://happymind.herokuapp.com/input
Report: https://happymind.herokuapp.com/report
Report (WebSockets): http://happymind.herokuapp.com/wsreport (WebSocket rapport)

### Torbjørn
API Root: http://toslhack.herokuapp.com/ 	
User: hack@statoil.com
Pwd: test
Kun innloggede brukere får skrive data.
Result: http://toslhack.herokuapp.com/hello/

### Asbjørn
The Happy Meter: https://waaazap.herokuapp.com/testws

### Mats
Result:  http://showsmileys.herokuapp.com/


# Credits / team

* Mats G. Andersen
* Fredrik Gundersen
* Torbjørn Slørdal
* Kåre Veland
* Asbjørn Alexander Fellinghaug
