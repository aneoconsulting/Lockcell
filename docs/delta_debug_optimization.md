---
lang: fr
title: "Titre du document"
---
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

> **Convention 1 (Espace de recherche) :** On appelle espace de recherche un ensemble fini E

Cette convention permet de remettre cette étude dans le contexte de son développement, en effet on a un ensemble de perturabations possibles et on recherche "Celles qui ont un impact important sur le resultat", dans le cas d'un code de simulation, on peut associer chaque élément de E à la perturbation d'une ligne de code. Précisons le sens "d'avoir un impact important sur le résultat"


> **Définition 1 (Fonction test)** Soit E un espace de recherche, on appelle fonction test sur E toute fonction croissante $$T: (E, \subseteq ) \longrightarrow (\{✓,✗\}, \leq)\text{ avec }✓ \leq ✗$$ $\newline$ Telle que:
>- $T(\varnothing) = ✓$
>- $T(E) = ✗$
>
> Autrement dit $\forall A,B \in \mathcal{P}(E), (A \subseteq B \text{ et } T(A) = ✗) \Rightarrow T(B) = ✗$

On dira que la fonction test échoue sur un ensemble si sa valeur évaluée en cet ensemble vaut ✗

> **Définition 2 (Problème)** On définit un problème comme une paire $(E, T)$, avec $E$ un espace de recherche et $T$ une fonction test sur ce dernier.

Avoir ces deux premières définitions nous permettent de mathématiser le problème. Pour un ensemble $A\in\mathcal{P}(E)$ il faut voir $T(A)=✗$ comme : quand on applique toutes les perturbation de A, on perturbe fortement le résultat final, la fonction test traduit donc ce que l'on voit dans la réalité lorsque l'on fait un run du programme en perturbant certaines lignes pour reprendre notre exemple précédent.\
La fonction test permet donc de savoir si la partie que l'on regarde "contient une partie du problème". Afin de préciser cette dernière affirmation, nous avons besoin de la définition de la propriété suivante : 

> **Définition 3 (Propriété ($\star$)) :** Soit $(E, T)$ un problème, $n\in\mathbb{N}^*$ et $b_1,...,b_n\in\mathcal{P}(E)$, on dit que $B = \{b_1,...,b_n\}$ verifie ($\star$) ou que $b_1,...,b_n$ vérifient ($\star$) si $$\forall i \neq j \in \llbracket 1, n\rrbracket, b_i \nsubseteq b_j \text{ et } \forall i \in \llbracket 1, n\rrbracket, b_i \neq \varnothing$$ 

On remarque que cette définition est symétrique quitte à inverser i et j.

> **Propriété 1 (Équivalence atomique)** Soit $(E, T)$ un problème, il existe des uniques $n\in\mathbb{N}^*$ et $b_1,...,b_n\in\mathcal{P}(E)$ vérifiant ($\star$) tels que $$\forall C \in \mathcal{P}(E), T(C) = ✗ \iff \exists i \in \llbracket 1, n\rrbracket: b_i \subseteq C$$
On dit alors que $b_1,...,b_n$ sont les atomes du problème.\
> De plus, l'application $f: T \mapsto \{b_1,...,b_n\}$ est une bijection de l'espace des fonctions test vers $\{\{b_1,...,b_n\} \in \mathcal{P}(E)^n \text{ } \big| \text{ } n \in \mathbb{N}^* \text{ et } \{b_1,...,b_n\} \text{ vérifient } (\star) \}$

>**Demo (propriété) :** Soit $(E, T)$ un problème, soit $\Gamma = \{A\in \mathcal{P}(E) \text{ }\big|\text{ } T(A)=✗\}$ Comme $E$ est fini $\Gamma$ l'est aussi et comme $T(E) = ✗$, $\Gamma$ est non vide donc il existe $n\in\mathbb{N}^*$ et $b_1,...,b_n$ les éléments minimaux de $\Gamma$.
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


> **Demo (fonction f) :**
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

Cette démonstration nous permettra donc de parler d'un problème indifféremment de sa définition que ce soit $(E, T)$ ou $(E, B = \{b_1,..,b_n\})$.

Maintenant que nous avons défini notre problème, il est clair que notre objectif va être de déterminer des éléments $b_1,...,b_n$ au sein d'un problème.

Cependant, il nous reste encore un aspect des problèmes à traiter, en effet, on a vu qu'au sein d'un problème on avait des atomes à déterminer, mais dans le cas où ces atomes ont des intersection non nulles il devient compliquer de les traiter dans la pratique.\
En effet, imaginons un ensemble simple {1, 2, 3} et $b_1 = \{1, 2\}$, $ b_2 = \{2, 3\}$, alors imaginons que nous "fixons" le bug représenté par $b_1$, alors on a "retiré" l'incertitude représentée par 2, dans le cas de nos lignes de code, cela correspond par exemple à augmenter la précision sur les lignes 1 et 2. Dans ce cas là, nous avons en quelque sorte retiré les perturbations possibles des lignes 1 et 2, et trouver $b_2$ n'a plus forcément de sens. Pour cette raison nous introduisons une dernière définition :

> **Définition 4 (problème bien posé):** Soit $(E, B)$ un problème, on dit que ce problème est bien posé si tous les éléments de B sont disjoints.

> ***Remarque :*** La définition précédente permet de se rendre compte de l'utilité de la bijection entre atomes et fonction test lorsque l'on veut parler d'un problème.

> **Défintion 5 (problème trivial):** On dit d'un problème $(E, B)$ qu'il est trivial si  E est un atome, c'est à dire si $B = \{E\}$.\
> Cela équivault à dire : $\forall A \in \mathcal{P}(E), T(A) = ✗ \iff A = E$

> **Définition 5 (sous problème):** Soit $(E,T)$ un problème et $B$ ses atomes. Soit F une sous partie de E telle que $T(F) = ✗$, on dit alors que $(F, T_{|F})$ est un sous problème de $(E, T)$.\
> On a alors que $(F, T_{|F})$ est un problème et ses atomes sont les élements de $B_{|F} = \{b\in B \text{ | } b \subseteq F\}$

> ***Remarque :*** On a bien $B_{|F}$ non vide, en effet d'après l'équivalence atomique comme $T(F) = ✗$ on a bien $b\in B$ tel que $b \subseteq F$

### 2. Introduction des outils

Maintenant que nous avons pu poser précisemment ce qu'est un problème, nous allons introduire les outils qui nous permettrons de trouver ses atomes.

> **Définition 5 (partition maximale):** Soit E un espace de recherche et $\Delta = (\Delta_i)_{i = 1}^n \in \mathcal{P}(E)^n$ une partition de E\
> On dit que $\Delta$ est maximale si $\Delta = \{\{x\}\text{ | }x\in E\}$

> **Définition 6 (raffinement de partitions):**
> Soit E un espace de recherche, $\Delta = (\Delta_i)_{i = 1}^n \in \mathcal{P}(E)^n \text{ et } \delta = (\delta_i)_{i = 1}^m \in \mathcal{P}(E)^m$ deux partitions de E. On dit que $\delta$ raffine $\Delta$ si :
>
> $$ \forall i \in \llbracket 1, n \rrbracket, (|\Delta_i| = 1\text{ et } \exists i_0 \in \llbracket 1, m \rrbracket: \Delta_i = \delta_{i_0})\text{ ou }(\exists i_0, j_0\in \llbracket 1, m \rrbracket: \delta_{i_0} \sqcup \delta_{j_0} = \Delta_i)$$
> On définit alors la fonction de correspondance $f: \llbracket 1, n \rrbracket \longrightarrow \mathcal{P}_1(\llbracket 1, m \rrbracket)\cup \mathcal{P}_2(\llbracket 1, m \rrbracket)$ telle que $$\forall i\in \llbracket 1, n \rrbracket, \Delta_i = \bigcup_{j \in f(i)} \delta_j$$

> ***Remarque :*** Cette définition est potentiellement un peu désagréable à digérer mais ce qu'il faut comprendre c'est que $\delta$ est la même partition que $\Delta$ où l'on a coupé chaque partie en deux d'où : $\exists i_0, j_0\in \llbracket 1, m \rrbracket: \delta_{i_0} \sqcup \delta_{j_0} = \Delta_i$, sauf dans le cas où $\Delta_i$ était de cardinal 1 au quel cas on l'a simplement conservé, d'où : $|\Delta_i| = 1\text{ et } \exists i_0 \in \llbracket 1, m \rrbracket: \Delta_i = \delta_{i_0}$

> **Définition 7:** On définit un raffinement $\Delta \rightarrow \delta$ comme la donnée de deux partitions $\Delta$ et $\delta$ telles que $\delta$ raffine $\Delta$ et d'une fonction de correspondance f telle que définie dans la défintion précédente

Cette première définition nous permet de faire une recherche binaire dans notre espace de recherche et de définir un arbre de recherche:

