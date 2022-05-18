# Projet-CMI-L2-
Théo Lavandier Mathilde Tissandier : PROJET CMI

Bonjour,
Dans le cadre de notre formation nous avons du créer un site internet reprenant les données du fichier csv : Pyrenees.
Nous avions pour consigne de reprendre ce fichier et de coder une base de données avec SQLite. Nous avons dans notre code data fait cela :
## Data :
### La database :
![Capture d’écran 2022-05-18 151754](https://user-images.githubusercontent.com/102798509/169049544-cb0c76dc-b763-4cd3-9bfa-f7cfec376ea0.png)

Nous commençons donc par faire les import qui nous serons primordiales pour la suite de notre code.

![Capture3](https://user-images.githubusercontent.com/102798483/169115581-b5fc8483-9973-48c4-b6eb-fc8589b7f0ac.PNG)

On fait notre première table, elle se nomme valley. On y met dedans un id qui s'incrémente automatiquement en commençant par 1 ainsi que les valleys : Ossau et Luz.

![Capture d’écran 2022-05-18 153343](https://user-images.githubusercontent.com/102798509/169051414-19694d37-f5ad-4c34-9590-9e16ac784dfe.png)

On fait notre deuxième table, elle se nome stations. On y met dedans un id qui s'incrémente automatiquement en commençant par 1. On y met le nom des stations, leur rang (range), leur altitude (Altitude), leur latitude (lat), leur longitude (lon) et on y met un id_valley qui sera une clé étrangère. Cette clé rajoutera une colonne dans laquelle on aura l'id de la valley qui correspond à 1 ou 2. (Chaque station est dans une des deux valleys).

![Capture d’écran 2022-05-18 153915](https://user-images.githubusercontent.com/102798509/169052493-f39f18ef-cb5a-4cac-a46b-0a3f0959a8d0.png)

On fait notre troisième table, elle se nomme arbre. On y met dedans un id qui s'incrémente automatiquement en commençant par 1. On y met le code de chaque arbre, l'espèce (Species), le volume du houppier (VH), la hauteur (H), la surface de projection du houppier (SH) et on y met un id_station qui sera une clé étrangère. Cette clé rajoutera une colonne dans laquelle on aura l'id de la station compris entre 1 et 10. (Chaque arbre est dans une des dix stations).

![Capture d’écran 2022-05-18 154453](https://user-images.githubusercontent.com/102798509/169054477-a7f9c47f-bf6d-46f3-af38-fdd7ad1b801a.png)

On fait notre dernière table, elle se nomme récolte. On y met dedans un id_r qui s'incrémente automatiquement en commençant par 1. ON y met l'id (ID) de la récolte, la semaine de récolte en jour julien (harv_num), le jour de récolte en jour julien (DD), la semaine de récolte en jour julien (harv), l'année (Year), la date (Date), la masse totale de glands (Mtot), la quantité totale de glands produits (Ntot), la quantité totale de glands produits sans les fruits mis à germer et sans les glands détérioré. Estimation de oneacorn se fait à partir de Ntot1 (Ntot1), la masse moyenne d'un gland (oneacorn), la quantité totale de glands mis à germer (tot_Germ), la masse des glands mis à germer (M_Germ), le nombre de glands qui ont gérmé (N_Germ), le ratio de glands qui ont germé (%) (rate_Germ) et on y met un id_arbre qui sera une clé étrangère. Cette clé rajoutera une colonne dans laquelle on aura l'id d'arbre compris entre 1 et 31. (Chaque station se trouve forcément dans un arbre).

Nous avons maintenant une base de données mais celle-ci est vide. IL nous faut donc la remplir.

![Capture2](https://user-images.githubusercontent.com/102798483/169114778-513218af-c2e5-4d35-b443-91c86eb8834d.PNG)

On commence par ouvrir le fichier csv et on se met en mode Reader (c'est pour pouvoir le lire). On fait une boucle for qui va parcourir entièrement le fichier. On commence avec une première requête query, on va sélectionner l'id de la station, ensuite, si on voit que les données de la table stations sont nulles, on va la remplir avec la deuxième requête query et l'exécuter avec : cur.execute(query).

![image](https://user-images.githubusercontent.com/102798509/169068474-ed5ca6f0-9c5a-4a3d-9fc2-726225fcf7e8.png)

On fait une nouvelle requête query, on va sélectionner l'id de la valley, ensuite, si on voit que les données de la table valley sont nulles, on va la remplir avec la deuxième requête query et l'exécuter avec : cur.execute(query).

![image](https://user-images.githubusercontent.com/102798509/169068926-57d9be88-7c50-4327-a176-5e9f71a185de.png)

On fait une nouvelle requête query, on va sélectionner l'id de l'arbre, ensuite, si on voit que les données de la table arbre sont nulles, on va la remplir avec la deuxième requête query et l'exécuter avec : cur.execute(query).

![Capture d’écran 2022-05-18 164238](https://user-images.githubusercontent.com/102798509/169069300-dcf34775-93e6-4054-b85c-a6a0eb04ed6c.png)

On fait une nouvelle requête query, on va sélectionner l'id_r de la récolte, ensuite, si on voit que les données de la table récolte sont nulles, on va la remplir avec la deuxième requête query et l'exécuter avec : cur.execute(query).

Ensuite, on va pouvoir s'occuper des clés étrangères. Les colonnes des clés étrangères sont remplies avec des 0.

![Capture d’écran 2022-05-18 164723](https://user-images.githubusercontent.com/102798509/169070451-03b45aa0-e1b2-4898-bf1e-0459db5d209e.png)

On commence par ouvrir le fichier csv et on se met en mode Reader (c'est pour pouvoir le lire). On fait une boucle for qui va parcourir entièrement le fichier. On commence avec une première requête query, on va sélectionner id_valley donc la clé étrangère de la table Station. Si cette clé est nulle, il faut faire une nouvelle requête query dans laquelle on va affecter à id_valley : valley.id, on va donc lier les tables Station et valley.

![Capture d’écran 2022-05-18 170542](https://user-images.githubusercontent.com/102798509/169074547-2842a742-5116-4c90-9f3a-3149f657cdc6.png)

On fait une nouvelle requête query, on va sélectionner id_station donc la clé étrangère de la table arbre. Si cette clé est nulle, il faut faire une nouvelle requête query dans laquelle on va affecter à id_station : Station.id, on va donc lier les tables arbre et Station.

![image](https://user-images.githubusercontent.com/102798509/169075766-be4467d2-c90d-4dcd-97aa-c71230bfe173.png)

On fait une nouvelle requête query, on va sélectionner id_arbre donc la clé étrangère de la table récolte. Si cette clé est nulle, il faut faire une nouvelle requête query dans laquelle on va affecter à id_arbre : récolte.id, on va donc lier les tables arbre et récolte.

![Capture d’écran 2022-05-18 171604](https://user-images.githubusercontent.com/102798509/169077441-5e7bc678-67a5-4a8e-8800-6f17406820a0.png)

Comme on avait la longitude et la latitude dans la table Station, il fallait la remplir. Cependant, dans notre csv nous n'avions pas de données la dessus. Nous avons donc du les rechercher sur internet et les rentrer à la main une par une d'où la longueur (sans oublier cur.execute(query) à chaque fois).

### Le code :

![Capture](https://user-images.githubusercontent.com/102798483/169113606-ec9f7d99-7b14-4c6e-9b72-0a056202b2a7.PNG)

On a ici 3 fonctions. La première get_valley va retourner une liste des valleys. La deuxième get_year va retourner une liste des années et la dernière, get_stations, va retourner la liste des stations. On utilise ces 3 fonctions pour construire les dropdowns plus tard.

![Capture d’écran 2022-05-18 205613](https://user-images.githubusercontent.com/102798509/169131681-62f574ac-9e7b-4e6c-b69f-9ea26610c2e2.png)






## Le GUI :

![Capture4](https://user-images.githubusercontent.com/102798483/169116847-a0b022d6-eed5-481c-9ce0-e274c839d8b1.PNG)

Comme pour la partie data, on commence par faire les import qui nous serons primordiales pour la suite de notre code.

### Le code :
![image](https://user-images.githubusercontent.com/102798509/169085672-c657230c-24d2-4287-bca2-b8aa8a12fe91.png)

![Capture d’écran 2022-05-18 205941](https://user-images.githubusercontent.com/102798509/169135421-e2410eea-b6db-4d75-81bf-c6e28dd6ac98.png)

On créé ici un dropdown. Quand on l'appliquera, il sera possible de sélectionner plusieurs éléments : multi=True et, quand on aura au début que tous les éléments seront sélectionnés : value=item_list. On a ici un exemple de dropdown produit par le code.

![Capture d’écran 2022-05-18 205751](https://user-images.githubusercontent.com/102798509/169133031-a72b50d2-65d5-41d0-8e43-a798ba772222.png)

![Capture d’écran 2022-05-18 175145](https://user-images.githubusercontent.com/102798509/169086900-1cd6d66f-38ff-437c-94e0-0c289cab363f.png)

Cette fonction permet d'initialiser un graph, elle sera utilisée pour tous les graphiques.

![Capture d’écran 2022-05-18 210407](https://user-images.githubusercontent.com/102798509/169136186-1e3ab275-a56a-45ca-b049-326efb7f6cbd.png)



## Le DASHAPP :


