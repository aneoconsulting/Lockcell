# 🔒 Lockcell

Lockcell is a parallelized version of the Verrou software by EDF.  
It uses ArmoniK to schedule computations and allows you to locate sources of computational instabilities in your code.

---

## ⚙️ Prerequisites

Before using Lockcell, you must have **ArmoniK installed on your machine**.  
If not, follow the official guide here:  
👉 https://armonik.readthedocs.io/en/latest/content/getting-started/installation/local.html

Once you have it installed, before installing Lockcell you need to deploy ArmoniK.

---


## 🚀 Deployment

To use Lockcell, you need a **running ArmoniK deployment**.

Go to the ArmoniK quick-deploy directory:

```bash
cd ArmoniK/infrastructure/quick-deploy/localhost
make deploy
```

This starts a local ArmoniK deployment.

To stop and remove the deployment later:

```bash
make destroy
```

---


## 📦 Dependencies

Lockcell uses [`uv`](https://github.com/astral-sh/uv) for dependency management and as a faster alternative to pip.  
To use the `Makefile`, install `uv` on your system:

```bash
pip install uv
```

> Note: All dependency installation and project commands rely on `uv`. Ensure it is installed globally before proceeding.

---


## 📥 Installing Lockcell

Once ArmoniK is deployed, go to the Lockcell project directory:

```bash
cd Lockcell
make install
```

You're now ready to use Lockcell!

---

## 🧪 Run the tests

```bash
make test
```

---

## ▶️ Run the project

```bash
make run
```

---

## 📝 Usage guide

A full usage guide will be provided soon.
