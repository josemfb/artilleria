# Artillería

**Artillería** es el proyecto de una nueva intranet para la Quinta Compañía
del Cuerpo de Bomberos de Santiago, Bomba «Arturo Prat».

En desarrollo.


- Python (Flask)
- htmx

- Formatear con:
  - `isort .`
  - `black .`
  - `djlint app/templates --profile=jinja --reformat`
- Lint con:
  - `flake8 --extend-exclude '.venv, .idea, .plan' --max-line-length 100 .`
  - `djlint app/templates --profile=jinja`
