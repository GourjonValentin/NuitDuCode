# Space Shooter

Projet réaliser suite à la **Nuit Du Code**

Il s'agit d'une imitation du jeu *Space invaders* en utilisant la bibliothèque graphique `pyxel` en python.

## Installation

Pour installer le projet, il suffit de cloner le dépôt et d'installer les dépendances.

```bash
git clone
pip install pyxel
```

## Lancement

Pour lancer le jeu, il suffit de lancer le fichier `main.py`.

```bash
python main.py
```

## Règles

Le but du jeu est de détruire les ennemis qui descendent vers le joueur.

A chaque ennemi détruit, le joueur gagne des points, et un objet peut tomber au sol.

Le joueur peut ramasser ces objets pour améliorer son vaisseau ou récupérer de la vie.

Le jeu se termine si le joueur n'a plus de vie.

## Commandes

| Commande         | Description                |
|------------------|----------------------------|
| Flèche du haut   | Déplacement vers le haut   |
| Flèche du bas    | Déplacement vers le bas    |
| Flèche de gauche | Déplacement vers la gauche |
| Flèche de droite | Déplacement vers la droite |
| Espace           | Tirer                      |
| P                | Pause                      |
| Q                | Quitter                    |