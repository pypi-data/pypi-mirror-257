@echo off
mypy --strict q1ss
pytest test --cov=./q1ss
coverage html
@pause
