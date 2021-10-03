### Para rodar a API em outra porta no ambiente de desenvolvimento

```
flask run --host=0.0.0.0 --port=9023
```

### Configurar variáveis de ambiente do banco de dados

```
SET DATABASE_HOST=localhost
```

```
SET DATABASE_NAME=hub_solidario_desenvolvimento
```

```
SET DATABASE_USER=postgres
```

```
SET DATABASE_PASSWORD=default_123
```

### Configurar variáveis de ambiente da aplicação

```
SET APP_SETTINGS=config.DevelopmentConfig
```