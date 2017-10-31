# Results

## Run #1: Simple linear regression

### Description

Ran a basic linear regression on every unit in the unit collection. After
filtering outliers, there were 15,894 units. The model was trained on all of
these.

### Model

`sklearn.linear_model.LinearRegression`

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|345.46|  0.53|
|2|373.27|  0.42|
|3|364.41|  0.48|
|4|360.20|  0.30|
|5|360.70|  0.43|
|Mean|360.81|  0.43|
|Std|  8.99|  0.07|

## Run #2: Linear regression on one zip code

### Description

Ran a basic linear regression. Narrowed down to units in zip code 98122. After
filtering outliers, this left 1118 listings.

### Model

`sklearn.linear_model.LinearRegression`

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|270.03|  0.69|
|2|257.09|  0.70|
|3|242.59|  0.64|
|4|231.57|  0.69|
|5|266.87|  0.66|
|Mean|253.63|  0.68|
|Std| 14.59|  0.02|

## Run #3: Random forest regressor

### Description

Ran a random forest regressor with a max-depth of 1000.

### Model

`sklearn.ensemble.RandomForestRegressor`

### Hyper-parameters

Max-depth: 1000

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|208.79|  0.55|
|2|193.98|  0.79|
|3|180.11|  0.76|
|4|187.42|  0.64|
|5|169.01|  0.66|
|Mean|187.86|  0.68|
|Std| 13.35|  0.09|

## Run #4: Random forest with more trees

### Description

### Model

`sklearn.ensemble.RandomForestRegressor`

Ran a random forest regressor with a max-depth of 10000.

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|216.73|  0.36|
|2|191.84|  0.78|
|3|190.05|  0.75|
|4|197.31|  0.64|
|5|163.18|  0.67|
|Mean|191.82|  0.64|
|Std| 17.17|  0.15|

## Run #5: Gradient boosting regressor

### Description

Ran a Gradinet Boosting Regressor with:
- `loss='ls'`
- `learning_rate=0.01`
- `n_estimators=1000`
- `max_depth=5`
- `subsample=0.5`

### Model

`sklearn.ensemble.GradientBoostingRegressor`

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|260.75|  0.43|
|2|224.28|  0.76|
|3|191.94|  0.78|
|4|197.16|  0.68|
|5|188.40|  0.68|
|Mean|212.51|  0.67|
|Std| 27.22|  0.13|

## Run #6: Re-ran Random Forest

### Description

After another run, there are 23467 units. Re-run Random Forest with
`max_depth=1000`

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|198.00|  0.69|
|2|170.26|  0.81|
|3|159.93|  0.69|
|4|139.27|  0.70|
|5|152.23|  0.61|
|Mean|163.94|  0.70|
|Std| 19.81|  0.06|

## Run #7-8: Run Random Forest on specific zip codes

### Description

Narrow down to zip codes 98122 and then 98102.

### Results

98122

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|133.30|  0.83|
|2|116.66|  0.89|
|3|133.16|  0.85|
|4|114.50|  0.88|
|5|120.01|  0.88|
|Mean|123.53|  0.87|
|Std|  8.12|  0.02|

98102

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|108.33|  0.92|
|2|150.51|  0.86|
|3|123.01|  0.84|
|4| 90.85|  0.89|
|5|100.41|  0.93|
|Mean|114.62|  0.89|
|Std| 20.81|  0.04|

## Run #9:

### Description

- Random Forest
- 50,000 estimators
- 25350

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|177.27|  0.79|
|2|187.74|  0.70|
|3|160.32|  0.84|
|4|143.63|  0.79|
|5|150.80|  0.67|
|6|129.65|  0.70|
|7|131.11|  0.78|
|8|112.77|  0.78|
|9|138.17|  0.65|
|10|117.49|  0.86|
|Mean|144.90|  0.76|
|Std| 23.26|  0.07|

## Run #10

### Description

- Random Forest
- 50,000 estimators
- 25350

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|177.27|  0.79|
|2|187.74|  0.70|
|3|160.32|  0.84|
|4|143.63|  0.79|
|5|150.80|  0.67|
|6|129.65|  0.70|
|7|131.11|  0.78|
|8|112.77|  0.78|
|9|138.17|  0.65|
|10|117.49|  0.86|
|Mean|144.90|  0.76|
|Std| 23.26|  0.07|

## Run #11

### Description

- Random Forest
- n_estimators=100
- 25342 (< $15k/mo, 7.5k sqft)

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|165.83|  0.83|
|2|143.26|  0.86|
|3|125.66|  0.87|
|4|115.69|  0.82|
|5|122.40|  0.85|
|Mean|134.57|  0.85|
|Std| 18.09|  0.02|

## Run #12

### Description

- Random Forest
- n_estimators=1000
- 25342 (< $15k/mo, 7.5k sqft)

### Results

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|164.16|  0.83|
|2|143.03|  0.86|
|3|124.58|  0.87|
|4|115.07|  0.82|
|5|121.59|  0.85|
|Mean|133.69|  0.85|
|Std| 17.84|  0.02|