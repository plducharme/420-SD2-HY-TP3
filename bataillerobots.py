import math
import random
from abc import ABC, abstractmethod
from collections import deque
from typing import List
import pickle

from PySide6.QtCore import QSize, QRect, QTimer
from PySide6.QtGui import QPainter, QPen, QColorConstants, QPixmap, QTransform
from PySide6.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QMainWindow, QPushButton, \
    QComboBox


###########################
# nom1 (utilisateur github)
# nom2 (utilisateur github)
# nom3 (utilisateur github)
##########################
class ChampBataille(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("La grande bataille de robots 2024")
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        disposition = QVBoxLayout()
        self.widget_central.setLayout(disposition)

        controles_widget = QWidget()
        self.robot1 = QComboBox()
        self.robot1.addItems(["RandyBot", "MathBot", "CampeurBot", "SuperBot"])
        self.robot2 = QComboBox()
        self.robot2.addItems(["RandyBot", "MathBot", "CampeurBot", "SuperBot"])

        disposition_controles = QHBoxLayout()
        controles_widget.setLayout(disposition_controles)
        disposition_controles.addWidget(self.robot1)
        disposition_controles.addWidget(self.robot2)
        self.bouton_bataille = QPushButton("Destruction!")
        disposition_controles.addWidget(self.bouton_bataille)
        self.bouton_bataille.clicked.connect(self.bouton_bataille_clicked)
        disposition.addWidget(controles_widget)

        self.canevas = QLabel()
        self.canevas.setFixedSize(Jeu.LARGEUR, Jeu.HAUTEUR)
        disposition.addWidget(self.canevas)

        self.jeu = Jeu(self)
        self.timer = None

    def recommencer(self):
        pass

    def bouton_bataille_clicked(self):
        self.bouton_bataille.hide()
        robots = [self.robot1.currentText(), self.robot2.currentText()]
        self.jeu.debuter(robots)
        self.timer = QTimer()
        self.timer.setInterval(333)
        self.timer.start()
        self.timer.timeout.connect(self.jeu.boucle_jeu)


class SpriteJeu(ABC):

    def __init__(self, pos_x: int, pos_y: int, direction: float):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._direction = direction

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, pos_x):
        self._pos_x = pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, pos_y):
        self._pos_y = pos_y

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    @abstractmethod
    def dessiner(self, canevas: QLabel):
        pass


class Robot(SpriteJeu, ABC):

    def __init__(self, pos_x: int, pos_y: int, direction: float):
        super().__init__(pos_x, pos_y, direction)
        self._nom = "Robot"
        # "https://www.flaticon.com/free-icons/chatbot"
        self._qpixmap = QPixmap(f"./images/robot.png")
        self._qpixmap.scaled(QSize(64, 64))
        self._sante = 0
        self._vitesse = 0
        self._instructions = deque()
        self._puissance_projectile = 0
        self._vitesse_projectile = 0
        self._projectiles = []

    @property
    def vitesse(self):
        return self._vitesse

    @vitesse.setter
    def vitesse(self, vitesse):
        self._vitesse = vitesse

    @property
    def projectiles(self):
        return self._projectiles

    @projectiles.setter
    def projectiles(self, projectiles):
        self._projectiles = projectiles

    @property
    def vitesse_projectile(self):
        return self._vitesse_projectile

    @vitesse_projectile.setter
    def vitesse_projectile(self, vitesse_projectile):
        self._vitesse_projectile = vitesse_projectile

    @property
    def puissance_projectile(self):
        return self._puissance_projectile

    @puissance_projectile.setter
    def puissance_projectile(self, puissance_projectile):
        self._puissance_projectile = puissance_projectile

    @property
    def instructions(self) -> deque:
        return self._instructions

    @instructions.setter
    def instructions(self, instructions: deque):
        self._instructions = instructions

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        self._nom = value

    @property
    def qpixmap(self):
        return self._qpixmap

    @qpixmap.setter
    def qpixmap(self, value):
        self._qpixmap = value

    @property
    def sante(self):
        return self._sante

    @sante.setter
    def sante(self, value):
        self._sante = value

    def charger_configuration_defaut(self):
        self.sante = 80
        self.vitesse = 20
        self.puissance_projectile = 25
        self.vitesse_projectile = 25
        self.instructions.append(Jeu.TIRER)
        self.instructions.append(Jeu.ROTATION)
        self.instructions.append(Jeu.DEPLACER)
        self.nom = random.choice(["Robotron", "Ferraille", "Rouille", "Jeff", "Anna"])

    # Ne pas toucher
    def dessiner(self, canevas: QPixmap):
        painter = QPainter(canevas)
        transform = QTransform()
        transform.translate(self._pos_x, self._pos_y)
        # transform.rotate(self._direction)
        painter.setTransform(transform)
        painter.drawPixmap(QRect(0, 0, 64, 64), self._qpixmap)
        painter.end()
        # print(f"{self.nom}: ({self.pos_x},{self.pos_y}) {self.direction}")

    def prochaine_instruction(self):
        prochaine_instruction = self._instructions.popleft()
        match prochaine_instruction:
            case Jeu.DEPLACER:
                self.deplacer()
            case Jeu.ROTATION:
                self.rotation()
            case Jeu.TIRER:
                self.tirer()
            case _:
                pass

        self._instructions.append(prochaine_instruction)

    def deplacer(self):
        # TODO implémenter le déplacement du robot

        # Fin TODO
        # Si le robot se déplace à l'extérieur, on le remet sur le côté
        if self.pos_x < 0:
            self.pos_x = 0
        elif self.pos_x > Jeu.LARGEUR:
            self.pos_x = Jeu.LARGEUR - 32
        elif self.pos_y < 0:
            self.pos_y = 0
        elif self.pos_y > Jeu.HAUTEUR:
            self.pos_y = Jeu.HAUTEUR - 32

    @abstractmethod
    def rotation(self):
        pass

    @abstractmethod
    def charger_configuration(self):
        pass

    def tirer(self):
        pos_x = int(64 * math.cos(math.radians(self.direction)))
        pos_y = int(64 * math.sin(math.radians(self.direction)))
        projectile = Projectile(self.pos_x + pos_x, self.pos_y + pos_y, self.direction, self.puissance_projectile,
                                self.vitesse_projectile)
        # print(f"Projectile généré à ({self.pos_x + pos_x},{self.pos_y + pos_y}) {self.direction}")
        self._projectiles.append(projectile)


class RandyBot(Robot):

    # TODO à implémenter
    def rotation(self):
        pass

    # TODO à implémenter
    def charger_configuration(self):
        self.charger_configuration_defaut()


class MathBot(Robot):
    # TODO à implémenter
    def rotation(self):
        pass

    # TODO à implémenter
    def charger_configuration(self):
        self.charger_configuration_defaut()


class CampeurBot(Robot):
    # TODO à implémenter
    def rotation(self):
        pass

    # TODO à implémenter
    def charger_configuration(self):
        self.charger_configuration_defaut()


class SuperBot(Robot):
    # TODO à implémenter
    def rotation(self):
        pass

    # TODO à implémenter
    def charger_configuration(self):
        self.charger_configuration_defaut()


class Projectile(SpriteJeu):

    def __init__(self, pos_x: int, pos_y: int, direction: float, puissance: int, vitesse: int):
        super().__init__(pos_x, pos_y, direction)
        if puissance + vitesse != 50:
            raise ValueError("Projectile prohibé! La vitesse plus la puissance ne donne pas 50! La GRC est en chemin!")
        if vitesse > 30:
            raise ValueError("Projectile prohibé! La vitesse maximale est de 30")
        self.__puissance = puissance
        self.__vitesse = vitesse
        self.__image = QPixmap("./images/projectile.png")
        self.__image.scaled(QSize(32, 32))

    @property
    def vitesse(self):
        return self.__vitesse

    @vitesse.setter
    def vitesse(self, vitesse):
        self.__vitesse = vitesse

    @property
    def puissance(self):
        return self.__puissance

    @puissance.setter
    def puissance(self, puissance):
        self.__puissance = puissance

    def dessiner(self, canevas: QPixmap):
        painter = QPainter(canevas)
        crayon = QPen()
        crayon.setColor(QColorConstants.Red)
        painter.translate(self.pos_x, self.pos_y)
        # painter.rotate(self.direction)
        painter.drawPixmap(QRect(0, 0, 32, 32), self.__image)
        painter.end()
        # print(f"projectile:({self.pos_x},{self.pos_y})")


