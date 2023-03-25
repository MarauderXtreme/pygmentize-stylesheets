#!/usr/bin/env bash

set -euxo pipefail

./src/get_styles.py | xargs -I{} sh -c 'pygmentize -S {} -f html -a .highlight > docs/css/themes/{}.css'

for file in docs/css/themes/*.css; do
	if [ ! -s "$file" ]; then
		echo "Deleting $file because it's empty."
		rm "$file"
	fi
done
