import pandas as pd
import numpy as np

def impute_miss_val(df, missing_threshold=0.7):
    """
    Imputes missing values or drops columns based on missing value proportion.

     Returns:
    - df: DataFrame with missing values imputed or columns dropped
    """
    # Calculate the proportion of missing values in each column
    missing_proportions = df.isnull().mean()

    # Identify columns to drop
    cols_to_drop = missing_proportions[missing_proportions > missing_threshold].index
    df = df.drop(columns=cols_to_drop)
  
    # Impute missing values in remaining columns
    for col in df.columns:
        if df[col].isnull().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                # Numeric column: impute with median
                median_value = df[col].median()
                if pd.isnull(median_value):
                    # If median cannot be computed, drop the column
                    df = df.drop(columns=[col])
                else:
                   df[col] = df[col].fillna(median_value)
            else:
                # Categorical column: impute with mode
                mode_series = df[col].mode()
                if not mode_series.empty:
                    mode_value = mode_series[0]
                    df[col] = df[col].fillna(mode_value)
                else:
                    # If mode cannot be computed, drop the column
                    df = df.drop(columns=[col])
    print("\nSummary after Imputation")
    print("Size of remaining data:", df.shape)
    return df

def rmv_low_var(df, mad_threshold=0.1, freq_threshold=0.05):
    """
    Removes numerical variables with Median Absolute Deviation (MAD) below a threshold.
    Excludes binary columns from MAD calculation.
    Removes  binary columns with very low frequencies
    Returns:
    - df: pandas DataFrame with low MAD columns removed
    """
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Filter out binary columns
    non_binary_cols = []
    binary_cols =[]
    for col in numeric_cols:
        unique_values = df[col].nunique()
        # Consider a column binary if it has 2 or fewer unique values
        # Also check if all values are 0 or 1
        is_binary = (unique_values <= 2) or (set(df[col].unique()) <= {0, 1, np.nan})
        if not is_binary:
            non_binary_cols.append(col)
        elif is_binary:
            binary_cols.append(col)

    # Calculate low frequency binary numeric column
    min_freq = freq_threshold
    X_bin = df[binary_cols]
    binary_counts = X_bin.apply(pd.value_counts, normalize=True)
    keep_cols = [col for col in X_bin.columns if 
            (binary_counts[col].min() >= min_freq if len(binary_counts[col]) == 2 else True)]
    X_bin = X_bin[keep_cols]
    
    # Normalise the numeric columns by max
    df_tmp = df
    for col in non_binary_cols:
        df[col] = df_tmp[col]/np.max(np.abs(df_tmp[col]))

    # Calculate MAD for each non-binary numeric column
    mad_values = {}
    for col in non_binary_cols:
        mad = np.median(np.abs(df[col] - np.median(df[col])))
        mad_values[col] = mad
    
    # Create a Series from the MAD values
    mad_series = pd.Series(mad_values)
    #print(mad_series)
    
    # Identify columns to keep: 
    # 1. Non-numeric columns
    # 2. Binary numeric columns
    # 3. Non-binary numeric columns with MAD above threshold
    cols_to_keep = set(df.columns) - set(non_binary_cols)-set(binary_cols)  # Start with all CAT columns
    cols_to_keep.update(mad_series[mad_series >= mad_threshold].index)  # Add high MAD columns
    
    # Keep only the identified columns
    X_comb = pd.concat([df[list(cols_to_keep)], X_bin], axis=1)
    df = X_comb
    
    # Print summary for debugging
    print(f"\nMAD Analysis Summary:")
    print(f"Total numeric columns: {len(numeric_cols)}")
    print(f"Non binary numeric columns: {len(non_binary_cols)}")
    print(f"Binary columns excluded from MAD: {len(numeric_cols) - len(non_binary_cols)}")
    print("High Frequency Binary columns kept:", X_bin.shape)
    print(f"Columns removed due to low MAD: {len(non_binary_cols) - len(mad_series[mad_series >= mad_threshold])}")
   
  
    return df

def rmv_high_corr(df, correlation_threshold=0.5):
    # Step 1: Select numeric columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_numeric = df[numeric_cols]  # DataFrame with only numeric columns

    # Step 2: Calculate the correlation matrix
    corr_matrix = df_numeric.corr().abs()

    # Step 3: Identify highly correlated columns with a double loop
    to_drop = set()  # Use a set to avoid duplicates
    num_cols = corr_matrix.shape[0]
    
    for i in range(num_cols):
        for j in range(i + 1, num_cols):  # Only look at the upper triangle
            if corr_matrix.iloc[i, j] > correlation_threshold:
                # Identify the columns with high correlation
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                
                # Add one of the columns to `to_drop`
                to_drop.add(col2)  # Arbitrarily drop the second column

    # Step 4: Drop highly correlated columns
   
    print("\nCORR Summary")
    print(f"Columns removed due to high correlation: {len(to_drop)}")
    df = df.drop(columns=list(to_drop))

    return df


if __name__ == "__main__":
    # Load the dataset
#    df = pd.read_csv("PPCG_badEx3_cat.csv", header=0, index_col=0)
#    df = pd.read_csv("PPCG_badEx3_CNA_bin.csv", header=0, index_col=0)
#    df = pd.read_csv("ISAtest.csv", header=0, index_col=0)
    df = pd.read_csv("ppcg_cna_ar.csv", header=0, index_col=0)
    print("Initial size:", df.shape)
    print("DF head beginning:", df.head)
    patient_ids = df.index
	  
    # Step 1: Impute missing values or drop columns
    missing_threshold = 0.5  # Adjust as needed
    df = impute_miss_val(df, missing_threshold)
    print("DF head after imputation:", df.head)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"Initial number of numeric columns: {len(numeric_cols)}")
    print(f"list of numeric columns: {numeric_cols}")

    # Step 2: Remove numerical variables with low MAD
    mad_threshold = 0.01  # Adjust as needed
    freq_threshold = 0.05  # Adjust as needed
    df = rmv_low_var(df, mad_threshold, freq_threshold)
    print("DF shape after MAD filtering:", df.shape)
   # print("DF head after MAD filtering:", df.head)

    # Step 3: Remove highly correlated numerical variables
    correlation_threshold = 0.8  # Adjust as needed
    df = rmv_high_corr(df, correlation_threshold)
    print("DF shape after CORR filtering:", df.shape)
    #print("DF head after CORR filtering:", df.head)

    df.index = patient_ids
    # Save the processed dataset 
    print("final size:", df.shape)
    df.to_csv('ppcg_cna_ar2rmv.csv', index=True)
#    df.to_csv('PPCG_badEx3_CNA_bin_rmv.csv', index=True)



