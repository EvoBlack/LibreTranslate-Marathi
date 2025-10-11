
#!/bin/sh
set -e

# Auto-install any .argosmodel files present in the project root
for model in *.argosmodel; do
	if [ -f "$model" ]; then
		echo "Installing Argos model: $model"
		python3 -m argostranslate.package install "$model"
	fi
done

echo "Model install script complete."
