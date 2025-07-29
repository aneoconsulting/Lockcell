from Tasks import Config
from pathlib import Path
import copy

class ConfigVerrou(Config):
    def __init__(self, workingdir : Path, RelrunPath : Path, RelCmpPath : Path):

        if not isinstance(workingdir, Path):
            raise TypeError(f"workingdir must be of class Path, not {type(workingdir).__name__}")
        if not isinstance(RelrunPath, Path):
            raise TypeError(f"runPath must be of class Path, not {type(RelrunPath).__name__}")
        if not isinstance(RelCmpPath, Path):
            raise TypeError(f"CmpPath must be of class Path, not {type(RelCmpPath).__name__}")
        super().__init__(1)

        # Permet de travailler proprement dans le dossier reservé à cette config (existera dans tous les conteneurs)
        self.workdir = workingdir
        self.runPath = RelrunPath
        self.CmpPath = RelCmpPath

    
    def parseGenRunFile(self):
        """
        Fais le run de référence, le stocke dans workingdir/ref, en même temps génère le fichier lignes.source dans le working directory.


        Raises:
            RuntimeError: Si le run de référence échoue.
        """
        import subprocess
        # Variables d’environnement pour le run de référence
        env = os.environ.copy()
        env["VERROU_ROUNDING_MODE"] = "nearest"
        env["VERROU_FLOAT"] = "no"
        env["VERROU_UNFUSED"] = "no"
        env["VERROU_MCA_MODE"] = "ieee"

        # Lancement de l’exécutable
        ref_result = subprocess.run(
                                    ["bash", "./parse.sh", str(self.workdir), str(self.runPath)], # parse.sh prend un dossier qui contient un executable et génère le parsing des \
                                    env = env                                                     # lignes dans lignes.source et la configuration de référence dans ref/result.dat
                                    )                                                           

        # vérification de la bonne execution
        if ref_result.returncode != 0:
            raise RuntimeError("Erreur lors de l'execution du run de référence, non perturbé")

    def generateSearchSpace(self) -> list:
        """
        Génère un searchspace à partir d'entiers

        Returns:
            list: ensemble des lignes perturbables
        Raises:
            FileNotFoundError: Si le parsing des lignes n'a pas été généré
        """
        In = self.workdir / self.runPath
        try:
            with open(In, 'r') as file:
                all_lines = file.readlines()
        except FileNotFoundError:
            raise FileNotFoundError("Cannot genrate a searchspace without the lines.source file, (Maybe you tried to call this function in a task and not in client ?)")

        return all_lines
    
    
    def copy(self) -> "ConfigVerrou":
        return ConfigVerrou(self.workdir, self.runPath, self.CmpPath)

    def Test(self, subspace: list) -> bool:
        
        import os
        import subprocess

        #Préparation du fichier des lignes à perturber pour verrou
        fout = self.workdir / "aperturber"
        with open(fout, 'w') as f:
            f.writelines(subspace)

        # Dossier pour stocker les résultats
        REF_DIR = str(self.workdir / "/ref")
        PERTURBED_DIR = str(self.workdir / "/pert")
        LIGNE_FICHIER = str(fout) 

        # Définition des variables d’environnement pour le run perturbé
        env = os.environ.copy()
        env["VERROU_SOURCE"] = LIGNE_FICHIER
        env["VERROU_ROUNDING_MODE"] = "random"
        env["VERROU_FLOAT"] = "no"
        env["VERROU_UNFUSED"] = "no"
        env["VERROU_LIBM_NOINST_ROUNDING_MODE"] = "nearest"

        # Étape 3 — Lancer le run perturbé
        os.makedirs(PERTURBED_DIR, exist_ok=True)
        pert_result = subprocess.run(
            ["./verrou/DD_RUN", PERTURBED_DIR],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env
        )
        if pert_result.returncode != 0:
            raise RuntimeError("Error during the run")

        # Étape 4 — Comparaison avec DD_CMP
        cmp_result = subprocess.run(["./verrou/DD_CMP.py", REF_DIR, PERTURBED_DIR])


        # Code de retour global
        return cmp_result.returncode == 0