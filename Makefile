sdist:
	rm -f dist/*
	python setup.py sdist

CLI.md: zanshincli/*.py
	# Workaround for lack of typer-cli support on new versions
	poetry add typer==0.3.2 typer-cli
	poetry run typer --version
	poetry run typer --app main_app zanshincli.main utils docs --output CLI.md --name zanshin

	# Workaround for lack of typer-cli support on new versions
	poetry remove typer-cli
	poetry add typer==0.7.0

README.md: BASE_README.md CLI.md
	cat BASE_README.md CLI.md > README.md

README.rst: README.md
	pandoc --from=gfm --to=rst -o README.rst README.md

lint:
	flake8 zanshincli --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

test:
	poetry run python -m unittest discover -s zanshincli -v

coverage:
	poetry run coverage run --source zanshincli -m unittest discover -s zanshincli
	poetry run coverage report

coverage_missing:
	poetry run coverage run --source zanshincli -m unittest discover -s zanshincli
	poetry run coverage report -m