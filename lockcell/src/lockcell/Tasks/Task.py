"""
Created on : 2025-07-07
Author   : Erwan Tchaleu
Email    : erwan.tchale@gmail.com

"""

from pymonik import task, MultiResultHandle

from typing import List, Tuple, Optional, Union
import lockcell.Tasks.TaskEnv as TaskEnv

### NTask


@task
def nTask(
    delta: list,
    n: Union[int, List[list]],
    config: TaskEnv.Config,
    me,
    Recurse=True,
    Result: Optional[bool] = None,
    oneSub: List[int] = [],
):
    """
    The only task that execute a test. If the test passes, it returns the result. If it fails,
    the task may resubmit additional sub-tests depending on the configuration.

    Args:
        delta (list): List of elements to perturb during the test.
        n (Union[int, List[list]]): Subdivision strategy — either an integer (split delta into `n` parts),
            or an explicit partition provided as a list of lists.
        config (BaseConfig.BaseConfig): Configuration object used to execute the test.
        me (Graph): Graph used for dependency tracking or visualization.
        Recurse (bool, optional): If False, the task returns the result directly without further subdivision.
            Defaults to True.
        Result (Optional[bool], optional): If known, the expected result. Used when only resubmitting a test.
            Defaults to None.
        oneSub (List[int], optional): When `n` is a list of lists, this indicates which subsets
            cannot be split further (typically because they are of size one). This is used to
            preserve the binary tree structure. Not used by this task, but forwarded for consistency.
            Defaults to an empty list.


    Returns:
    Tuple[Union[List[list], str], bool]: A pair where:
        - the first element is either a list containing the 1 minimal failing subset of `delta`,
          or the string `"Input"` if `Recurse` is False (used as a marker to indicate delegation);
        - the second element is a boolean indicating whether `delta` is a failing subset.

    This task may delegate to a nAGG task, which returns a result in the same format.

    """

    ### PrintGraph ###
    gPrint = me is not None
    if gPrint:
        from controllers import Graph

        me.setType(f"{n}Task")

    # Si le resultat est déjà connu on ne teste pas
    test = None
    if Result is None:
        test = config.Test(delta)
    else:
        test = Result

    if test:  # Test le delta passé en param
        ### PrintGraph ###
        if gPrint:
            me.sout(me, [None, True])
        return None, True

    if not Recurse:  # Si pas de récusivité
        ### PrintGraph ###
        if gPrint:
            me.sout(me, ["Input", False])
        return "Input", False

    # Si le test fail

    # Si |Delta| = 1 on a fini
    if len(delta) == 1:
        ### PrintGraph ###
        if gPrint:
            me.sout(me, [[delta], False])
        return [delta], False

    # Sinon on split en n (= granularity)
    if isinstance(n, int):
        subdiv = TaskEnv.split(delta, n)
    else:
        subdiv = n
    subdivArg = [
        (delta, 2, config, Graph() if gPrint else None) for delta in subdiv
    ]  # Mise en forme pour le passage en paramètre
    GrOut = None

    ### PrintGraph ###
    if gPrint:
        GrOut = Graph()
    result = nTask.map_invoke(subdivArg)  # type: ignore

    ### PrintGraph ###
    if gPrint:
        counter = 0
        for i in subdivArg:
            if counter in oneSub:
                me.down(i[3], i[0], "o")
            else:
                me.down(i[3], i[0])
            counter += 1
            out = i[3].out[0]
            while out != out.out[0]:
                out = out.out[0]
            GrOut.sup(*out.out)
        me.sout(GrOut, None)
    if isinstance(n, list):
        n = len(n)

    return nAGG.invoke(subdiv, result, n, config, GrOut, oneSub, delegate=True)  # type: ignore


#########################################################################################################
### NAGG
#########################################################################################################


