# Introduction 
This repo tracks the evidi_fabric package which is intended to collect useful helper when working with fabric

# Build and Test

For fast patch, build and publish, you can use the following command:

```poetry version patch && poetry build && python3 -m twine upload dist/*```

and for faster upload simply run the below, to only upload the newest version

```poetry run python -m update_package```

To upgrade your local repositories with the latest version of the package with pip, run:

```pip install --upgrade evidi_fabric```


## find a specific line of code in all scripts:
run below in a bash terminal
```./helpers/find_file_with_line_of_code.sh "TEXT YOU WANT TO FIND"```