# DSTK

<!-- <img src=`docs/source/_static/dstk.png` width=`200`/> -->
![](docs/source/_static/dstk.png)

- Free software: Apache Software License 2.0

# Overview

**DSTK** est une libraire haut-niveau pour faciliter le développement et le déploiment d'outil de machine learning. Il s'articule essentiellement autour de 2 outils :
  * PyTorch ;
  * Scikit-Learn.

L'ancien nom x250 faisait référence au code boite X250 qui est le code boite de datalabs/IA Factory. Le développement de ce package est étroitement lié au développement du template data science (qui aujourd'hui a fusionné avec le socle Python).

**DTSK** est compatible avec `Python >= 3.5`, mais `Python >= 3.8` est fortement recommandé.

# Documentation

[Une documentation Sphinx hébergée par Read the Docs est disponible.](https://x250.readthedocs.io/en/latest/index.html "Document DSTK")

# Installation

Pour installer DSTK utiliser la commande : `pip install dstk-x250`.

## Release Notes

### 3.0

  * Changement de nom, **la librairie x250 devient DSTK** afin d'être rendu publique sur PyPi dans un premiet temps et sur conda dans un second.

### 2.0

  * Résolutions de bugs diverses.
  * Concept de Callback pour x250.pytorch permettant de rendre la partie entraînement plus modulaire et lisible.
  * Intégration du concept de SWA (Stochastic Weight Averaging) pour rendre les modèles plus robuste à l'inférence.

### 1.0

  * Séparation du template data science et des _utils.py afin d'être intégré au socle Python d'Arkéa.
  * Création du package x250 restructurant les _utils.py.
  * Intégration de l'utilitaire PyTorch permettant de wrapper un réseau profond à Scikit-Learn simplement.
    
### 0.1

  * Intégration de fonctions et classes utilitaires au template dans des fichiers _utils.py à différent niveau de la structure du template.

### 0.0

  * Création du squelette template data science.
