<!-- TABLE OF CONTENTS -->
<summary>Table of Contents</summary>
<ol>
  <li><a href="#about-turkle">About</a></li>
  <li><a href="#getting-started">Getting Started</a></li>
  <li>
    <a href="#usage">Usage</a>
    <ul> 
      <li><a href="#preparing-your-data">Preparing your data</a></li>
      <li><a href="#running-the-evaluation">Running the evalution</a></li>
      <li><a href="#root-cause-analysis">Conducting root cause analysis</a></li>
      <li><a href="#fine-tuning">Fine tuning</a></li>
    </ul>
  </li>
  <li><a href="#license">License</a></li>
  <li><a href="#contact">Contact</a></li>
</ol>


<!-- ABOUT THE PROJECT -->
## About Turkle

The Turkle package is designed for 1<sup>st</sup> line monitoring of credit scoring models as well as an aid in root cause analysis of performance issues.
The goal is to give standardized and comparable metrics for different models in production. The package gives a common framework for root-cause analysis to use across models and teams.


<!-- GETTING STARTED -->
## Getting Started

To install Turkle monitoring:

```bash
pip install turkle-monitoring
```

<!-- USAGE -->
## Usage

Using the Turkle monitoring package involves these steps:
<ol>
  <li>Preparing your data</li>
  <li>Running the evaluation of your model(s)</li>
  <li>Conducting root cause analysis when issues are found</li>
  <li>Fine tuning Turkle to improve monitoring</li>
</ol>

### Preparing your data

All monitoring features are build around the ```turkle.Model``` class.
<br/>
A ```Model``` instance expects reference and production data passed as dataframes containing individual loan applications, both rejected and approved. Each model is evaluated through its own ```Model``` instance:

```python
from turkle import Model

my_credit_model = Model(ref_data, prod_data)

my_credit_model.evaluate()
```

#### Reserved columns

The following non-feature column names are reserved and required in both the production and reference dataframes:


```timestamp``` <br/> Observation timestamp of application. Datetime, timestamp or string that is directly castable to timestamp format eg. "2023-01-31" or "2023/01/31".

```label``` <br/> Outcome of accepted applications. Integer, 1 = default, 0 = non-default. Nulls can safely be passed for rejected applications and delayed labels.

```predicted_probability``` <br/> Predicted probability of belonging to class 1 from your model. Float between 0 and 1.

```credit_score``` <br/> The credit score assigned to the application as used in your risk management. Int or float.


#### Features
Any other columns passed are interpreted as features. Columns must be identical in reference and production dataframes. Numerical values are interpreted as continuous and will be binned, while other values are assumed to be categorical. See the <a href="#fine-tuning">fine tuning</a> section for more information about binning.


### Running the evalution

To run the basic evaluation:

```python
my_credit_model = Model(ref_data, prod_data)

my_credit_model.evaluate()
```

![plot](./plots/default_rates.png)
![plot](./plots/gini.png)

The ```evaluate()``` function outputs two plots: Default rates per scoreband and Gini. These metrics and their trends give an overview of the model's overall health.

### Root cause analysis

The cause of performance deterioration is primarily evaluated using the ```concept_drift()``` and ```feature_drift()``` methods. Both of these methods accept the ```plot``` (True by default) and ```return_data``` (False by default) arguments.
```plot``` toggles the drawing of the corresponding plots. If ```return_data``` is set to true, the method will return the underlying data as a dataframe.

#### Feature drift

The ```feature_drift()``` method calculates PSI for each feature and highlights the three worst performers by plotting the distribution and PSI trend for these features:

```python
my_credit_model.feature_drift()
```

![plot](./plots/feature_drift.png)

```return_data=True``` returns the underlying data as a dataframe:

```python
feature_drift_df = my_credit_model.feature_drift(plot=False, return_data=True)
```

#### Concept drift

Concept drift measures changes in the relationship between features and the target. The ```concept_drift()``` method calculates concept drift magnitude as total rate of label change (from 0 to 1 or 1 to 0) and highlight the three worst performers:

```python
my_credit_model.concept_drift()
```

![plot](./plots/concept_drift.png)

```return_data=True``` returns the underlying data as a dataframe:

```python
concept_drift_df = my_credit_model.concept_drift(plot=False, return_data=True)
```

#### Evaluating individual features

The ```evaluate_feature(feature_name)``` method shows feature and concept drift of a single feature:

```python
my_credit_model.evaluate_feature('Age')
```

![plot](./plots/feature_eval.png)

#### Evaluating performance

The ```default_rate()``` method gives an overview of default rates over different score bands. The output is designed to easily show both the overall rank ordering and trends of individual scorebands:

```python
my_credit_model.default_rate()
```

![plot](./plots/default_rates.png)

The ```check_gini()``` method plots model Gini over time:

```python
my_credit_model.check_gini()
```

![plot](./plots/gini.png)

### Fine tuning

Turkle allows to fine tune bin edges, intervals and timespans to get more accurate insights.

#### Binning

Continuous features are automatically binned in order to calculate PSI. **Numerical types are automatically interpreted as continuous.** If you have numerical category data, please cast to string to avoid binning of this data.

By default, continuous features are binned in 10 equal width bins between the min and max values of the feature.

Custom bin edges can be passed using the ```bins``` parameter, containing a dict with feature names as keys and list of bin edges as values. Keys must correspond to feature columns in the production and reference datasets. In addition to feature, bins are also calculated for the ```credit_score``` columns. Custom bins may be passed for this columns as well.



```python
from turkle import Model
import numpy as np

#ref and prod data is assumed to contain customer_age and customer_income features.
#It is recommended to leave outermost bins open-ended, eg. by setting upper bound to infinity.

custom_bins = {
  'credit_score' : [0, 600, 615, 630, 645, 660, np.inf],
  'customer_income' : [0, 1000, 2000, 3000, 4000, np.inf]
  }

my_credit_model = Model(ref_data, prod_data, bins=custom_bins)
```

#### Interval

By default all trends are calculated as monthly. This can be changed in individual method calls using the ```interval``` parameter. It can also be changed by setting a new default for the model using ```set_interval()```.

Example:

```python
my_credit_model = Model(ref_data, prod_data)

#shows monthly interval (the default)
my_credit_model.feature_drift()

#shows weekly interval
my_credit_model.feature_drift(interval="weekly")

#change default
my_credit_model.set_interval("weekly")

#Now shows weekly, the new default
my_credit_model.feature_drift()
```

#### Time filter

By default the entire production dataset is used when plotting and calculating metrics.
Custom timeframes can be set by passing ```start_date``` and ```end_date``` to individual functions, or by changing the default dates by using the ```set_start_date()``` and ```set_end_date()``` methods. Accepted types are anything that can be casted to timestamp, eg. strings and datetime.

Example:

```python
#Uses entire production dataset
my_credit_model.feature_drift()

#only considers production data from the year 2022
my_credit_model.feature_drift(start_date="2022-01-01", end_date="2022-12-31")

#Start or end may be omitted to have open ended limits:

#All data after 1.1.2022 is used
my_credit_model.feature_drift(start_date="2022-01-01")

#All data before 31.12.2022 is used
my_credit_model.feature_drift(end_date="2022-12-31")

#Change default
my_credit_model.set_datespan(start_date="2022-01-01", end_date="2022-12-31")

#Now only considers production data from year 2022 by default
my_credit_model.feature_drift()

```

Note that Reference data can not be filtered without re-fitting using ```Model()``` and new reference dataset.


## License

Turkle is distributed under an Apache License Version 2.0. All contributions will be distributed under this license.

<p align="right">(<a href="#readme-top">back to top</a>)</p>