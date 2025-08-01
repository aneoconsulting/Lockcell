# 🔒 Lockcell

Lockcell is a Python project that depends on having **ArmoniK** installed and running locally.

## ⚙️ Prerequisites

Before using Lockcell, you must have **ArmoniK installed on your machine**.  
If not, follow the official guide here:  
👉 https://armonik.readthedocs.io/en/latest/content/getting-started/installation/local.html

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

## 📦 Installing Lockcell

Once ArmoniK is deployed, go to the Lockcell project directory:

```bash
cd Lockcell
make install
```

You're now ready to use Lockcell!

## 🧪 Run the tests

```bash
make test
```

## ▶️ Run the project

```bash
make run
```

## 📝 Usage guide

A full usage guide will be provided soon.
