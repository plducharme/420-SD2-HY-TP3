# La grande bataille des robots 2024

La grande bataille des robots est l'évènement tant attendu par tous les férus de robotique.
Vous devez implémenter le système de chargement de la configuration des divers robots.

# Prérequis
- Créer un environnement virtuel (venv)
- Python >= 3.10
- installer le package "PySide6"
  - Pyside6 est un package open-source basé sur PyQt pour la conception d'interfaces graphiques.


# Explications
Le module bataillerobots.py contient toutes les classes nécessaires à la grande bataille des robots.

## Classe ChampBataille
Cette classe implémente l'interface graphique. Vous n'avez rien à modifier dans cette classe. C'est un exemple rapide
d'interface graphique que vous allez construire dans le cours 420-SD3-HY.

## Classe SpriteJeu
Cette classe abstraite définie une entité pouvant être dessinée (Robot, Projectile).
```
Contient les propriétés:
    - pos_x
        - int: la position en X sur le champ de bataille 
    - pos_y
        - int: la position en y sur le champ de bataille
        - l'axe des y est inversé, les valeurs positives sont vers le bas
    - direction
        - int: la direction vers laquelle le Sprite est aligné en degré
        - l'angle se calcule dans la direction horaire au lieu de la direction antihoraire
            - par exemple, un Sprite avec une direction de 90 degrés sera aligné vers le bas 
```
Vous n'avez rien à modifier dans cette classe.

## Classe Robot
Classe abstraite représentant un robot.
```
En plus des propriétés héritées, contient les propriétés:
    - nom
        - str: Le nom du robot
    - sante
        - int: la santé du robot, si la sante d'un robot tombe à 0, il se brise
    - vitesse
        - int: la vitesse en pixel à laquelle le robot se déplace
    **Note: Le total de la santé et de la vitesse doit donner 100.**
    - instructions
        - deque: la liste d'instructions que le robot va exécuter
    - puissance_projectile
        - int: le dommage que le projectile fera
    - vitesse_projectile
        - int: la vitesse de déplacement du projectile en pixel
    **Note: puissance_projectile + vitesse_projectile doit donner 50.**
    - projectiles
        - list[Projectile]: liste de Projectile de ce robot existant sur le champ de bataille
```
Vous avez une méthode à implémenter dans cette classe.

## Classe Projectile
Classe abstraite représentant un projectile tiré par un robot.
```
En plus des propriétés héritées, contient les propriétés:
    - puissance
        - int: le dommage que le projectile fera
    - vitesse
        - int: la vitesse de déplacement du projectile en pixel
    **Note: puissance + vitesse doit donner 50.**
```

## Classe Jeu
Classe qui implémente la logique de jeu.
```
Contient les propriétés:
    - en_cours
        - Boolean: True si la partie est en cours
    - termine
        - Boolean: True si la partie est terminée
    - vue
        - ChampBataille: l'interface graphique du jeu
    - etape_jeu
        - int: compteur de "tick" serveur. Les instructions des robots sont exécutées toutes les 3 ticks
                serveur, alors que les projectiles sont mis-à-jour à chaque "tick".
    - robots
        - list[Robot]: liste des robots se battant dans l'arène.
    - gagnant
        - str: contient le nom du Robot gagnant
    - partie_nulle
        - Boolean: True si c'est une partie nulle
    - ecran_fin
        - QPixmap: image de l'écran de fin de jeu
```

# Requis
On vous a mis en charge d'implémenter le chargement de la configuration des Robots.
Malheureusement pour vous, c'est une compétition internationale et les sources de données ne sont pas standardisées.
Vous devrez donc utiliser plusieurs méthodes de lecture de la configuration des robots.

## Les Robots

## RandyBot

