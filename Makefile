sdist:
	rm -f dist/*
	python setup.py sdist

CLI.md: zanshincli/*.py
	# Workaround for lack of typer-cli support on new versions
	pip install typer==0.3.2 typer-cli
	typer --help
	typer --version
	typer --app main_app zanshincli.main utils docs --output CLI.md --name zanshin

	# Workaround for lack of typer-cli support on new versions
	pip uninstall -y typer-cli
	pip install typer==0.6.1

README.md: BASE_README.md CLI.md
	cat BASE_README.md CLI.md > README.md

README.rst: README.md
	pandoc --from=gfm --to=rst -o README.rst README.md

pypi: README.rst sdist
	python setup.py clean
	twine upload --repository pypi dist/*

pypitest: README.rst sdist
	python setup.py clean
	twine upload --repository pypitest dist/*

lint:
	flake8 zanshincli --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

test:
	python -m unittest discover -s zanshincli -v

coverage:
	coverage run --source zanshincli -m unittest discover -s zanshincli
	coverage report

coverage_missing:
	coverage run --source zanshincli -m unittest discover -s zanshincli
	coverage report -m
