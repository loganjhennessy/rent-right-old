# Results

**Run #1**

Description:

Ran a basic linear regression on every unit in the unit collection. After
filtering outliers, there were 15,894 units. The model was trained on all of
these.

Model: `sklearn.linear_model.LinearRegression`

Results:

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|345.46|  0.53|
|2|373.27|  0.42|
|3|364.41|  0.48|
|4|360.20|  0.30|
|5|360.70|  0.43|
|Mean|360.81|  0.43|
|Std|  8.99|  0.07|

# Run #2

Ran a basic linear regression. Narrowed down to units in zip code 98122. After
filtering outliers, this left 1118 listings.

Model: `sklearn.linear_model.LinearRegression`

|Run|Error|R<sup>2</sup>|
|:-:|--:|--:|
|1|270.03|  0.69|
|2|257.09|  0.70|
|3|242.59|  0.64|
|4|231.57|  0.69|
|5|266.87|  0.66|
|Mean|253.63|  0.68|
|Std| 14.59|  0.02|
