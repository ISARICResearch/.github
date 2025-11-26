import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def lasso_var_sel_binary(df, outcome_col='mapped_outcome', random_state=42):
    """
    Prepare data and select features using binary logistic regression with elastic net penalty.
    Specifically designed for binary outcomes only.
    """
    if outcome_col not in df.columns:
        raise ValueError(f"Outcome column '{outcome_col}' not found in DataFrame")

    # Remove 'ID' column if it exists
    if 'ID' in df.columns:
        df = df.drop('ID', axis=1)
    
    # Separate predictors and outcome
    y = df[outcome_col].copy()
    X = df.drop(columns=[outcome_col])

    # Encode the binary outcome
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    
    # Verify that we have a binary outcome
    n_classes = len(np.unique(y))
    if n_classes != 2:
        raise ValueError("This function is designed for binary classification only. More than two classes found.")

    print("\nOutcome classes:", dict(zip(label_encoder.classes_, range(len(label_encoder.classes_)))))
    
    # Encode categorical predictors
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

    print(f"\nInitial shape of X: {X.shape}")
    if X.shape[1] > 0:
        print("First actual predictor column:", X.columns[0])
    else:
        raise ValueError("No predictor columns left after dropping outcome (and ID if applicable).")

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

    # Fit binary logistic regression with elastic net
    # For binary classification, multi_class defaults to 'ovr', which yields a single set of coefficients.
    logistic = LogisticRegressionCV(
        penalty='elasticnet',
        l1_ratios=[0.8, 0.9],
        solver='saga',
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state),
        random_state=random_state,
        max_iter=5000,
        class_weight='balanced',
        Cs=np.logspace(-4, 8, 20),
        tol=5e-4
    )

    logistic.fit(X_scaled, y)

    # logistic.coef_ will have shape (1, n_features) for binary classification
    coef_df = pd.DataFrame(logistic.coef_, columns=X.columns)
    # No indexing by classes since it's binary (one row of coefficients)

    # Compute feature importance as absolute value of coefficients
    # Since there's only one class row, mean across rows is just that row
    feature_importance = np.abs(coef_df.iloc[0, :])

    # Select features with non-zero importance
    selected_features = feature_importance[feature_importance > 0].index.tolist()

    # Predictions
    y_pred = logistic.predict(X_scaled)

    # Performance metrics
    print("\nPerformance Metrics:")
    print("-------------------")

    # Find the best C and corresponding CV score
    best_c = logistic.C_[0]
    c_index = np.where(logistic.Cs_ == best_c)[0][0]
    all_class_scores = []
    for cl in logistic.scores_:
        all_class_scores.extend(logistic.scores_[cl][:, c_index])
    best_cv_score = np.mean(all_class_scores)

    print(f"Best C value: {best_c}")
    print("\nConfusion Matrix:")
    conf_matrix = confusion_matrix(y, y_pred)
    print(conf_matrix)
    print("\nClassification Report:")

    target_names = [str(c) for c in label_encoder.classes_]
    print(classification_report(y, y_pred, target_names=target_names))
    print(f"Best CV score: {best_cv_score}")

    # l1_ratio_ returns the best ratio found for each class. For binary, there should be one:
    print(f"Best l1_ratio: {logistic.l1_ratio_[0]}")

    print(f"\nSelected {len(selected_features)} features")

    # Print feature importance for selected features
    print("\nFeature importance for selected features:")
    for feat in sorted(selected_features, key=lambda x: feature_importance[x], reverse=True):
        print(f"{feat}: {feature_importance[feat]:.4f}")

    X_selected = X[selected_features]
    print(f"Final shape of selected features: {X_selected.shape}")

    # Store metrics in a dictionary
    metrics = {
        'confusion_matrix': conf_matrix,
        'classification_report': classification_report(y, y_pred, target_names=label_encoder.classes_, output_dict=True),
        'accuracy': accuracy_score(y, y_pred),
        'cv_scores': all_class_scores
    }

    # Create a results_df for selected features
    results_df = pd.DataFrame({
        'Feature': selected_features,
        'Average_Coefficient': feature_importance[selected_features]
    })
    results_df = results_df.sort_values('Average_Coefficient', ascending=False)
    
    results_df.to_csv('feature_coefficients_binary.csv', index=False)
    print("\nSelected features and their coefficients:")
    print(results_df.head())

    return results_df, X_selected, y, selected_features, coef_df, label_encoder, feature_importance, metrics
    



if __name__ == "__main__":
    # Load the dataset
 #   df = pd.read_csv("ISARIC_redbin.csv", header=0, index_col=0)
    df = pd.read_csv("ppcg_cna_ar2rmv.csv", header=0, index_col=0)
 #   df = pd.read_csv("cat_out_data.csv", header=0, index_col=0)
 #   df = pd.read_csv("PPCG_badEx3_CNA_bin_rmv.csv", header=0, index_col=0)
    print(df.columns)
    print("Initial size:", df.shape)
    patient_ids = df.index

    results_df, X_selected, y, selected_features, coef_df, label_encoder, feature_importance, metrics = lasso_var_sel_binary(
 #       df, outcome_col='mapped_outcome'   
        df, outcome_col='outcome'      
    )
