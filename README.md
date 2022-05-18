# Projet-CMI-L2-
Théo Lavandier Mathilde Tissandier : PROJET CMI

Bonjour,
Dans le cadre de notre formation nous avons du créer un site internet reprenant les données du fichier csv : Pyrenees.
Nous avions pour consigne de reprendre ce fichier et de coder une base de données avec SQLite. Nous avons dans notre code data fait cela :
## LE DATA :
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

Cette fonction prend en argument un connecteur, une liste de station, et un interval range.
Elle permet de retourner un dataframe construit à parir d'une requête SQL. La liste de station et la range 
interviennent quand à eux comme des conditions pour créer notre dataframe. Ici on ne veut que les lignes contenant
la où les stations passées en arguments, et nous voulons trier certaines valeurs en fonction de l'interval range.
Nous avons d'autre fonctions qui fonctionnent en suivant le même principe d'arguments conditions.
Ces dataframes, retournés par nos différentes fonctions, nous permettrons de constuire des graphs avec différentes données.

## LE GUI :

![Capture4](https://user-images.githubusercontent.com/102798483/169116847-a0b022d6-eed5-481c-9ce0-e274c839d8b1.PNG)

Comme pour la partie data, on commence par faire les import qui nous serons primordiales pour la suite de notre code.

### Le code :
![image](https://user-images.githubusercontent.com/102798509/169085672-c657230c-24d2-4287-bca2-b8aa8a12fe91.png)

![Capture d’écran 2022-05-18 205941](https://user-images.githubusercontent.com/102798509/169135421-e2410eea-b6db-4d75-81bf-c6e28dd6ac98.png)

On créé ici un dropdown. Quand on l'appliquera, il sera possible de sélectionner plusieurs éléments : multi=True et, quand on aura au début que tous les éléments seront sélectionnés : value=item_list. On a ici un exemple de dropdown produit par le code.

![Capture d’écran 2022-05-18 205751](https://user-images.githubusercontent.com/102798509/169133031-a72b50d2-65d5-41d0-8e43-a798ba772222.png)

Ces deux fonctions sont très similaire à notre fonction build_dropdown_menu_options, car elles retournent aussi un composant
Dash. 
	- build_radioitems permet de créer une sorte de liste de valeurs que nous choisissons avec le paramètre item_list.
	 Nous pouvons sélectionner une valeur de cette liste à la fois.
	- build_slider permet de créer une barre latérale, pour pouvoir choisir manuellement une intervalle de valeurs. 
	 Nous devons donc choisir dans notre fonction une intervalle de valeurs. Dans notre cas nous avons choisit [0;55000].
Dans le deux cas, la variable id permet de donner un identifiant id à notre composant, dans le but de pouvoir l'identifier par la suite.

![Capture d’écran 2022-05-18 175145](https://user-images.githubusercontent.com/102798509/169086900-1cd6d66f-38ff-437c-94e0-0c289cab363f.png)

Cette fonction permet d'initialiser un graph, elle sera utilisée pour tous les graphiques.

![Capture d’écran 2022-05-18 210407](https://user-images.githubusercontent.com/102798509/169136186-1e3ab275-a56a-45ca-b049-326efb7f6cbd.png)

Cette fonction permet de créer un scatter plot à partir d'un dataframe placé en paramètre. Dans notre projet, nous utilisons les dataframes
produits par nos fonctions prepare_data ,que nous avons dans la partie précédente, pour nos fonctions build. Les fonctions build
comme celle-ci utilisent la librairy plotly-express pour créer des graphs. Ces graphs seront affichés sur notre app, et seront rendus 
intéractifs.

## LE DASHAPP :

![Capture d’écran 2022-05-18 210654](https://user-images.githubusercontent.com/102798509/169137054-b05da799-86f4-4efa-b3f7-814a2ce3680d.png)

Comme pour les deux autres parties, on commence par faire les import qui nous serons primordiales pour la suite de notre code.

![Capture d’écran 2022-05-18 210913](https://user-images.githubusercontent.com/102798509/169137734-c32c9aad-ab76-4631-819b-0fa952d75c72.png)

Ensuite, on se connecte à notre database Pyrenees.db qui se trouve dans notre répertoire model. On crée un curseur pour pouvoir utiliser et modifier
cette database. Ensuite, si la database n'a pas déjà été créée, on appelle nos fonctions setup_table et csv_into_table, dont nous avons parlé dans la partie
Data. Quand cela est fait, on initialise notre app avec dash.Dash.

Dans notre application, nous avons fait beaucoup de CSS pour mettre en forme cette dernière. Cependant, nous ne nous attarderons pas sur cette
partie pour éviter que cette présentation soit trop longue.

Notre application sera principalement divisée en deux parties :
	-Nous aurons un menu sur la gauche de notre site, nous permettant de se déplacer sur le site dans les differents graphiques.
	-Puis nous aurons une partie contenant les graphiques et les différentes intéractions qui leurs sont associées. 

![Capture d’écran 2022-05-18 211424](https://user-images.githubusercontent.com/102798509/169138571-06f11146-a9b8-4a7e-a52b-02a914879f8c.png)

Voici le code permettant de créer notre menu 'sidebar'. Celui ci est principalement composé de Html. Nous avons le titre de notre application,
'TISSANDIER LAVANDIER', un autre titre sur le thème, une image etc... Mais pricipalement nous utilisons un dbc.Nav. C'est une sorte de navigateur,
qui permet de changer d'url quand on clique sur un bouton de celui-ci. Nous allons voir que c'est grace à celui-ci que nous allons pouvoir 
afficher différents graphiques, de manière distincte, sur notre site.

![Capture d’écran 2022-05-18 211525](https://user-images.githubusercontent.com/102798509/169138788-6ae048d0-ea58-4239-a09b-eb3425a7a7da.png)

Puis nous avons le code qui permet de créer la partie contenant les graphiques; notre 'content'. Nous allons voir que son contenu 
dépendra de l'url de notre site.

![Capture d’écran 2022-05-18 211739](https://user-images.githubusercontent.com/102798509/169139115-a6b4dd41-23ef-446f-94fd-8737e3a0ffbd.png)

Nous regroupons ces deux parties de notre app.layout. 

![Capture d’écran 2022-05-18 211840](https://user-images.githubusercontent.com/102798509/169139359-41a6bfc7-012b-4fbe-8c2b-6f08b46a8931.png)
![Capture d’écran 2022-05-18 211909](https://user-images.githubusercontent.com/102798509/169139400-96e775cb-4aaa-4e98-93f2-2dd2cc62f715.png)

Nous avons ensuite notre première fonction utilisant un callback. Cette fonction permet de mettre à jour la partie 'content' de notre site,
en fonction de l'url de ce dernier. On voit que le callback a pour input notre url, défini dans notre layout, et pour output page-content, 
l'id de notre partie 'content'.
Le paramètre de notre est fonction est pathname, c'est le pathname de l'url sur lequel on se trouve.
Ici, on voit que si l'on se trouve sur le pathname "/piechart", alors on renvoit dans content deux dropdown, un sur les valleys, et un sur
les years. On renvoit également un graph d'id 'piechart'. Cette fonction permet donc de mettre en place le contenu de notre content, en fonction
de l'url sur lequel l'utilisateur se trouve.

![Capture d’écran 2022-05-18 212023](https://user-images.githubusercontent.com/102798509/169139544-058b1989-cb19-4626-a88b-11bd06f5e00b.png)

Ici, nous avons une deuxième fonction avec un callback. Cette fonction permet de mettre à jour notre piechart en fonction des valeurs de deux
dropdowns. Nous voyons que notre callback a pour input les id de nos deux dropdown, et pour output l'id de notre graph piechart. Nous appelons
ensuite prepare_data_piechart avec en argument les deux listes contenant les valeurs de nos deux dropdown. Les valeurs des dropdowns vont donc
trier les données renvoyées par prepare_data, et nous utiliserons ces données pour construire notre graphique.
Les données sont donc mise à jour à chaque fois que nos dropdowns changent de valeurs, ce qui permet une interraction avec les graphiques.
Nous avons plusieurs fonction pour mettre à jours nos graphique qui fonctionnent en suivant le même principe que celle-ci. 

![Capture d’écran 2022-05-18 212112](https://user-images.githubusercontent.com/102798509/169139666-0ba9ca5e-5ebf-4b8f-9d84-0a6cc8c7c44c.png)

Ici, on run les serveur, et quand on le ferme, on se déconnecte de la database.

## LES MODELISATIONS :
