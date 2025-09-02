# Titre de l’article

_Auteur(s), Date_

---

## Introduction

Ici, tu présentes le contexte du problème, la motivation et l’énoncé à démontrer.

Exemple d’énoncé mathématique simple en **LaTeX** :  
$E = mc^2$ ou bien une équation affichée :  

$$
\int_{0}^{1} x^2 \, dx = \frac{1}{3}
$$

---

## Définitions

Quelques symboles utiles :  

- Ensembles : $\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}$  
- Appartenance : $x \in A$, inclusion $A \subseteq B$  
- Complémentaire : $A^c$  
- Cardinalité : $|A|$  

Exemple de définition :  

> **Définition.** Une suite $(u_n)_{n \in \mathbb{N}}$ est dite convergente s’il existe $L \in \mathbb{R}$ tel que  
> $$
> \forall \varepsilon > 0, \exists N \in \mathbb{N}, \forall n \geq N, \ |u_n - L| < \varepsilon.
> $$

---

## Propriétés

### Propriétés générales
- Linéarité : $a(b+c) = ab + ac$  
- Distributivité : $(x+y)z = xz + yz$  
- Commutativité : $x+y = y+x$  

### Symboles utiles
- Sommes : $\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$  
- Produits : $\prod_{k=1}^{n} k = n!$  
- Limites : $\lim_{n \to \infty} \frac{1}{n} = 0$  
- Dérivées : $\frac{d}{dx} \left( x^n \right) = nx^{n-1}$  
- Intégrales : $\int e^x dx = e^x + C$  
- Équations différentielles : $\frac{dy}{dx} + y = 0$  
- Matrices :  
  $$
  A = \begin{pmatrix}
  a & b \\
  c & d
  \end{pmatrix}, \quad
  A^{-1} = \frac{1}{ad-bc} \begin{pmatrix}
  d & -b \\
  -c & a
  \end{pmatrix}
  $$

---

## Cœur de la preuve

1. **Hypothèses de départ**  
   Soit $f : \mathbb{R} \to \mathbb{R}$ continue et dérivable.  

2. **Étapes intermédiaires**  
   On utilise la dérivée :  
   $$
   f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
   $$  

   Puis on applique un théorème (par ex. Rolle, Cauchy, Taylor).  

3. **Cas particuliers**  
   - Pour $n=0$ : trivial.  
   - Pour $n=1$ : on vérifie directement.  

4. **Conclusion partielle**  
   On regroupe les résultats :  
   $$
   \forall n \in \mathbb{N}, \quad P(n) \implies P(n+1).
   $$  

---

## Conclusion

On résume la démonstration et on ouvre sur une généralisation possible.  

**Formule finale démontrée :**  
$$
e^{i\pi} + 1 = 0
$$

---

## Annexe : gros bloc de symboles pour référence rapide

- Racine : $\sqrt{x}$, $\sqrt[n]{x}$  
- Fractions : $\frac{a}{b}$  
- Indices : $x_i$, exposants : $x^n$  
- Vecteur : $\vec{u}$, $\overrightarrow{AB}$  
- Norme : $\|x\|$  
- Probabilités : $\mathbb{P}(A)$, Espérance : $\mathbb{E}[X]$, Variance : $\mathrm{Var}(X)$  
- Logique : $\forall, \exists, \neg, \implies, \iff$  
- Inférieur/égal : $\leq$, Supérieur/égal : $\geq$  
- Ensemble vide : $\varnothing$  
- Accolades : $\{ x \in \mathbb{R} \mid x > 0 \}$  
- Somme double : $\sum_{i=1}^{n} \sum_{j=1}^{m} a_{ij}$  
- Produit scalaire : $\langle u, v \rangle$  
- Dét(A) : $\det(A)$  

---