>**Définition 7 (Arbre de recherche):** Soit $E$ un espace de recherche, on définit un arbre de recherche de taille n sur E comme une suite de partitions $(\Delta^i)_{i=1}^n$ telle que $\Delta^1 = \{E\}$ et :
> $$ \forall i \in \llbracket 1, n-1 \rrbracket, \Delta^{i+1} \text{ raffine } \Delta^i$$

>***Remarque :*** On pourra de la même façon définir un arbre de recherche à partir d'une suite de correspondances : $\Delta^1\rightarrow...\rightarrow\Delta^n$

> **Défintition 8 (Arbre terminal):** Soit $E$ un espace de recherche et $\Delta = (\Delta_i)_{i = 1}^n \in \mathcal{P}(E)^n$ un arbre sur $E$.
>- On dit que $\Delta$ est un arbre terminal si $\Delta^n$ est une partition maxiamale

> **Propriété 2 :** Soit $E$ un espace de recherche, la taille des arbres de recherche sur $E$ est bornée par $|E|$\
> De plus, la partition la plus fine d'un arbre de recherche de taille maximale est maximale 

> **Démo :**

Le sens de cette dernière définition est assez clair normalement, on coupe récursivement notre ensemble en deux, ce qui s'apparente au parcours d'un arbre.\
Néanmoins pour éviter des surprises désagréables lors des démonstration il est préférable de travailler avec des "arbres équilibrés".


> **Définition 8 (partition équilibrée):** Soit E un espace de recherche et $\Delta = (\Delta_i)_{i = 1}^n \in \mathcal{P}(E)^n$ une partition de ce dernier. On dit que $\Delta$ est équilibrée si :
> $$\forall i,j \in \llbracket 1, n \rrbracket, \big| |\Delta_i| - |\Delta_j|\big| \leq 1

> **Définition 9 (arbre équilibré):** On dit d'un arbre qu'il est équilibré si toutes les partitions qui le composent sont équilibrées.

> **Propriété 3 :** La taille des arbres de recherhce équilibrés sur un espace de recherche $E$ est bornée par $\lceil log_2(|E|)\rceil$\
> De plus la partition la plus fine d'un arbre de recherche équilibré est maximale ssi l'arbre est de taille maximale 

> **Démo :**

On définit ainsi la notion de "couper notre ensemble en deux de façon équilibré". On pourrait montrer que de tels arbres existent, mais on exhibera plus loin une façon de le faire dans un algorithme, ce qui prouvera leur existence.


Nous allons par la suite beaucoup travailler avec des partitions alors, afin de s'éviter de complexes unions d'ensembles qui pourraient inutilement nuire à la compréhensions, nous allons introduire quelques notations en plus.

> **Convention 2:** Soit $\Delta$ une partition de E, on se permettra d'indicer les éléments de $\Delta$ par eux même et donc d'écire $\Delta_i, i\in\Delta$ pour les représenter.

> **Convention 3:** Dans la suite de cet étude nous nous intéresserons très régulièrement aux complémentaires des élements d'une partition $\Delta$ à tel point que l'on notera, pour $i\in\Delta$, $\nabla_i$ le complémentaire de $\Delta_i$ dans E.

> ***Remarque :*** Notez dans dans l'exemple précédent nous utilisons la convention numéro 2 pour désigner un élément de $\Delta$ par lui même.

Comme nous manipulerons beaucoup de partitons dans la suite de cette étude nous convenons maintenant que l'indice du haut correspondra systématiquement aux élément d'une famille de partition, alors que l'indice du bas lui correspond à un élément de cette partition. Si bien que $\Delta^n$ représente une partition, $\Delta^n_i$ un élément de cette partition et $\nabla^n_i$ le complémentaire de cet élément dans l'espace de recherche courant (celui que partitionne $\Delta^n$).


Enfin nous introduisons la notion de conjugaison :

> **Definition n(conjugaison):** Soit E un espace de recherche et $\Delta^1 \rightarrow \Delta^2$ un raffinement et $f$ la fonction de correspondance associée.\
> Soit $i,j \in \Delta^2$ on dit que $\Delta^2_i$ et $\Delta^2_j$ sont conjugués et on note $\overline{\Delta^2_i} = \Delta^2_j$ si :
> $$\{i,j\}\in Im(f)$$
> On remarque que quand on ne peut pas couper en deux lors du raffinement et que l'on a $\Delta^1_{i_0} = \Delta^2_{j_0}$ alors $\Delta^2_{j_0}$ est son propre conjugué.

>***Remarque :*** On étend la notation aux complementaire de la façon suivante :
>- Si $\overline{\Delta_i} = \Delta_j$ alors $\overline{\nabla_i} = \nabla_j$
>
> La relation être conjugué de quelqu'un est symétrique


### 3. Problème projeté

Enfin, avant de rentrer dans le coeur du sujet, il nous reste à définir la notion de projection qui nous permettra de manipuler aisément nos partition et leurs interactions avec la fonction test.

> **Définition n(partition grossière):** Soit $(E, T)$ un probblème, on dit d'une partition $\Delta$ qu'elle est grossière si
> $$\forall i\in\Delta, T(\nabla_i) = ✓$$
> On la dit séparante dans le cas contraire

>***Remarques :*** La défintion précédente implique directement que $\forall i\in\Delta, T(\Delta_i) = ✓$
>- On rappelle que l'on indice les éléments de $\Delta$ par eux même, donc $\forall i\in\Delta, T(\Delta_i) = ✓$ signifie que pour tous les éléments de notre partition la fonction test n'échoue pas dessus.
>- De même $\forall i\in\Delta, T(\nabla_i) = ✓$ signifie que la fonction test n'échoue sur aucun des complémentaires des éléments de notre partition.

Cette définition nous permet de dire d'une partition si elle est intéressante, en effet si un partition est séparante, cela signifie que l'on peut trouver $i\in \Delta$ tel que $T(\nabla_i) = ✗$.\
On peut donc trouver un ensemble strictement plus petit qui contient une partie du problème.

> **Proposition 1 :** Soit $(E, T)$ un problème. Soit $\Delta_1 \rightarrow \Delta_2$ un raffinement, alors si $\Delta_2$ est grossière $\Delta_1$ l'est aussi.

> **Démo :**


> **Remarque :** Cette proposition est équivalente à :\
> Soit $\Delta_1 \rightarrow \Delta_2$ un raffinement, alors si $\Delta_1$ est séparante $\Delta_2$ l'est aussi. (Contraposée)

> **Définition (Raffinement efficace):** Soit $\Delta^1 \rightarrow \Delta^2$ un raffinement, on dit qu'il est efficace si $\Delta^1$ est grossière et que $\Delta^2$ est séparante.

>**Proposition 2 :** Soit $(E, T)$ un problème, $\Delta^1 \rightarrow \Delta^2$ un raffinement efficace, soit $i,j\in\Delta^2$ on a :
> $$\overline{\nabla_i} = \nabla_j \Rightarrow T(\nabla_i\cap\nabla_j) = ✓$$

> **Démo :**

Maintenant, il ne nous reste qu'à définir la projection d'un problème

