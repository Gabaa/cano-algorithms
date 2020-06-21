# cano-algorithms

Kan håndtere LAN opgaverne i CANO.

Det bruger Python 3 og køres ved at skrive "python main.py" i terminalen.
Der kan også gives et argument med en fil (ligesom sample-exam.txt) som sætter switches, addresses og forbindelser mellem disse op for dig.

## Commands

- send: Tager 2 argumenter, A og B, hvor A og B er navne på addresser. Sender beskeden fra A til B og opdaterer forwarding tables. Output viser hvilke switches der så beskeden.
- view: Tager 1 argument, S, hvor S er navnet på en switch. Viser forwarding table for switchen.
- reset: Rydder alle forwarding tables.
- exit: Lukker programmet.
