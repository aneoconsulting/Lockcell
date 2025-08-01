.PHONY: install clean

# Installer les dépendances avec uv
install:
	uv pip install -r lockcell/uv.lock

# Nettoyer les fichiers inutiles
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +