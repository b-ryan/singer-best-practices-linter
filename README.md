# singer-best-practices-linter

## Usage

    singer-best-practices-linter --tap tap-closeio --config config.json

## Checks

Currently inspects the following:

- That a critical log exists in the main function
- No empty schemas are found in schemas
- "additionalProperties" key is found in all schemas

## TODO

Right now the linter is checking for JSON files to lint the schemas. But it
should instead use the --discovery option of the tap.
