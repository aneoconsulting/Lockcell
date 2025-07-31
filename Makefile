.PHONY: install test clean

# Installer les dépendances avec uv
install:
	uv pip install -r uv.lock

# Lancer les tests (ex: avec pytest)
test:
	pytest tests/

# Nettoyer les fichiers inutiles
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