class Jeu:
    LARGEUR = 800
    HAUTEUR = 600
    DEPLACER = "deplacer"
    TIRER = "tirer"
    ROTATION = "rotation"

    def __init__(self, vue: ChampBataille):
        self.__en_cours = False
        self.__termine = False
        self.__vue = vue
        self.__etape_jeu = 0
        self.__robots = []
        self.__gagnant = None
        self.__partie_nulle = False

        # href = "https://stockcake.com/i/vibrant-fireworks-display_273737_54656"
        self._ecran_fin = QPixmap("./images/feux.jpg")
        self._ecran_fin.scaled(QSize(Jeu.LARGEUR, Jeu.HAUTEUR))

    def debuter(self, liste_robots):
        emplacements = Jeu.generer_emplacements_depart()
        self.__etape_jeu = 0
        for nom_robot in liste_robots:

            match nom_robot:
                case "RandyBot":
                    emplacement = emplacements.pop()
                    print(f"RandyBot généré à ({emplacement[0]},{emplacement[1]},{emplacement[2]})")
                    robot = RandyBot(emplacement[0], emplacement[1], emplacement[2])
                    robot.charger_configuration()
                    self.__robots.append(robot)
                case "MathBot":
                    emplacement = emplacements.pop()
                    print(f"MathBot généré à ({emplacement[0]},{emplacement[1]},{emplacement[2]})")
                    robot = MathBot(emplacement[0], emplacement[1], emplacement[2])
                    robot.charger_configuration()
                    self.__robots.append(robot)
                case "CampeurBot":
                    emplacement = emplacements.pop()
                    print(f"CampeurBot généré à ({emplacement[0]},{emplacement[1]},{emplacement[2]})")
                    robot = CampeurBot(emplacement[0], emplacement[1], emplacement[2])
                    robot.charger_configuration()
                    self.__robots.append(robot)
                case "SuperBot":
                    emplacement = emplacements.pop()
                    print(f"SuperBot généré à ({emplacement[0]},{emplacement[1]},{emplacement[2]})")
                    robot = SuperBot(emplacement[0], emplacement[1], emplacement[2])
                    robot.charger_configuration()
                    self.__robots.append(robot)
                case _:
                    raise ValueError(f"Robot inconnu: {nom_robot}")

    @staticmethod
    def generer_emplacements_depart():
        # (x, y, direction)
        gauche = (random.randint(75, 125), random.randint(350, 400), 0)
        droit = (random.randint(600, 650), random.randint(350, 400), 180)

        return [gauche, droit]

    def mise_a_jour_jeu(self):
        if self.__etape_jeu % 3 == 0:
            for robot in self.__robots:
                robot.prochaine_instruction()

        for robot in self.__robots:
            for projectile in robot.projectiles:
                # on bouge le projectile dans la bonne direction
                # TODO Implémenter le déplacement du projectile

                # Fin TODO
                # on vérifie si le projectile touche un robot
                self.verifier_collision(projectile)
                # si le projectile sort du champ de bataille, on le détruit
                if projectile.pos_x < 0 or projectile.pos_x > Jeu.LARGEUR:
                    del projectile
                elif projectile.pos_y < 0 or projectile.pos_y > Jeu.HAUTEUR:
                    del projectile

        self.__etape_jeu += 1

    def verifier_collision(self, projectile: Projectile):
        for robot in self.__robots:
            if (projectile.pos_x + 32 in range(robot.pos_x, robot.pos_x + 64) and projectile.pos_y + 32 in
                    range(robot.pos_y, robot.pos_y + 64)):
                # on diminue la santé du robot touché
                robot.sante -= projectile.puissance
                print(f"{robot.nom} touché! Santé {robot.sante}")

    def boucle_jeu(self):

        if self.__termine:
            self.dessiner_ecran_fin(self.__vue.canevas)
            return

        self.mise_a_jour_jeu()
        # "https://stockcake.com/i/charred-earth-texture_238671_45779"
        arriere_plan = QPixmap("./images/sol.jpg")
        arriere_plan.scaled(QSize(Jeu.LARGEUR, Jeu.HAUTEUR))
        pixmap = arriere_plan
        self.dessiner_robots(pixmap)
        self.__vue.canevas.setPixmap(pixmap)
        self.verifier_fin_jeu()

    def dessiner_ecran_fin(self, canevas: QLabel):

        if self.__partie_nulle:
            painter = QPainter(canevas)
            painter.fillRect(0, 0, Jeu.LARGEUR, Jeu.HAUTEUR)
            painter.drawText(200, 250, "Partie Nulle!")
            painter.end()
        else:
            painter = QPainter(self._ecran_fin)
            painter.drawText(200, 250, f"Le gagnant est {self.__gagnant}")
            canevas.setPixmap(self._ecran_fin)
            painter.end()

    def dessiner_robots(self, canevas: QPixmap):
        for robot in self.__robots:
            robot.dessiner(canevas)
            for projectile in robot.projectiles:
                projectile.dessiner(canevas)

    def verifier_fin_jeu(self):
        # Le compte de robots brisés (santé <= 0)
        compte_brise = 0
        for robot in self.__robots:
            if robot.sante <= 0:
                compte_brise += 1
        # On a un gagnant (un robot restant)
        if len(self.__robots) - compte_brise == 1:
            self.__termine = True
            # on trouve le gagnant
            for robot in self.__robots:
                if robot.sante > 0:
                    self.__gagnant = robot.nom
        # Partie Nulle
        elif len(self.__robots) - compte_brise == 0:
            self.__termine = True
            self.__partie_nulle = True


# Ne pas toucher à la classe PickleConfig
class PickleConfig:

    def __init__(self, nom: str, vitesse: int, sante: int, puissance_projectile: int, vitesse_projectile: int,
                 instructions: List[str]):
        self.__nom = nom
        self.__vitesse = vitesse
        self.__sante = sante
        self.__puissance_projectile = puissance_projectile
        self.__vitesse_projectile = vitesse_projectile
        self.__instructions = instructions

    @property
    def nom(self):
        return self.__nom

    @property
    def vitesse(self):
        return self.__vitesse

    @property
    def sante(self):
        return self.__sante

    @property
    def puissance_projectile(self):
        return self.__puissance_projectile

    @property
    def vitesse_projectile(self):
        return self.__vitesse_projectile

    @property
    def instructions(self):
        return self.__instructions


if __name__ == '__main__':
    # Code d'exécution, ne pas toucher
    app = QApplication()
    champ = ChampBataille()
    champ.show()
    app.exec()
