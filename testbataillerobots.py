import unittest

from PySide6.QtWidgets import QApplication

from bataillerobots import Robot, RandyBot, MathBot, SuperBot, CampeurBot, Jeu, Projectile, ChampBataille
from collections import deque

class TestBatailleRobots(unittest.TestCase):

    def setUp(self):
        super().setUp()

    def test_randybot_configuration(self):
        randybot = RandyBot(10, 10, 0)
        randybot.charger_configuration()
        self.assertEqual(randybot.nom, "RandyBot")
        self.assertEqual(randybot.sante, 75)
        self.assertEqual(randybot.vitesse, 25)
        self.assertEqual(randybot.vitesse_projectile, 25)
        self.assertEqual(randybot.puissance_projectile, 25)
        self.assertEqual(randybot.instructions, deque(["tirer", "deplacer", "rotation"]))

    def test_mathbot_configuration(self):
        mathbot = MathBot(10, 10, 0)
        mathbot.charger_configuration()
        self.assertEqual(mathbot.nom, "MathBot")
        self.assertEqual(mathbot.sante, 10)
        self.assertEqual(mathbot.vitesse, 90)
        self.assertEqual(mathbot.vitesse_projectile, 20)
        self.assertEqual(mathbot.puissance_projectile, 30)
        self.assertEqual(mathbot.instructions, deque(["deplacer", "rotation", "tirer", "rotation", "tirer", "deplacer",
                                                "deplacer", "party", "rotation", "tirer"]))

    def test_superbot_configuration(self):
        superbot = SuperBot(10, 10, 0)
        superbot.charger_configuration()
        self.assertEqual(superbot.nom, "SuperBot")
        self.assertEqual(superbot.sante, 100)
        self.assertEqual(superbot.vitesse, 50)
        self.assertEqual(superbot.vitesse_projectile, 25)
        self.assertEqual(superbot.puissance_projectile, 25)
        self.assertEqual(superbot.instructions, deque(['tirer', 'deplacer', 'rotation', 'tirer']))

    def test_campeurbot_configuration(self):
        campeurbot = CampeurBot(10, 10, 0)
        campeurbot.charger_configuration()
        self.assertEqual(campeurbot.nom, "CampeurBot")
        self.assertEqual(campeurbot.sante, 80)
        self.assertEqual(campeurbot.vitesse, 20)
        self.assertEqual(campeurbot.vitesse_projectile, 20)
        self.assertEqual(campeurbot.puissance_projectile, 30)
        self.assertEqual(campeurbot.instructions, deque(["tirer", "rotation"]))

    def test_randybot_rotation(self):
        randybot = RandyBot(10, 10, 0)
        randybot.rotation()
        self.assertIn(randybot.direction, range(0, 360))

    def test_mathbot_rotation(self):
        mathbot = MathBot(10, 10, 0)
        mathbot.rotation()
        premiere_rotation = TestBatailleRobots.__calcul_rotation_mathbot(6.8, -6, -18.7, 0)
        self.assertEqual(mathbot.direction, premiere_rotation)
        deuxieme_rotation = TestBatailleRobots.__calcul_rotation_mathbot(12.8, 6, -0.8, 0)
        self.assertEqual(mathbot.direction, deuxieme_rotation)
        troisieme_rotation = TestBatailleRobots.__calcul_rotation_mathbot(-3.6, -7.1, -10.5, 0.2)
        self.assertEqual(mathbot.direction, troisieme_rotation)

    def test_superbot_rotation(self):
        superbot = SuperBot(10, 10, 0)
        superbot.rotation()
        self.assertEqual(superbot.direction, 60)
        superbot.rotation()
        self.assertEqual(superbot.direction, 30)
        superbot.rotation()
        self.assertEqual(superbot.direction, 90)

    def test_campeurbot_rotation(self):
        campeurbot = CampeurBot(10, 10, 0)
        campeurbot.rotation()
        self.assertEqual(campeurbot.direction, 15)
        campeurbot.direction = 350
        campeurbot.rotation()
        self.assertEqual(campeurbot.direction, 5)

    def test_deplacement_robot(self):
        randybot = RandyBot(10, 10, 0)
        randybot.deplacer()
        self.assertEqual(randybot.pos_x, 30)
        self.assertEqual(randybot.pos_y, 10)
        randybot.direction = 90
        randybot.deplacer()
        self.assertEqual(randybot.pos_x, 30)
        self.assertEqual(randybot.pos_y, 30)
        randybot.direction = 135
        randybot.deplacer()
        self.assertEqual(randybot.pos_x, 30-14)
        self.assertEqual(randybot.pos_y, 30+14)

    # TODO: ajouter un getter de robots à Jeu pour tester les projectiles et remplacer le "name mangling"
    def test_deplacement_projectile(self):
        app = QApplication()
        champ = ChampBataille()
        jeu = Jeu(champ)
        robot = RandyBot(10, 10, 0)

        jeu.debuter([robot])

        robot.vitesse_projectile = 25
        robot.puissance_projectile = 25
        robot.tirer()
        projectile = robot.projectiles[0]

        jeu.mise_a_jour_jeu()
        self.assertEqual(projectile.pos_x, 35)






    def tearDown(self):
        super().tearDown()

    @staticmethod
    def __calcul_rotation_mathbot(maximale, moyenne, minimale, precipitations):
        return float((abs(maximale)**abs(moyenne) * abs(minimale) + precipitations) % 360)
