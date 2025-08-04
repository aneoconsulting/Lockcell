.PHONY: install clean test

TESTVERROU_CONFIG_FILE=exemples/TestVerrou/config.yaml
PWD=$(shell pwd)

# Add the configuration file
test:
	@if [ ! -f $(TESTVERROU_CONFIG_FILE) ]; then \
		echo "Creating config.yaml..."; \
		echo "paths:" > $(TESTVERROU_CONFIG_FILE); \
		echo "  working_directory: $(PWD)/data/integral/" >> $(TESTVERROU_CONFIG_FILE); \
	else \
		echo "$(TESTVERROU_CONFIG_FILE) already exists."; \
	fi

# Install dependencies
install:
	uv pip install -r lockcell/uv.lock

#TODO: Clean configuration files, currently only clean pycache
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +