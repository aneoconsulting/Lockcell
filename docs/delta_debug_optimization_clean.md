---
lang: fr
title: "Titre du document"
---
<link rel="stylesheet" href="./styles.css">

# Titre de l'article / Rapport

_Auteur(s), Date_

---



## I. Introduction

Présente le contexte, le problème étudié et l'objectif de l'article.

Exemple d’énoncé mathématique :  
$E = mc^2$

Ou équation en affichage centré :  

$$
\int_{0}^{1} x^2 \, dx = \frac{1}{3}
$$

---

## II. Définitions et Propriétés

### 1. Mathématisation du problème

Dans cette première partie nous introduisons les premiers concepts fondamentaux à la compréhension du problème et à sa mathématisation, nous essayerons de toujours nous appuyer sur l'exemple des lignes d'un code de simulation afin de donner une idée du sens des définissions au lecteur.

<div class="convention">
  <div class="convention-title">Convention : Espace de recherche</div>
  <div class="convention-body">

> On appelle espace de recherche un ensemble fini $E$

  </div>
</div>

Cette convention permet de remettre cette étude dans le contexte de son développement, en effet on a un ensemble de perturabations possibles et on recherche "Celles qui ont un impact important sur le resultat", dans le cas d'un code de simulation, on peut associer chaque élément de E à la perturbation d'une ligne de code. Précisons le sens "d'avoir un impact important sur le résultat"

<div class="definition">
  <div class="definition-title">Définition : Fonction test</div>
  <div class="definition-body">

> Soit E un espace de recherche, on appelle fonction test sur E toute fonction croissante $$T: (E, \subseteq ) \longrightarrow (\{✓,✗\}, \leq)\text{ avec }✓ \leq ✗$$ $\newline$ Telle que:
>- $T(\varnothing) = ✓$
>- $T(E) = ✗$
>
> Autrement dit $\forall A,B \in \mathcal{P}(E), (A \subseteq B \text{ et } T(A) = ✗) \Rightarrow T(B) = ✗$

  </div>
</div>

On dira que la fonction test échoue sur un ensemble si sa valeur évaluée en cet ensemble vaut ✗

<div class="definition">
  <div class="definition-title">Définition : Problème</div>
  <div class="definition-body">

> On définit un problème comme une paire $(E, T)$, avec $E$ un espace de recherche et $T$ une fonction test sur ce dernier.

  </div>
</div>

Avoir ces deux premières définitions nous permettent de mathématiser le problème. Pour un ensemble $A\in\mathcal{P}(E)$ il faut voir $T(A)=✗$ comme : quand on applique toutes les perturbation de A, on perturbe fortement le résultat final, la fonction test traduit donc ce que l'on voit dans la réalité lorsque l'on fait un run du programme en perturbant certaines lignes pour reprendre notre exemple précédent.\
La fonction test permet donc de savoir si la partie que l'on regarde "contient une partie du problème". Afin de préciser cette dernière affirmation, nous avons besoin de la définition de la propriété suivante : 

<div class="definition">
  <div class="definition-title">
  
> Définition : Propriété ($\star$)

</div>
  <div class="definition-body">

> Soit $(E, T)$ un problème, $n\in\mathbb{N}^*$ et $b_1,...,b_n\in\mathcal{P}(E)$, on dit que $B = \{b_1,...,b_n\}$ verifie ($\star$) ou que $b_1,...,b_n$ vérifient ($\star$) si $$\forall i \neq j \in \llbracket 1, n\rrbracket, b_i \nsubseteq b_j \text{ et } \forall i \in \llbracket 1, n\rrbracket, b_i \neq \varnothing$$ 

  </div>
</div>

On remarque que cette définition est symétrique quitte à inverser i et j.

<div class="propriete">
  <div class="propriete-title">Propriété : Équivalence atomique</div>
  <div class="propriete-body">

> Soit $(E, T)$ un problème, il existe des uniques $n\in\mathbb{N}^*$ et $b_1,...,b_n\in\mathcal{P}(E)$ vérifiant ($\star$) tels que $$\forall C \in \mathcal{P}(E), T(C) = ✗ \iff \exists i \in \llbracket 1, n\rrbracket: b_i \subseteq C$$
On dit alors que $b_1,...,b_n$ sont les atomes du problème.\
> De plus, l'application $f: T \mapsto \{b_1,...,b_n\}$ est une bijection de l'espace des fonctions test vers $\{\{b_1,...,b_n\} \in \mathcal{P}(E)^n \text{ } \big| \text{ } n \in \mathbb{N}^* \text{ et } \{b_1,...,b_n\} \text{ vérifient } (\star) \}$

  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo : (Partie 1)</div>
  <div class="demo-body">

<details>
  <summary><strong>Cliquer pour voir la preuve</strong></summary>

> Soit $(E, T)$ un problème, soit $\Gamma = \{A\in \mathcal{P}(E) \text{ }\big|\text{ } T(A)=✗\}$ Comme $E$ est fini $\Gamma$ l'est aussi et comme $T(E) = ✗$, $\Gamma$ est non vide donc il existe $n\in\mathbb{N}^*$ et $b_1,...,b_n$ les éléments minimaux de $\Gamma$.
>
> ### <u>Existence</u> :
>-  Soit $i \neq j\in \llbracket 1, n\rrbracket$, on a $b_i\in\Gamma$ et $b_i \neq b_j$ donc par minimalité de $b_j$ on a $b_i \nsubseteq b_j$, ainsi $b_1,...,b_n$ vérifient ($\star$)
>
> Soit $C\in \mathcal{P}(E)$ :\
> $[\Leftarrow]$ Supposons qu'il existe $i \in \llbracket 1, n\rrbracket$ tel que $b_i\subseteq C$
>- Alors comme $b_i \in \Gamma$ on a $T(b_i) = ✗$ et donc $T(C) = ✗$ par croissance de T.
>
> $[\Rightarrow]$ Supposons maintenant que $T(C) = ✗$
>- Si $C$ est minimal alors on a $i \in \llbracket 1, n\rrbracket$ tel que $C = b_i$, alors on a bien $b_i \subseteq C$
>- Dans le cas général on procède par récurrence sur $|C|$:
>   - Si $|C| = 1$, comme $T(\varnothing) = ✓$ on C est minimal dans $\Gamma$ et on a déjà traité ce cas.
>   - Supposons l'assertion vraie pour $|C| \leq n$ pour un certain $n\in \mathbb{N}$:
>      - Si $C$ n'est pas minimal alors on a $A\in\Gamma$ tel que $A\subset C$ alors on a $|A| \lt |C|$
>      - Par hypothèse de récurrence on a $i \in \llbracket 1, n\rrbracket$ tel que $b_i\subseteq A$ et donc par transitivité de l'inclusion on a $b_i\subseteq C$, ce qui clot la récurrence.
>
> Ce qui prouve l'existance.
> ### <u>Unicité</u> :
> Soit $m\in \mathbb{N}^*$ et $c_1,...,c_m \in \mathcal{P}(E)$ des atomes du problème, montrons que $\{c_1,...,c_m\} = \{b_1,...,b_n\}$, ce qui montrera au passage $m = n$.
>- Soit $i\in \llbracket 1, m\rrbracket$, comme $c_i$ est un atome, on a $T(c_i) = ✗$
>- Or comme $b_1,...,b_n$ sont aussi les atomes du problème on a :
>   - $j\in \llbracket 1, n\rrbracket$ tel que $b_j \subseteq c_i$
>- Or tout comme pour $c_i$, on a $T(b_j) = ✗$
>   - Donc on a $k\in \llbracket 1, n\rrbracket$ tel que $c_k \subseteq b_j$
>- Ainsi on a : $c_k \subseteq b_j \subseteq c_i$, donc $c_k \subseteq c_i$
>- Comme $c_1,...,c_m$ verifient ($\star$) on a $k=i$ et donc les inclusions sont des égalités et $c_i = b_j$, ce qui prouve que $\{c_1,...,c_m\} \subseteq \{b_1,...,b_n\}$
>
>- Le problème étant symétrique on a utilisé aucune caractéristique de B dans la démonstration, on a donc bien $\{c_1,...,c_m\} = \{b_1,...,b_n\}$
>
> Ce qui conclut.
</details>
  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo : (Partie 2)</div>
  <div class="demo-body">

<details>
  <summary><strong>Cliquer pour voir la preuve</strong></summary>

> Les éléments minimaux d'un ensemble fini étant bien définis on en déduit une bonne définition de f.
>
> $f$ est clairement injective, en effet si on a deux fonctions test $T_1$ et $T_2$ tels que $f(T_1) = f(T_2)$, la propriété 1 nous permet de conclure : 
> $$\begin{align}
> \forall C \in \mathcal{P}(E), T_1(C) = ✗ &\iff \exists b \in f(T_1): b \subseteq C \tag{propriété 1}\\
>                                         &\iff \exists b \in f(T_2): b \subseteq C, \tag{$f(T_1) = f(T_2)$} \\
>                                         &\iff \forall C \in \mathcal{P}(E), T_2(C)  = ✗ \tag{propriété 1}
> \end{align}$$
> Comme une fonction test est à valeur dans un ensemble à deux éléments on a $(\forall C \in \mathcal{P}(E), T_1(C) \iff \forall C \in \mathcal{P}(E), T_2(C)  = ✗) \iff T_1 = T_2$, d'où l'injectivité de $f$.
>
> Réciproquement si on prend $n\in\mathbb{N}^*$ et $b_1,...,b_n\in \mathcal{P}(E)$ vérifiant ($\star$) alors on peut bien définir une fonction test $T$ sur $E$, en posant $\forall C \in \mathcal{P}(E), T(C) = ✗ \iff \exists i \in \llbracket 1, n\rrbracket: b_i \subseteq C$, on obtient bien une fonction croissante (par transitivité de l'inclusion), les deux autres conditions sont triviales étant donnée la non nullité de n et des $b_i$ fournie par ($\star$)\
> L'unicité fournit $f(T) = \{b_1,..,b_n\}$

</details>
  </div>
</div>

Cette démonstration nous permettra donc de parler d'un problème indifféremment de sa définition que ce soit $(E, T)$ ou $(E, B = \{b_1,..,b_n\})$.

Maintenant que nous avons défini notre problème, il est clair que notre objectif va être de déterminer des éléments $b_1,...,b_n$ au sein d'un problème.

Cependant, il nous reste encore un aspect des problèmes à traiter, en effet, on a vu qu'au sein d'un problème on avait des atomes à déterminer, mais dans le cas où ces atomes ont des intersections non nulles il devient compliquer de les traiter dans la pratique.\
En effet, imaginons un ensemble simple {1, 2, 3} et $b_1 = \{1, 2\}$, $ b_2 = \{2, 3\}$, alors imaginons que nous "fixons" le bug représenté par $b_1$, alors on a "retiré" l'incertitude représentée par 2, dans le cas de nos lignes de code, cela correspond par exemple à augmenter la précision sur les lignes 1 et 2. Dans ce cas là, nous avons en quelque sorte retiré les perturbations possibles des lignes 1 et 2, et trouver $b_2$ n'a plus forcément de sens. Pour cette raison nous introduisons une dernière définition :
<div class="definition">
  <div class="definition-title">Définition : Problème bien posé</div>
  <div class="definition-body">

> Soit $(E, B)$ un problème, on dit que ce problème est bien posé si tous les éléments de B sont disjoints.

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> La définition précédente permet de se rendre compte de l'utilité de la bijection entre atomes et fonction test lorsque l'on veut parler d'un problème.

  </div>
</div>

<div class="definition">
  <div class="definition-title">Définition : Problème trivial</div>
  <div class="definition-body">

> On dit d'un problème $(E, B)$ qu'il est trivial si E est un atome, c'est à dire si $B = \{E\}$.\
> Cela équivault à dire : $\forall A \in \mathcal{P}(E), T(A) = ✗ \iff A = E$

  </div>
</div>

<div class="definition">
  <div class="definition-title">Définition : Sous problème</div>
  <div class="definition-body">

> Soit $(E,T)$ un problème et $B$ ses atomes. Soit F une sous partie de E telle que $T(F) = ✗$, on dit alors que $(F, T_{|F})$ est un sous problème de $(E, T)$.\

  </div>
</div>

<div class="propriete">
  <div class="propriete-title">Propriété : </div>
  <div class="propriete-body">

> Soit $(E,T)$ un problème, $B$ ses atomes et $(F, T_{|F})$ un sous problème de $(E,T)$.\
> Alors $(F, T_{|F})$ est un problème et ses atomes sont les élements de $B_{|F} = \{b\in B \text{ | } b \subseteq F\}$

  </div>
</div>


### 2. Introduction des outils

Maintenant que nous avons pu poser précisemment ce qu'est un problème, nous allons introduire les outils qui nous permettrons de trouver ses atomes.

<div class="definition">
  <div class="definition-title">Définition : Partition maximale</div>
  <div class="definition-body">

> Soit E un espace de recherche et $\Delta = (\Delta_i)_{i = 1}^n \in \mathcal{P}(E)^n$ une partition de E\
> On dit que $\Delta$ est maximale si $\Delta = \{\{x\}\text{ | }x\in E\}$

  </div>
</div>

<div class="definition">
  <div class="definition-title">Définition : Raffinement de partition</div>
  <div class="definition-body">

> Soit E un espace de recherche, $\Delta = (\Delta_i)_{i = 1}^n \in \mathcal{P}(E)^n \text{ et } \delta = (\delta_i)_{i = 1}^m \in \mathcal{P}(E)^m$ deux partitions de E. On dit que $\delta$ raffine $\Delta$ si :
> 
>
> $$ \forall i \in \llbracket 1, n \rrbracket, (|\Delta_i| = 1\text{ et } \exists i_0 \in \llbracket 1, m \rrbracket: \Delta_i = \delta_{i_0})\text{ ou }(\exists i_0, j_0\in \llbracket 1, m \rrbracket: \delta_{i_0} \sqcup \delta_{j_0} = \Delta_i)$$
> On définit alors la fonction de correspondance $f: \llbracket 1, n \rrbracket \longrightarrow \mathcal{P}_1(\llbracket 1, m \rrbracket)\cup \mathcal{P}_2(\llbracket 1, m \rrbracket)$ telle que $$\forall i\in \llbracket 1, n \rrbracket, \Delta_i = \bigcup_{j \in f(i)} \delta_j$$

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> Cette définition est potentiellement un peu désagréable à digérer mais ce qu'il faut comprendre c'est que $\delta$ est la même partition que $\Delta$ où l'on a coupé chaque partie en deux d'où : $\exists i_0, j_0\in \llbracket 1, m \rrbracket: \delta_{i_0} \sqcup \delta_{j_0} = \Delta_i$, sauf dans le cas où $\Delta_i$ était de cardinal 1 au quel cas on l'a simplement conservé, d'où : $|\Delta_i| = 1\text{ et } \exists i_0 \in \llbracket 1, m \rrbracket: \Delta_i = \delta_{i_0}$


  </div>
</div>

<div class="definition">
  <div class="definition-title">Définition : Raffinement</div>
  <div class="definition-body">

> On définit un raffinement $\Delta \rightarrow \delta$ comme la donnée de deux partitions $\Delta$ et $\delta$ telles que $\delta$ raffine $\Delta$ et d'une fonction de correspondance f telle que définie dans la défintion précédente

  </div>
</div>


<div class="definition">
  <div class="definition-title">Définition : Sous partition</div>
  <div class="definition-body">

> Soit $(E,T)$ un problème et $\Delta^1$ une partition de $E$. On dit que $\Delta^2$ est une sous partition si $\Delta^2 \subseteq \Delta^1$

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> Un sous partition de $\Delta$, un partition sur un espace $E$, n'est rien d'autre qu'une partition d'un sous ensemble de E, à condition que cette ensemble soit descriptible par $\Delta$

  </div>
</div>

Cette première définition nous permet de faire une recherche binaire dans notre espace de recherche et de définir un arbre de recherche:

<div class="definition">
  <div class="definition-title">Définition : Arbre de recherche</div>
  <div class="definition-body">

> Soit $E$ un espace de recherche, on définit un arbre de recherche de taille n sur E comme une suite de partitions de E $(\Delta^i)_{i=1}^n$ telle que et :
> $$ \forall i \in \llbracket 1, n-1 \rrbracket, \Delta^{i+1} \text{ raffine } \Delta^i$$
>
> On note $|\Delta|$ la taille de $\Delta$.

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> On pourra de la même façon définir un arbre de recherche à partir d'une suite de correspondances : $\Delta^1\rightarrow...\rightarrow\Delta^n$

  </div>
</div>

<div class="definition">
  <div class="definition-title">Définition : Sous arbre de recherche</div>
  <div class="definition-body">

> Soit $E$ un espace de recherche et $\Delta = (\Delta^i)_{i=1}^n$ un arbre de recherche sur E, on définit un sous arbre de $\Delta$ un arbre $\Delta' = (\Delta'^i)_{i=k}^n$ pour un certain $k\in ⟦k, n⟧$ tel que $\forall i\in ⟦k, n⟧, \Delta'^i\text{ est une sous partition de } \Delta^i$.\
> On dit que k est l'indice du sous arbre.

  </div>
