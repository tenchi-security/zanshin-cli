sdist:
	rm -f dist/*
	python setup.py sdist

CLI.md: src/*.py
	# Workaround for lack of typer-cli support on new versions
	poetry add typer==0.3.2 typer-cli==0.0.12
	poetry run typer --version
	poetry run typer --app main_app src.main utils docs --output CLI.md --name zanshin

	# Workaround for lack of typer-cli support on new versions
	poetry remove typer-cli
	poetry add typer==0.7.0

README.md: BASE_README.md CLI.md
	cat BASE_README.md CLI.md > README.md

README.rst: README.md
	pandoc --from=gfm --to=rst -o README.rst README.md

lint:
	poetry run pre-commit run -a

test:
	python -m unittest discover test -p "*_test.py"

coverage:
	poetry run coverage run --source src -m unittest discover -s src
	poetry run coverage report

coverage_missing:
	poetry run coverage run --source src -m unittest discover -s src
	poetry run coverage report -m