@task
def nAGG(
    subdiv: List[list],
    answers: List[Tuple[List[list] | None, bool]],
    n: int,
    config: TaskEnv.Config,
    me,
    oneSub: List[int] = [],
):
    """
    nAGG is a task that analyzes the results of multiple `nTask` executions. If some tasks failed,
    it aggregates their results. Otherwise, it proceeds to test the complement of the tested subsets.

    Args:
        subdiv (List[list]): The current subdivision of `delta`, representing the subsets tested by each `nTask`.
        answers (List[Tuple[Optional[List[list]], bool]]): Results from each `nTask`. Each tuple contains either:
            - a 1 minimal failing subset list (or None), and
            - a boolean indicating whether the tested subset failed.
        n (int): The number of subsets in `subdiv`.
        config (BaseConfig.BaseConfig): Configuration object passed to downstream tasks. Also specifies
            post-processing behavior through `config.mode`, which can be `"default"` or `"analyse"`.
        me (Graph): Graph used for dependency tracking or visualization.
        oneSub (List[int], optional): This indicates which element of subdiv
            cannot be split further (typically because they are of size one). This is used to
            preserve the binary tree structure. Can be updated in this task #TODO, forwarded for consistency.
            Defaults to an empty list.

    Returns:
        Tuple[List[list], bool]: A pair where:
            - the first element is a list containing the 1 minimal failing subsets of delta.
            - the second element is a boolean indicating whether the combined subset (delta = the union of subsets) is failing.

        This task may delegate to a `nAGG2` or a `nAnalyser`, or return directly, following the same format.

    """

    ### PrintGraph ###
    gPrint = me is not None
    if gPrint:
        from controllers import Graph

        me.setType(f"{n}AGG")

    test = False
    for a in answers:
        if not a[1]:
            test = True
            break

    def merge(tabofrep):  # Merge sans doublon
        dic = {}
        res = []
        for rep in tabofrep:
            if rep[0] is None:
                continue
            for val in rep[0]:
                key = val.__str__()
                if key not in dic:
                    dic[key] = val
                    res.append(val)
        return res

    if test:  # Si l'un des sets à fail, on retourne directe l'union des set de subset
        rep = merge(answers)

        ### PrintGraph ###
        if gPrint:
            me.sout(me, [rep, False])
        return rep, False

    if (
        n == 2
    ):  # Optimisation : Si la granularité vaut 2, on ne test pas les complémentaires et on augmente directement la granularité
        omega = sum(subdiv, [])
        if len(omega) <= n:
            ### PrintGraph ###
            if gPrint:
                me.sout(me, [[omega], False])
            return [omega], False

        newdivision = []  # Pour le 2nAGG
        newdivisionArg = []  # Pour les nTask

        # TODO: Add the updating of oneSub, it doesn't happen often (granularity = 2) but for 3 sized delta it is important
        k = min(2 * n, len(omega))
        for delta in subdiv:  # Mise en forme des lis
            if len(delta) >= 2:
                temp = TaskEnv.split(delta, 2)
                newdivisionArg.append((temp[0], 2, config, Graph() if gPrint else None))
                newdivisionArg.append((temp[1], 2, config, Graph() if gPrint else None))
                newdivision.append(temp[0])
                newdivision.append(temp[1])
            else:
                newdivisionArg.append((delta, 2, config, Graph() if gPrint else None))
                newdivision.append(delta)

        result = nTask.map_invoke(newdivisionArg)  # type: ignore
        GrOut = None

        ### PrintGraph ###
        if gPrint:
            GrOut = Graph()
            for i in newdivisionArg:
                me.down(i[3], i[0])
                GrOut.sup(*i[3].out)
            me.sout(GrOut, None)

        return nAGG.invoke(newdivision, result, k, config, GrOut, delegate=True)  # type: ignore

    next = nAGG2
    recursion = True
    # Sinon on teste les complémentaires
    if config.mode == "Analyse":
        ### PrintGraph ###
        if gPrint:
            me.setType(f"{n}Analyser - Up")

        # Changement du type d'execution si mode Analyser
        recursion = False
        next = nAnalyser

    omega = sum(subdiv, [])
    k = max(2, n - 1)
    nablas = [
        (TaskEnv.listminus(omega, delta), k, config, Graph() if gPrint else None, recursion)
        for delta in subdiv
    ]
    result = nTask.map_invoke(nablas)  # type: ignore
    GrOut = None

    ### PrintGraph ###
    if gPrint:
        GrOut = Graph()
        counter = 0
        for i in nablas:
            if counter in oneSub:
                me.down(i[3], i[0], "o")
            else:
                me.down(i[3], i[0])
            counter += 1
            GrOut.sup(*i[3].out)
        me.sout(GrOut, None)

    return next.invoke(subdiv, result, n, config, GrOut, oneSub, delegate=True)  # type: ignore


#########################################################################################################
### NAGG2
#########################################################################################################