> **Définition n (Problème projeté):** Soit $(E, T)$ un problème et $\Delta$ une partition de $E$. On définit $T_{\Delta}$ une fonction test sur $\Delta$ (en tant qu'ensemble) de la façon suivante: 
> $$ \forall I \subseteq \Delta, T_{\Delta}(I) = T\Big(\bigcup_{i\in I}\Delta_i\Big)$$
> On vérifie bien que $T_{\Delta}$ est une fonction test sur $\Delta$.\
> On appelle $(\Delta, T_{\Delta})$ le projeté de $(E, T)$ sur $\Delta$.

> **Definition (Projection exacte):** Soit $(E, T)$ un problème $B$ ses atomes, $\Delta$ une partition de $E$, et $(\Delta, T_{\Delta})$ le projeté de $(E, T)$ sur $\Delta$.\
> On définit la projection exacte de $B$ sur $\Delta$ comme l'ensemble:
> $$\Big\{\{k\in \Delta\text{ | } B_i \cap \Delta_k \neq \varnothing \}\text{ } \Big | \text{ } i \in \llbracket 1, card(B)\rrbracket\Big\}

Illustration

Même si $(E, T)$ est bien posé et donc que $B$ vérifie ($\star$), il est possible que la projection exacte de $B$ sur $\Delta$ ne vérifie pas ($\star$), pour cela on définit la projection (réduite) de $B$ sur $\Delta$

> **Definition (Projection):** Soit $(E, T)$ un problème $B$ ses atomes, $\Delta$ une partition de $E$, et $B'$ le projeté de $B$ sur $\Delta$, on pose :
> $$ P_{\Delta} = \{b\in B' \text{ | } \exists b' \in B' : b' \subset b \} $$
> Et on définit, $B^{\Delta}$ la projection réduite de $B$ sur $\Delta$ comme :
> $$ B^{\Delta} = B' \setminus P_{\Delta}$$
> On abusera du langage et on parlera directement de "projection" de $B$ sur $\Delta$.\
> On dit que les atomes correspondants aux éléments de $P_{\Delta}$ sont perdus.

> **Propriété :** Soit $(E, T)$ un problème et B ses atomes, $\Delta$ une partition de E, $(\Delta, T_{\Delta})$ le problème projeté et $B^{\Delta}$ la projection de $B$ sur $\Delta$.
>$$\text{Les atomes projetés } B^{\Delta} \text{sont les atomes de} (\Delta, T_{\Delta})$$

> **Démo :**

> **Proposition :** Les atomes de cardinal 1 ne sont jamais perdus.

> **Démo :**

La notion de projection n'a rien de mystérieux, il faut considérer cela comme regarder notre ensemble de départ à travers les éléments de la partition. Les éléments d'un même $\Delta_i$ sont inséparable et quand on trouve nos atomes à cette échelle, on raffine cette partition afin de retirer les bouts inutiles, voici une illustration grossière pour mieux comprendre :


Maintenant que nous avons introduit les notions essentielles à l'étude de nos espaces de recherche afin de déterminer leur atomes, nous allons pouvoir entrer dans le coeur du sujet avec la description l'algorithme central.

## III. Description de l’algorithme

On considère un algorithme récursif :

### Entrées et Sorties

- **Entrée :**  
  - un problème $(E, T)$
    - Sous la forme d'une liste E, représentant les éléments de E
    - Et d'une fonction 'test', représentant T 

- **Sortie :**  
  - Liste de sous liste de la liste d'entrée E, contentant une partie des atomes de notre problème

### Pseudo-code

```text
Algorithm NomDeLAlgo(G, s):
  // Initialisation
  pour chaque sommet v dans V:
      d[v] ← ∞
      parent[v] ← null
  d[s] ← 0

  Q ← file de priorité contenant tous les sommets

  // Boucle principale
  tant que Q ≠ ∅:
      u ← extraire_min(Q)
      pour chaque voisin v de u:
          si d[u] + w(u,v) < d[v]:
              d[v] ← d[u] + w(u,v)
              parent[v] ← u
              mettre_à_jour(Q)

  retourner d, parent
```

## IV. Preuve de Correction

### Invariants

> **Invariant principal :** après chaque itération de la boucle, les sommets extraits de $Q$ possèdent leur distance minimale définitive.

Tu peux aussi énoncer des **lemmes** intermédiaires si nécessaire :  

> **Lemme 1.** Si un sommet $u$ est extrait de $Q$ avec $d[u]$, alors $d[u] = d^*(u)$ (distance optimale).  

**Preuve (esquisse) :**  
On montre par induction sur le nombre de sommets extraits :  

- **Base :** $d[s] = 0$ est correct à l’initialisation.  
- **Hérédité :** supposons l’invariant vrai jusqu’au $k$-ième sommet extrait.  
  À l’étape $k+1$, on choisit $u$ de distance minimale, donc aucune mise à jour future ne peut améliorer $d[u]$.  
- **Conclusion :** par induction, chaque sommet extrait est correct.  

Ainsi, à la fin de l’exécution :  

$$
\forall v \in V, \quad d[v] = d^*(v)
$$

Ce qui prouve la **correction** de l’algorithme. $\square$

---

## V. Preuve de Terminaison

On montre que la boucle principale ne peut pas être infinie :

- À chaque itération, au moins un sommet est retiré de $Q$.  
- Comme $Q$ contient initialement $|V|$ sommets et qu’aucun n’est réinséré, le nombre d’itérations est au plus $|V|$.  

Donc l’algorithme termine toujours après un nombre fini d’étapes. $\square$

---

## VI. Analyse de Complexité

### Complexité en Temps

Décompose les coûts étape par étape :  

1. **Initialisation :**  
   $O(n)$ affectations pour $d[v]$ et `parent[v]`.

2. **Boucle principale :**
   - Extraction du minimum : $O(\log n)$ avec un tas binaire (répété $n$ fois → $O(n \log n)$).  
   - Relaxations : $O(m)$ mises à jour potentielles, chacune coûte $O(\log n)$ → $O(m \log n)$.  

**Bilan :**  

$$
T(n,m) = O(n \log n + m \log n) = O((n+m)\log n)
$$

> Si $m = O(n)$ (graphe peu dense), on peut simplifier : $T = O(n \log n)$.

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
