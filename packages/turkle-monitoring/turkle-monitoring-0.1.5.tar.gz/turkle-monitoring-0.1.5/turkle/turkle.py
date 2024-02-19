from pandas.api.types import is_numeric_dtype, is_integer_dtype
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from turkle.plotting import Colors, create_bar_plot, create_line_plot

from sklearn.metrics import roc_auc_score

class Model:

  def __init__(self, ref: pd.DataFrame, prod: pd.DataFrame, bins: dict = {}):

    #list of columns that are not features
    self.meta_columns = ['timestamp', 'label', 'predicted_probability']

    #Data validation
    if ref.columns.tolist() != prod.columns.tolist():
      raise ValueError("Columns in reference and production datasets do not match.")
    
    for col in self.meta_columns:
      if col not in ref.columns.tolist():
        raise ValueError("Column missing from reference dataset: " + col)
      if col not in prod.columns.tolist():
        raise ValueError("Column missing from production dataset: " + col)

    self.ref = ref
    self.prod = prod

    plt.style.use('ggplot')
    
    self.prod["year-week"] = pd.to_datetime(self.prod['timestamp']).dt.strftime('%Y-%V')
    self.prod["year-month"]= pd.to_datetime(self.prod['timestamp']).dt.strftime('%Y-%m')

    self.ref["year-week"] = pd.to_datetime(self.ref['timestamp']).dt.strftime('%Y-%V')
    self.ref["year-month"]= pd.to_datetime(self.ref['timestamp']).dt.strftime('%Y-%m')

    self.meta_columns.append("year-week")
    self.meta_columns.append("year-month")

    self.supported_intervals = ["monhtly", "weekly"]
    self.interval = "monthly"
    self.start_date = pd.to_datetime(self.prod["timestamp"]).min()
    self.end_date = pd.to_datetime(self.prod["timestamp"]).max()

    self.ref_binned = ref.copy(deep=True) #binned df placeholder
    self.prod_binned = prod.copy(deep=True) #binned df placeholder

    self.features = {}
    self.bins = bins

    def generate_bin_label(bins):

      #function for generating bin labels based on custom bin edges

      bins.sort()
      labels = []

      for i, edge in enumerate(bins):
        if i == len(bins)-1:
          break
        labels.append("(" + str(round(edge, 2)) + ", " + str(round(bins[i+1], 2)) + "]")
      
      return labels
    
    #parse the type of each feature and generate corresponding binned dataframes
    for feature, type in self.ref.drop(self.meta_columns, axis=1).dtypes.to_dict().items():
      self.features[feature] = {"type": type, "is_continuous" : is_numeric_dtype(type)}

      if feature in self.bins:
        self.features[feature]["bins"] = self.bins[feature]

      if is_numeric_dtype(type):
        if feature in self.bins:
          self.ref_binned[feature] = pd.cut(self.ref[feature], self.bins[feature], right=True, labels=generate_bin_label(self.bins[feature]), duplicates='drop')
          self.prod_binned[feature] = pd.cut(self.prod[feature], self.bins[feature], right=True, labels=generate_bin_label(self.bins[feature]), duplicates='drop')
        else:
          #combine ref and prod population to calculate common bin edges
          total_population = pd.concat([self.ref_binned[feature], self.prod_binned[feature]]).dropna()
          #bin size hardcoded to number of categories in feature up to maximum of 10
          bins_n = min(10, total_population.value_counts().size)
          if is_integer_dtype(type):
            bin_edges = np.linspace(total_population.min(), total_population.max(), bins_n).astype(int).tolist()
          
          else:
            bin_edges = np.histogram_bin_edges(total_population, bins=bins_n).tolist()
            
          bin_edges.append(-float("inf"))
          bin_edges.append(float("inf"))
          self.ref_binned[feature] = pd.cut(self.ref[feature], bin_edges, right=True, labels=generate_bin_label(bin_edges), duplicates="drop")
          self.prod_binned[feature] = pd.cut(self.prod[feature], bin_edges, right=True, labels=generate_bin_label(bin_edges), duplicates="drop")
                          

  def _calculate_feature_psi(self, ref : pd.Series, prod: pd.Series):
    """
    Helper function for calculating psi given two series of data.

    Returns PSI scalar value, rounded to two decimal points.ß
    """
    ref_freq = ref.value_counts(normalize=True)
    prod_freq = prod.value_counts(normalize=True)

    expected_percents = np.clip(ref_freq, a_min=0.00001, a_max=None)
    actual_percents = np.clip(prod_freq, a_min=0.00001, a_max=None)
  
    psi_value = (expected_percents - actual_percents) * np.log(expected_percents / actual_percents)
    psi = sum(psi_value)

    return round(psi, 2)


  def _parse_interval(self, interval):
    """
    parses given interval and returns corresponding column name
    If None is passed, use model default interval
    """
    if interval == None:
      return(self._parse_interval(self.interval))
    
    if interval not in ["monthly", "weekly"]:
      raise ValueError("Interval " + str(interval) + " is not supported.")
    
    interval_col = "year-month"
    interval_label = "Month"
    if interval == "weekly":
      interval_col = "year-week"
      interval_label = "Week"
    
    return(interval_col, interval_label)
  
  
  def _calculate_concept_drift_one_feature(self, ref_binned: pd.Series, prod_binned: pd.Series, ref_bad_rate: pd.Series, prod_bad_rate: pd.Series):
  #helper function for calculating concept drift magnitude given two series of data and corresponding badrates
    

    
    ref_freq = ref_binned.value_counts(normalize=True)
    prod_freq = prod_binned.value_counts(normalize=True)

    overlap = ref_freq.index.intersection(ref_bad_rate.index)
      
    ref_freq = ref_freq[overlap]
    prod_freq = prod_freq[overlap]

    # Calculate P(Y=1|X) - the overall probability of seeing an applicant in bin X default.
    ref_p_y1X = ref_freq * ref_bad_rate
    prod_p_y1X = prod_freq * prod_bad_rate
    
    # 0 = no concept drift, 1 = all targets would change from 0 to 1 or vice versa
    
    if len(ref_freq) != 0:
      concept_magnitude = (1/(len(ref_freq))) * (sum(prod_p_y1X - ref_p_y1X))
    else:
      # if the prod sample has no overlap with the reference, return nan
      concept_magnitude = np.nan
    # Unit: Percentage
    return round(concept_magnitude, 4)


  def _parse_timestamps(self, start, end):
    """
    Parses given timestamps and returns clipped prod dataframes accordingly.
    Returns both original and binned df.
    """
    try:
      start_ts = pd.Timestamp(start)
      if start == None:
        start_ts = self.start_date
    except Exception as e:
      start_ts = pd.to_datetime(self.prod["timestamp"]).min()
      print("Could not parse start date " + start + ", will use earliest possible date from prod instead.")
    
    try:
      end_ts = pd.Timestamp(end)
      if end == None:
        end_ts = self.end_date
    except Exception as e:
      end_ts = pd.to_datetime(self.prod["timestamp"]).max()
      print("Could not parse end date " + end + ", will use latest possible date from prod instead.")

    if (start_ts > end_ts):
      raise ValueError("Start time must be smaller than end time.")
    
    parsed_df = self.prod[(pd.to_datetime(self.prod["timestamp"]) >= start_ts) & (pd.to_datetime(self.prod["timestamp"]) <= end_ts)]
    parsed_df_binned = self.prod_binned[(pd.to_datetime(self.prod_binned["timestamp"]) >= start_ts) & (pd.to_datetime(self.prod_binned["timestamp"]) <= end_ts)]

    if len(parsed_df) == 0:
      raise ValueError("Specified timespan does not contain any data.")

    if len(parsed_df) < 100:
      print("Warning: Specified timespan contains less than 100 samples.")

    return parsed_df, parsed_df_binned
  

  def set_interval(self, interval):

    """
    Set the default interval.
    """
    if interval not in self.supported_intervals:
      raise ValueError("Interval not supported.")
    
    self.interval = interval

    print("Default interval set succesfully.")

  def set_datespan(self, start, end):

    """
    Set the default start and end times.
    """

    #attempt to parse given timestamps
    _,_ = self._parse_timestamps(start, end)
    
    #if successful, save as defaults
    self.start_date = start
    self.end_date = end

    print("Default start and end times set successfully.")

  def calculate_psi(self, interval=None, start_date=None, end_date=None):
    
    """
    Calculates PSI for each feature at specified intervals and for the entire period.
    Returns dataframe with PSI values.
    """

    interval_col, interval_label = self._parse_interval(interval)

    result_list = []

    prod_sliced, prod_sliced_binned = self._parse_timestamps(start_date, end_date)

    #iterate over each feature and calculate psi values
    for feature in self.features:
      row = {"Feature" : feature}
      
      #total psi
      row["total_psi"] = self._calculate_feature_psi(self.ref_binned[feature], prod_sliced_binned[feature])
      
      #psi for each interval
      for interval in prod_sliced_binned[interval_col].unique():
        ref_series = self.ref_binned[feature]
        prod_series = prod_sliced_binned[prod_sliced_binned[interval_col]==interval][feature]
        row[interval] = self._calculate_feature_psi(ref_series, prod_series)
      
      result_list.append(row)

    psi_table = pd.DataFrame(result_list)

    return psi_table


  def feature_drift(self, interval=None, start_date=None, end_date=None, plot=True, return_data=False):
    """
    If plot=True: Plot the distribution and PSI trend of the features that have drifted most. 
    
    May return data as df with return_data=True.
    """

    # Calculate the PSI of each feature
    psi_table = self.calculate_psi(interval, start_date, end_date)

    _, interval_label = self._parse_interval(interval)

    prod_sliced, prod_sliced_binned = self._parse_timestamps(start_date, end_date)

    # Drop the credit score from this analysis
    psi_table = psi_table[psi_table['Feature'] != 'credit_score']

    psi_table = psi_table.sort_values(by=psi_table.columns[-1], ascending=False)

    if plot:

      fig, axs = plt.subplots(3, 2, figsize=(15, 10))
      show_top_n = 3
      most_drifted_features = psi_table.iloc[:show_top_n]['Feature'].values

      
    # Plot the distribution of the features that have drifted most
      for i, feature in enumerate(most_drifted_features):

        ref_freq = self.ref_binned[feature].value_counts(normalize=True).sort_index()
        prod_freq = prod_sliced_binned[feature].value_counts(normalize=True).sort_index()

        # Left column: Distribution plots
        bar_width = 0.35
        ref_positions = np.arange(len(ref_freq))
        prod_positions = np.arange(len(prod_freq)) + bar_width

        axs[i, 0] = create_bar_plot(axs[i, 0], 
                                          xdata=ref_positions, 
                                          ydata=ref_freq.values, 
                                          title=f'{feature} - PSI: {psi_table[psi_table["Feature"] == feature]["total_psi"].values[0]:.2f}', 
                                          xlabel=None, 
                                          ylabel='Density', 
                                          label='Reference', 
                                          width=bar_width, 
                                          xticks=np.arange(len(ref_freq)), 
                                          xticklabels=ref_freq.index,
                                          color=Colors.GREY)
        axs[i, 0] = create_bar_plot(axs[i, 0], 
                                          prod_positions, 
                                          prod_freq.values, 
                                          title=f'{feature} - PSI: {psi_table[psi_table["Feature"] == feature]["total_psi"].values[0]:.2f}', 
                                          xlabel=None, 
                                          ylabel='Density', 
                                          label='Production', 
                                          width=bar_width, 
                                          xticks=np.arange(len(ref_freq)), 
                                          xticklabels=ref_freq.index,
                                          color=Colors.RED)

        # Right column: PSI trend plots
        last_n_months = min(len(psi_table.columns)-2, 6)

        monthly_psi_values = psi_table.loc[psi_table['Feature'] == feature, psi_table.columns[-last_n_months:]].values.flatten()

        xticklabels = psi_table.columns[-len(monthly_psi_values):]
      
        axs[i, 1] = create_line_plot(axs[i, 1], 
                                          ydata=monthly_psi_values, 
                                          title=f'{feature} - PSI Trend', 
                                          xlabel=interval_label, 
                                          ylabel='PSI', 
                                          xticks=range(len(monthly_psi_values)), 
                                          xticklabels=xticklabels)

      fig.suptitle('Top three features with most feature drift', fontsize=15)
      plt.tight_layout()
      plt.show()

    if return_data:
      return psi_table


  def concept_drift(self, interval=None, start_date=None, end_date=None, plot=True, return_data=False):
    """
    If plot = True: Plot default rate and concept drift magnitude of features that have 
    experienced the most performance deterioration

    May return data as df with return_data=True.
    """

    concept_drift_table = self.calculate_concept_drift_magnitude(interval, start_date, end_date)

    concept_drift_table = concept_drift_table.sort_values(by='total_concept_drift', ascending=False)


    if plot:
      fig, axs = plt.subplots(3, 2, figsize=(15, 10))

      show_top_n = 3

      worst_features = concept_drift_table.iloc[:show_top_n]['Feature'].values

      for i, feature in enumerate(worst_features):
        
        # Left column: Bad rates plots
        bar_width = 0.35

        ref_freq = self.ref_binned[feature].value_counts(normalize=True).sort_index()
        prod_freq = self.prod_binned[feature].value_counts(normalize=True).sort_index()

        ref_badrates = self.ref_binned.groupby(feature)["label"].mean().fillna(0)
        prod_badrates = self.prod_binned.groupby(feature)["label"].mean().fillna(0)
        
        ref_positions = np.arange(len(ref_badrates))
        prod_positions = np.arange(len(prod_badrates)) + bar_width

        # Plot the reference frequency
        axs[i, 0] = create_line_plot(axs[i, 0],
                                          ydata=prod_freq.values, 
                                          label = 'Prod distribution',
                                          alpha=0.5)

        # Plot the bad rates
        axs[i, 0] = create_bar_plot(axs[i, 0], 
                                          ref_positions, 
                                          ref_badrates.values, 
                                          title=f'{feature}', 
                                          xlabel=None, 
                                          ylabel='Bad rate', 
                                          label='Reference', 
                                          width=bar_width, 
                                          xticks=np.arange(len(ref_badrates)), 
                                          xticklabels=ref_badrates.index,
                                          color=Colors.GREY
                                          )
        axs[i, 0] = create_bar_plot(axs[i, 0], 
                                          prod_positions, 
                                          prod_badrates.values, 
                                          title=f'{feature}', 
                                          xlabel=None, 
                                          ylabel='Bad rate', 
                                          label='Production', 
                                          width=bar_width, 
                                          xticks=np.arange(len(ref_badrates)), 
                                          xticklabels=ref_badrates.index,
                                          color=Colors.RED
                                          )

        last_n_months = 6
        monthly_concept_drift_values = concept_drift_table.loc[concept_drift_table['Feature'] == feature, concept_drift_table.columns[-last_n_months:]].values.flatten()

        # Right column: Concept drift magnitude plots
        axs[i, 1] = create_line_plot(axs[i, 1], 
                                          ydata=monthly_concept_drift_values, 
                                          title=f'{feature} - Concept drift trend', 
                                          xlabel='Month', 
                                          ylabel='Rate of label change', 
                                          xticks=range(len(monthly_concept_drift_values)), 
                                          xticklabels=concept_drift_table.columns[-last_n_months:]
                                          )
      
      fig.suptitle('Top three features with the most concept drift', fontsize=15)
      plt.tight_layout()
      plt.show()

    if return_data:
      return concept_drift_table

  def calculate_concept_drift_magnitude(self, interval=None, start_date=None, end_date=None):

    interval_col, interval_label = self._parse_interval(interval)

    prod_sliced, prod_sliced_binned = self._parse_timestamps(start_date, end_date)
    result_list = []

    #iterate over each feature and calculate the concept drift magnitude
    for feature in self.features:
      #ignore credit score
      if feature == "credit_score":
        continue
      row = {"Feature" : feature}
      
      ref_bad_rate = self.ref_binned.groupby(feature)['label'].mean()
      prod_bad_rate = prod_sliced_binned.groupby(feature)['label'].mean()
      # Filter prod_bad_rate and ref_bad_rate to not include bins with NaN
      prod_bad_rate = prod_bad_rate[~np.isnan(prod_bad_rate)]
      ref_bad_rate = ref_bad_rate[~np.isnan(ref_bad_rate)]
      # Save only the overlap of the two
      overlap = prod_bad_rate.index.intersection(ref_bad_rate.index)
      prod_bad_rate = prod_bad_rate[overlap]
      ref_bad_rate = ref_bad_rate[overlap]

      #total concept drift magnitude
      row["total_concept_drift"] = self._calculate_concept_drift_one_feature(self.ref_binned[feature], prod_sliced_binned[feature], ref_bad_rate, prod_bad_rate)
      
      #total concept drift magnitude for each month
      for interval in prod_sliced_binned[interval_col].unique():
        ref_binned = self.ref_binned[feature]
        prod_binned = prod_sliced_binned[prod_sliced_binned[interval_col]==interval][feature]
        prod_bad_rate = prod_sliced_binned[prod_sliced_binned[interval_col]==interval].groupby(feature)['label'].mean()
        prod_bad_rate = prod_bad_rate[~np.isnan(prod_bad_rate)]
        overlap = ref_bad_rate.index.intersection(prod_bad_rate.index)
        prod_bad_rate = prod_bad_rate[overlap]
        ref_bad_rate = ref_bad_rate[overlap]
        row[interval] = self._calculate_concept_drift_one_feature(ref_binned, prod_binned, ref_bad_rate, prod_bad_rate)
      
      result_list.append(row)

    concept_drift_table = pd.DataFrame(result_list)

    return concept_drift_table


  def check_gini(self, interval=None, start_date=None, end_date=None, plot=True, return_data=False): 
    """
    If plot = True: Plot the gini coefficient per month of the model.
    Plots production and reference separately.
    May return data as df with return_data=True.
    """

    interval_col, interval_label = self._parse_interval(interval)
    prod_sliced, prod_sliced_binned = self._parse_timestamps(start_date, end_date)

    def calculate_gini(df, interval_col):

      gini = df.groupby(interval_col).apply(lambda x: 2*roc_auc_score(x['label'], x['predicted_probability']) - 1)
      
      return gini.reset_index(name='gini')


    ref_gini = calculate_gini(self.ref.dropna(subset=['label']), interval_col)
    prod_gini = calculate_gini(prod_sliced.dropna(subset=['label']), interval_col)

    if plot:
      #plotting
      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6), sharey=True, gridspec_kw={'width_ratios': [len(ref_gini), len(prod_gini)]})

      ax1 = create_line_plot(ax1, 
                            ref_gini['gini'], 
                            title='Reference', 
                            xlabel=interval_label, 
                            ylabel='Gini Coefficient', 
                            xticks=range(len(ref_gini)), 
                            xticklabels=ref_gini[interval_col].astype(str)
                            )
      
      ax2 = create_line_plot(ax2, 
                            prod_gini['gini'], 
                            title='Production', 
                            xlabel=interval_label, 
                            xticks=range(len(prod_gini)), 
                            xticklabels=prod_gini[interval_col].astype(str)
                            )

      # Plot a vertical line at the last month of the reference data
      ax1.grid(True)
      ax2.grid(True)
      plt.tight_layout()
      plt.show()

    if return_data:
      return prod_gini
  

    
  def default_rate(self, interval=None, start_date=None, end_date=None, plot=True, return_data=False):
    """ 
    If plot=True: Plot the default rate of the model over time.

    May return data as df with return_data=True.
    """
    interval_col, interval_label = self._parse_interval(interval)
    prod_sliced, prod_sliced_binned = self._parse_timestamps(start_date, end_date)

    ref_bad_rate = pd.DataFrame(self.ref_binned.groupby('credit_score')['label'].mean()).reset_index()
    prod_bad_rate = pd.DataFrame(prod_sliced_binned.groupby('credit_score')['label'].mean()).reset_index()
    
    # Generate the bad rate of each score bin for the last six months of production data
    last_n_months = 6
    result_list = []
    month_labels = self.prod_binned[interval_col].unique()[-last_n_months:]
    month_labels = month_labels[::-1]

    for score_bin in self.prod_binned['credit_score'].cat.categories:
        row = {'score_bin': score_bin}
        for month in self.prod_binned[interval_col].unique()[-last_n_months:]:
            all_score_bins = self.prod_binned[self.prod_binned[interval_col] == month].groupby('credit_score')['label'].mean()
            row[month] = all_score_bins[score_bin]
        result_list.append(row)

    br_table = pd.DataFrame(result_list)
    br_table = br_table.round(3)
    # For each of the score_bins, save the information in the monthly columns as a list to one column called "Trend"
    br_table['Trend'] = br_table.iloc[:, 1:].values.tolist()   
    br_table = br_table.drop(columns=br_table.columns[1:-1])

    # Merge the br_table with prod_bad_rate
    prod_bad_rate = prod_bad_rate.set_index('credit_score')
    br_table = br_table.set_index('score_bin')
    prod_bad_rate = br_table.join(prod_bad_rate, on='score_bin').reset_index()

    # Heights of the bars indicating the ref_bad_rate
    bar_heights = 0.8
    y_positions = np.arange(len(ref_bad_rate))

    if plot:
      # Create the figure and axis
      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 9), gridspec_kw={'width_ratios': [3, 1]})

      # Plot the bars
      bars = ax1.barh(y_positions, prod_bad_rate['label'], height=bar_heights, color=Colors.GREY, label='Production Bad Rate')
      
      added_reference_to_legend = False
      
      # Plot the reference lines for each bar
      for idx, y in enumerate(y_positions):
          ref_rate = ref_bad_rate.loc[idx]['label']
          # Calculate the vertical position for the start and end of the line
          line_start = y - bar_heights / 2
          line_end = y + bar_heights / 2
          # Add a label only for the first line to avoid duplicate legend entries
          if not added_reference_to_legend:
            ax1.plot([ref_rate, ref_rate], [line_start, line_end], color='black', linewidth=1, label='Reference Bad Rate')
            added_reference_to_legend = True
          else:
            ax1.plot([ref_rate, ref_rate], [line_start, line_end], color='black', linewidth=1)

      # Set labels and title
      ax1.set_yticks(y_positions)
      ax1.set_yticklabels(ref_bad_rate['credit_score'], fontsize=12)
      ax1.legend(fontsize=12)
      ax1.set_xlabel('Bad Rate', fontsize=15)
      ax1.set_ylabel('Credit Score Bin', fontsize=15)
      ax1.set_title('Default Rates by Credit Score Bin', fontsize=15)

      # Collect all mini bar positions and corresponding labels for setting y-ticks later
      all_mini_bar_positions = []
      all_mini_bar_labels = []

      # Plot the trend data on the second subplot
      for idx, y in enumerate(y_positions):
          trend_data = prod_bad_rate['Trend'].iloc[idx]
          # Reverse the order of the trend data
          trend_data = trend_data[::-1]
          mini_bar_width = bar_heights / (2 * len(trend_data))  # Adjust the width of mini bars
          spacing_factor = 2.2  # Adjust this factor to increase spacing between bars
          mini_bar_positions = y + np.linspace(-bar_heights / spacing_factor, bar_heights / spacing_factor, len(trend_data))
          # mini_bar_positions = y + np.linspace(-bar_heights / 4, bar_heights / 4, len(trend_data))

          mini_bar_labels = month_labels
          all_mini_bar_labels.extend(mini_bar_labels)

          # Collect all positions and labels
          all_mini_bar_positions.extend(mini_bar_positions)
          
          ax2.barh(mini_bar_positions, trend_data, height=mini_bar_width, color=Colors.RED, 
                      label='Monthly Trend' if idx == 0 else "")
          
      # Set the y-tick positions and labels for the mini bars
      ax2.set_xlabel('Bad Rate', fontsize=15)
      ax2.set_yticks(all_mini_bar_positions)
      ax2.set_yticklabels(all_mini_bar_labels, fontsize=7)
      
      ax2.set_title(' Default Rate Trend by ' + interval_label, fontsize=15)
      # Ensure the bars remain at the same vertical levels
      ax2.set_ylim(ax1.get_ylim())

      plt.tight_layout()
      plt.show()

    if return_data:
      return(prod_bad_rate)


  def evaluate_feature(self, feature, interval=None, start_date=None, end_date=None):
    """
    Plots psi, frequency distribution, badrates and concept drift impact.
    """

    interval_col, interval_label = self._parse_interval(interval)
    prod, prod_binned = self._parse_timestamps(start_date, end_date)

    ref_freq = self.ref_binned[feature].value_counts(normalize=True).sort_index()
    prod_freq = prod_binned[feature].value_counts(normalize=True).sort_index()

    total_psi = self._calculate_feature_psi(self.ref_binned[feature], prod_binned[feature])
    psi_trend = {}
    for value in prod_binned[interval_col].unique():
      psi_trend[value] = self._calculate_feature_psi(self.ref_binned[feature], prod_binned[prod_binned[interval_col]==value][feature])

    psi_trend_s = pd.Series(psi_trend)

    ref_bad_rate = self.ref_binned.groupby(feature)['label'].mean()
    prod_bad_rate = prod_binned.groupby(feature)['label'].mean()
    # Filter prod_bad_rate and ref_bad_rate to not include bins with NaN
    prod_bad_rate = prod_bad_rate[~np.isnan(prod_bad_rate)]
    ref_bad_rate = ref_bad_rate[~np.isnan(ref_bad_rate)]
    # Save only the overlap of the two
    overlap = prod_bad_rate.index.intersection(ref_bad_rate.index)
    prod_bad_rate = prod_bad_rate[overlap]
    ref_bad_rate = ref_bad_rate[overlap]

    #total concept drift magnitude
    total_concept_drift = self._calculate_concept_drift_one_feature(self.ref_binned[feature], prod_binned[feature], ref_bad_rate, prod_bad_rate)

    concept_drift_trend = {}

    for value in prod_binned[interval_col].unique():
      ref_binned = self.ref_binned[feature]
      prod_binned_feat = prod_binned[prod_binned[interval_col]==value][feature]
      prod_bad_rate = prod_binned[prod_binned[interval_col]==value].groupby(feature)['label'].mean()
      prod_bad_rate = prod_bad_rate[~np.isnan(prod_bad_rate)]
      overlap = ref_bad_rate.index.intersection(prod_bad_rate.index)
      prod_bad_rate = prod_bad_rate[overlap]
      ref_bad_rate = ref_bad_rate[overlap]
      concept_drift_trend[value] = self._calculate_concept_drift_one_feature(ref_binned, prod_binned_feat, ref_bad_rate, prod_bad_rate)
    
    concept_drift_trend_s = pd.Series(concept_drift_trend)

    ref_badrates = self.ref_binned.groupby(feature)["label"].mean().fillna(0)
    prod_badrates = prod_binned.groupby(feature)["label"].mean().fillna(0)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Distribution plot
    bar_width = 0.35
    ref_positions = np.arange(len(ref_freq))
    prod_positions = np.arange(len(prod_freq)) + bar_width

    axs[0, 0] = create_bar_plot(axs[0, 0], 
                                        xdata=ref_positions, 
                                        ydata=ref_freq.values, 
                                        label='Reference', 
                                        width=bar_width, 
                                        color=Colors.GREY
                                        )
    
    axs[0, 0] = create_bar_plot(axs[0, 0], 
                                        xdata=prod_positions, 
                                        ydata=prod_freq.values, 
                                        title=f'Frequency distribution (total PSI: {total_psi:.2f})', 
                                        ylabel='Density', 
                                        label='Production', 
                                        width=bar_width, 
                                        xticks=np.arange(len(ref_freq)), 
                                        xticklabels=ref_freq.index,
                                        color=Colors.RED)

    #PSI plot
    last_n_months = 6
    monthly_psi_values = psi_trend_s[-last_n_months:].values.flatten()

    axs[0, 1] = create_line_plot(axs[0, 1],
                                        ydata=monthly_psi_values, 
                                        title='PSI Trend', 
                                        xlabel='Month', 
                                        ylabel='PSI', 
                                        xticks=range(len(monthly_psi_values)), 
                                        xticklabels=psi_trend_s[-last_n_months:].index,
                                        )

    #Bad rates plot

    ref_positions = np.arange(len(ref_badrates))
    prod_positions = np.arange(len(prod_badrates)) + bar_width

    # Plot the reference frequency
    axs[1, 0] = create_line_plot(axs[1, 0],
                                        ydata=prod_freq.values, 
                                        label = 'Prod distribution',
                                        alpha=0.5)

    # Plot the bad rates
    axs[1, 0] = create_bar_plot(axs[1, 0], 
                                        ref_positions, 
                                        ref_badrates.values, 
                                        label='Reference', 
                                        width=bar_width,
                                        color=Colors.GREY)

    axs[1, 0] = create_bar_plot(axs[1, 0], 
                                        prod_positions, 
                                        prod_badrates.values, 
                                        title=f'Bad rates by bin (total concept drift: {total_concept_drift})', 
                                        ylabel='Bad rate', 
                                        label='Production', 
                                        width=bar_width, 
                                        xticks=np.arange(len(ref_badrates)), 
                                        xticklabels=ref_badrates.index,
                                        color=Colors.RED)

    # Plot concept drift magnitude
    last_n_months = 6
    monthly_concept_drift_values = concept_drift_trend_s[-last_n_months:].values.flatten()

    axs[1, 1] = create_line_plot(axs[1, 1], 
                                        ydata=monthly_concept_drift_values, 
                                        title='Concept drift trend', 
                                        xlabel='Month', 
                                        ylabel='Rate of label change', 
                                        xticks=range(len(monthly_concept_drift_values)), 
                                        xticklabels=concept_drift_trend_s[-last_n_months:].index)
    fig.suptitle(feature, fontsize=15)
    plt.tight_layout()
    plt.show()


  def evaluate(self, interval=None, start_date=None, end_date=None):
      """
      Plot default rate and check_gini.
      """

      # Plot the default rate per month
      self.default_rate(interval, start_date, end_date)
      
      # Plot the gini coefficient per month
      self.check_gini(interval, start_date, end_date)