@task
def nAGG2(
    subdiv: List[list],
    answers: List[Tuple[List[list] | None, bool]],
    n: int,
    config: TaskEnv.Config,
    me,
    oneSub: List[int] = [],
):
    """
    `nAGG2` is a task triggered after a `nAGG` submits `nTask`s on the complementary subsets of `delta`.
    It analyzes the results of these `nTask` executions. If any tasks fail, it aggregates the results.
    Otherwise, it increases the granularity by splitting each subset in `subdiv` into two and resubmitting
    `nTask`s on those finer subsets. The resulting outputs are later gathered by a `nAGG`, which may in turn
    re-launch the complementary testing process if necessary.

    Args:
        subdiv (List[list]): The current subdivision of `delta`.
        answers (List[Tuple[Optional[List[list]], bool]]): Results returned from each `nTask`, where each task
            was executed on the **complementary** of a subset in `subdiv`. Each tuple contains:
            - either a 1 minimal failing subset list (or `None`), and
            - a boolean indicating whether the tested complementary subset failed.
        n (int): The number of subsets in `subdiv`.
        config (BaseConfig.BaseConfig): Configuration object forwarded to downstream tasks.
            The presence of a `nAGG2` implies that the program is running in `"default"` mode.
        me (Graph): Graph used for coordination or visualization, same as in other tasks.
        oneSub (List[int], optional): Not used in `"default"` mode, but required for signature consistency.
            This allows `nAGG` to treat `nAnalyser` and `nAGG2` interchangeably. Defaults to an empty list.

    Returns:
        Tuple[List[list], bool]: A pair where:
            - the first element is either a list containing the 1 minimal failing subsets of delta.
            - the second element is a boolean indicating whether the combined subset is failing.

        This task may delegate to a `nAGG`, or return directly, following the same result structure.
    """
    ### PrintGraph ###
    gPrint = me is not None
    if gPrint:
        from controllers import Graph

        me.setType(f"{n}AGG2")

    test = False
    for a in answers:
        if not a[1]:
            test = True
            break

    def merge(tabofrep):  # Merge sans doublon
        dic = {}
        res = []
        for rep in tabofrep:
            if rep[0] is None:
                continue
            for val in rep[0]:
                key = val.__str__()
                if key not in dic:
                    dic[key] = val
                    res.append(val)
        return res

    if test:  # Si l'un des complémentaire à fail, on retourne directe l'union des set de subset
        rep = merge(answers)

        ### PrintGraph ###
        if gPrint:
            me.sout(me, [rep, False])
        return rep, False

    # Sinon on augmente la granularité

    omega = sum(subdiv, [])
    if len(omega) <= n:  # Si granularité max on retourne le delta courant (omega)
        ### PrintGraph ###
        if gPrint:
            me.sout(me, [[omega], False])
        return [omega], False

    newdivision = []  # Pour le 2nAGG
    newdivisionArg = []  # Pour les nTask

    k = min(2 * n, len(omega))
    for delta in subdiv:  # Mise en forme des lis
        if len(delta) >= 2:
            temp = TaskEnv.split(delta, 2)
            newdivisionArg.append((temp[0], 2, config, Graph() if gPrint else None))
            newdivisionArg.append((temp[1], 2, config, Graph() if gPrint else None))
            newdivision.append(temp[0])
            newdivision.append(temp[1])
        else:
            newdivisionArg.append((delta, 2, config, Graph() if gPrint else None))
            newdivision.append(delta)
    result = nTask.map_invoke(newdivisionArg)  # type: ignore
    GrOut = None

    ### PrintGraph ###
    if gPrint:
        GrOut = Graph()
        for i in newdivisionArg:
            me.down(i[3], i[0])
            GrOut.sup(*i[3].out)
        me.sout(GrOut, None)

    return nAGG.invoke(newdivision, result, k, config, GrOut, delegate=True)  # type: ignore


#########################################################################################################
### NAnalyser
#########################################################################################################


@task
def nAnalyser(
    subdiv: List[list],
    answers: List[Tuple[List[list] | None, bool]],
    n: int,
    config: TaskEnv.Config,
    me,
    oneSub: List[int] = [],
):
    """
    `nAnalyser` is a task triggered after a `nAGG` submits `nTask`s on the complementary subsets of `delta`.
    It analyzes the results of these tasks. If any fail, it proceeds with further analysis (see algorithm
    documentation), prioritizing easy cases. In complex cases it submits computations for relevant complementary intersections and delegates to a `nAnalyserDown`.

    Otherwise, it increases the granularity by splitting each subset in `subdiv` into two and resubmitting
    `nTask`s on the finer subsets. The outputs are later gathered by a `nAGG`, which may re-launch the
    complementary testing process if necessary.

    Args:
        subdiv (List[list]): The current subdivision of `delta`.
        answers (List[Tuple[Optional[List[list]], bool]]): Results returned from each `nTask`, each executed
            on the **complement** of a subset in `subdiv`. Each tuple contains:
            - "Input" or None, since they were running in not recursing mode
            - a boolean indicating whether the tested set failed.
        n (int): The number of subsets in `subdiv`.
        config (BaseConfig.BaseConfig): Configuration object forwarded to downstream tasks.
            The presence of a `nAnalyser` implies the program is running in `"Analyse"` mode.
        me (Graph): Graph used for coordination or visualization, as in other tasks.
        oneSub (List[int], optional): Used to identify conjugate subsets.
            Defaults to an empty list.

    Returns:
        Tuple[List[list], bool]: A pair where:
            - the first element is a list of 1 minimal failing subsets of `delta`;
            - the second element is a boolean indicating whether the combined subset is failing.

        This task may delegate to a `nAGG` or a `nAnalyserDown`, or return directly, using the same result structure.
    """

    ### PrintGraph ###
    gPrint = me is not None
    if gPrint:
        from controllers import Graph

        me.setType(f"{n}Analyser - Down")

    test = False
    idxs = []
    idx = 0
    for a in answers:
        if not a[1]:
            test = True
            idxs.append(idx)
        idx += 1

    omega = sum(subdiv, [])  # Utile pour faire tous les complémentaires etc

    if test:  ##### Si l'un des complémentaire a fail, on analyse
        # Est-on au niveau de découpage le plus fin
        granularityMax = len(omega) == n
        if granularityMax and (len(idxs) == 1):  # TODO: cf. preuve
            rep = [TaskEnv.listminus(omega, subdiv[idxs[0]])]
            ### PrintGraph ###
            if gPrint:
                me.addLabel("One fail")
                me.addLabel("Granularity Max !")
                me.sout(me, [rep, False])
            return rep, False

        if len(idxs) == 1:  # Si un seul fail on recurse dessus
            # On prépare les arguments
            idx = idxs[0]
            nabla = TaskEnv.listminus(omega, subdiv[idx])

            GrOut = None
            ### PrintGraph ###
            if gPrint:
                me.addLabel("One fail")
                GrOut = Graph(emphas="orange")
                me.down(GrOut, nabla)
                me.sout(GrOut, None)

            newdivision = []
            oneSub = []
            idx_ = 0
            for div in subdiv:
                if div == subdiv[idx]:
                    continue
                if len(div) == 1:
                    newdivision.append(div)
                    oneSub.append(idx_)
                    idx_ += 1
                else:
                    temp = TaskEnv.split(div, 2)
                    newdivision.append(temp[0])
                    newdivision.append(temp[1])
                    idx_ += 2
            return nTask.invoke(
                nabla, newdivision, config, GrOut, True, False, oneSub, delegate=True
            )

        Achanger = True  # TODO: Activation de l'analyse ou pas à retirer
        if Achanger:
            ### PrintGraph ###
            if gPrint:
                me.setType(f"{n}Analyser - Middle")

            # On prépare les arguments pour chaque nabla qui bug, avec le nabla associé, la subdiv adaptée et on a déjà le resultat
            Args = []
            vals = [True for i in range(n)]
            for idx in idxs:
                vals[idx] = False

            # Création des Arguments pour tester les intersections
            # TODO: Adapter pour que si le split en deux n'etait pas possible on le sache
            idx = 0
            while idx < n:
                if idx in oneSub:
                    if not vals[idx]:
                        for j in range(idx + 1, n):
                            if not vals[j]:
                                intersection = TaskEnv.listminus(omega, subdiv[idx])
                                intersection = TaskEnv.listminus(intersection, subdiv[j])
                                Args.append(
                                    (intersection, 2, config, Graph() if gPrint else None, False)
                                )
                    idx += 1
                    continue
                if not vals[idx]:
                    for j in range(idx + 2, n):
                        if not vals[j]:
                            intersection = TaskEnv.listminus(omega, subdiv[idx])
                            intersection = TaskEnv.listminus(intersection, subdiv[j])
                            Args.append(
                                (intersection, 2, config, Graph() if gPrint else None, False)
                            )
                idx += 1
                if not vals[idx]:
                    for j in range(idx + 1, n):
                        if not vals[j]:
                            intersection = TaskEnv.listminus(omega, subdiv[idx])
                            intersection = TaskEnv.listminus(intersection, subdiv[j])
                            Args.append(
                                (intersection, 2, config, Graph() if gPrint else None, False)
                            )
                idx += 1

            # Building the conjugated tab
            conjugate = [None for _ in range(n)]
            idx = 0
            while idx < n:
                if idx in oneSub:
                    conjugate[idx] = idx if not vals[idx] else None  # type: ignore
                    idx += 1
                    continue
                if not vals[idx] and not vals[idx + 1]:
                    conjugate[idx] = idx + 1  # type: ignore
                    conjugate[idx + 1] = idx  # type: ignore
                else:
                    conjugate[idx] = idx if not vals[idx] else None  # type: ignore
                    conjugate[idx + 1] = idx + 1 if not vals[idx + 1] else None  # type: ignore
                idx += 2

            Nanswers = nTask.map_invoke(Args)
            GrOut = None

            ### PrintGraph ###
            if gPrint:
                GrOut = Graph()
                for arg in Args:
                    me.down(arg[3], arg[0])
                    GrOut.sup(*arg[3].out)
                me.sout(GrOut, None)

            return nAnalyserDown.invoke(
                subdiv, Nanswers, conjugate, n, config, GrOut, delegate=True
            )

        else:  # Pas de traitement
            ### PrintGraph ###
            if gPrint:
                me.addLabel("No Opti")

            # On prépare les arguments pour chaque nabla qui bug, avec le nabla associé, la subdiv adaptée et on a déjà le resultat
            Args = []
            vals = [True for i in range(n)]

            for idx in idxs:
                k = min(n - 1, len(omega) - len(subdiv[idx]))
                Args.append(
                    (
                        TaskEnv.listminus(omega, subdiv[idx]),
                        k,
                        config,
                        Graph(emphas="orange") if gPrint else None,
                        True,
                        False,
                    )
                )
            answers = nTask.map_invoke(Args)

            GrOut = None

            ### PrintGraph ###
            if gPrint:
                GrOut = Graph()
                for arg in Args:
                    me.down(arg[3], arg[0])
                    GrOut.sup(*arg[3].out)
                me.sout(GrOut, None)

            return nAGG2.invoke(subdiv, answers, len(idxs), config, GrOut, delegate=True)  # type: ignore

    # Sinon on augmente la granularité

    if len(omega) <= n:  # Si granularité max on retourne le delta courant (omega)
        ### PrintGraph ###
        if gPrint:
            me.addLabel("Granularity Max !")
            me.sout(me, [[omega], False])
        return [omega], False

    ### PrintGraph ###
    if gPrint:
        me.addLabel("granularity up")

    newdivision = []  # Pour le 2nAGG
    newdivisionArg = []  # Pour les nTask

    k = min(2 * n, len(omega))
    oneSub = []
    idx = 0
    for delta in subdiv:  # Mise en forme des lis
        if len(delta) >= 2:
            temp = TaskEnv.split(delta, 2)
            newdivisionArg.append((temp[0], 2, config, Graph() if gPrint else None))
            newdivisionArg.append((temp[1], 2, config, Graph() if gPrint else None))
            newdivision.append(temp[0])
            newdivision.append(temp[1])
            idx += 2
        else:
            newdivisionArg.append((delta, 2, config, Graph() if gPrint else None))
            newdivision.append(delta)
            oneSub.append(idx)
            idx += 1
    result = nTask.map_invoke(newdivisionArg)  # type: ignore
    GrOut = None

    ### PrintGraph ###
    if gPrint:
        GrOut = Graph()
        for i in newdivisionArg:
            me.down(i[3], i[0])
            GrOut.sup(*i[3].out)
        me.sout(GrOut, None)

    return nAGG.invoke(newdivision, result, k, config, GrOut, oneSub, delegate=True)  # type: ignore


