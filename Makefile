init:
	pip install -r requirements.txt
	pip install -r requirements.dev.txt
	pip install --editable .[dev]

update-deps:
    # --allow-unsafe pins packages considered unsafe: distribute, pip, setuptools.
	pip install --upgrade pip-tools pip setuptools
	pip-compile --upgrade --build-isolation \
		--allow-unsafe --resolver=backtracking --strip-extras \
		--output-file requirements.txt \
		requirements.in
	pip-compile --allow-unsafe --upgrade --build-isolation \
		--allow-unsafe --resolver=backtracking --strip-extras \
		--output-file requirements.dev.txt \
		requirements.dev.in

update: update-deps init

redeploy:
	cd ~ && docker compose up -d --build --force-recreate dagster_codelocation_ads

.PHONY: init update-deps update redeploy