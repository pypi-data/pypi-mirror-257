# Fao56 Model

[![Build Main](https://github.com/stephansmit/fao56_model/actions/workflows/build-main.yml/badge.svg)](https://github.com/stephansmit/fao56_model/actions/workflows/build-main.yml)

This is an implementation of the [FAO56 model](https://www.fao.org/3/X0490E/x0490e00.htm).
Only the method where the effect of both crop transpiration and soil evaporation are integrated into a single crop coefficient is implemented now.



## TO DO

- [ ] add the crop dependant and stage dependent crop yield reduction factor (now hardcoded to 1)
- [ ] add the crop coefficient correction for the initial stage
- [ ] generalize the output
- [ ] add the dual crop coefficient method
- [ ] add more crops to the database
- [ ] validate the model using the FAO56 data
- [ ] add tests


## Development

To install all the dependencies

```
poetry install --with dev
```

Install the pre-commit hooks
    
```
pre-commit install
```
    
To test

```
poetry run pytest
```

Bump the version to publish
    
```
poetry version patch
git add fao56_model
git commit -am 'Bump version'
git push
```
