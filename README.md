# La grande bataille des robots 2024

La grande bataille des robots est l'évènement tant attendu par tous les férus de robotique.
Vous devez implémenter le système de chargement de la configuration des divers robots.

# Prérequis
- Créer un environnement virtuel (venv)
- Python >= 3.10
- installer le package "PySide6"

# Explications
Le module bataillerobots.py contient toutes les classes nécessaires à la grande bataille des robots.
## Classe ChampBataille
Cette classe implémente l'interface graphique. Ne pas toucher à cette classe.
## Classe SpriteJeu
Cette classe abstraite définie une entité pouvant être dessinée (Robot, Projectile).
Contient les propriétés:
    - pos_x
        - la position en X sur le champ de bataille 
    - pos_y
        - la position en y sur le champ de bataille
        - l'axe des y est inversé, les valeurs positives sont vers le bas
    - direction
        - la direction vers laquelle le Sprite est aligné en degré
        - l'angle se calcule dans la direction horaire au lieu de la direction antihoraire
            - par exemple, un Sprite avec une direction de 90 degrés sera aligné vers le bas 
## Classe Robot
Classe abstraite représentant un robot.
Contient les propriétés:
    - sante
        - la santé du robot, si la sante d'un robot tombe à 0, il se brise
    - vitesse
        - la vitesse en pixel à laquelle le robot se déplace
    **Note: Le total de la santé et de la vitesse doit donner 100.**
    - 

## Classe Jeu


# Requis


# Évaluation
Ce travail pratique compte pour 25% de la note finale et fait partie de l'épreuve terminale de cours.