# Paperzoom
Dispositif d'exploration numérique avec une kinect et une feuille de papier

## Démarrage
1. Allumer le vidéoprojecteur avec la télécommande noire
2. wakeUp avec l'application web de lab_monitoring : charge le scénario de la fouille de l'Antiquaille
3. Brancher un clavier et appuyer sur les touches numériques pour afficher un scénario particulier

### Déroulement de scripts
Note : le python qui se lance automatiquement au boot n'est pas Bureau/Labs/Paperzoom.py mais Kinect-2012-clean/Kinect/PaperKinect-2012-21.py grâce au script de monitoring


### Procédure d'extinction
Éteindre le VP

----------

## Calibration
- le script ``Paperzoom.py``permet la calibration "Live" avec des sliders intégrés
- Afficher les sliders avec la touche `w` : 

### Description des sliders de Gauche à droite:
* **1er groupe de slider** : Transformations du masque créé par la Kinect (à adapter en cas de déplacement de la Kinect ou de retaillage du carton)
  * Scale X
  * Scale Y
  * Position X
  * Position Y
* **2eme et 3eme groupe de sliders** : Pas de fonction relevée
* **4eme groupe de sliders** (un seul slider)
  * Zoom, dezoom de l'image globale (Fond + Masque Kinect)
* **5eme groupe de sliders** Déplacement du coin supérieur droit de l'image, permet de corriger le trapéze
  * en X
  * en Y
* **6eme groupe de sliders** Réglage des seuils hauts et bas de l'interaction
  * seuil bas : mettre la feuille au plus proche de la table, mais au moins 15 cm. Manipuler le slider pour faire juste apparaitre le rectangle
  * seuil haut : Régler ce slider pour faire régler l'écart entre les couches
  * non opérant
 



