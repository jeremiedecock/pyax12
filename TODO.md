# TODO

## Version 0.3

- [x] finir de changer le nom "pydynamixel" -> "pyax12"

## Version 0.4

- [ ] écrire les fonctions dump(), scan(), reset() (et d'autres ?)
- [ ] ajouter des méthodes "print()" pour connexion, InstructionPacket et
      StatusPacket qui affichent des informations facilement intelligibles par un
      humain plutôt que des codes hexa (ex: "position=...°\nspeed=..." ; "baudrate=...\nport=...\n...")
- [ ] ajouter/pusher un tag v0.3

## Version 0.5

- [ ] ajouter des exemples
- [ ] ajouter une vidéo de démonstration dans le README.md
- [ ] amélorer la description dans le README.md
- [ ] ajouter/pusher un tag v0.4

## Version 0.6

- [ ] corriger les "TODO" restant
- [ ] vérifier systématiquement la validité des arguments (type, bornes, ...)
- [ ] remplacer les warning par des exceptions ?
- [ ] rendre le code de lecture plus robuste dans connection.send()
- [ ] ajouter/pusher un tag v0.5

## Version 1.0

- [ ] revoir la gestion des modules/paquets/imports (cf. pyai) ?
- [ ] tester si la génération de paquets Debian fonctionne toujours
- [ ] tester si la setup.py fonctionne toujours
- [ ] tester sous Windows
- [ ] ajouter/pusher un tag v1.0

## Misc

- [ ] créer le référentiel pyax12gui (PyAX-12-gui) : des outils graphiques (GTK+3) pour manipuler les servos Dynamixel avec PyAX-12
- [ ] tester depuis un RaspberryPi sans usbdynamixel (utiliser les GPIO) et sans CM-5 (utiliser des piles ou des LiPo)