</div>

<div class="propriete">
  <div class="propriete-title">Propriété : Taille d'un sous arbre</div>
  <div class="propriete-body">

> Soit $E$ un espace de recherche, $\Delta$ un arbre de recherche sur E et $\Delta'$ un sous arbre de $\Delta$ d'indice $k\in\mathbb{N}*$ alors :
> $$ |\Delta'| = |\Delta| - k$$
>

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> Trivial en se servant uniquement de la définition.

  </div>
</div>

  </div>
</div>

<div class="definition">
  <div class="definition-title">Définition : Arbre terminal</div>
  <div class="definition-body">

> Soit $E$ un espace de recherche et $\Delta = (\Delta_i)_{i = 1}^n \in \mathcal{P}(E)^n$ un arbre sur $E$.
>- On dit que $\Delta$ est un arbre terminal si $\Delta^n$ est une partition maxiamale

  </div>
</div>

<div class="propriete">
  <div class="propriete-title">Propriété : </div>
  <div class="propriete-body">

> Soit $E$ un espace de recherche, la taille des arbres de recherche sur $E$ est bornée par $|E|$\
> De plus, la partition la plus fine d'un arbre de recherche de taille maximale est maximale 

  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> TODO

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> Il est assez clair après cette démonstration que l'on peut sans peine améliorer la borne en $max_{i\in\Delta^1}\{|\Delta^1_i|\}$.\
> Un sous arbre d'un arbre terminal est trivialement terminal (sous partition d'un partition maximale est maximale).

  </div>
</div>


Le sens de cette dernière définition est assez clair normalement, on coupe récursivement notre ensemble en deux, ce qui s'apparente au parcours d'un arbre.\
Néanmoins pour éviter des surprises désagréables lors des démonstration il est préférable de travailler avec des "arbres équilibrés".

<div class="definition">
  <div class="definition-title">Définition : Partition équilibrée</div>
  <div class="definition-body">

> Soit E un espace de recherche et $\Delta = (\Delta_i)_{i = 1}^n \in \mathcal{P}(E)^n$ une partition de ce dernier. On dit que $\Delta$ est équilibrée si :
> $$\forall i,j \in \llbracket 1, n \rrbracket, \big| |\Delta_i| - |\Delta_j|\big| \leq 1$$


  </div>
</div>

<div class="proposition">
  <div class="proposition-title">Proposition : </div>
  <div class="proposition-body">

> Une sous partition d'une partition équilibrée est elle même équilibrée.

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

<details>
  <summary><strong>Cliquez pour voir la preuve</strong></summary>

> Être équilibré pour une partition est équivalent au fait que toute paire d'élement de cette partiton vérifient une certiaine, ceci se transmet evidemment aux sous ensembles.

</details>

  </div>
</div>

  </div>
</div>

<div class="definition">
  <div class="definition-title">Définition : Arbre équilibré</div>
  <div class="definition-body">

> On dit d'un arbre qu'il est équilibré si toutes les partitions qui le composent sont équilibrées.

  </div>
</div>

<div class="propriete">
  <div class="propriete-title">Propriété : </div>
  <div class="propriete-body">

> La taille des arbres de recherhce équilibrés sur un espace de recherche $E$ est bornée par $\lceil log_2(|E|)\rceil$\
> De plus la partition la plus fine d'un arbre de recherche équilibré est maximale ssi l'arbre est de taille maximale 

  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> TODO

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> Il est assez clair après cette démonstration que l'on peut sans peine améliorer la borne en $max_{i\in\Delta^1}\{log_2(|\Delta^1_i|)\}$

  </div>
</div>

<div class="proposition">
  <div class="proposition-title">Proposition : </div>
  <div class="proposition-body">

> Un sous-arbre d'un arbre equilibré est lui même équilibré

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> Trivial en se servant de la même chose sur les sous partitions des partition équilibrées

  </div>
</div>


On définit ainsi la notion de "couper notre ensemble en deux de façon équilibré". On pourrait montrer que de tels arbres existent, mais on exhibera plus loin une façon de le faire dans un algorithme, ce qui prouvera leur existence.


Nous allons par la suite beaucoup travailler avec des partitions alors, afin de s'éviter de complexes unions d'ensembles qui pourraient inutilement nuire à la compréhensions, nous allons introduire quelques notations en plus.

<div class="convention">
  <div class="convention-title">Convention : </div>
  <div class="convention-body">

> Soit $\Delta$ une partition de E, on se permettra d'indicer les éléments de $\Delta$ par eux même et donc d'écire $\Delta_i, i\in\Delta$ pour les représenter.

  </div>
</div>

<div class="convention">
  <div class="convention-title">Convention : </div>
  <div class="convention-body">

> Dans la suite de cet étude nous nous intéresserons très régulièrement aux complémentaires des élements d'une partition $\Delta$ à tel point que l'on notera, pour $i\in\Delta$, $\nabla_i$ le complémentaire de $\Delta_i$ dans E.

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> Notez dans dans l'exemple précédent nous utilisons la convention numéro ** pour désigner un élément de $\Delta$ par lui même.

  </div>
</div>



Comme nous manipulerons beaucoup de partitons dans la suite de cette étude nous convenons maintenant que l'indice du haut correspondra systématiquement aux élément d'une famille de partition, alors que l'indice du bas lui correspond à un élément de cette partition. Si bien que $\Delta^n$ représente une partition, $\Delta^n_i$ un élément de cette partition et $\nabla^n_i$ le complémentaire de cet élément dans l'espace de recherche courant (celui que partitionne $\Delta^n$).


Enfin nous introduisons la notion de conjugaison :

<div class="definition">
  <div class="definition-title">Définition : Conjugaison</div>
  <div class="definition-body">

> Soit E un espace de recherche et $\Delta^1 \rightarrow \Delta^2$ un raffinement et $f$ la fonction de correspondance associée.\
> Soit $i,j \in \Delta^2$ on dit que $\Delta^2_i$ et $\Delta^2_j$ sont conjugués et on note $\overline{\Delta^2_i} = \Delta^2_j$ si :
> $$\{i,j\}\in Im(f)$$
> On remarque que quand on ne peut pas couper en deux lors du raffinement et que l'on a $\Delta^1_{i_0} = \Delta^2_{j_0}$ alors $\Delta^2_{j_0}$ est son propre conjugué.

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> On étend la notation aux complementaire de la façon suivante :
>- Si $\overline{\Delta_i} = \Delta_j$ alors $\overline{\nabla_i} = \nabla_j$
>
> La relation être conjugué de quelqu'un est symétrique

  </div>
</div>


Maintenant il nous faut définir les notions qui nous permettront de manipuler aisément nos partition et leurs interactions avec la fonction test.

<div class="definition">
  <div class="definition-title">Définition : Partition grossière</div>
  <div class="definition-body">

> Soit $(E, T)$ un problème, on dit d'une partition $\Delta$ qu'elle est grossière si
> $$\forall i\in\Delta, T(\nabla_i) = ✓$$
> On la dit séparante dans le cas contraire et on note $I_{\Delta} = \{i\in\Delta \text { | } T(\nabla_i) = ✗\}$

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> La défintion précédente implique directement que $\forall i\in\Delta, T(\Delta_i) = ✓$, sauf pour la partition triviale $\{E\}$
>- On rappelle que l'on indice les éléments de $\Delta$ par eux même, donc $\forall i\in\Delta, T(\Delta_i) = ✓$ signifie que pour tous les éléments de notre partition la fonction test n'échoue pas dessus.
>- De même $\forall i\in\Delta, T(\nabla_i) = ✓$ signifie que la fonction test n'échoue sur aucun des complémentaires des éléments de notre partition.

  </div>
</div>

Cette définition nous permet de dire d'une partition si elle est intéressante, en effet si un partition est séparante, cela signifie que l'on peut trouver $i\in \Delta$ tel que $T(\nabla_i) = ✗$.\
On peut donc trouver un ensemble strictement plus petit qui contient une partie du problème.

<div class="proposition">
  <div class="proposition-title">Proposition : </div>
  <div class="proposition-body">

> Soit $(E, T)$ un problème. Soit $\Delta_1 \rightarrow \Delta_2$ un raffinement, alors si $\Delta_2$ est grossière $\Delta_1$ l'est aussi.

  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> TODO

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> Cette proposition est équivalente à :\
> Soit $\Delta_1 \rightarrow \Delta_2$ un raffinement, alors si $\Delta_1$ est séparante $\Delta_2$ l'est aussi. (Contraposée)


  </div>
</div>

<div class="definition">
  <div class="definition-title">Définition : Raffinement efficace</div>
  <div class="definition-body">

> Soit $\Delta^1 \rightarrow \Delta^2$ un raffinement, on dit qu'il est efficace si $\Delta^1$ est grossière et que $\Delta^2$ est séparante.

  </div>
</div>

<div class="proposition">
  <div class="proposition-title">Proposition : </div>
  <div class="proposition-body">

> Soit $(E, T)$ un problème, $\Delta^1 \rightarrow \Delta^2$ un raffinement efficace, soit $i,j\in\Delta^2$ on a :
> $$\overline{\nabla_i} = \nabla_j \Rightarrow T(\nabla_i\cap\nabla_j) = ✓$$

  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> TODO

  </div>
</div>

<div class="proposition">
  <div class="proposition-title">Proposition : </div>
  <div class="proposition-body">

> Soit $(E, T)$ un problème, $\Delta$ une partition sur E à la fois maximale et grossière alors $(E, T)$ est trivial, et les atomes du problème sont $B = \{E\}$

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

<details>
  <summary><strong>Cliquez pour voir la preuve</strong></summary>

> TODO

</details>

  </div>
</div>

  </div>
</div>

<div class="proposition">
  <div class="proposition-title">Proposition : </div>
  <div class="proposition-body">

> Une sous partition d'une partition maximale est elle aussi maximale.

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> Triviale

  </div>
</div>

  </div>
</div>



### 3. Problème projeté
Maintenant, il ne nous reste qu'à définir la projection d'un problème

<div class="definition">
  <div class="definition-title">Définition : Problème projeté</div>
  <div class="definition-body">

> Soit $(E, T)$ un problème et $\Delta$ une partition de $E$. On définit $T_{\Delta}$ une fonction test sur $\Delta$ (en tant qu'ensemble) de la façon suivante: 
> $$ \forall I \subseteq \Delta, T_{\Delta}(I) = T\Big(\bigcup_{i\in I}\Delta_i\Big)$$
> On vérifie bien que $T_{\Delta}$ est une fonction test sur $\Delta$.\
> On appelle $(\Delta, T_{\Delta})$ le projeté de $(E, T)$ sur $\Delta$.

  </div>
</div>

<div class="definition">
  <div class="definition-title">Définition : Projection exacte</div>
  <div class="definition-body">

> Soit $(E, T)$ un problème $B$ ses atomes, $\Delta$ une partition de $E$, et $(\Delta, T_{\Delta})$ le projeté de $(E, T)$ sur $\Delta$.\
> On définit la projection exacte de $B$ sur $\Delta$ comme l'ensemble:
> $$\Big\{\{k\in \Delta\text{ | } B_i \cap \Delta_k \neq \varnothing \}\text{ } \Big | \text{ } i \in \llbracket 1, card(B)\rrbracket\Big\}

  </div>
</div>


Illustration

Même si $(E, T)$ est bien posé et donc que $B$ vérifie ($\star$), il est possible que la projection exacte de $B$ sur $\Delta$ ne vérifie pas ($\star$), pour cela on définit la projection (réduite) de $B$ sur $\Delta$

<div class="definition">
  <div class="definition-title">Définition : Projection (réduite)</div>
  <div class="definition-body">

> Soit $(E, T)$ un problème $B$ ses atomes, $\Delta$ une partition de $E$, et $B'$ le projeté de $B$ sur $\Delta$, on pose :
> $$ P_{\Delta} = \{b\in B' \text{ | } \exists b' \in B' : b' \subset b \} $$
> Et on définit, $B^{\Delta}$ la projection réduite de $B$ sur $\Delta$ comme :
> $$ B^{\Delta} = B' \setminus P_{\Delta}$$
> On abusera du langage et on parlera directement de "projection" de $B$ sur $\Delta$.\
> On dit que les atomes correspondants aux éléments de $P_{\Delta}$ sont perdus.

  </div>
</div>

<div class="proposition">
  <div class="proposition-title">Proposition : </div>
  <div class="proposition-body">

> Soit $(E, T)$ un problème et B ses atomes, $\Delta$ une partition de E, $(\Delta, T_{\Delta})$ le problème projeté et $B^{\Delta}$ la projection de $B$ sur $\Delta$.
>$$\text{Les atomes projetés } B^{\Delta} \text{sont les atomes de} (\Delta, T_{\Delta})$$
> En particulier, $B^{\Delta}$ verifie ($\star$).

  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> TODO

  </div>
</div>

<div class="proposition">
  <div class="proposition-title">Proposition : </div>
  <div class="proposition-body">

> Les atomes de cardinal 1 ne sont jamais perdus.

  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> TODO

  </div>
</div>


La notion de projection n'a rien de mystérieux, il faut considérer cela comme regarder notre ensemble de départ à travers les éléments de la partition. Les éléments d'un même $\Delta_i$ sont inséparable et quand on trouve nos atomes à cette échelle, on raffine cette partition afin de retirer les bouts inutiles, voici une illustration grossière pour mieux comprendre :


### 4. Matrice d'interaction

Nous pouvons maintenant parler librement de nos partions, en prendre des intersetions, leur appliquer la fonction test, définissons alors un outils qui sera essentiel à la preuve de l'algorithme

<div class="definition">
  <div class="definition-title">Définition : Matrice d'interaction</div>
  <div class="definition-body">

> Soit $(E,T)$ un problème et $\Delta$ une partition sur $E$ et $n$ son cardinal, on définit la matrice d'interaction de $\Delta$ comme la matrice $M$ de $M_n({✓, ✗})$ telles que :
> $$ \forall i,j in \Delta, M_{i,j} = T(\nabla_i \cap \nabla_j)


  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> On note que l'on a ici encore utilisé des éléments de $\Delta$ pour indexer les éléments de la matrice.
  </div>
</div>

<div class="propriete">
  <div class="propriete-title">Propriété :</div>
  <div class="propriete-body">

> Soit $(E,T)$ un problème et $\Delta$ une partition sur $E$ et $M$ sa matrice de perturbation, si on a $\nabla_i$ un complémentaire d'un élément de $\Delta$ tel que $T(\nabla_i) = ✓$ alors la colonne et la ligne associée à $\nabla_i$ sont nulles (égales à ✓ partout).

  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

> La démonstration découle directement de la croissance de T


  </div>
</div>

La proposition précédente nous pousse à définir l'objet suivant :

<div class="definition">
  <div class="definition-title">Définition : Matrice d'interaction réduite</div>
  <div class="definition-body">

> Soit $(E,T)$ un problème, $\Delta$ une partition sur $E$ et $M$ sa matrice d'interaction, on définit la matrice d'interaction réduite $MR$ comme la matrice $M$ à laquelle on a retiré les lignes et les colonnes correspondants à des $\nabla_i$ tels que $T(\nabla_i) = ✓$

  </div>
</div>

Maintenant que nous avons introduit les notions essentielles à l'étude de nos espaces de recherche afin de déterminer leur atomes, nous allons pouvoir entrer dans le coeur du sujet avec la description l'algorithme central.

# III. Description des algorithmes

## 0. Définition des fonction auxiliaires :

### is_maximal
---
#### Entrées et Sorties

- **Entrée :**  
  - une partition P d'un ensemble E


- **Sortie :**  
  - Un booléen qui vaut true si tous les éléments de P sont des singletons, donc si P est maximale


### split
---
#### Entrées et Sorties

- **Entrée :**  
  - une partition P d'un ensemble E


- **Sortie :**  
  - Un raffinement de P ainsi qu'une fonction de conjugaison ($\text{conj}(\nabla_i) = \overline{\nabla_i}$)


### complementaire
---
#### Entrées et Sorties

- **Entrée :**  
  - une partie A d'un ensemble E et cet ensemble E


- **Sortie :**  
  - la liste représentant le complémentaire de A dans E

### generate_test_matrix
---
#### Entrées et Sorties

- **Entrée :**  
  - une partition $P$ d'un ensemble $E$
  - les indices $I$ de $P$ tels que $\text{test}(P[i]) = ✗$
  - Une fonction $\text{conj}$ de conjugaison sur $P$

- **Sortie :**  
  - un matrice M $n\times n$ où $n = |P|$ d'éléments de $\{✓,✗\}$ telle que $\forall i, j \in ⟦1, n⟧, M_{i,j} = test(\nabla_i\cap\nabla_j)$

On étudira plus loin la complexité de cette fonction.


## 1. L'algorithme récursif de base : DDMin

### Entrées et Sorties

- **Entrée :**  
  - un problème $(E, T)$
    - Sous la forme d'une liste de liste : 'delta', représentant une partition grossière de E
    - Et d'une fonction 'test', représentant T 


- **Sortie :**  
  - Liste de sous liste de la liste d'entrée E, contentant une partie des atomes de notre problème

### Pseudo-code


```pseudo 
Algorithme DDMin(delta, test):

  // Initialisation
  E = la concaténation de delta

  Tant que is_maximal(delta) est faux:

      // on raffine la partition et crée la fonction de conjugaison
      delta, conj = split(delta)

      // on pose nabla comme l'ensemble des complémentaires des élements de delta
      nabla = [complementaire(delta_i, E) pour delta_i dans delta]

      // se calcule en parallèle
      resultats = [test(nabla_i) pour nabla_i dans nabla]


      Si (resultat == ✓ pour tout resultat dans results):
          // La partition est grossière, on raffine
          continue

      Sinon:
          // certains complementaire échouent, on va récurser
          I = La liste des indices de nabla tels que test(nabla[i]) == ✗

          // se calcule en parallèle
          M = generate_test_matrix(nabla, I, conj) 
          // M est égale à la matrice n*n des test(nabla_i inter nabla_j)

          MR = la matrice réduite où l'on a retiré les lignes et les colonnes correspondants à des éléments qui ne sont pas dans I, construite directement à partir de M

          Si pour tout resultat dans MR, resultat == ✗:

              // l'ensemble sur lequel on va récurser
              preparation = intersection de nabla[i] pour i

              // on garde bien la même structure de partition (sous partition)
              next = [delta_i pour delta_i dans delta tel que (delta_i inclu dans preparation)]

              retourner DDMin(next, test)
          Sinon:
              i, j = find_non_failing(MR)
              // où find_non_failing(matrix) renvoie le premier couple i, j dans l'ordre lexicographique tel que matrix[i][j] == ✓
              
              I = la liste des indices i_0 tels que MR[i][i_0] == ✗
              J = la liste des indices j_0 tels que MR[j][j_0] == ✗
              // En particulier I contient i et J contient j donc sont non vides

              // on crée les ensembles sur lesquels on va récurser
              preparation1 = intersection de nabla[i] pour i dans I
              preparation2 = intersection de nabla[j] pour j dans J
              
              // on fait bien attention à garder la structure de partition du départ (sous partition)
              next1 = [delta_i pour delta_i dans delta tel que (delta_i inclu dans preparation1)]
              next2 = [delta_j pour delta_j dans delta tel que (delta_j inclu dans preparation2)]


              retourner DDMin(next1, test) union DDMin(next2, test) // L'execution se lance en parallèle

  retourner [E]
```

## 2. L'algorithme complet : RDDMin

### Entrées et Sorties

- **Entrée :**  
  - un problème $(E, T)$, supposé bien posé
    - Sous la forme d'une liste E, représentant les éléments de E
    - Et d'une fonction 'test', représentant T 

- **Sortie :**  
  - Liste de sous liste de la liste d'entrée E, contentant l'ensemble des atomes du problème d'entrée

### Pseudo-code

```pseudo 
Algorithme RDDMin(E, test):

    Si test(E) == ✗:
        // on trouve des atomes de l'espace_de_recherche_actuel
        atomes = DDMin([E], test)
        
        // on retire les atomes trouvés de l'espace_de_recherche_actuel
        a_retirer = la concaténation de atomes
        espace_de_recherche_réduit = complémentaire(a_retirer, E)

        retourner atomes union RDDMin(espace_de_recherche_réduit, test)

    Sinon :
        retourner []
```


# IV. Preuves de Terminaison et de correction

Avant toute chose nous allons faire une hypothèse simplificatrice sur la taille des problèmes projetés dans la suite des démonstrations, en gardant en tête que cette hypothèse n'est pas nécessaire et qu'une meilleure implémentation de l'algorithme permettrait de s'en débarrasser.

<div class="definition">
  <div class="definition-title">Définition : Partition simple</div>
  <div class="definition-body">

> Soit $(E,T)$ un problème et $B$ ses atomes. Soit $\Delta$ une partition sur E, on dit que $\Delta$ est simple si $|B^{\Delta}| \leq 2$

  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> Nous verrons plus tard une relation entre le cardinal des atomes projetés et le cardinal maximum d'un arbre de partition grossière, qui permettra de se rendre compte que cette hypothèse n'est pas si forte qu'il n'y parait dans le cas d'atomes de petit cardinal.

  </div>
</div>

On s'autorisera dans la suite de l'étude à supposer que sur des partitions étudiées sont simples.

Avant de s'attaquer à la preuve à proprement parler, démontrons une propriété dans le cas des partitions simples: 

<div class="proposition">
  <div class="proposition-title">Proposition : Critère de séparation</div>
  <div class="proposition-body">

> Soit $(E,T)$ un problème et $\Delta$ une partition simple sur $E$, $MR \in M_k(\{✓, ✗\})$ sa matrice de perturbation réduite et $B^{\Delta}$ le projeté des atomes du problème sur $\Delta$ alors:
>
>$$ |B^{\Delta}| = 1 \iff MR = ✗_{M_k(\{✓, ✗\})}$$


  </div>
</div>

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

<details>
  <summary><strong>Cliquez pour voir la preuve</strong></summary>

> On montre le résultat par double implication:
>
> $[\Rightarrow]$ Si $|B^{\Delta}| = 1$, on note $b$ son seul élément et on a $\forall \nabla_i \in \Delta, T(\nabla_i) = ✗ \iff b\subseteq\nabla_i$ en réduisant la propriété d'équivalence atomique au cas où l'on à qu'un seul atome.
>- Donc $\forall i, j \in I_{\Delta}, b\subseteq \nabla_i \text{ et } b\subseteq \nabla_j$ 
>- D'où  $\forall i, j \in I_{\Delta}, b\subseteq \nabla_i \cap \nabla_j$
>- Ainsi $\forall i, j \in I_{\Delta}, T(\nabla_i \cap \nabla_j) = ✗$ (D'après la propriété **)
>- Et donc $\forall i, j \in I_{\Delta}, (MR)_{i,j} = ✗$
> Ce qui est la même chose que $MR = ✗_{M_k(\{✓, ✗\})}$.
>
> $[\Leftarrow]$ Si $MR = ✗_{M_k(\{✓, ✗\})}$, soit $b_1, b_2 \in B^{\Delta}$. Supposons $b_1 \neq b_2$:\
> Comme $B^{\Delta}$ verifie ($\star$) d'après la proposition **, on sait que $b_1$ et $b_2$ ne sont pas inclus l'un dans l'autre, on a donc $i, j\in\Delta$ tels que:
> $$\Delta_i \not\in b_1\text{ et } \Delta_i \in b_2$$
> et
> $$\Delta_j \not\in b_2\text{ et } \Delta_j \in b_1$$
> En particulier on a $(b_1\subseteq\nabla_i$ et $b_1\nsubseteq\nabla_j)$ et $(b_2\subseteq\nabla_j$ et $b_2\nsubseteq\nabla_i)$.\
> On en déduit : $b_1, b_2\nsubseteq\nabla_i\cap\nabla_j$ et comme $\Delta$ est simple on a au plus 2 eléments dans $B^{\Delta}$ et donc $\nabla_i\cap\nabla_j$ ne contient aucun atome.\
> D'après la propriété d'équivalence atomique on a $T(\nabla_i\cap\nabla_j) = ✓$ et donc $(MR)_{i,j} = ✓$, absurde.
> 
> Ce qui conclut la démonstration.

</details>

  </div>
</div>

## L'algorithme DDMin:

<div class="proposition">
  <div class="proposition-title">Proposition : Terminaison et Correction de DDMin </div>
  <div class="proposition-body">

> Démo :\
> Soit pour tout $N\in\mathbb{N}^*, P(N)$, l'assertion : $\forall (E, T)\text{ problème}, |E| \leq N \Rightarrow DDMin(\{E\}, T)\text{ termine et retourne une partie non vide des atomes de E}$.\
> Montrons $\forall N\in\mathbb{N}^*, P(N)$ par récurrence :
> 
> ### Initialisation :
> Si $N = 1$, soit $(E, T)$ un problème tel que $|E| \leq 1$, comme $T(E) = ✗ \neq ✓ = T(\varnothing)$ on a forcément $E\neq\varnothing$ et la seule partition de E est $\{E\}$, elle est bien grossière (cf. la définition) et maximale, on a donc E, atome de E et is_maximal(E) == True d'où $DDMin(\{E\}, T) = [E]$ et donc P(1)
>
> ### Hérédité :
> Soit $N\in\mathbb{N}^*$ tel que $P(N)$, montrons $P(N+1)$ :
>
> Soit $(E, T)$ un problème tel que $|E| \leq N+1$, on note les partitions delta succesive de chaque passage dans la boucle les $\Delta^1,...,\Delta^n$ avec $n\in\mathbb{N}^* \cup \{\infty \}$, or comme pour tout $i\in\mathbb{N}^*$ $\Delta_{i+1}$ est un raffinement de $\Delta_{i}$, $\{E\} = \Delta^1 \rightarrow ... \rightarrow \Delta^i$ est un arbre sur E pour tout $i \lt n$. Or d'après la proposition ** la taille d'un arbre est bornée, d'où $n \lt \infty$
> On a forcément $\Delta^1,...,\Delta^{n-1}$ grossière, sinon on n'aurait pas créé de $\Delta^n$.
>
> Si $\Delta^n$ est grossière, alors forcément elle est maximale. En effet, si ce n'était pas le cas on aurait parcouru encore une fois la boucle et on aurait eu $\Delta^{n+1}$. Et si c'est le cas alors DDMin retourne $[E]$ et donc termine. De plus on a $\Delta^n$ un partition de $E$ grossière et maximale, donc d'après la proposition **, $(E, T)$ est trivial et donc $E$ est bien un atome du problème.
>
> Si $\Delta^n$ n'est pas grossière alors on crée la matrice réduite MR de $\Delta^n$ (On suppose encore ici que $\Delta^n$ est simple).


> Si $MR = ✗$ alors on sait d'après le critère de séparation que $B^{\Delta^n}$ est de cardinal 1, on a alors en notant $b$ sont unique élément:
> $$\forall \nabla^n_i \in \Delta, T(\nabla^n_i) = ✗ \iff b\subseteq\nabla^n_i$$
>- D'où
> $$\forall i \in I_{\Delta}, b\subseteq\nabla^n_i$$
>- Et donc
> $$b\in\bigcap_{i\in I_{\Delta}} \nabla^n_i$$
>- Ainsi si $Next = \bigcap_{i\in I_{\Delta^n}} \nabla^n_i$ on a bien $T(Next) = ✗$ et donc $(Next, T)$ est un sous problème de $(E, T)$ qui a pour atomes les atomes de $(E, T)$ inclus dans $Next$, qui est non vide. De plus, clairement $|Next| \lt |E|$, d'où $|Next| \leq N$
>- On retourne $DDMin(Next, T)$, qui d'après $P(N)$ termine et renvoie une partie non vides des atomes de $(Next, T)$.\
>- Ainsi le programme termine et retourne bien une partie non vide des atomes de $(E, T)$


> Sinon on a $i,j \in I_{\Delta^n}, T(\nabla^n_i\cap\nabla^n_j) = ✓$, comme $\Delta^n$ est simple on a $b_1, b_2$ les deux atomes du problème et donc forcément $(b_1\subseteq\nabla^n_i$ et $b_2\nsubseteq\nabla^n_i)$ et $(b_2\subseteq\nabla^n_j$ et $b_1\nsubseteq\nabla^n_j)$ quitte à les échanger.
>- Donc $\forall i_0\in I_{\Delta^n}, T(\nabla^n_i\cap\nabla^n_{i_0}) = ✗\iff b_1\subseteq\nabla^n_{i_0}$
>- D'où $I_i = \{i_0 \in I_{\Delta^n} \text{ | } T(\nabla^n_i\cap\nabla^n_{i_0}) = ✗\} = \{i_0 \in I_{\Delta^n} \text{ | } b_1\subseteq\nabla^n_{i_0} \}$
>- Et donc $b_1 \subseteq Next1 = \bigcap_{i_0\in I_i} \nabla^n_{i_0}$, c'est même le plus petit sous ensemble de $\Delta^n$ le contenant au sens de l'inclusion.
>- De la même façon on a $b_2 \subseteq Next2 = \bigcap_{i_0\in I_j}$, avec $I_j$ défini de la même façon que $I_i$
>- On a comme pour $Next$ : $|Next1|, |Next2| \leq N$ et $(Next1, E)$, $(Next2, T)$ sont des sous problèmes de $(E, T)$, donc d'après $P(N)$ : $DDMin(Next1, T)$ et $DDMin(Next2, T)$ terminent et renvoient chacun une partie non vides des atomes chacun des problèmes.
>- En faisant l'union des deux on obtient bien une partie non vides des atomes de $(E, T)$.
>
> D'où $P(N+1)$, ce qui clot la récurrence.
>
> $\forall N\in \mathbb{N}^* P(N)$ implique directement la terminaison et la correction.\
> Ce qui conclut.

  </div>
</div>

<div class="proposition">
  <div class="proposition-title">Proposition : Terminaison et Correction de RDDMin</div>
  <div class="proposition-body">

> Soit pour tout $N\in\mathbb{N}*$, $P(N)$, l'assertion : $\forall (E,T)\text{ bien posé }, |E| \leq N \Rightarrow RDDMin(E,T) = B$ où $B$ désigne les atomes du problème.\
>Démontrons $\forall N\in\mathbb{N}*, P(N)$ par récurrence:
>
> ### Initialisation :
> Soit $(E, T)$ un problème bien posé et B ses atomes tel que $|E| \leq 1$, comme précédemment on a forcément $|E| = 1$ et $B = \{E\}$.
> Alors $DDMin([E], T)$ va nécessairement retourner $[E]$ et $RDDMin(\varnothing, T)$ retourne la liste vide, d'où $RDDMin(E, T) = [E]$ et donc P(1)$
> 
> ### Hérédité :
> Soit $N\in\mathbb{N}^*$ tel que $P(N)$, montrons $P(N+1)$ :
>
> Soit $(E, T)$ un problème bien posé et B ses atomes tel que $|E| \leq N+1$.\
> Soit $B'= DDMin([E], T)$, on a d'après la proposition précédente, $B' \subseteq B$ et $B' \neq \varnothing$.\
> Soit $R = \bigcup_{b\in B'} b$, on a donc $|R| >= 1$. D'où si $E' = E\setminus R$ :
$$
\begin{align}
|E'| &= |E\setminus R|\notag \\
     &= |E| - |R|\tag{car $R\subseteq E$}\\
     &\leq N \notag
\end{align}     
$$
> Si $B' = B$, alors $T(E') = ✓$ et le programme termine en renvoyant $B' = B$.
> Sinon on a $T(E') = ✗$ et alors $(E', T)$ est un sous problème de $(E, T)$, et l'ensemble de ses atomes est exactement :
$$
\begin{align}
B_2 &=\{b\in B\text{ | } b \subseteq E'\} \tag{D'après propriété ** } \\
     &= \{b\in B \text{ | } b\nsubseteq R\} \tag{élements de B disjoints (problème bien posé)} \\
     &= \{b\in B \text{ | } b\not\in B'\} \tag{$R = \bigcup_{b\in B'} b$ + éléments de B disjoints}\\
     &= B\setminus B'
\end{align}  
$$
> Comme $|E'| \leq N$, d'après $P(N)$ : $RDDMin(E', T)$ termine et retourne $B_2$, donc $RDDMin(E, T)$ termine et retourne $B'\cup B_2 = B' \cup (B\setminus B') = B$ (car $B' \subseteq B$). \
> D'où $P(N+1)$, ce qui clot la récurrence.
>
> $\forall N\in \mathbb{N}^* P(N)$ implique directement la terminaison et la correction.\
> Ce qui conclut.

  </div>
</div>

# VI. Structure de DDMin

Le découpage récursif de chaque élément de la partition en 2 dans l'algorithme DDMin peut fortement faire penser à une dichotomie, cette remarque est essentielle et permettra de donner une borne supérieure pour la compléxité de DDMin

<div class="proposition">
  <div class="proposition-title">Proposition : Structure arborescente de DDMin</div>
  <div class="proposition-body">

> Soit $P$ une partition d'un problème, alors il existe $n\in\mathbb{N}*$ et un arbre $\Delta = (\Delta^i)_{i=0}^n$ terminal tels que dans tous les parcours de la boucle principale de $DDMin(P, T)$ après l'appel à split : $delta = \Delta^i$ avec $i\in\mathbb⟦1, n⟧$ le nombre de passage dans la boucle principale.\
> Si la partition passée en paramètre à $DDMin$ est équilibrée alors $\Delta$ l'est aussi.\
>
> Lors d'un appel récursif, l'arbre associé à $DDMin(P', T)$, où $P'$ est un sous partition d'une certaine partition $\Delta^i\in\Delta$, est un sous arbre de $\Delta$ d'indice $i$.
>
> De plus, si $delta$ est une sous partition de $\Delta^i$ alors si $\Delta$ est n'est pas maxiamale : $spilt(delta)[0]$ est une sous partition de $\Delta^{i+1}$

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

<details>
  <summary><strong>Cliquez pour voir la preuve</strong></summary>

> TODO

</details>

  </div>
</div>
  </div>
</div>

<div class="remarque">
  <div class="remarque-title">Remarque : </div>
  <div class="remarque-body">

> On notera que ici la numérotation de l'arbre commence à 0 

  </div>
</div>

## VI. Analyse de Complexité

### Complexité du chemin critique

<div class="proposition">
  <div class="proposition-title">Proposition : Complexité critique de DDMin en $2ln_2(n)</div>
  <div class="proposition-body">

> La longueur de la plus longue séquence d'appels à la fonction test dans une execution de DDMin sur un problème avec un espace de recherche de cardinal N vaut au plus $\lceil 2ln_2(N)\rceil$.

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

<details>
  <summary><strong>Cliquez pour voir la preuve</strong></summary>

> Soit $(E,T)$ un problème, $P$ une partition de E et $\mathcal{A} = \Delta^0\rightarrow...\rightarrow\Delta^n$ où $\Delta^0 = P$ l'arbre terminal associé à l'exection de $DDMin(P, T)$.\
> On montre par récurrence forte sur $n\geq 0$ que la longueur de la plus longue séquence d'appels à test est inférieur à 2n, on note cette assertion $P(n)$
>
> ## Initialisation:
> Si $n = 0$ comme l'arbre est terminal on a alors $\Delta^0$ maximale et donc le programme retourne immédiatement sans executer de fonction test, d'où $P(0)$
>
> ## Hérédité:
> Soit $n\in\mathbb{N}$ tel que $\forall m\leq n, P(m)$, montrons $P(n+1)$:
>
> Soit k le nombre de passage dans la boucle principale de $DDMin$, on note $delta_i$ la valeur de $delta$ dans chaque boucle (en numérotant les boucles de 1 à k).\
> En se servant de la structure de DDMin, on sait que $\forall i\in ⟦1, k⟧, delta_i = \Delta^i$ et ainsi on a $k\leq n$.
> On notera que, par boucle, la plus grande séquence d'appels à test est de longueur 2, un pour les nabla et un pour la matrice (qui peut dans certains cas ne pas executer de tests du tout).
>- Si on termine en sortant de la boucle, on a appelé la fonction test au plus $2k$ fois et on conclut.
>
>- Sinon soit $i\in⟦1, k⟧$ le numéro de la boucle dans laquelle on fait un appel récursif.
>- Si on fait un seul appel récursif :
>   - $next1$ est une sous partition de $delta_i$ donc de $\Delta^i$, d'où l'arbre associé à $DDMin(next1, T)$ un sous arbre de $\Delta$ d'indice i et $m = (n+1) - (i+1)$ sa taille (on a des arbres qui commencent à zéro).\
>   - Donc d'après P(m) (on a bien $m\leq n$) la séquence d'appel la plus longue dans $DDMin(next1, T)$ est inférieure à 2m et donc au total on a une séquence maximale d'une longueur $l\leq 2m + 2i \leq 2n$ et on conclut.
>- Si on en fait deux la démonstration est essentiellement la même, il faudra seulement prendre en compte le max des deux séquences d'appel qui sont toutes deux majorées par 2m.
> D'où P(n+1), ce qui clot la récurrence.
>
> Or dans le cas où P = \{E\}, comme P est équilibré d'après la structure de DDMin $\mathcal{A}$ est équilibré.\
> Et d'après la proposition ** on a $|\mathcal{A}| = n \leq \lceil ln_2(|E|)\rceil$.\
> Donc la longueur de la plus longue séquence d'appels à la fonction test dans l'execution de $DDMin(\{E\}, T)$ est d'au plus $\lceil 2ln_2(N)\rceil$.
>
> Ce qui conclut.

</details>

  </div>
</div>

  </div>
</div>

<div class="proposition">
  <div class="proposition-title">Proposition : Temps d'attente des atomes de cardinal 1</div>
  <div class="proposition-body">

> Soit $(E, T)$ un problème et $B$ ses atomes, soit $b\in B$ de cardinal 1, alors $RDDMin$ trouve $b à la première itération et le chemin critique jusqu'au retour d'une liste contenant $b$ contient moins de $\lceil ln_2(N)\rceil + 1$ appels à la fonction test

<div class="demo">
  <div class="demo-title">Démo :</div>
  <div class="demo-body">

<details>
  <summary><strong>Cliquez pour voir la preuve</strong></summary>

> La démonstration est essentiellement la même que la précédente en notant en plus que toute partition non triviale d'un problème qui contient au moins un atome de cardinal 1 est sépartante. A partir de là, chaque appel à DDMin ne peut faire qu'une itération dans la boucle avant de terminer (soit par maximalité, soit parce que la partition est séparante), et à chaque fois on transmet une partition de cardinal 1, on la split en 2, un des deux coté fail (parce que l'atome de cardinal 1 est forcément d'un des deux côté (d'où la suffisance)), le calcul de la matrice dans le cas où l'on a une partition à deux éléments ne nécessite pas d'appel à test (quand on divise en deux on a $\nabla_1 = \Delta_2$ et $\nabla_2 = \Delta_1$, donc les intersection sont soit vides soit triviales ($\nabla_1\cap\nabla_1 = \nabla_1$, on connait déjà le resultat)) et puis on fait un appel récursif sur l'un des deux nabla ou sur les deux qui se font en parallèle. Ensuite la structure de DDMin montre qu'il y a eu au plus $\lceil ln_2(N)\rceil$ appels récursifs, ce qui conclut.

</details>

  </div>
</div>

  </div>
</div>

### Complexité en Espace

- Tableaux `d[]` et `parent[]` : $O(n)$  
- File de priorité : $O(n)$  
- Mémoire totale : $O(n)$

---

## VI. Conclusion et Perspectives

Résumé des résultats :  

- L’algorithme **NomDeLAlgo** est **correct** (preuve section 4).  
- Il **termine toujours** (section 5).  
- Sa **complexité** est $O((n+m)\log n)$ avec un tas binaire (section 6).  

### Perspectives / Améliorations

- Utiliser un **Fibonacci heap** pour obtenir $O(m + n \log n)$.  
- Adapter l’algorithme aux graphes dirigés avec poids négatifs (Johnson’s algorithm).  
- Étendre à des cas où les arêtes sont ajoutées dynamiquement (algorithme en ligne).

> Ainsi, l’algorithme est optimal pour les graphes denses et peut être amélioré pour des cas spécifiques. $\square$
