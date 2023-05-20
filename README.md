# Learn SQL Model

learning sql model

## Development

```console
pip install hatch
hatch shell
```

## Start the Server

```console
learn-sql-model api run
```

## Use the cli to manage Heros

```console
learn-sql-model hero create

# show them
learn-sql-model hero get

# show one
learn-sql-model hero get --id 0
```

## Use python to manage Heros

```python
from learn_sql_model.models.hero import Hero
# create a hero
bruce = Hero(name="Batman", secret_name="Bruce Wayne")
bruce.post()
# list all heros
Hero.get()
# get one hero
Hero.get(0)
```

## Use api to create hero

```console
# create a curl POST request to create hero
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "Batman", "secret_name": "Bruce Wayne"}' \
  http://localhost:5000/heros

# list all heros
curl http://localhost:5000/heros
curl -X 'GET' \
  'http://localhost:5000/heros/' \
  -H 'accept: application/json'

# get one hero
curl -X 'GET' \
  'http://localhost:5000/hero/9' \
  -H 'accept: application/json'
```

## License

`learn-sql-model` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
