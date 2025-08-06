# 🔒 Lockcell

Lockcell is a parallelized version of the Verrou software by EDF.  
It uses ArmoniK to schedule computations and allows you to locate sources of computational instabilities in your code.

---

## ⚙️ Prerequisites

In the following, I will assume that you have a running ArmoniK cluster with a PymoniK partition on it, if you dont have any, here is how to deploy locally

### Installing Armonik

You must have **ArmoniK installed on your machine**.  
If not, follow the official guide here:  
👉 https://armonik.readthedocs.io/en/latest/content/getting-started/installation/local.html

Once you have it installed, before installing Lockcell you need to deploy ArmoniK.

---


### 🚀 Deployment

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

Once ArmoniK is deployed, clone the repository and go to the Lockcell project directory:

```bash
git clone https://github.com/aneoconsulting/Lockcell.git
cd Lockcell
make install
```

You're now ready to use Lockcell!

---

## 🧪 Run the Tests

### ▶️ Example Test: 

This project includes a test that runs the classic [Integral Example from Verrou](https://github.com/edf-hpc/verrou_support/blob/main/tutorial-fr/tp-verrou/tp-verrou.pdf).

To execute it:

1. Run the test initialization from the project root:

   ```bash
   make test
   ```

2. Navigate to the example directory:

   ```bash
   cd exemples/TestVerrou
   ```

3. Open the `main.py` file to inspect what the test is doing.

4. Run the test using:

   ```bash
   uv run main.py
   ```

> **Note:** An active **ArmoniK deployment** is required to run this test successfully.

## 📝 Usage guide

A full usage guide will be provided soon.
