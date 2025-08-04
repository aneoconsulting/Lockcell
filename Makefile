.PHONY: install clean

TESTVERROU_CONFIG_FILE=exemples/TestVerrou/config.yaml
PWD=$(shell pwd)

# Ajouter les fichiers de configuration
init-config:
	@if [ ! -f $(TESTVERROU_CONFIG_FILE) ]; then \
		echo "Creating config.yaml..."; \
		echo "paths:" > $(TESTVERROU_CONFIG_FILE); \
		echo "  working_directory: $(PWD)/data/integral/" >> $(TESTVERROU_CONFIG_FILE); \
	else \
		echo "$(TESTVERROU_CONFIG_FILE) already exists."; \
	fi

# Installer les dépendances avec uv
install:
	uv pip install -r lockcell/uv.lock

# Nettoyer les fichiers inutiles
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +