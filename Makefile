.PHONY: install run clean train

install:
	pip install -r requirements.txt

run:
	python main.py

train:
	python main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 *.py utils/*.py --max-line-length=120

test:
	python -m pytest tests/ -v
