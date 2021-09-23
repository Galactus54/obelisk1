.PHONY: install
install:
	poetry install

convert:
	poetry run python -m obelisk -c