RandyBot est chaotique. Il est imprévisible car il effectue des rotations au hasard.
```
- À implémenter:
  - charger_configuration(self)
    - Enlever la configuration par défaut
    - Sa configuration se trouve dans le fichier "robots/randybot/config.json"
  - rotation(self)
    - il retourne un float ayant une valeur entre 0 et 360
```
## MathBot
MathBot se fie sur une fonction mathématique pour décider de sa rotation.
```
- À implémenter:
  - charger_configuration(self)
    - Enlever la configuration par défaut
    - La configuration de MathBot se trouve dans un fichier binaire "robots/mathbot/config.bin"
      - La structure est comme suit:
        - 7 octets contenant le nom du robot
        - 5 octets ayant la valeur "STATS"
        - 2 octets contenant la valeur numérique de la vitesse de MathBot
        - 2 octets contenant la valeur numérique de la santé de MathBot
        - 3 octets ayant la valeur "MUN"
        - 2 octets contenant la valeur numérique de la vitesse des projectiles de MathBot
        - 2 octets contenant la valeur numérique de la puissance des projectiles de MathBot
        - 12 octets ayant la valeur "INSTRUCTIONS"
        - des blocs de 8 octets chaque contenant les instructions
          - Lire chaque instruction
            - Si une instruction contient des espaces vides à la fin, supprimer les espaces
            - Ajouter l'instruction à la liste d'instruction
  - rotation(self)
    - Pour ce qui est de la rotation, MathBot utilise les informations météo contenues dans le fichier "robots/mathbot/rotation.csv"
      - il calcule sa direction en utilisant la formule suivante:
        `rotation_degre = (abs(Maximale)**abs(Moyenne) * abs(Minimale) + Précipitations) % 360 `
      - La première rotation est le résultat de la première ligne de données, la deuxième rotation est le résultat de la
        deuxième ligne et ainsi de suite.
      - Lorsqu'il n'y a plus de ligne de données, on revient à la première ligne
      - Retourner la valeur (float)
```
## CampeurBot
CampeurBot est un campeur. Il ne bouge pas et préfère juste faire sa rotation de façon méthodique et tirer
```
- À implémenter:
  - charger_configuration(self)
    - Enlever la configuration par défaut
    - Sa configuration est dans le fichier XML "robots/campeurbot/config.xml"
  - rotation(self)
    - doit retourner 15 degrés de plus que sa direction actuelle
      - La valeur doit être située entre 0 (inclus) et 360 (non-inclus)
        - ex: 365 degrés = 5 degrés
```
## SuperBot
SuperBot croit dans l'équilibre des statistiques. 
```
- À implémenter:
  - charger_configuration(self)
    - Enlever la configuration par défaut
    - Sa configuration est un objet PickleConfig qui a été sérialisé en utilisant "pickle" dans le fichier "robots/superbot/superbot.config"
  - rotation(self)
    - Aux rotations impaires (1,3,5,...), il ajoute 60 degrés à sa direction actuelle
    - Aux rotations paires (2,4,6,...), il soustrait 30 degrés à sa direction actuelle
```
## Autre Requis
```
- À implémenter:
  - Dans la méthode deplacer(self) de la classe Robot, implémenter le déplacement du robot. Dans la section TODO, ajouter le code
    qui va calculer la nouvelle position du robot. Le robot se déplace dans la direction indiquée par la propriété direction du robot à
    une vitesse donnée par la variable vitesse du robot.
  - Dans la méthode mise_a_jour_jeu(self) de la classe Jeu, implémenter le déplacement du projectile. Dans la section TODO, ajouter le code
    qui va calculer la nouvelle position du projectile. Le projectile se déplace dans la direction indiquée par la propriété direction du projectile à
    une vitesse donnée par la variable vitesse du projectile.
```

# Évaluation
Ce travail pratique compte pour 25% de la note finale et fait partie de l'épreuve terminale de cours.
```
La répartition des points est comme suit:
    - Implémentation RandyBot: 5pts
    - Implémentation MathBot: 5pts
    - Implémentation CampeurBot: 5pts
    - Implémentation SuperBot: 5pts
    - Autres requis: 5pts
```
Des points seront enlevés pour le non-respect des PEP-008
Possibilité de points bonis qui peuvent ajouter jusqu'à 5%. Il est donc possible d'avoir 30/25.

## Points bonis (5pts)
```
- implémenter un log du combat
  - Ajouter du code qui va créer un fichier nommé "partie_x.log" où "x" est le numéro de la partie débutant à 1.
    - ex: si "partie_1.log" existe, un fichier "partie_2.log" devra être créé
    - Le fichier devra être un fichier texte avec le format suivant:
      - À chaque instruction d'un robot, ajouter une ligne avec le format "etape_jeu::nom_robot::instruction"
        - où etape_jeu est la valeur de la variable self.__etape_jeu de la classe Jeu
        - où nom_robot est le nom du robot exécutant l'instruction
        - où instruction est l'instruction exécutée
      - Générer seulement si self.__etape_jeu <= 30
```

## À propos des TODO
Pour vous aider, les TODOs ont été ajoutés pour vous permettre de consulter la liste dans PyCharm.
Cependant, ceci va causer un message d'avertissement lors du premier commit à partir du projet. Vous pouvez choisir l'option permettant
de faire le commit quand même ou vous pouvez désactiver la vérification des TODOs.

```
File | Settings | Version Control | Commit sur Windows et Linux
PyCharm | Settings | Version Control | Commit sur macOS

Before Commit
  Check TODO -> décocher
```