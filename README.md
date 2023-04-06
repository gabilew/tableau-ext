# Tableau

Tableau is A meltano utility extension for Tableau that wraps the `tableau` command.
This extension supports the `refresh` method that refreshes a tableau data source [api doc](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#update_data_source)

## Installing this extension for local development

1. Install the project dependencies with `poetry install`:

```shell
cd path/to/your/project
poetry install
```

2. Verify that you can invoke the extension:

```shell
poetry run tableau_extension --help
poetry run tableau_extension describe --format=yaml
poetry run tableau_invoker --help # if you have are wrapping another tool
```

## Cofiguration
Add the following env vars:
```
TABLEAU_TOKEN_SECRET=<tableau token secret>
TABLEAU_TOKEN_NAME=<tableau token name>
TABLEAU_BASE_URL=<tableau api url>
TABLEAU_SITE_ID=<tableau site>
TABLEAU_API_VERSION=<api version>
```
or
```
TABLEAU_USERNAME=<tableau username>
TABLEAU_PASSWORD=<tableau password>
TABLEAU_BASE_URL=<tableau api url>
TABLEAU_SITE_ID=<tableau site>
TABLEAU_API_VERSION=<api version>
```
## Running the invoke methods
The refresh method updated a datasource based on the datasource luid from tableau

```shell
poetry run tableau_invoker:refresh <datasource-luid>
```

## Template updates

This project was generated with [copier](https://copier.readthedocs.io/en/stable/) from the [Meltano EDK template](https://github.com/meltano/edk).
Answers to the questions asked during the generation process are stored in the `.copier_answers.yml` file.

Removing this file can potentially cause unwanted changes to the project if the supplied answers differ from the original when using `copier update`.