#########################################################################################################
### NAnalyserDown
#########################################################################################################


@task
def nAnalyserDown(
    subdiv: List[list],
    answers: List[Tuple[List[list] | None, bool]],
    conj: List[Optional[int]],
    n: int,
    config: TaskEnv.Config,
    me,
):
    """
    `nAnalyserDown` is a task triggered by a `nAnalyser`, after it submits `nTask`s on the relevant
    intersections of the complementary subsets of `delta`.

    It analyzes the results of these tasks. As described in the algorithm documentation, it attempts to
    identify separable failing subsets. If such cases are found, it proceeds accordingly.
    Otherwise, it reconstructs a classical execution path and simulates a standard delta debugging process
    for the remaining steps.

    Args:
        subdiv (List[list]): The current subdivision of `delta`.
        answers (List[Tuple[Optional[str], bool]]): Results returned from each `nTask`, which ran in
            non-recursive mode. Each tuple contains:
            - `"Input"` or `None`, and
            - a boolean indicating whether the tested set failed.
        conj (List[Optional[int]]): Built from the `oneSub` list used in other tasks.
            `conj[i]` is the index of the subset conjugate to the i-th one.
            It is equal to its own index if the subset was size one and not splittable,
            or `None` if the i-th subset did not fail.

        n (int): The number of subsets in `subdiv`.
        config (BaseConfig.BaseConfig): Configuration object forwarded to downstream tasks.
        me (Graph): Graph used for coordination or visualization, as in other tasks.

    Returns:
        Tuple[List[list], bool]: A pair where:
            - the first element is a list of 1 minimal failing subsets of `delta`;
            - the second element is a boolean indicating whether the combined subset is failing.

        This task may delegate to a `Corrector` or a `nAGG`, or return directly, using the same result structure.
    """

    ### PrintGraph ###
    gPrint = me is not None
    if gPrint:
        from controllers import Graph

        me.setType(f"{n}Analyser - Down")

    ### Transform answers into matrix
    lst = [i for (i, x) in enumerate(conj) if x is not None]

    nb = len(lst)

    matrix: List[List[bool]] = [[True] * n for _ in range(n)]
    for i in range(nb):
        matrix[lst[i]][lst[i]] = False
    if nb == 1:
        raise RuntimeError(
            "AnalyserDown called with only one failing subset (Should have directly recurse)"
        )

    idx1 = 0
    idx2 = 1
    for anwser in answers:  # On parcours les réponses comme si on parcourait une matrice triangulaire supérieur ligne par ligne (sans la diagonale)
        if conj[lst[idx1]] == lst[idx2]:  # On saute les conjugués
            idx2 += 1

        if not anwser[1]:
            matrix[lst[idx1]][lst[idx2]] = False
            matrix[lst[idx2]][lst[idx1]] = False

        idx2 += 1
        if idx2 >= nb:  # Si on est arrivés au bout on recommance ligne suivante
            idx1 += 1
            idx2 = idx1 + 1

    ### Analysis of the matrix
    def extractSquareMatrix(mat, tab):  # extract the square matrix with the indexes given by tab
        size = len(tab)
        rep = [[True] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                rep[i][j] = mat[tab[i]][tab[j]]
        return rep

    def extractMatrix(mat, col, rows):  # extract the square matrix with the indexes given by tab
        size = len(col)
        lenght = len(rows)
        rep = [[True] * lenght for _ in range(size)]
        for i in range(size):
            for j in range(lenght):
                rep[i][j] = mat[col[i]][rows[j]]
        return rep

    def isnull(mat):  # Checks if a matrix is null
        for col in mat:
            for elt in col:
                if elt:
                    return False
        return True

    def two(mat, size) -> Tuple[bool, int, int]:
        idx1 = None
        idx2 = None
        for i in range(
            size
        ):  # Finding two disctincts nablas that each have a element that the other doesn't have
            for j in range(size):
                if mat[i][j]:
                    idx1 = i
                    idx2 = j
        if idx1 is None or idx2 is None:
            raise RuntimeError("trying to find two complementary subsets in a null matrix")

        tab1 = []
        for idx in mat[idx1]:
            if not mat[idx1][idx]:
                tab1.append(idx)
        tab2 = []
        for idx in mat[idx2]:
            if not mat[idx2][idx]:
                tab2.append(idx)

        if not (
            isnull(extractSquareMatrix(mat, tab2)) and isnull(extractSquareMatrix(mat, tab1))
        ):  # If there is only two elements, each nabla contain exactly one element (A, B)
            return False, None, None

        ### Need to make sure that there isn't any other element

        # Every nabla contains one of the two elements (A or B)
        for i in range(size):
            if mat[idx1][i] and mat[idx2][i]:
                return False, None, None

        # If there is a third element C, we have a nabla that contains C and not A and another that contain C and not B
        # So one that contain A and C and another B and C (since each nabla contains A or B)
        # The intersection of those 2 should not fail

        firstNotsecond = []
        for idx in tab1:
            if mat[idx2][idx]:
                firstNotsecond.append(idx)
        secondNotFirst = []
        for idx in tab2:
            if mat[idx1][idx]:
                firstNotsecond.append(idx)
        if not isnull(extractMatrix(mat, firstNotsecond, secondNotFirst)):
            return False, None, None
        return True, idx1, idx2

    omega = sum(subdiv, [])

    ### If only one failing subset (deg = 1) #########################################################################
    if isnull(extractSquareMatrix(matrix, lst)):
        # Launching calculus on the full intersection
        newDelta = omega
        for idx in lst:
            newDelta = TaskEnv.listminus(newDelta, subdiv[idx])

        Gr1 = Graph() if gPrint else None
        newdivision = []
        oneSub = []
        idx_ = 0
        for idx in range(n):
            if idx in lst:
                continue
            if len(subdiv[idx]) == 1:
                newdivision.append(subdiv[idx])
                oneSub.append(idx_)
                idx_ += 1
            else:
                temp = TaskEnv.split(subdiv[idx], 2)
                newdivision.append(temp[0])
                newdivision.append(temp[1])
                idx_ += 2
        res = MultiResultHandle(
            [nTask.invoke(newDelta, newdivision, config, Gr1, True, None, oneSub, delegate=True)]
        )

        GrOut = None

        ### PrintGraph ###
        if gPrint:
            me.addLabel("One subset")
            GrOut = Graph(emphas="blue")
            me.down(Gr1, newDelta)
            out = Gr1.out[0]
            while out != out.out[0]:
                out = out.out[0]
            GrOut.sup(*out.out)
            me.sout(GrOut, None)

        return Corrector.invoke(1, subdiv, res, matrix, n, config, GrOut, delegate=True)

    ### If there is two failing subsets (deg = 2) ####################################################################
    test, idx1, idx2 = two(extractMatrix(matrix, lst, lst), nb)
    if test:
        idx1 = lst[idx1]
        idx2 = lst[idx2]
        tab1 = []
        for idx in range(n):
            if not matrix[idx1][idx]:
                tab1.append(idx)
        tab2 = []
        for idx in range(n):
            if not matrix[idx2][idx]:
                tab2.append(idx)

        NewNabla1 = omega
        for idx in tab1:
            NewNabla1 = TaskEnv.listminus(NewNabla1, subdiv[idx])
        Gr1 = Graph() if gPrint else None

        NewNabla2 = omega
        for idx in tab2:
            NewNabla2 = TaskEnv.listminus(NewNabla2, subdiv[idx])
        Gr2 = Graph() if gPrint else None

        newdivision1 = []
        oneSub1 = []
        idx_1 = 0
        for idx in range(n):
            if idx in tab1:
                continue
            if len(subdiv[idx]) == 1:
                newdivision1.append(subdiv[idx])
                oneSub1.append(idx_1)
                idx_1 += 1
            else:
                temp = TaskEnv.split(subdiv[idx], 2)
                newdivision1.append(temp[0])
                newdivision1.append(temp[1])
                idx_1 += 2
        newdivision2 = []
        oneSub2 = []
        idx_2 = 0
        for idx in range(n):
            if idx in tab2:
                continue
            if len(subdiv[idx]) == 1:
                newdivision2.append(subdiv[idx])
                oneSub2.append(idx_2)
                idx_2 += 1
            else:
                temp = TaskEnv.split(subdiv[idx], 2)
                newdivision2.append(temp[0])
                newdivision2.append(temp[1])
                idx_2 += 2

        Args = [
            (NewNabla1, newdivision1, config, Gr1, True, None, oneSub1),
            (NewNabla2, newdivision2, config, Gr2, True, None, oneSub2),
        ]
        res = nTask.map_invoke(Args)
        GrOut = None

        ### PrintGraph ###
        if gPrint:
            me.addLabel("Two subsets")
            GrOut = Graph(emphas="blue")
            me.down(Gr1, NewNabla1)
            out = Gr1.out[0]
            while out != out.out[0]:
                out = out.out[0]
            GrOut.sup(*out.out)

            me.down(Gr2, NewNabla2)
            out = Gr2.out[0]
            while out != out.out[0]:
                out = out.out[0]
            GrOut.sup(*out.out)
            me.sout(GrOut, None)

        return Corrector.invoke(2, subdiv, res, matrix, n, config, GrOut, delegate=True)

    ### Sinon on simule une execution classique ######################################################################
    else:
        # TODO: On peut faire bien mieux
        results = []
        fakesons = []
        for idx in range(n):  # Correspond à une n-1 Task
            nabla = TaskEnv.listminus(omega, subdiv[idx])
            if idx not in lst:  # Si c'est un tache qui ne fail pas, on la génère simplement
                results.append(
                    nTask.invoke(nabla, n - 1, config, Graph(emphas="orange"), False, True)
                )
                continue

            subdivArg = []
            newSubdiv = []
            graphs = []
            for i in range(n):
                if i == idx:
                    continue
                nablaPrime = TaskEnv.listminus(nabla, subdiv[i])
                newSubdiv.append(subdiv[i])
                rep = matrix[idx][i]
                ### PrintGraph ###
                if gPrint:
                    graphs.append(Graph(emphas="orange"))
                newdivision = []
                for j in range(n):
                    if j == idx:
                        continue
                    if j == i:
                        continue
                    newdivision.append(subdiv[j])
                subdivArg.append(
                    (nablaPrime, newdivision, config, graphs[-1] if gPrint else None, True, rep)
                )  # Mise en forme pour le passage en paramètre

            result = nTask.map_invoke(subdivArg)  # type: ignore

            fakeMother = None

            ### PrintGraph ###
            if gPrint:
                fakeMother = Graph(emphas="orange")
                fakeMother.setType(f"{n - 1}Task")
                me.down(fakeMother, nabla)
                fakesons.append(fakeMother)

            GrOut1 = None

            ### PrintGraph ###
            if gPrint:
                GrOut1 = Graph()

                for i in subdivArg:
                    fakeMother.down(i[3], i[0])
                    out = i[3].out[0]
                    while out != out.out[0]:
                        out = out.out[0]
                    GrOut1.sup(*out.out)
                fakeMother.sout(GrOut1, None)

            results.append(nAGG.invoke(newSubdiv, result, n, config, GrOut1))

        ## On a récupéré les données des n-1 task et on lance donc un n aggregateur pour sortir la réponse
        GrOut = None

        ### PrintGraph ###
        if gPrint:
            GrOut = Graph()

            for i in fakesons:
                out = i.out[0]
                while out != out.out[0]:
                    out = out.out[0]
                GrOut.sup(*out.out)
            me.sout(GrOut, None)
        results = MultiResultHandle(results)
        return nAGG.invoke(subdiv, results, n, config, GrOut)


#########################################################################################################
### Corrector
#########################################################################################################


@task
def Corrector(
    mode: int,
    subdiv: List[list],
    answers: List[Tuple[List[list] | None, bool]],
    matrix: List[List[bool]],
    n: int,
    config: TaskEnv.Config,
    me,
):
    """
    `Corrector` is a unique task that verifies whether the guess made by `nAnalyser` was correct.
    See the algorithm documentation for more details.

    # TODO: Implement the actual correction logic.

    Args:
        mode (int): Identifies which hypothesis the `nAnalyser` chose to explore.
        subdiv (List[list]): The current subdivision of `delta`.
        answers (List[Tuple[Optional[List[list]], bool]]): Results returned from each `nTask`,
            executed on sets determined by the analyser's guess. Each tuple contains:
            - either a list of 1 minimal failing subset (or `None`), and
            - a boolean indicating whether the tested set failed.
        matrix (List[List[bool]]): A `n x n` matrix where `matrix[i][j]` represents the result of the
            test function applied to the intersection of the complements of the i-th and j-th subsets.
        n (int): The size of the matrix.
        config (BaseConfig.BaseConfig): Configuration object forwarded to downstream tasks.
        me (Graph): Graph used for coordination or visualization, as in other tasks.

    Raises:
        RuntimeError: If the analyser's guess turns out to be incorrect.

    Returns:
        Tuple[List[list], bool]: A pair where:
            - the first element is a list of 1 minimal failing subsets of `delta`;
            - the second element is a boolean indicating whether the combined subset is failing.
    """

    ### PrintGraph ###
    gPrint = me is not None
    if gPrint:
        me.setType("Checked")

    if mode == 1:
        if not answers[0][1]:
            ### PrintGraph ###
            if gPrint:
                me.addLabel("Simple")
                me.sout(me, answers[0])
            return answers[0]
    if mode == 2:

        def merge(tabofrep):  # Merge sans doublon
            dic = {}
            res = []
            for rep in tabofrep:
                if rep[0] is None:
                    continue
                for val in rep[0]:
                    key = val.__str__()
                    if key not in dic:
                        dic[key] = val
                        res.append(val)
            return res

        if not answers[0][1] and not answers[1][1]:
            rep = merge(answers)
            ### PrintGraph ###
            if gPrint:
                me.addLabel("Double")
                me.sout(me, [rep, False])
            return rep, False

    raise RuntimeError("Gestion du fail guess non implémentée")
