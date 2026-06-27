import numpy as np
import pandas as pd

_plot_history = {
    'line_plot_called': False,
    'title_set': None,
    'xlabel_set': None,
    'ylabel_set': None,
    'scatter_plot_called': False,
    'histogram_called': False,
    'lmplot_called': False,
    'heatmap_called': False,
}

try:
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes
    import seaborn as sns

    # Plot
    _orig_plt_plot = plt.plot
    def _custom_plt_plot(*args, **kwargs):
        _plot_history['line_plot_called'] = True
        return _orig_plt_plot(*args, **kwargs)
    plt.plot = _custom_plt_plot

    _orig_axes_plot = Axes.plot
    def _custom_axes_plot(self, *args, **kwargs):
        _plot_history['line_plot_called'] = True
        return _orig_axes_plot(self, *args, **kwargs)
    Axes.plot = _custom_axes_plot

    # Title
    _orig_plt_title = plt.title
    def _custom_plt_title(label, *args, **kwargs):
        _plot_history['title_set'] = label
        return _orig_plt_title(label, *args, **kwargs)
    plt.title = _custom_plt_title

    _orig_axes_set_title = Axes.set_title
    def _custom_axes_set_title(self, label, *args, **kwargs):
        _plot_history['title_set'] = label
        return _orig_axes_set_title(self, label, *args, **kwargs)
    Axes.set_title = _custom_axes_set_title

    # xlabel
    _orig_plt_xlabel = plt.xlabel
    def _custom_plt_xlabel(xlabel, *args, **kwargs):
        _plot_history['xlabel_set'] = xlabel
        return _orig_plt_xlabel(xlabel, *args, **kwargs)
    plt.xlabel = _custom_plt_xlabel

    _orig_axes_set_xlabel = Axes.set_xlabel
    def _custom_axes_set_xlabel(self, xlabel, *args, **kwargs):
        _plot_history['xlabel_set'] = xlabel
        return _orig_axes_set_xlabel(self, xlabel, *args, **kwargs)
    Axes.set_xlabel = _custom_axes_set_xlabel

    # ylabel
    _orig_plt_ylabel = plt.ylabel
    def _custom_plt_ylabel(ylabel, *args, **kwargs):
        _plot_history['ylabel_set'] = ylabel
        return _orig_plt_ylabel(ylabel, *args, **kwargs)
    plt.ylabel = _custom_plt_ylabel

    _orig_axes_set_ylabel = Axes.set_ylabel
    def _custom_axes_set_ylabel(self, ylabel, *args, **kwargs):
        _plot_history['ylabel_set'] = ylabel
        return _orig_axes_set_ylabel(self, ylabel, *args, **kwargs)
    Axes.set_ylabel = _custom_axes_set_ylabel

    # Scatter
    _orig_plt_scatter = plt.scatter
    def _custom_plt_scatter(*args, **kwargs):
        _plot_history['scatter_plot_called'] = True
        return _orig_plt_scatter(*args, **kwargs)
    plt.scatter = _custom_plt_scatter

    _orig_axes_scatter = Axes.scatter
    def _custom_axes_scatter(self, *args, **kwargs):
        _plot_history['scatter_plot_called'] = True
        return _orig_axes_scatter(self, *args, **kwargs)
    Axes.scatter = _custom_axes_scatter

    _orig_sns_scatterplot = sns.scatterplot
    def _custom_sns_scatterplot(*args, **kwargs):
        _plot_history['scatter_plot_called'] = True
        return _orig_sns_scatterplot(*args, **kwargs)
    sns.scatterplot = _custom_sns_scatterplot

    # Histogram
    _orig_plt_hist = plt.hist
    def _custom_plt_hist(*args, **kwargs):
        _plot_history['histogram_called'] = True
        return _orig_plt_hist(*args, **kwargs)
    plt.hist = _custom_plt_hist

    _orig_axes_hist = Axes.hist
    def _custom_axes_hist(self, *args, **kwargs):
        _plot_history['histogram_called'] = True
        return _orig_axes_hist(self, *args, **kwargs)
    Axes.hist = _custom_axes_hist

    if hasattr(sns, 'histplot'):
        _orig_sns_histplot = sns.histplot
        def _custom_sns_histplot(*args, **kwargs):
            _plot_history['histogram_called'] = True
            return _orig_sns_histplot(*args, **kwargs)
        sns.histplot = _custom_sns_histplot

    # lmplot
    _orig_sns_lmplot = sns.lmplot
    def _custom_sns_lmplot(*args, **kwargs):
        _plot_history['lmplot_called'] = True
        return _orig_sns_lmplot(*args, **kwargs)
    sns.lmplot = _custom_sns_lmplot

    # heatmap
    _orig_sns_heatmap = sns.heatmap
    def _custom_sns_heatmap(*args, **kwargs):
        _plot_history['heatmap_called'] = True
        return _orig_sns_heatmap(*args, **kwargs)
    sns.heatmap = _custom_sns_heatmap
except Exception:
    pass

class ExerciseStep:
    def __init__(self, check_fn, hint_msg, solution_msg):
        self.check_fn = check_fn
        self.hint_msg = hint_msg
        self.solution_msg = solution_msg

    def check(self, *args, **kwargs):
        try:
            res = self.check_fn(*args, **kwargs)
            if res is True or res is None:
                print("🎉 Correct!")
            elif isinstance(res, str):
                print(f"❌ Incorrect: {res}")
            else:
                print("❌ Incorrect: Something went wrong with your solution.")
        except Exception as e:
            print(f"❌ Error during check: {str(e)}")

    def hint(self):
        print(f"💡 Hint: {self.hint_msg}")

    def solution(self):
        print(f"🔑 Solution:\n{self.solution_msg}")

# --- Check Functions ---
def ch1_s1_check(result_df):
    if not isinstance(result_df, pd.DataFrame):
        return "Output should be a pandas DataFrame."
    expected_cols = ['Name', 'Score']
    if list(result_df.columns) != expected_cols:
        return f"Expected columns {expected_cols}, but got {list(result_df.columns)}."
    if len(result_df) != 2:
        return f"Expected 2 rows (Charlie and David), but got {len(result_df)}."
    charlie = result_df[result_df['Name'] == 'Charlie']
    david = result_df[result_df['Name'] == 'David']
    if charlie.empty or david.empty:
        return "The rows should correspond to Charlie (Age 35) and David (Age 40)."
    if charlie.iloc[0]['Score'] != 95 or david.iloc[0]['Score'] != 80:
        return "The scores are incorrect."
    return True


def ch1_s2_check(agg_df):
    if not isinstance(agg_df, pd.DataFrame):
        return "Output should be a pandas DataFrame."
    expected_cols = ['Avg_Revenue', 'Total_Quantity']
    if list(agg_df.columns) != expected_cols:
        return f"Expected columns {expected_cols}, but got {list(agg_df.columns)}."
    if len(agg_df) != 3:
        return f"Expected 3 groups (Clothing, Electronics, Home), but got {len(agg_df)}."
    expected_values = {
        'Clothing': (300.0, 13),
        'Electronics': (1250.0, 25),
        'Home': (450.0, 9)
    }
    for cat, vals in expected_values.items():
        if cat not in agg_df.index:
            return f"Missing group for '{cat}' in the index."
        row = agg_df.loc[cat]
        if not np.isclose(row['Avg_Revenue'], vals[0]):
            return f"For group '{cat}', expected Avg_Revenue {vals[0]}, but got {row['Avg_Revenue']}."
        if row['Total_Quantity'] != vals[1]:
            return f"For group '{cat}', expected Total_Quantity {vals[1]}, but got {row['Total_Quantity']}."
    return True


def ch1_s3_check(func):
    if not callable(func):
        return "Input should be a function."
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[5.0], [6.0]])
    try:
        out = func(A, B)
    except Exception as e:
        return f"Error executing your function: {str(e)}"
    expected = np.array([[17/3], [39/7]])
    if not isinstance(out, np.ndarray):
        return "Output should be a numpy array."
    if not np.allclose(out, expected):
        return f"Incorrect values. Expected\n{expected}\nbut got\n{out}"
    return True


def ch2_s1_check(s_imputed):
    if not isinstance(s_imputed, pd.Series):
        return "Output should be a pandas Series."
    if s_imputed.isnull().any():
        return "Series still contains missing values."
    expected = pd.Series([10.0, 25.0, 20.0, 30.0, 25.0, 40.0])
    if not np.allclose(s_imputed.values, expected.values):
        return f"Incorrect values. Expected\n{expected.values}\nbut got\n{s_imputed.values}"
    return True


def ch2_s2_check(encoded_df):
    if not isinstance(encoded_df, pd.DataFrame):
        return "Output should be a pandas DataFrame."
    if 'Size_Encoded' not in encoded_df.columns:
        return "Column 'Size_Encoded' is missing."
    if not np.allclose(encoded_df['Size_Encoded'].values, [0, 1, 2, 1, 0]):
        return f"Incorrect encoding for 'Size_Encoded'. Expected [0, 1, 2, 1, 0], got {encoded_df['Size_Encoded'].values.tolist()}."
    color_cols = [c for c in encoded_df.columns if 'color_' in c.lower() or c.lower() in ['red', 'blue', 'green']]
    if len(color_cols) < 3:
        return f"Could not find one-hot encoded columns for 'Color'. Found columns: {list(encoded_df.columns)}"
    red_col = [c for c in color_cols if 'red' in c.lower()]
    blue_col = [c for c in color_cols if 'blue' in c.lower()]
    green_col = [c for c in color_cols if 'green' in c.lower()]
    if not red_col or not blue_col or not green_col:
        return "Could not identify separate columns for Red, Blue, and Green."
    if not np.allclose(encoded_df[red_col[0]].values, [1, 0, 1, 0, 0]):
        return f"Incorrect values for Red column. Expected [1, 0, 1, 0, 0], got {encoded_df[red_col[0]].values.tolist()}"
    if not np.allclose(encoded_df[blue_col[0]].values, [0, 1, 0, 0, 1]):
        return f"Incorrect values for Blue column."
    if not np.allclose(encoded_df[green_col[0]].values, [0, 0, 0, 1, 0]):
        return f"Incorrect values for Green column."
    return True


def ch2_s3_check(func):
    if not callable(func):
        return "Input should be a function."
    arr = np.array([-100, 1, 2, 3, 4, 5, 6, 7, 8, 100])
    try:
        out = func(arr, 0.0, 1.0)
    except Exception as e:
        return f"Error executing your function: {str(e)}"
    p10 = np.percentile(arr, 10)
    p90 = np.percentile(arr, 90)
    clipped = np.clip(arr, p10, p90)
    expected = (clipped - clipped.min()) / (clipped.max() - clipped.min()) if clipped.max() != clipped.min() else clipped
    if not isinstance(out, np.ndarray):
        return "Output should be a numpy array."
    if not np.allclose(out, expected):
        return f"Incorrect values. Expected\n{expected}\nbut got\n{out}"
    return True


def ch3_s1_check():
    title = _plot_history['title_set']
    xlabel = _plot_history['xlabel_set']
    ylabel = _plot_history['ylabel_set']
    if not title or str(title).strip() == "":
        return "The plot is missing a title."
    if not xlabel or str(xlabel).strip() == "":
        return "The plot is missing an X-axis label."
    if not ylabel or str(ylabel).strip() == "":
        return "The plot is missing a Y-axis label."
    if not _plot_history['histogram_called']:
        return "Could not find any bars/patches in the active plot. Make sure you plotted a histogram."
    return True


def ch3_s2_check():
    if not _plot_history['lmplot_called'] and not _plot_history['scatter_plot_called']:
        return "Could not find scatter plot points. Make sure you plotted a scatter plot."
    return True


def ch3_s3_check():
    if not _plot_history['heatmap_called']:
        return "Could not find a heatmap. Make sure you used sns.heatmap."
    return True


def ch4_s1_check(model, preds):
    from sklearn.linear_model import LinearRegression
    if not isinstance(model, LinearRegression):
        return "Model should be a scikit-learn LinearRegression instance."
    if not hasattr(model, "coef_"):
        return "The model has not been fitted yet."
    np.random.seed(42)
    X_train = np.random.rand(100, 1) * 10
    y_train = (2.5 * X_train + 4 + np.random.randn(100, 1)).ravel()
    X_test = np.array([[2.0], [5.0], [8.0]])
    ref_model = LinearRegression().fit(X_train, y_train)
    expected_preds = ref_model.predict(X_test)
    if not np.allclose(preds.ravel(), expected_preds.ravel(), atol=1e-4):
        return "Your predictions are incorrect. Did you fit on X_train and predict on X_test?"
    if not np.allclose(model.coef_, ref_model.coef_, atol=1e-4) or not np.isclose(model.intercept_, ref_model.intercept_, atol=1e-4):
        return "Your model coefficients do not match. Did you train on the correct training data?"
    return True


def ch4_s2_check(func):
    if not callable(func):
        return "Input should be a function."
    X = np.array([1.0, 2.0, 3.0, 4.0])
    y = np.array([3.0, 5.0, 7.0, 9.0])
    try:
        w, b = func(X, y, lr=0.01, epochs=1000)
    except Exception as e:
        return f"Error executing your gradient_descent: {str(e)}"
    if not np.isclose(w, 2.0, atol=0.1) or not np.isclose(b, 1.0, atol=0.2):
        return f"Expected w close to 2.0 and b close to 1.0, but got w={w:.4f}, b={b:.4f}"
    return True


def ch4_s3_check(coef_l1, coef_l2):
    if not isinstance(coef_l1, np.ndarray) or not isinstance(coef_l2, np.ndarray):
        return "Coefficients should be numpy arrays."
    if coef_l1.shape != coef_l2.shape:
        return "L1 and L2 coefficients must have the same shape."
    l1_zeros = np.sum(np.isclose(coef_l1, 0.0, atol=1e-5))
    l2_zeros = np.sum(np.isclose(coef_l2, 0.0, atol=1e-5))
    if l1_zeros == 0:
        return "Your L1 coefficients have no exact zeros. Double check if you applied L1 penalty (Lasso) and configured the regularization strength."
    if l1_zeros <= l2_zeros:
        return f"Expected L1 (Lasso) to produce more sparse coefficients (more zeros) than L2 (Ridge), but got L1 zeros={l1_zeros}, L2 zeros={l2_zeros}."
    return True


def ch5_s1_check(dt_model):
    from sklearn.tree import DecisionTreeClassifier
    if not isinstance(dt_model, DecisionTreeClassifier):
        return "Model should be a scikit-learn DecisionTreeClassifier."
    if dt_model.max_depth != 3:
        return f"Expected max_depth=3, but got {dt_model.max_depth}."
    if dt_model.random_state != 42:
        return f"Expected random_state=42, but got {dt_model.random_state}."
    if not hasattr(dt_model, "classes_"):
        return "The model is not fitted. Did you run .fit()?"
    return True


def ch5_s2_check(rf_model, rf_acc):
    from sklearn.ensemble import RandomForestClassifier
    if not isinstance(rf_model, RandomForestClassifier):
        return "Model should be a scikit-learn RandomForestClassifier."
    if rf_model.n_estimators != 100:
        return f"Expected n_estimators=100, but got {rf_model.n_estimators}."
    if rf_model.max_depth != 5:
        return f"Expected max_depth=5, but got {rf_model.max_depth}."
    if rf_model.min_samples_split != 4:
        return f"Expected min_samples_split=4, but got {rf_model.min_samples_split}."
    if rf_model.random_state != 42:
        return f"Expected random_state=42, but got {rf_model.random_state}."
    if not hasattr(rf_model, "classes_"):
        return "The model is not fitted. Did you run .fit()?"
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    expected_acc = accuracy_score(y_test, rf_model.predict(X_test))
    if not np.isclose(rf_acc, expected_acc):
        return f"Incorrect accuracy score. Expected {expected_acc:.4f}, but got {rf_acc:.4f}."
    return True


def ch5_s3_check(importances, selected_indices, X_train_filtered):
    if not isinstance(importances, np.ndarray):
        return "importances should be a numpy array."
    if not isinstance(selected_indices, np.ndarray):
        return "selected_indices should be a numpy array."
    if not isinstance(X_train_filtered, np.ndarray):
        return "X_train_filtered should be a numpy array."
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=4, random_state=42).fit(X_train, y_train)
    ref_importances = rf.feature_importances_
    ref_indices = np.where(ref_importances > 0.1)[0]
    ref_filtered = X_train[:, ref_indices]
    if not np.allclose(importances, ref_importances):
        return "Feature importances do not match the random forest model."
    if not np.array_equal(selected_indices, ref_indices):
        return f"Selected indices do not match. Expected {ref_indices.tolist()}, got {selected_indices.tolist()}."
    if not np.allclose(X_train_filtered, ref_filtered):
        return "Filtered training features do not match."
    return True


def ch6_s1_check(nb_model):
    from sklearn.naive_bayes import MultinomialNB
    if not isinstance(nb_model, MultinomialNB):
        return "Model should be a scikit-learn MultinomialNB."
    if nb_model.alpha != 1.0:
        return f"Expected alpha=1.0, but got {nb_model.alpha}."
    if not hasattr(nb_model, "classes_"):
        return "The model is not fitted."
    return True


def ch6_s2_check(svm_model, support_indices):
    from sklearn.svm import SVC
    if not isinstance(svm_model, SVC):
        return "Model should be a scikit-learn SVC."
    if svm_model.kernel != 'linear':
        return f"Expected kernel='linear', but got {svm_model.kernel}."
    if not np.array_equal(support_indices, svm_model.support_):
        return "Support indices do not match the support_ attribute of the model."
    return True


def ch6_s3_check(acc_linear, acc_rbf):
    if acc_rbf <= acc_linear:
        return f"Expected RBF SVM accuracy ({acc_rbf:.4f}) to be higher than linear SVM accuracy ({acc_linear:.4f}) on the moons dataset."
    if acc_rbf > 1.0 or acc_linear > 1.0 or acc_rbf < 0.0 or acc_linear < 0.0:
        return "Accuracy values must be between 0.0 and 1.0."
    return True


def ch7_s1_check(X_pca):
    if not isinstance(X_pca, np.ndarray):
        return "Output should be a numpy array."
    if X_pca.shape[1] != 2:
        return f"Expected 2 columns (2 principal components), but got {X_pca.shape[1]}."
    from sklearn.datasets import load_iris
    from sklearn.decomposition import PCA
    iris = load_iris()
    ref_pca = PCA(n_components=2, random_state=42).fit_transform(iris.data)
    if not np.allclose(np.abs(X_pca), np.abs(ref_pca), atol=1e-4):
        return "PCA values do not match standard PCA on the Iris dataset."
    return True


def ch7_s2_check(inertias):
    if not isinstance(inertias, list):
        return "Inertias should be a list."
    if len(inertias) != 5:
        return f"Expected list of length 5 (for k=1..5), but got length {len(inertias)}."
    for i in range(1, len(inertias)):
        if inertias[i] >= inertias[i-1]:
            return f"Inertias must decrease as k increases. Got {inertias}."
    return True


def ch7_s3_check(func):
    if not callable(func):
        return "Input must be a function."
    np.random.seed(42)
    X = np.concatenate([
        np.random.normal(loc=[0.0, 0.0], scale=0.5, size=(50, 2)),
        np.random.normal(loc=[5.0, 5.0], scale=0.5, size=(50, 2))
    ])
    try:
        centers, labels = func(X, 2, max_iters=100)
    except Exception as e:
        return f"Error executing your kmeans_scratch function: {str(e)}"
    if not isinstance(centers, np.ndarray) or not isinstance(labels, np.ndarray):
        return "Centers and labels must be numpy arrays."
    if centers.shape != (2, 2):
        return f"Expected centers shape (2, 2), but got {centers.shape}."
    if labels.shape != (100,):
        return f"Expected labels shape (100,), but got {labels.shape}."
    sorted_centers = np.sort(centers, axis=0)
    expected_centers = np.array([[0.0, 0.0], [5.0, 5.0]])
    dist1 = np.linalg.norm(sorted_centers[0] - expected_centers[0]) + np.linalg.norm(sorted_centers[1] - expected_centers[1])
    dist2 = np.linalg.norm(sorted_centers[0] - expected_centers[1]) + np.linalg.norm(sorted_centers[1] - expected_centers[0])
    if min(dist1, dist2) > 1.0:
        return f"Centers are not close to the actual cluster centroids. Got {centers}."
    return True


def ch8_s1_check(X_poly):
    if not isinstance(X_poly, np.ndarray):
        return "Output should be a numpy array."
    if X_poly.shape[1] != 5:
        return f"Expected 5 columns, but got {X_poly.shape[1]}."
    X = np.array([[2.0, 3.0], [4.0, 5.0]])
    from sklearn.preprocessing import PolynomialFeatures
    ref_poly = PolynomialFeatures(degree=2, include_bias=False).fit_transform(X)
    if not np.allclose(X_poly, ref_poly):
        return "Polynomial values do not match expected features."
    return True


def ch8_s2_check(df_processed):
    if not isinstance(df_processed, pd.DataFrame):
        return "Output should be a pandas DataFrame."
    for col in ['hour_sin', 'hour_cos']:
        if col not in df_processed.columns:
            return f"Missing column: {col}."
    expected_sin = np.sin(2 * np.pi * np.array([0, 6, 12, 18]) / 24.0)
    expected_cos = np.cos(2 * np.pi * np.array([0, 6, 12, 18]) / 24.0)
    if not np.allclose(df_processed['hour_sin'].values, expected_sin, atol=1e-4):
        return "Incorrect values for 'hour_sin'."
    if not np.allclose(df_processed['hour_cos'].values, expected_cos, atol=1e-4):
        return "Incorrect values for 'hour_cos'."
    return True


def ch8_s3_check(rfe_model, X_selected, ranking):
    from sklearn.feature_selection import RFE
    if not isinstance(rfe_model, RFE):
        return "rfe_model should be a scikit-learn RFE instance."
    if X_selected.shape[1] != 3:
        return f"Expected 3 selected features, but got {X_selected.shape[1]}."
    from sklearn.datasets import make_classification
    from sklearn.ensemble import RandomForestClassifier
    X, y = make_classification(n_samples=500, n_features=8, n_informative=3, random_state=42)
    ref_rf = RandomForestClassifier(random_state=42)
    ref_rfe = RFE(estimator=ref_rf, n_features_to_select=3).fit(X, y)
    ref_selected = ref_rfe.transform(X)
    if not np.array_equal(ranking, ref_rfe.ranking_):
        return "Feature ranking does not match expected RFE ranking."
    if not np.allclose(X_selected, ref_selected):
        return "Selected features do not match expected RFE selection."
    return True


def ch9_s1_check(mean_cv_score):
    from sklearn.datasets import make_classification
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import KFold, cross_val_score
    X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
    rf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    expected_score = cross_val_score(rf, X, y, cv=KFold(5, shuffle=True, random_state=42)).mean()
    if not np.isclose(mean_cv_score, expected_score):
        return f"Incorrect CV score. Expected {expected_score:.4f}, but got {mean_cv_score:.4f}."
    return True


def ch9_s2_check(best_params_grid, best_params_random):
    if not isinstance(best_params_grid, dict) or not isinstance(best_params_random, dict):
        return "Best parameters should be dictionaries."
    expected_keys = {'max_depth', 'min_samples_split'}
    if set(best_params_grid.keys()) != expected_keys:
        return f"Expected grid search keys {expected_keys}, but got {set(best_params_grid.keys())}."
    if set(best_params_random.keys()) != expected_keys:
        return f"Expected random search keys {expected_keys}, but got {set(best_params_random.keys())}."
    if best_params_grid['max_depth'] not in [3, 5, 7] or best_params_grid['min_samples_split'] not in [2, 5, 10]:
        return "Grid search parameters are outside specified grids."
    return True


def ch9_s3_check(best_threshold, max_f1):
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import f1_score
    X, y = make_classification(n_samples=500, n_classes=2, weights=[0.7, 0.3], random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X_train, y_train)
    y_probs = clf.predict_proba(X_test)[:, 1]
    best_t = 0.0
    best_f1 = 0.0
    for t in np.arange(0.1, 0.91, 0.01):
        preds = (y_probs >= t).astype(int)
        score = f1_score(y_test, preds)
        if score > best_f1:
            best_f1 = score
            best_t = t
    if not np.isclose(best_threshold, best_t, atol=1e-4):
        return f"Incorrect threshold. Expected {best_t:.2f}, but got {best_threshold:.2f}."
    if not np.isclose(max_f1, best_f1, atol=1e-4):
        return f"Incorrect max F1 score. Expected {best_f1:.4f}, but got {max_f1:.4f}."
    return True


def ch10_s1_check(mlp_model):
    from sklearn.neural_network import MLPClassifier
    if not isinstance(mlp_model, MLPClassifier):
        return "Model should be a scikit-learn MLPClassifier."
    if mlp_model.hidden_layer_sizes != (64, 32):
        return f"Expected hidden_layer_sizes=(64, 32), but got {mlp_model.hidden_layer_sizes}."
    if mlp_model.activation != 'relu':
        return f"Expected activation='relu', but got '{mlp_model.activation}'."
    if not hasattr(mlp_model, "classes_"):
        return "Model has not been fitted."
    return True


def ch10_s2_check(predict_fn, train_fn):
    if not callable(predict_fn) or not callable(train_fn):
        return "Both inputs must be callable functions."
    weights = np.array([1.0, -1.0])
    bias = -0.5
    try:
        p1 = predict_fn(np.array([1.0, 1.0]), weights, bias)
        p2 = predict_fn(np.array([2.0, 1.0]), weights, bias)
    except Exception as e:
        return f"Error executing predict function: {str(e)}"
    if p1 != 0 or p2 != 1:
        return f"Incorrect predictions. For inputs [1,1] and [2,1] with weights [1,-1] and bias -0.5, expected outputs 0 and 1, but got {p1} and {p2}."
    X = np.array([[0,0], [0,1], [1,0], [1,1]])
    y = np.array([0, 0, 0, 1])
    try:
        w, b = train_fn(X, y, lr=0.1, epochs=100)
    except Exception as e:
        return f"Error executing train function: {str(e)}"
    for xi, yi in zip(X, y):
        pi = predict_fn(xi, w, b)
        if pi != yi:
            return f"Perceptron did not converge. Failed on input {xi.tolist()}, expected {yi}, predicted {pi}."
    return True


def ch10_s3_check(SimpleNNClass):
    if not isinstance(SimpleNNClass, type):
        return "Input should be the SimpleNN class definition, not an instance."
    try:
        nn = SimpleNNClass(input_dim=2, hidden_dim=4, output_dim=1)
        X = np.array([[0,0], [0,1], [1,0], [1,1]])
        y = np.array([[0], [1], [1], [0]])
        nn.train(X, y, lr=0.1, epochs=10000)
        preds = nn.forward(X)
    except Exception as e:
        return f"Error executing your neural network class: {str(e)}"
    if not isinstance(preds, np.ndarray):
        return "Predictions from forward pass should be a numpy array."
    if preds.shape != (4, 1):
        return f"Expected prediction shape (4, 1), but got {preds.shape}."
    binary_preds = (preds > 0.5).astype(int)
    if not np.array_equal(binary_preds, y):
        return f"Neural network failed to learn XOR. Expected outputs {y.ravel().tolist()}, but got predictions {preds.ravel().tolist()}."
    return True


def ch11_s1_check(rolling_mean, rolling_std):
    if not isinstance(rolling_mean, pd.Series) or not isinstance(rolling_std, pd.Series):
        return "rolling_mean and rolling_std must be pandas Series."
    if rolling_mean.isnull().sum() != 6 or rolling_std.isnull().sum() != 6:
        return "The rolling statistics must use a window size of 7."
    np.random.seed(42)
    time = pd.date_range(start='2026-01-01', periods=100, freq='D')
    value = np.sin(np.linspace(0, 20, 100)) + np.random.normal(scale=0.1, size=100)
    df = pd.DataFrame({'value': value}, index=time)
    expected_mean = df['value'].rolling(window=7).mean()
    expected_std = df['value'].rolling(window=7).std()
    if not np.allclose(rolling_mean.dropna(), expected_mean.dropna()):
        return "Incorrect rolling mean values."
    if not np.allclose(rolling_std.dropna(), expected_std.dropna()):
        return "Incorrect rolling standard deviation values."
    return True


def ch11_s2_check(diff_series, adf_pvalue):
    if not isinstance(diff_series, pd.Series):
        return "diff_series must be a pandas Series."
    if len(diff_series) != 99:
        return "Differencing a 100-length series once should result in a 99-length series."
    np.random.seed(42)
    time = pd.date_range(start='2026-01-01', periods=100, freq='D')
    value = np.sin(np.linspace(0, 20, 100)) + np.random.normal(scale=0.1, size=100) + np.linspace(0, 5, 100)
    df = pd.DataFrame({'value': value}, index=time)
    expected_diff = df['value'].diff().dropna()
    from statsmodels.tsa.stattools import adfuller
    expected_p = adfuller(expected_diff)[1]
    if not np.allclose(diff_series.values, expected_diff.values):
        return "Incorrect differenced values."
    if not np.isclose(adf_pvalue, expected_p):
        return f"Incorrect ADF test p-value. Expected {expected_p:.6f}, got {adf_pvalue:.6f}."
    return True


def ch11_s3_check(mape):
    np.random.seed(42)
    time = pd.date_range(start='2026-01-01', periods=100, freq='D')
    value = np.sin(np.linspace(0, 20, 100)) + np.random.normal(scale=0.1, size=100) + np.linspace(0, 5, 100)
    df = pd.DataFrame({'value': value}, index=time)
    train, test = df.iloc[:80], df.iloc[80:]
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(train, order=(1,1,0)).fit()
    fc = model.forecast(steps=20)
    expected_mape = np.mean(np.abs((test['value'] - fc) / test['value'])) * 100
    if not np.isclose(mape, expected_mape, atol=1e-2):
        return f"Incorrect MAPE value. Expected {expected_mape:.4f}%, but got {mape:.4f}%."
    return True


def ch12_s1_check(cleaned_tokens, freq_dist):
    if not isinstance(cleaned_tokens, list):
        return "cleaned_tokens must be a list."
    expected_tokens = ['welcome', 'learning', 'of', 'python', 'nlp', 'nlp', 'powerful', 'tool', 'learning', 'python']
    from collections import Counter
    expected_counts = dict(Counter(expected_tokens))
    if cleaned_tokens != expected_tokens:
        return f"Tokens do not match. Expected {expected_tokens}, got {cleaned_tokens}."
    if not isinstance(freq_dist, dict) and not isinstance(freq_dist, Counter):
        return "freq_dist must be a dictionary or Counter object."
    if dict(freq_dist) != expected_counts:
        return f"Frequency distribution does not match. Expected {expected_counts}, got {dict(freq_dist)}."
    return True


def ch12_s2_check(similarity_matrix):
    if not isinstance(similarity_matrix, np.ndarray):
        return "similarity_matrix must be a numpy array."
    if similarity_matrix.shape != (3, 3):
        return f"Expected shape (3, 3), but got {similarity_matrix.shape}."
    if not np.allclose(np.diag(similarity_matrix), 1.0):
        return "Diagonal of similarity matrix must be exactly 1.0."
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    docs = [
        "cats eat fish and love milk",
        "dogs chase cats and love bones",
        "fish swim in the deep water"
    ]
    vec = TfidfVectorizer()
    tfidf = vec.fit_transform(docs)
    expected_sim = cosine_similarity(tfidf)
    if not np.allclose(similarity_matrix, expected_sim):
        return "Similarity values do not match expected cosine similarity matrix."
    return True


def ch12_s3_check(sentence_vectors, test_acc):
    if not isinstance(sentence_vectors, np.ndarray):
        return "sentence_vectors must be a numpy array."
    if sentence_vectors.shape != (4, 3):
        return f"Expected sentence_vectors shape (4, 3), but got {sentence_vectors.shape}."
    word_vectors = {
        'happy': np.array([0.5, 0.8, -0.1]),
        'sad': np.array([-0.6, -0.5, 0.2]),
        'good': np.array([0.4, 0.6, 0.0]),
        'bad': np.array([-0.5, -0.7, 0.1]),
        'day': np.array([0.1, 0.1, 0.1]),
        'night': np.array([-0.1, -0.1, 0.0])
    }
    sentences = [
        "happy good day",
        "sad bad night",
        "good day",
        "bad night"
    ]
    expected_vecs = []
    for s in sentences:
        tokens = s.split()
        vecs = [word_vectors[t] for t in tokens if t in word_vectors]
        expected_vecs.append(np.mean(vecs, axis=0))
    expected_vecs = np.array(expected_vecs)
    if not np.allclose(sentence_vectors, expected_vecs):
        return "Sentence vectors are computed incorrectly."
    if test_acc < 0.0 or test_acc > 1.0:
        return "Accuracy must be between 0.0 and 1.0."
    return True


def ch13_s1_check(outliers_z, outliers_iqr):
    if not isinstance(outliers_z, np.ndarray) or not isinstance(outliers_iqr, np.ndarray):
        return "outliers_z and outliers_iqr must be numpy arrays."
    np.random.seed(42)
    X = np.random.normal(loc=10.0, scale=2.0, size=100)
    X[15] = 25.0
    X[65] = -5.0
    z = (X - X.mean()) / X.std()
    expected_z = X[np.abs(z) > 3]
    q25, q75 = np.percentile(X, 25), np.percentile(X, 75)
    iqr = q75 - q25
    expected_iqr = X[(X < q25 - 1.5 * iqr) | (X > q75 + 1.5 * iqr)]
    if not np.array_equal(np.sort(outliers_z), np.sort(expected_z)):
        return "Incorrect outliers found using Z-score method."
    if not np.array_equal(np.sort(outliers_iqr), np.sort(expected_iqr)):
        return "Incorrect outliers found using IQR method."
    return True


def ch13_s2_check(scores, anomalies):
    if not isinstance(scores, np.ndarray) or not isinstance(anomalies, np.ndarray):
        return "scores and anomalies must be numpy arrays."
    from sklearn.ensemble import IsolationForest
    np.random.seed(42)
    normal = np.random.normal(loc=0.0, scale=0.5, size=(100, 2))
    anom = np.array([[3.0, 3.0], [-3.0, -3.0]])
    X = np.concatenate([normal, anom], axis=0)
    model = IsolationForest(contamination=0.02, random_state=42).fit(X)
    expected_scores = model.decision_function(X)
    expected_anom = model.predict(X)
    if not np.allclose(scores, expected_scores):
        return "Anomaly decision scores do not match."
    if not np.array_equal(anomalies, expected_anom):
        return "Anomaly predictions do not match."
    return True


def ch13_s3_check(func):
    if not callable(func):
        return "Input should be a function."
    X = np.array([[1.0, 2.0], [2.0, 4.0], [5.0, 6.0]])
    try:
        out = func(X)
    except Exception as e:
        return f"Error executing your mahalanobis function: {str(e)}"
    if not isinstance(out, np.ndarray):
        return "Output must be a numpy array."
    cov = np.cov(X.T)
    inv_cov = np.linalg.inv(cov)
    mean = X.mean(axis=0)
    expected = []
    for x in X:
        diff = x - mean
        d = np.sqrt(diff.T @ inv_cov @ diff)
        expected.append(d)
    expected = np.array(expected)
    if not np.allclose(out, expected):
        return "Incorrect Mahalanobis distance values."
    return True


def ch14_s1_check(voting_clf, test_acc):
    from sklearn.ensemble import VotingClassifier
    if not isinstance(voting_clf, VotingClassifier):
        return "voting_clf must be a VotingClassifier."
    if voting_clf.voting != 'soft':
        return "Voting strategy should be 'soft'."
    if len(voting_clf.estimators) != 3:
        return "Voting classifier must consist of exactly 3 estimators."
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import accuracy_score
    X, y = make_classification(n_samples=500, n_features=6, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    expected_voting = VotingClassifier(
        estimators=[
            ('lr', LogisticRegression(random_state=42)),
            ('dt', DecisionTreeClassifier(max_depth=3, random_state=42)),
            ('nb', GaussianNB())
        ],
        voting='soft'
    ).fit(X_train, y_train)
    expected_acc = accuracy_score(y_test, expected_voting.predict(X_test))
    if not np.isclose(test_acc, expected_acc):
        return f"Incorrect test accuracy score. Expected {expected_acc:.4f}, but got {test_acc:.4f}."
    return True


def ch14_s2_check(adaboost_clfs, accuracies):
    if not isinstance(adaboost_clfs, list) or not isinstance(accuracies, list):
        return "Inputs must be lists."
    if len(adaboost_clfs) != 3 or len(accuracies) != 3:
        return "Both lists should contain exactly 3 items."
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.metrics import accuracy_score
    X, y = make_classification(n_samples=500, n_features=6, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    expected_accs = []
    for n in [1, 10, 50]:
        clf = AdaBoostClassifier(n_estimators=n, random_state=42).fit(X_train, y_train)
        expected_accs.append(accuracy_score(y_test, clf.predict(X_test)))
    if not np.allclose(accuracies, expected_accs):
        return "Incorrect accuracies list."
    return True


def ch14_s3_check(meta_features, test_acc):
    if not isinstance(meta_features, np.ndarray):
        return "meta_features must be a numpy array."
    if meta_features.shape != (100, 2):
        return f"Expected shape of meta-features (100, 2), got {meta_features.shape}."
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    X, y = make_classification(n_samples=500, n_features=6, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    knn = KNeighborsClassifier().fit(X_train, y_train)
    svm = SVC(probability=True, random_state=42).fit(X_train, y_train)
    expected_meta = np.column_stack([
        knn.predict_proba(X_test)[:, 1],
        svm.predict_proba(X_test)[:, 1]
    ])
    meta_clf = LogisticRegression(random_state=42).fit(
        np.column_stack([knn.predict_proba(X_train)[:, 1], svm.predict_proba(X_train)[:, 1]]),
        y_train
    )
    expected_acc = accuracy_score(y_test, meta_clf.predict(expected_meta))
    if not np.allclose(meta_features, expected_meta):
        return "Incorrect meta features."
    if not np.isclose(test_acc, expected_acc):
        return "Incorrect stacked model accuracy score."
    return True


def ch15_s1_check(X_lda):
    if not isinstance(X_lda, np.ndarray):
        return "X_lda must be a numpy array."
    if X_lda.shape[1] != 1:
        return f"Expected shape of LDA transform to have 1 feature, got {X_lda.shape[1]}."
    from sklearn.datasets import make_classification
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    X, y = make_classification(n_samples=300, n_features=4, n_classes=2, random_state=42)
    expected_lda = LinearDiscriminantAnalysis().fit_transform(X, y)
    if not np.allclose(np.abs(X_lda), np.abs(expected_lda)):
        return "LDA transform values do not match."
    return True


def ch15_s2_check(X_kpca):
    if not isinstance(X_kpca, np.ndarray):
        return "X_kpca must be a numpy array."
    if X_kpca.shape[1] != 2:
        return f"Expected shape of KPCA to have 2 features, got {X_kpca.shape[1]}."
    from sklearn.datasets import make_circles
    from sklearn.decomposition import KernelPCA
    X, y = make_circles(n_samples=300, factor=0.5, noise=0.05, random_state=42)
    expected_kpca = KernelPCA(n_components=2, kernel='rbf', gamma=15, random_state=42).fit_transform(X)
    if not np.allclose(np.abs(X_kpca), np.abs(expected_kpca)):
        return "Kernel PCA projection values do not match."
    return True


def ch15_s3_check(tsne_silhouette, pca_silhouette):
    if not isinstance(tsne_silhouette, float) or not isinstance(pca_silhouette, float):
        return "Silhouette scores must be float values."
    if tsne_silhouette < 0.1 or pca_silhouette < 0.1:
        return f"Expected t-SNE to produce better cluster separation than PCA on non-linear dataset, but got t-SNE={tsne_silhouette:.4f}, PCA={pca_silhouette:.4f}."
    return True


def ch16_s1_check(recommendations):
    if not isinstance(recommendations, list) and not isinstance(recommendations, np.ndarray):
        return "recommendations must be a list or numpy array."
    expected = [0, 2, 1]
    if list(recommendations) != expected:
        return f"Incorrect recommendation order. Expected {expected}, got {list(recommendations)}."
    return True


def ch16_s2_check(predicted_rating):
    expected = 4.4924
    if not isinstance(predicted_rating, (float, np.floating)):
        try:
            predicted_rating = float(predicted_rating)
        except:
            return "predicted_rating must be a float number."
    if not np.isclose(predicted_rating, expected, atol=1e-3):
        return f"Incorrect predicted rating. Expected ~{expected:.4f}, but got {predicted_rating:.4f}."
    return True


def ch16_s3_check(P, Q):
    if not isinstance(P, np.ndarray) or not isinstance(Q, np.ndarray):
        return "P and Q must be numpy arrays."
    if P.shape[1] != 2 or Q.shape[1] != 2:
        return "Latent dimension must be K=2."
    R = np.array([
        [5, 3, 0, 1],
        [4, 0, 0, 1],
        [1, 1, 0, 5],
        [1, 0, 0, 4],
        [0, 1, 5, 4],
    ])
    R_pred = P @ Q.T
    mask = R > 0
    diff = np.abs(R[mask] - R_pred[mask])
    if np.mean(diff) > 1.5:
        return f"Your matrix factorization reconstruction error is too high (mean absolute diff: {np.mean(diff):.4f})."
    return True


def ch17_s1_check(support, confidence, lift):
    expected_sup = 0.6
    expected_conf = 0.75
    expected_lift = 0.9375
    if not np.isclose(support, expected_sup):
        return f"Incorrect support. Expected {expected_sup}, got {support}."
    if not np.isclose(confidence, expected_conf):
        return f"Incorrect confidence. Expected {expected_conf}, got {confidence}."
    if not np.isclose(lift, expected_lift):
        return f"Incorrect lift. Expected {expected_lift}, got {lift}."
    return True


def ch17_s2_check(frequent_itemsets):
    if not isinstance(frequent_itemsets, list):
        return "frequent_itemsets must be a list."
    itemsets_sets = [set(x) for x in frequent_itemsets]
    required = [
        {'milk'}, {'bread'}, {'diaper'}, {'beer'},
        {'milk', 'bread'}, {'milk', 'diaper'}, {'milk', 'beer'},
        {'bread', 'diaper'}, {'bread', 'beer'}, {'diaper', 'beer'},
        {'milk', 'diaper', 'beer'}, {'bread', 'diaper', 'beer'}
    ]
    for r in required:
        if r not in itemsets_sets:
            return f"Missing frequent itemset: {r}."
    if len(frequent_itemsets) != 12:
        return f"Expected exactly 12 frequent itemsets, got {len(frequent_itemsets)}."
    return True


def ch17_s3_check(rules):
    if not isinstance(rules, list):
        return "rules must be a list."
    has_beer_diaper = False
    for antecedent, consequent, conf, lift in rules:
        if set(antecedent) == {'beer'} and set(consequent) == {'diaper'}:
            if np.isclose(conf, 1.0) and np.isclose(lift, 1.25):
                has_beer_diaper = True
    if not has_beer_diaper:
        return "Could not find expected rule: {'beer'} -> {'diaper'} with conf=1.0 and lift=1.25."
    return True


def ch18_s1_check(lp_model, acc):
    from sklearn.semi_supervised import LabelPropagation
    if not isinstance(lp_model, LabelPropagation):
        return "lp_model must be a scikit-learn LabelPropagation instance."
    if not hasattr(lp_model, "transduction_"):
        return "Model has not been fitted yet."
    if acc < 0.7 or acc > 1.0:
        return f"Accuracy seems incorrect: {acc:.4f}."
    return True


def ch18_s2_check(func):
    if not callable(func):
        return "Input must be a function."
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    np.random.seed(42)
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2, random_state=42)
    y_masked = y.copy()
    y_masked[50:] = -1
    try:
        clf = func(X, y_masked, threshold=0.9)
    except Exception as e:
        return f"Error executing your pseudo-labeling function: {str(e)}"
    if not hasattr(clf, "coef_"):
        return "Function should return a fitted model."
    return True


def ch18_s3_check(best_gamma, best_acc):
    if best_gamma not in [0.1, 1.0, 10.0, 100.0]:
        return "best_gamma must be one of the evaluated gammas."
    if best_gamma < 10.0:
        return f"Are you sure gamma={best_gamma} is the best?"
    if best_acc < 0.8:
        return f"Accuracy is too low: {best_acc}."
    return True


def ch19_s1_check(accuracy, f1):
    expected_acc = 0.95
    expected_f1 = 0.487179
    if not np.isclose(accuracy, expected_acc):
        return f"Incorrect accuracy. Expected {expected_acc}, got {accuracy}."
    if not np.isclose(f1, expected_f1, atol=1e-4):
        return f"Incorrect macro F1 score. Expected {expected_f1:.4f}, got {f1:.4f}."
    return True


def ch19_s2_check(func):
    if not callable(func):
        return "Input should be a function."
    X = np.array([[1, 2], [3, 4], [5, 6]])
    y = np.array([0, 0, 1])
    try:
        X_res, y_res = func(X, y)
    except Exception as e:
        return f"Error executing your oversampler: {str(e)}"
    if len(X_res) != 4 or len(y_res) != 4:
        return f"Expected balanced output of length 4, got lengths {len(X_res)} and {len(y_res)}."
    counts = np.bincount(y_res)
    if counts[0] != 2 or counts[1] != 2:
        return f"Output is not balanced. Class counts: {counts.tolist()}."
    return True


def ch19_s3_check(cost_sensitive_score):
    if cost_sensitive_score < 0.7 or cost_sensitive_score > 1.0:
        return f"Score seems incorrect: {cost_sensitive_score}."
    return True


def ch20_s1_check(study):
    import optuna
    if not isinstance(study, optuna.study.Study):
        return "study must be an Optuna Study instance."
    if len(study.trials) < 20:
        return "You should run at least 20 trials."
    best_params = study.best_params
    if 'x' not in best_params or 'y' not in best_params:
        return "Parameters optimized must be 'x' and 'y'."
    if not np.isclose(best_params['x'], 2.0, atol=2.0) or not np.isclose(best_params['y'], 3.0, atol=2.0):
        return f"Optuna study did not converge close to the minimum (2, 3). Got best parameters: {best_params}."
    return True


def ch20_s2_check(best_params, best_value):
    if not isinstance(best_params, dict):
        return "best_params must be a dictionary."
    expected_keys = {'n_estimators', 'max_depth', 'learning_rate'}
    if not expected_keys.issubset(best_params.keys()):
        return f"Missing optimized keys. Expected {expected_keys}, got {best_params.keys()}."
    if best_value < 0.8 or best_value > 1.0:
        return f"Best value (accuracy) seems too low or incorrect: {best_value}."
    return True


def ch20_s3_check(func):
    if not callable(func):
        return "Input must be a function."
    objective = lambda x: -(x[0] - 1.5)**2 + 4.0
    bounds = np.array([[0.0, 3.0]])
    try:
        best_x, best_y = func(objective, bounds, n_iters=10)
    except Exception as e:
        return f"Error executing your Bayesian Optimization function: {str(e)}"
    if not np.isclose(best_x[0], 1.5, atol=0.5):
        return f"Bayesian Optimization did not find the maximum close to 1.5. Got best_x = {best_x}."
    return True


# --- Easy Check Functions ---
def ch1_s1_easy_check(arr):
    if not isinstance(arr, np.ndarray): return "Output should be a numpy array."
    if arr.shape != (10,): return f"Expected shape (10,), but got {arr.shape}."
    if not np.array_equal(arr, np.arange(1, 11)): return f"Expected values [1..10], but got {arr}."
    return True

def ch1_s2_easy_check(arr):
    if not isinstance(arr, np.ndarray): return "Output should be a numpy array."
    if arr.shape != (5,): return f"Expected shape (5,), but got {arr.shape}."
    if not np.array_equal(arr, np.array([10, 20, 30, 40, 50])): return f"Expected [10, 20, 30, 40, 50], got {arr}."
    return True

def ch1_s3_easy_check(col):
    if not isinstance(col, pd.Series): return "Output should be a pandas Series."
    if list(col.values) != [25, 30]: return f"Expected values [25, 30], but got {list(col.values)}."
    return True

def ch2_s1_easy_check(s):
    if not isinstance(s, pd.Series): return "Output should be a pandas Series."
    if list(s.values) != [1.5, 0.0, 2.5, 0.0, 3.5]: return f"Expected values [1.5, 0.0, 2.5, 0.0, 3.5], but got {list(s.values)}."
    return True

def ch2_s2_easy_check(df):
    if not isinstance(df, pd.DataFrame): return "Output should be a pandas DataFrame."
    if len(df) != 1: return f"Expected an empty DataFrame after dropna, but got {len(df)} rows (expected 1)."
    return True

def ch2_s3_easy_check(s):
    if not isinstance(s, pd.Series): return "Output should be a pandas Series."
    if list(s.values) != ['red', 'blue', 'green']: return f"Expected ['red', 'blue', 'green'], but got {list(s.values)}."
    return True

def ch3_s1_easy_check():
    if not _plot_history['line_plot_called']:
        return "No line plot was drawn. Use plt.plot(x, y)."
    return True

def ch3_s2_easy_check():
    title = _plot_history['title_set']
    xlabel = _plot_history['xlabel_set']
    ylabel = _plot_history['ylabel_set']
    if not title or str(title).strip() == "": return "Plot is missing a title."
    if not xlabel or str(xlabel).strip() == "": return "Plot is missing X-axis label."
    if not ylabel or str(ylabel).strip() == "": return "Plot is missing Y-axis label."
    return True

def ch3_s3_easy_check():
    if not _plot_history['scatter_plot_called']: return "No scatter plot collection found. Make sure you used sns.scatterplot."
    return True

def ch4_s1_easy_check(model):
    from sklearn.linear_model import LinearRegression
    if not isinstance(model, LinearRegression): return "Output should be a LinearRegression instance."
    return True

def ch4_s2_easy_check(val):
    if not np.isclose(val, 0.03): return f"Expected MSE of 0.03, but got {val}."
    return True

def ch4_s3_easy_check(model):
    if not hasattr(model, "coef_"): return "Model has not been trained yet. Call model.fit(X, y)."
    if not np.isclose(model.coef_[0], 2.0): return f"Expected coef_ close to 2.0, but got {model.coef_[0]}."
    return True

def ch5_s1_easy_check(model):
    from sklearn.tree import DecisionTreeClassifier
    if not isinstance(model, DecisionTreeClassifier): return "Output should be a DecisionTreeClassifier."
    if model.max_depth != 3: return f"Expected max_depth=3, got {model.max_depth}."
    return True

def ch5_s2_easy_check(preds):
    if not isinstance(preds, np.ndarray): return "Output should be a numpy array."
    if not np.array_equal(preds, [0, 1]): return f"Expected predictions [0, 1], got {preds}."
    return True

def ch5_s3_easy_check(val):
    if not np.isclose(val, 0.75): return f"Expected accuracy 0.75, got {val}."
    return True

def ch6_s1_easy_check(model):
    from sklearn.naive_bayes import MultinomialNB
    if not isinstance(model, MultinomialNB): return "Output should be a MultinomialNB."
    return True

def ch6_s2_easy_check(model):
    from sklearn.svm import SVC
    if not isinstance(model, SVC): return "Output should be an SVC."
    if model.kernel != 'linear': return f"Expected kernel='linear', got {model.kernel}."
    return True

def ch6_s3_easy_check(probs):
    if not isinstance(probs, np.ndarray): return "Output should be a numpy array."
    if probs.shape != (1, 2): return f"Expected shape (1, 2), got {probs.shape}."
    return True

def ch7_s1_easy_check(model):
    from sklearn.decomposition import PCA
    if not isinstance(model, PCA): return "Output should be a PCA model."
    if model.n_components != 2: return f"Expected n_components=2, got {model.n_components}."
    return True

def ch7_s2_easy_check(model):
    from sklearn.cluster import KMeans
    if not isinstance(model, KMeans): return "Output should be a KMeans model."
    if model.n_clusters != 3: return f"Expected n_clusters=3, got {model.n_clusters}."
    return True

def ch7_s3_easy_check(labels):
    if not isinstance(labels, np.ndarray): return "Output should be a numpy array."
    if len(labels) != 6: return f"Expected 6 labels, got {len(labels)}."
    return True

def ch8_s1_easy_check(df):
    if 'A_B' not in df.columns: return "Column 'A_B' is missing."
    if list(df['A_B'].values) != [10, 30, 60]: return f"Expected values [10, 30, 60], got {list(df['A_B'].values)}."
    return True

def ch8_s2_easy_check(df):
    if 'Log_Skewed' not in df.columns: return "Column 'Log_Skewed' is missing."
    expected = np.log([10.0, 100.0, 1000.0])
    if not np.allclose(df['Log_Skewed'].values, expected): return f"Incorrect log values."
    return True

def ch8_s3_easy_check(df):
    if 'x_squared' not in df.columns: return "Column 'x_squared' is missing."
    if list(df['x_squared'].values) != [1, 4, 9, 16]: return f"Expected [1, 4, 9, 16], got {list(df['x_squared'].values)}."
    return True

def ch9_s1_easy_check(X_tr, X_te, y_tr, y_te):
    if len(X_tr) != 4 or len(X_te) != 1: return f"Expected split sizes 4 train, 1 test. Got {len(X_tr)}, {len(X_te)}."
    return True

def ch9_s2_easy_check(kf):
    from sklearn.model_selection import KFold
    if not isinstance(kf, KFold): return "Output should be a KFold instance."
    if kf.n_splits != 5: return f"Expected 5 splits, got {kf.n_splits}."
    return True

def ch9_s3_easy_check(val):
    if not np.isclose(val, 1.0): return f"Expected precision 1.0, got {val}."
    return True

def ch10_s1_easy_check(model):
    from sklearn.neural_network import MLPClassifier
    if not isinstance(model, MLPClassifier): return "Output should be an MLPClassifier."
    if model.hidden_layer_sizes != (10,): return f"Expected hidden_layer_sizes=(10,), got {model.hidden_layer_sizes}."
    return True

def ch10_s2_easy_check(func):
    if not callable(func): return "Input must be a function."
    if not np.isclose(func(0.0), 0.5): return "sigmoid(0.0) should be 0.5."
    return True

def ch10_s3_easy_check(z):
    if not np.isclose(z, -1.5): return f"Expected w . x + b = -1.5, got {z}."
    return True

def ch11_s1_easy_check(s_lag):
    if not isinstance(s_lag, pd.Series): return "Output should be a Series."
    if not pd.isna(s_lag.iloc[0]): return "The first element of shifted series should be NaN."
    if s_lag.iloc[1] != 10: return f"Expected index 1 to be 10, got {s_lag.iloc[1]}."
    return True

def ch11_s2_easy_check(s_diff):
    if not isinstance(s_diff, pd.Series): return "Output should be a Series."
    if not pd.isna(s_diff.iloc[0]): return "First element should be NaN."
    if s_diff.iloc[1] != 2: return f"Expected diff values [NaN, 2, 3, 4, 5], got {s_diff.tolist()}."
    return True

def ch11_s3_easy_check(s_roll):
    if not isinstance(s_roll, pd.Series): return "Output should be a Series."
    if not pd.isna(s_roll.iloc[0]) or not pd.isna(s_roll.iloc[1]): return "First two elements should be NaN."
    if s_roll.iloc[2] != 2.0: return f"Expected window 3 rolling mean at index 2 to be 2.0, got {s_roll.iloc[2]}."
    return True

def ch12_s1_easy_check(words):
    if not isinstance(words, list): return "Output must be a list of words."
    if words != ['machine', 'learning', 'is', 'fun']: return f"Expected ['machine', 'learning', 'is', 'fun'], got {words}."
    return True

def ch12_s2_easy_check(vec):
    from sklearn.feature_extraction.text import CountVectorizer
    if not isinstance(vec, CountVectorizer): return "Output must be a CountVectorizer."
    return True

def ch12_s3_easy_check(sim):
    if sim != 1: return f"Expected dot product 1, got {sim}."
    return True

def ch13_s1_easy_check(mean, std):
    if not np.isclose(mean, 5.0): return f"Expected mean 5.0, got {mean}."
    if not np.isclose(std, 2.0): return f"Expected std 2.0, got {std}."
    return True

def ch13_s2_easy_check(indices):
    if not isinstance(indices, np.ndarray): return "Output should be a numpy array."
    if list(indices) != [1, 3]: return f"Expected indices [1, 3], got {list(indices)}."
    return True

def ch13_s3_easy_check(model):
    from sklearn.ensemble import IsolationForest
    if not isinstance(model, IsolationForest): return "Output should be an IsolationForest."
    return True

def ch14_s1_easy_check(preds):
    if not isinstance(preds, np.ndarray): return "Output should be a numpy array."
    if not np.array_equal(preds, [0, 1, 0]): return f"Expected [0, 1, 0], got {preds}."
    return True

def ch14_s2_easy_check(model):
    from sklearn.ensemble import AdaBoostClassifier
    if not isinstance(model, AdaBoostClassifier): return "Output should be an AdaBoostClassifier."
    return True

def ch14_s3_easy_check(model):
    from sklearn.ensemble import BaggingClassifier
    if not isinstance(model, BaggingClassifier): return "Output should be a BaggingClassifier."
    return True

def ch15_s1_easy_check(model):
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    if not isinstance(model, LinearDiscriminantAnalysis): return "Output should be a LinearDiscriminantAnalysis."
    return True

def ch15_s2_easy_check(model):
    from sklearn.manifold import TSNE
    if not isinstance(model, TSNE): return "Output should be a TSNE instance."
    if model.n_components != 2: return f"Expected n_components=2, got {model.n_components}."
    return True

def ch15_s3_easy_check(val):
    if not np.isclose(val, 0.92566, atol=1e-3): return f"Expected silhouette score close to 0.926, got {val}."
    return True

def ch16_s1_easy_check(score):
    if not np.isclose(score, 22.0): return f"Expected score 22.0, got {score}."
    return True

def ch16_s2_easy_check(mag):
    if not np.isclose(mag, 5.0): return f"Expected magnitude 5.0, got {mag}."
    return True

def ch16_s3_easy_check(mat):
    if not isinstance(mat, pd.DataFrame): return "Output should be a DataFrame."
    if mat.shape != (2, 2): return f"Expected shape (2, 2), got {mat.shape}."
    return True

def ch17_s1_easy_check(support):
    if not np.isclose(support, 0.25): return f"Expected support 0.25, got {support}."
    return True

def ch17_s2_easy_check(confidence):
    if not np.isclose(confidence, 0.75): return f"Expected confidence 0.75, got {confidence}."
    return True

def ch17_s3_easy_check(lift):
    if not np.isclose(lift, 1.5): return f"Expected lift 1.5, got {lift}."
    return True

def ch18_s1_easy_check(model):
    from sklearn.semi_supervised import LabelPropagation
    if not isinstance(model, LabelPropagation): return "Output should be a LabelPropagation model."
    return True

def ch18_s2_easy_check(count):
    if count != 3: return f"Expected 3 unlabeled samples, got {count}."
    return True

def ch18_s3_easy_check(model):
    from sklearn.semi_supervised import LabelSpreading
    if not isinstance(model, LabelSpreading): return "Output should be a LabelSpreading model."
    return True

def ch19_s1_easy_check(counts):
    if list(counts) != [9, 1]: return f"Expected counts [9, 1], got {list(counts)}."
    return True

def ch19_s2_easy_check(model):
    from sklearn.tree import DecisionTreeClassifier
    if not isinstance(model, DecisionTreeClassifier): return "Output should be a DecisionTreeClassifier."
    if model.class_weight != 'balanced': return f"Expected class_weight='balanced', got {model.class_weight}."
    return True

def ch19_s3_easy_check(val):
    # Just checking it executes and returns a numeric balanced accuracy score
    if not isinstance(val, float): return "Output should be a float."
    return True

def ch20_s1_easy_check(optuna_module):
    if optuna_module.__name__ != 'optuna': return "Invalid optuna module import."
    return True

def ch20_s2_easy_check(study):
    import optuna
    if not isinstance(study, optuna.study.Study): return "Output should be an Optuna Study instance."
    if study.direction != optuna.study.StudyDirection.MINIMIZE: return "Study direction should be minimize."
    return True

def ch20_s3_easy_check(lr):
    if not (0.01 <= lr <= 0.2): return f"Suggested learning rate {lr} is not in bounds [0.01, 0.2]."
    return True


# --- Chapter 1 ---
class Ch1:
    step_1 = ExerciseStep(
        ch1_s1_easy_check,
        'Use np.arange(1, 11) or np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).',
        'arr_easy = np.arange(1, 11)'
    )
    step_2 = ExerciseStep(
        ch1_s2_easy_check,
        'Use slice syntax: arr_to_slice[:5].',
        'arr_sliced = arr_to_slice[:5]'
    )
    step_3 = ExerciseStep(
        ch1_s3_easy_check,
        "Use df_easy['Age'].",
        "age_column = df_easy['Age']"
    )
    step_4 = ExerciseStep(
        ch1_s1_check,
        "Use df[df['Age'] > 30][['Name', 'Score']]",
        "result_df = df[df['Age'] > 30][['Name', 'Score']]"
    )
    step_5 = ExerciseStep(
        ch1_s2_check,
        "Use sales_df.groupby('Category').agg(Avg_Revenue=('Revenue', 'mean'), Total_Quantity=('Quantity', 'sum'))",
        "agg_df = sales_df.groupby('Category').agg(\n    Avg_Revenue=('Revenue', 'mean'),\n    Total_Quantity=('Quantity', 'sum')\n)"
    )
    step_6 = ExerciseStep(
        ch1_s3_check,
        'Use np.sum(A, axis=1, keepdims=True) to compute row sums. Divide A by these sums to normalize. Then use np.dot or @ for multiplication.',
        'def normalize_and_multiply(A, B):\n    row_sums = np.sum(A, axis=1, keepdims=True)\n    A_norm = A / row_sums\n    return A_norm @ B'
    )

ch1 = Ch1()

# --- Chapter 2 ---
class Ch2:
    step_1 = ExerciseStep(
        ch2_s1_easy_check,
        'Use s_easy.fillna(0.0).',
        's_filled = s_easy.fillna(0.0)'
    )
    step_2 = ExerciseStep(
        ch2_s2_easy_check,
        'Use df_miss.dropna().',
        'df_clean = df_miss.dropna()'
    )
    step_3 = ExerciseStep(
        ch2_s3_easy_check,
        'Use s_str.str.lower().',
        's_lower = s_str.str.lower()'
    )
    step_4 = ExerciseStep(
        ch2_s1_check,
        'Use s.fillna(s.mean()) to replace NaNs with the average of the series.',
        's_imputed = s.fillna(s.mean())'
    )
    step_5 = ExerciseStep(
        ch2_s2_check,
        "Map 'Size' with a dictionary, and use pd.get_dummies(df, columns=['Color']) for one-hot encoding.",
        "df['Size_Encoded'] = df['Size'].map({'Small': 0, 'Medium': 1, 'Large': 2})\nencoded_df = pd.get_dummies(df, columns=['Color'])"
    )
    step_6 = ExerciseStep(
        ch2_s3_check,
        'Calculate percentiles using np.percentile(arr, 10) and np.percentile(arr, 90). Clip the array using np.clip. Then do min-max scaling.',
        'def custom_scale(arr, min_val, max_val):\n    p10 = np.percentile(arr, 10)\n    p90 = np.percentile(arr, 90)\n    clipped = np.clip(arr, p10, p90)\n    scaled = (clipped - clipped.min()) / (clipped.max() - clipped.min()) * (max_val - min_val) + min_val\n    return scaled'
    )

ch2 = Ch2()

# --- Chapter 3 ---
class Ch3:
    step_1 = ExerciseStep(
        ch3_s1_easy_check,
        'Call plt.plot(x, y).',
        'plt.plot(x, y)'
    )
    step_2 = ExerciseStep(
        ch3_s2_easy_check,
        "Use plt.title('My First Plot'), plt.xlabel('X Axis'), and plt.ylabel('Y Axis').",
        "plt.title('My First Plot')\nplt.xlabel('X Axis')\nplt.ylabel('Y Axis')"
    )
    step_3 = ExerciseStep(
        ch3_s3_easy_check,
        'Use sns.scatterplot(x=x_coords, y=y_coords).',
        'sns.scatterplot(x=x_coords, y=y_coords)'
    )
    step_4 = ExerciseStep(
        ch3_s1_check,
        'Use plt.hist(data) or sns.histplot(data). Remember to add plt.title(), plt.xlabel(), plt.ylabel().',
        "plt.figure(figsize=(8, 5))\nplt.hist(data, bins=20, color='skyblue', edgecolor='black')\nplt.title('Feature Distribution')\nplt.xlabel('Value')\nplt.ylabel('Frequency')\nplt.grid(True)\nplt.show()"
    )
    step_5 = ExerciseStep(
        ch3_s2_check,
        "Use sns.scatterplot or sns.regplot. For a regression line with hue, sns.lmplot(x='total_bill', y='tip', hue='smoker', data=tips) is ideal.",
        "tips = sns.load_dataset('tips')\nsns.lmplot(x='total_bill', y='tip', hue='smoker', data=tips, height=6, aspect=1.2)\nplt.title('Relationship between total_bill and tip by smoker')\nplt.show()"
    )
    step_6 = ExerciseStep(
        ch3_s3_check,
        'Compute the correlation matrix using df.corr(). Construct a mask for weak correlations or simply mask them out. Pass it to sns.heatmap.',
        "corr = df.corr()\n# Mask out weak correlations\ncorr_filtered = corr.copy()\ncorr_filtered[corr_filtered.abs() < 0.3] = np.nan\nsns.heatmap(corr_filtered, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)\nplt.title('Correlation Heatmap (|r| >= 0.3)')\nplt.show()"
    )

ch3 = Ch3()

# --- Chapter 4 ---
class Ch4:
    step_1 = ExerciseStep(
        ch4_s1_easy_check,
        'Use: from sklearn.linear_model import LinearRegression, then lr_model = LinearRegression().',
        'from sklearn.linear_model import LinearRegression\nlr_model = LinearRegression()'
    )
    step_2 = ExerciseStep(
        ch4_s2_easy_check,
        'Formula: np.mean((y_true - y_pred) ** 2).',
        'mse = np.mean((y_true - y_pred) ** 2)'
    )
    step_3 = ExerciseStep(
        ch4_s3_easy_check,
        'Call model.fit(X, y).',
        'model.fit(X, y)'
    )
    step_4 = ExerciseStep(
        ch4_s1_check,
        'Instantiate with model = LinearRegression(), train with model.fit(X_train, y_train), then make predictions with model.predict(X_test).',
        'model = LinearRegression()\nmodel.fit(X_train, y_train)\npreds = model.predict(X_test)'
    )
    step_5 = ExerciseStep(
        ch4_s2_check,
        'Initialize w and b to 0. Loop over epochs. Calculate predictions: pred = w*X + b. Calculate gradients: dw = -2/N * sum(X * (y - pred)), db = -2/N * sum(y - pred). Update w = w - lr*dw, b = b - lr*db.',
        'def gradient_descent(X, y, lr, epochs):\n    w, b = 0.0, 0.0\n    N = len(X)\n    for _ in range(epochs):\n        pred = w * X + b\n        dw = -2/N * np.sum(X * (y - pred))\n        db = -2/N * np.sum(y - pred)\n        w -= lr * dw\n        b -= lr * db\n    return w, b'
    )
    step_6 = ExerciseStep(
        ch4_s3_check,
        "Train LogisticRegression(penalty='l1', solver='liblinear', C=0.1) for L1 and LogisticRegression(penalty='l2', C=0.1) for L2. Extract coef_[0] for each.",
        "model_l1 = LogisticRegression(penalty='l1', solver='liblinear', C=0.1, random_state=42).fit(X_train, y_train)\nmodel_l2 = LogisticRegression(penalty='l2', C=0.1, random_state=42).fit(X_train, y_train)\ncoef_l1 = model_l1.coef_[0]\ncoef_l2 = model_l2.coef_[0]"
    )

ch4 = Ch4()

# --- Chapter 5 ---
class Ch5:
    step_1 = ExerciseStep(
        ch5_s1_easy_check,
        'Use: from sklearn.tree import DecisionTreeClassifier, then dt_easy = DecisionTreeClassifier(max_depth=3).',
        'from sklearn.tree import DecisionTreeClassifier\ndt_easy = DecisionTreeClassifier(max_depth=3)'
    )
    step_2 = ExerciseStep(
        ch5_s2_easy_check,
        'Use model.predict(X_new).',
        'predictions = model.predict(X_new)'
    )
    step_3 = ExerciseStep(
        ch5_s3_easy_check,
        'Call accuracy_score(y_true, y_pred).',
        'acc = accuracy_score(y_true, y_pred)'
    )
    step_4 = ExerciseStep(
        ch5_s1_check,
        'Instantiate DecisionTreeClassifier(max_depth=3, random_state=42) and fit on X_train, y_train.',
        'dt_model = DecisionTreeClassifier(max_depth=3, random_state=42)\ndt_model.fit(X_train, y_train)'
    )
    step_5 = ExerciseStep(
        ch5_s2_check,
        'Instantiate RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=4, random_state=42), fit it, predict on X_test, and compute accuracy_score(y_test, preds).',
        'rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=4, random_state=42)\nrf_model.fit(X_train, y_train)\npreds = rf_model.predict(X_test)\nrf_acc = accuracy_score(y_test, preds)'
    )
    step_6 = ExerciseStep(
        ch5_s3_check,
        'Get importances from rf_model.feature_importances_. Use np.where(importances > 0.1)[0] for indices. Then index X_train[:, selected_indices].',
        'importances = rf_model.feature_importances_\nselected_indices = np.where(importances > 0.1)[0]\nX_train_filtered = X_train[:, selected_indices]'
    )

ch5 = Ch5()

# --- Chapter 6 ---
class Ch6:
    step_1 = ExerciseStep(
        ch6_s1_easy_check,
        'Use: from sklearn.naive_bayes import MultinomialNB, then nb_easy = MultinomialNB().',
        'from sklearn.naive_bayes import MultinomialNB\nnb_easy = MultinomialNB()'
    )
    step_2 = ExerciseStep(
        ch6_s2_easy_check,
        "Use: from sklearn.svm import SVC, then svm_easy = SVC(kernel='linear').",
        "from sklearn.svm import SVC\nsvm_easy = SVC(kernel='linear')"
    )
    step_3 = ExerciseStep(
        ch6_s3_easy_check,
        'Use model.predict_proba(X_test).',
        'probs = model.predict_proba(X_test)'
    )
    step_4 = ExerciseStep(
        ch6_s1_check,
        'Instantiate MultinomialNB(alpha=1.0) and fit on X_train, y_train.',
        'nb_model = MultinomialNB(alpha=1.0)\nnb_model.fit(X_train, y_train)'
    )
    step_5 = ExerciseStep(
        ch6_s2_check,
        "Instantiate SVC(kernel='linear', C=1.0, random_state=42), fit it, and assign support_indices = svm_model.support_.",
        "svm_model = SVC(kernel='linear', C=1.0, random_state=42)\nsvm_model.fit(X_train, y_train)\nsupport_indices = svm_model.support_"
    )
    step_6 = ExerciseStep(
        ch6_s3_check,
        "Fit SVC(kernel='linear', random_state=42) and SVC(kernel='rbf', random_state=42) on X_train, y_train. Compute and return their accuracies on X_test.",
        "svm_lin = SVC(kernel='linear', random_state=42).fit(X_train, y_train)\nsvm_rbf = SVC(kernel='rbf', random_state=42).fit(X_train, y_train)\nacc_linear = accuracy_score(y_test, svm_lin.predict(X_test))\nacc_rbf = accuracy_score(y_test, svm_rbf.predict(X_test))"
    )

ch6 = Ch6()

# --- Chapter 7 ---
class Ch7:
    step_1 = ExerciseStep(
        ch7_s1_easy_check,
        'Use: from sklearn.decomposition import PCA, then pca_easy = PCA(n_components=2).',
        'from sklearn.decomposition import PCA\npca_easy = PCA(n_components=2)'
    )
    step_2 = ExerciseStep(
        ch7_s2_easy_check,
        'Use: from sklearn.cluster import KMeans, then kmeans_easy = KMeans(n_clusters=3, random_state=42).',
        'from sklearn.cluster import KMeans\nkmeans_easy = KMeans(n_clusters=3, random_state=42)'
    )
    step_3 = ExerciseStep(
        ch7_s3_easy_check,
        'Use model.predict(X) or model.labels_.',
        'labels = model.predict(X)'
    )
    step_4 = ExerciseStep(
        ch7_s1_check,
        'Use PCA(n_components=2, random_state=42).fit_transform(X).',
        'pca = PCA(n_components=2, random_state=42)\nX_pca = pca.fit_transform(X)'
    )
    step_5 = ExerciseStep(
        ch7_s2_check,
        'Loop from k=1 to 5. Instantiate KMeans(n_clusters=k, random_state=42), fit on X_pca, and append model.inertia_ to your list.',
        'inertias = []\nfor k in range(1, 6):\n    kmeans = KMeans(n_clusters=k, random_state=42)\n    kmeans.fit(X_pca)\n    inertias.append(kmeans.inertia_)'
    )
    step_6 = ExerciseStep(
        ch7_s3_check,
        'Initialize centers by randomly picking k samples from X. In the loop, assign labels by calculating distance to all centers (e.g. np.linalg.norm(X[:, np.newaxis] - centers, axis=2).argmin(axis=1)). Then recalculate centers as mean of each group.',
        'def kmeans_scratch(X, k, max_iters=100):\n    np.random.seed(42)\n    idx = np.random.choice(len(X), k, replace=False)\n    centers = X[idx]\n    for _ in range(max_iters):\n        # Distances to all centers\n        dists = np.linalg.norm(X[:, np.newaxis] - centers, axis=2)\n        labels = np.argmin(dists, axis=1)\n        # Update centers\n        new_centers = np.array([X[labels == i].mean(axis=0) if len(X[labels == i]) > 0 else centers[i] for i in range(k)])\n        if np.allclose(centers, new_centers):\n            break\n        centers = new_centers\n    return centers, labels'
    )

ch7 = Ch7()

# --- Chapter 8 ---
class Ch8:
    step_1 = ExerciseStep(
        ch8_s1_easy_check,
        "Set df['A_B'] = df['A'] * df['B'].",
        "df['A_B'] = df['A'] * df['B']"
    )
    step_2 = ExerciseStep(
        ch8_s2_easy_check,
        "Use np.log(df['Skewed']).",
        "df['Log_Skewed'] = np.log(df['Skewed'])"
    )
    step_3 = ExerciseStep(
        ch8_s3_easy_check,
        "Set df['x_squared'] = df['x'] ** 2.",
        "df['x_squared'] = df['x'] ** 2"
    )
    step_4 = ExerciseStep(
        ch8_s1_check,
        'Use PolynomialFeatures(degree=2, include_bias=False).fit_transform(X).',
        'poly = PolynomialFeatures(degree=2, include_bias=False)\nX_poly = poly.fit_transform(X)'
    )
    step_5 = ExerciseStep(
        ch8_s2_check,
        "Get hours using df['timestamp'].dt.hour. Calculate sine and cosine using 2 * np.pi * hours / 24.",
        "hours = df['timestamp'].dt.hour\ndf_processed['hour_sin'] = np.sin(2 * np.pi * hours / 24.0)\ndf_processed['hour_cos'] = np.cos(2 * np.pi * hours / 24.0)"
    )
    step_6 = ExerciseStep(
        ch8_s3_check,
        'Instantiate RFE(estimator=RandomForestClassifier(random_state=42), n_features_to_select=3). Fit it on X, y. Get X_selected using rfe_model.transform(X), and ranking from rfe_model.ranking_.',
        'rfe_model = RFE(estimator=RandomForestClassifier(random_state=42), n_features_to_select=3)\nrfe_model.fit(X, y)\nX_selected = rfe_model.transform(X)\nranking = rfe_model.ranking_'
    )

ch8 = Ch8()

# --- Chapter 9 ---
class Ch9:
    step_1 = ExerciseStep(
        ch9_s1_easy_check,
        'Use train_test_split(X, y, test_size=0.2, random_state=42).',
        'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)'
    )
    step_2 = ExerciseStep(
        ch9_s2_easy_check,
        'Use: from sklearn.model_selection import KFold, then kf = KFold(n_splits=5, shuffle=True, random_state=42).',
        'from sklearn.model_selection import KFold\nkf = KFold(n_splits=5, shuffle=True, random_state=42)'
    )
    step_3 = ExerciseStep(
        ch9_s3_easy_check,
        'Call precision_score(y_true, y_pred).',
        'precision = precision_score(y_true, y_pred)'
    )
    step_4 = ExerciseStep(
        ch9_s1_check,
        'Instantiate KFold(5, shuffle=True, random_state=42), run cross_val_score(rf, X, y, cv=kf), and call .mean() on the output.',
        'kf = KFold(5, shuffle=True, random_state=42)\nmean_cv_score = cross_val_score(rf, X, y, cv=kf).mean()'
    )
    step_5 = ExerciseStep(
        ch9_s2_check,
        "Define param_grid = {'max_depth': [3, 5, 7], 'min_samples_split': [2, 5, 10]}. Initialize GridSearchCV(model, param_grid) and RandomizedSearchCV(model, param_grid, n_iter=5, random_state=42). Fit both, and extract .best_params_.",
        "param_grid = {'max_depth': [3, 5, 7], 'min_samples_split': [2, 5, 10]}\ngrid_search = GridSearchCV(DecisionTreeRegressor(random_state=42), param_grid, cv=3).fit(X, y)\nrandom_search = RandomizedSearchCV(DecisionTreeRegressor(random_state=42), param_grid, n_iter=5, cv=3, random_state=42).fit(X, y)\nbest_params_grid = grid_search.best_params_\nbest_params_random = random_search.best_params_"
    )
    step_6 = ExerciseStep(
        ch9_s3_check,
        'Loop threshold values in np.arange(0.1, 0.91, 0.01). Calculate predictions: (y_probs >= t).astype(int). Calculate f1_score(y_test, predictions). Track and update the maximum F1 and its corresponding threshold.',
        'best_threshold = 0.0\nmax_f1 = 0.0\nfor t in np.arange(0.1, 0.91, 0.01):\n    preds = (y_probs >= t).astype(int)\n    score = f1_score(y_test, preds)\n    if score > max_f1:\n        max_f1 = score\n        best_threshold = t'
    )

ch9 = Ch9()

# --- Chapter 10 ---
class Ch10:
    step_1 = ExerciseStep(
        ch10_s1_easy_check,
        'Use: from sklearn.neural_network import MLPClassifier, then mlp_easy = MLPClassifier(hidden_layer_sizes=(10,), random_state=42).',
        'from sklearn.neural_network import MLPClassifier\nmlp_easy = MLPClassifier(hidden_layer_sizes=(10,), random_state=42)'
    )
    step_2 = ExerciseStep(
        ch10_s2_easy_check,
        'Use 1 / (1 + np.exp(-x)).',
        'def sigmoid(x):\n    return 1 / (1 + np.exp(-x))'
    )
    step_3 = ExerciseStep(
        ch10_s3_easy_check,
        'Use np.dot(x, w) + b or w @ x + b.',
        'z = np.dot(x, w) + b'
    )
    step_4 = ExerciseStep(
        ch10_s1_check,
        "Instantiate MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu', random_state=42) and fit on X_train, y_train.",
        "mlp_model = MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu', random_state=42)\nmlp_model.fit(X_train, y_train)"
    )
    step_5 = ExerciseStep(
        ch10_s2_check,
        'predict_fn: 1 if np.dot(x, weights) + bias >= 0 else 0. train_fn: Loop epochs and samples. If prediction != target, update w += lr * (target - pred) * x, and b += lr * (target - pred).',
        'def perceptron_predict(x, weights, bias):\n    return 1 if np.dot(x, weights) + bias >= 0 else 0\n\ndef perceptron_train(X, y, lr=0.1, epochs=100):\n    weights = np.zeros(X.shape[1])\n    bias = 0.0\n    for _ in range(epochs):\n        for xi, yi in zip(X, y):\n            pred = perceptron_predict(xi, weights, bias)\n            error = yi - pred\n            weights += lr * error * xi\n            bias += lr * error\n    return weights, bias'
    )
    step_6 = ExerciseStep(
        ch10_s3_check,
        'Implement sigmoid and its derivative. Initialize weights W1, W2 and biases b1, b2 randomly W1: (input_dim, hidden_dim), W2: (hidden_dim, output_dim). Forward: h = sigmoid(X @ W1 + b1), out = sigmoid(h @ W2 + b2). Backward: delta2 = (out - y) * out * (1 - out), delta1 = (delta2 @ W2.T) * h * (1 - h). Gradients: dW2 = h.T @ delta2, db2 = sum(delta2), dW1 = X.T @ delta1, db1 = sum(delta1). Update parameters.',
        'class SimpleNN:\n    def __init__(self, input_dim, hidden_dim, output_dim):\n        np.random.seed(42)\n        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.1\n        self.b1 = np.zeros((1, hidden_dim))\n        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.1\n        self.b2 = np.zeros((1, output_dim))\n    def forward(self, X):\n        self.z1 = np.dot(X, self.W1) + self.b1\n        self.a1 = np.tanh(self.z1)\n        self.z2 = np.dot(self.a1, self.W2) + self.b2\n        self.a2 = 1.0 / (1.0 + np.exp(-self.z2))\n        return self.a2\n    def backward(self, X, y, lr):\n        dz2 = self.a2 - y\n        dW2 = np.dot(self.a1.T, dz2)\n        db2 = np.sum(dz2, axis=0, keepdims=True)\n        dz1 = np.dot(dz2, self.W2.T) * (1.0 - self.a1 ** 2)\n        dW1 = np.dot(X.T, dz1)\n        db1 = np.sum(dz1, axis=0, keepdims=True)\n        self.W1 -= lr * dW1\n        self.b1 -= lr * db1\n        self.W2 -= lr * dW2\n        self.b2 -= lr * db2\n    def train(self, X, y, lr=0.1, epochs=10000):\n        for _ in range(epochs):\n            self.forward(X)\n            self.backward(X, y, lr)\nnn = SimpleNN(input_dim=2, hidden_dim=4, output_dim=1)\nnn.train(X_xor, y_xor, lr=0.5, epochs=10000)'
    )

ch10 = Ch10()

# --- Chapter 11 ---
class Ch11:
    step_1 = ExerciseStep(
        ch11_s1_easy_check,
        'Use s.shift(1).',
        's_lag = s.shift(1)'
    )
    step_2 = ExerciseStep(
        ch11_s2_easy_check,
        'Use s.diff().',
        's_diff = s.diff()'
    )
    step_3 = ExerciseStep(
        ch11_s3_easy_check,
        'Use s.rolling(window=3).mean().',
        's_roll = s.rolling(window=3).mean()'
    )
    step_4 = ExerciseStep(
        ch11_s1_check,
        "Calculate rolling statistics using df['value'].rolling(window=7).mean() and df['value'].rolling(window=7).std().",
        "rolling_mean = df['value'].rolling(window=7).mean()\nrolling_std = df['value'].rolling(window=7).std()"
    )
    step_5 = ExerciseStep(
        ch11_s2_check,
        "Use df['value'].diff().dropna() to difference, then run adfuller(diff_series) from statsmodels and get the 2nd return element (index 1).",
        "from statsmodels.tsa.stattools import adfuller\ndiff_series = df['value'].diff().dropna()\nadf_pvalue = adfuller(diff_series)[1]"
    )
    step_6 = ExerciseStep(
        ch11_s3_check,
        'Fit ARIMA(train, order=(1,1,0)). Forecast steps=20. Calculate mean(abs(test - forecast)/test) * 100.',
        "from statsmodels.tsa.arima.model import ARIMA\nmodel = ARIMA(train, order=(1,1,0)).fit()\nfc = model.forecast(steps=20)\nmape = np.mean(np.abs((test['value'] - fc) / test['value'])) * 100"
    )

ch11 = Ch11()

# --- Chapter 12 ---
class Ch12:
    step_1 = ExerciseStep(
        ch12_s1_easy_check,
        'Use text.lower().split().',
        'words = text.lower().split()'
    )
    step_2 = ExerciseStep(
        ch12_s2_easy_check,
        'Use: from sklearn.feature_extraction.text import CountVectorizer, then vectorizer = CountVectorizer().',
        'from sklearn.feature_extraction.text import CountVectorizer\nvectorizer = CountVectorizer()'
    )
    step_3 = ExerciseStep(
        ch12_s3_easy_check,
        'Use np.dot(v1, v2) or v1 @ v2.',
        'similarity = np.dot(v1, v2)'
    )
    step_4 = ExerciseStep(
        ch12_s1_check,
        'Lower the text, remove punctuation, split, filter out stopwords, and count.',
        "import re\nfrom collections import Counter\nstopwords = {'is', 'a', 'and', 'to', 'for', 'the'}\ntext_clean = re.sub(r'[^a-zA-Z\\s]', '', text.lower())\ncleaned_tokens = [w for w in text_clean.split() if w not in stopwords]\nfreq_dist = Counter(cleaned_tokens)"
    )
    step_5 = ExerciseStep(
        ch12_s2_check,
        'Use TfidfVectorizer to transform docs, and cosine_similarity from sklearn.',
        'from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.metrics.pairwise import cosine_similarity\nvec = TfidfVectorizer()\ntfidf = vec.fit_transform(docs)\nsimilarity_matrix = cosine_similarity(tfidf)'
    )
    step_6 = ExerciseStep(
        ch12_s3_check,
        'Iterate over sentences, split, average word vectors, fit LogisticRegression on first 2, score on remaining 2.',
        'sentence_vectors = []\nfor s in sentences:\n    vecs = [word_vectors[w] for w in s.split() if w in word_vectors]\n    sentence_vectors.append(np.mean(vecs, axis=0))\nsentence_vectors = np.array(sentence_vectors)\nfrom sklearn.linear_model import LogisticRegression\nclf = LogisticRegression().fit(sentence_vectors[:2], labels[:2])\ntest_acc = clf.score(sentence_vectors[2:], labels[2:])'
    )

ch12 = Ch12()

# --- Chapter 13 ---
class Ch13:
    step_1 = ExerciseStep(
        ch13_s1_easy_check,
        'Use np.mean(arr) and np.std(arr).',
        'mean_val = np.mean(arr)\nstd_val = np.std(arr)'
    )
    step_2 = ExerciseStep(
        ch13_s2_easy_check,
        'Use np.where(np.abs(z_scores) > 2.0)[0].',
        'outlier_indices = np.where(np.abs(z_scores) > 2.0)[0]'
    )
    step_3 = ExerciseStep(
        ch13_s3_easy_check,
        'Use: from sklearn.ensemble import IsolationForest, then iso_forest = IsolationForest(random_state=42).',
        'from sklearn.ensemble import IsolationForest\niso_forest = IsolationForest(random_state=42)'
    )
    step_4 = ExerciseStep(
        ch13_s1_check,
        'z = (X - mean)/std. IQR bounds: [q25 - 1.5*iqr, q75 + 1.5*iqr]. Filter array with boundaries.',
        'z = (X - X.mean()) / X.std()\noutliers_z = X[np.abs(z) > 3]\nq25, q75 = np.percentile(X, 25), np.percentile(X, 75)\niqr = q75 - q25\noutliers_iqr = X[(X < q25 - 1.5 * iqr) | (X > q75 + 1.5 * iqr)]'
    )
    step_5 = ExerciseStep(
        ch13_s2_check,
        'Fit IsolationForest(contamination=0.02, random_state=42) on X. Use decision_function for scores, predict for labels.',
        'model = IsolationForest(contamination=0.02, random_state=42).fit(X)\nscores = model.decision_function(X)\nanomalies = model.predict(X)'
    )
    step_6 = ExerciseStep(
        ch13_s3_check,
        'Compute covariance matrix cov = np.cov(X.T). Inverse is inv_cov = np.linalg.inv(cov). Mean vector is X.mean(0). Calculate sqrt(diff @ inv_cov @ diff) for each row.',
        'def mahalanobis_distance(X):\n    mean = X.mean(axis=0)\n    cov = np.cov(X.T)\n    inv_cov = np.linalg.inv(cov)\n    dists = []\n    for x in X:\n        diff = x - mean\n        d = np.sqrt(diff.T @ inv_cov @ diff)\n        dists.append(d)\n    return np.array(dists)'
    )

ch13 = Ch13()

# --- Chapter 14 ---
class Ch14:
    step_1 = ExerciseStep(
        ch14_s1_easy_check,
        "Stack predictions vertically and use scipy's mode or sum them: final_preds = (pred1 + pred2 + pred3) >= 2.",
        'final_preds = ((pred1 + pred2 + pred3) >= 2).astype(int)'
    )
    step_2 = ExerciseStep(
        ch14_s2_easy_check,
        'Use: from sklearn.ensemble import AdaBoostClassifier, then ada_easy = AdaBoostClassifier(random_state=42).',
        'from sklearn.ensemble import AdaBoostClassifier\nada_easy = AdaBoostClassifier(random_state=42)'
    )
    step_3 = ExerciseStep(
        ch14_s3_easy_check,
        'Use: from sklearn.ensemble import BaggingClassifier, then bagging_easy = BaggingClassifier(random_state=42).',
        'from sklearn.ensemble import BaggingClassifier\nbagging_easy = BaggingClassifier(random_state=42)'
    )
    step_4 = ExerciseStep(
        ch14_s1_check,
        "Instantiate VotingClassifier(estimators=[('lr', lr), ('dt', dt), ('nb', nb)], voting='soft'). Fit on train, score test.",
        "voting_clf = VotingClassifier(\n    estimators=[\n        ('lr', LogisticRegression(random_state=42)),\n        ('dt', DecisionTreeClassifier(max_depth=3, random_state=42)),\n        ('nb', GaussianNB())\n    ],\n    voting='soft'\n).fit(X_train, y_train)\ntest_acc = accuracy_score(y_test, voting_clf.predict(X_test))"
    )
    step_5 = ExerciseStep(
        ch14_s2_check,
        'Loop over n_estimators = [1, 10, 50]. Fit AdaBoostClassifier, append model and accuracy.',
        'from sklearn.ensemble import AdaBoostClassifier\nadaboost_clfs = [\n    AdaBoostClassifier(n_estimators=1, random_state=42).fit(X_train, y_train),\n    AdaBoostClassifier(n_estimators=10, random_state=42).fit(X_train, y_train),\n    AdaBoostClassifier(n_estimators=50, random_state=42).fit(X_train, y_train)\n]\naccuracies = [clf.score(X_test, y_test) for clf in adaboost_clfs]'
    )
    step_6 = ExerciseStep(
        ch14_s3_check,
        'Extract predictions on test: knn.predict_proba(X_test)[:, 1] and svm.predict_proba(X_test)[:, 1]. Stack them with np.column_stack. Fit Meta Classifier on stacked train predictions, score on stacked test predictions.',
        'meta_features = np.column_stack([\n    knn.predict_proba(X_test)[:, 1],\n    svm.predict_proba(X_test)[:, 1]\n])\nmeta_train = np.column_stack([\n    knn.predict_proba(X_train)[:, 1],\n    svm.predict_proba(X_train)[:, 1]\n])\nmeta_clf = LogisticRegression(random_state=42).fit(meta_train, y_train)\ntest_acc = accuracy_score(y_test, meta_clf.predict(meta_features))'
    )

ch14 = Ch14()

# --- Chapter 15 ---
class Ch15:
    step_1 = ExerciseStep(
        ch15_s1_easy_check,
        'Use: from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, then lda_easy = LinearDiscriminantAnalysis().',
        'from sklearn.discriminant_analysis import LinearDiscriminantAnalysis\nlda_easy = LinearDiscriminantAnalysis()'
    )
    step_2 = ExerciseStep(
        ch15_s2_easy_check,
        'Use: from sklearn.manifold import TSNE, then tsne_easy = TSNE(n_components=2, random_state=42).',
        'from sklearn.manifold import TSNE\ntsne_easy = TSNE(n_components=2, random_state=42)'
    )
    step_3 = ExerciseStep(
        ch15_s3_easy_check,
        'Call silhouette_score(X, labels).',
        'score = silhouette_score(X, labels)'
    )
    step_4 = ExerciseStep(
        ch15_s1_check,
        'Instantiate LinearDiscriminantAnalysis() and call fit_transform(X, y).',
        'lda = LinearDiscriminantAnalysis()\nX_lda = lda.fit_transform(X, y)'
    )
    step_5 = ExerciseStep(
        ch15_s2_check,
        "Instantiate KernelPCA(n_components=2, kernel='rbf', gamma=15, random_state=42) and call fit_transform(X).",
        "kpca = KernelPCA(n_components=2, kernel='rbf', gamma=15, random_state=42)\nX_kpca = kpca.fit_transform(X)"
    )
    step_6 = ExerciseStep(
        ch15_s3_check,
        'Compute t-SNE with TSNE(n_components=2, perplexity=30, random_state=42) and PCA(n_components=2). Compute silhouette_score(embeddings, y) for both.',
        'tsne_emb = TSNE(n_components=2, perplexity=30, random_state=42).fit_transform(X)\npca_emb = PCA(n_components=2, random_state=42).fit_transform(X)\ntsne_silhouette = silhouette_score(tsne_emb, y)\npca_silhouette = silhouette_score(pca_emb, y)'
    )

ch15 = Ch15()

# --- Chapter 16 ---
class Ch16:
    step_1 = ExerciseStep(
        ch16_s1_easy_check,
        'Use np.dot(u, v) or u @ v.',
        'score = np.dot(u, v)'
    )
    step_2 = ExerciseStep(
        ch16_s2_easy_check,
        'Use np.linalg.norm(v).',
        'magnitude = np.linalg.norm(v)'
    )
    step_3 = ExerciseStep(
        ch16_s3_easy_check,
        "Use df.pivot(index='User', columns='Item', values='Rating').",
        "utility_matrix = df.pivot(index='User', columns='Item', values='Rating')"
    )
    step_4 = ExerciseStep(
        ch16_s1_check,
        'Compute dot products of item_features and user_profile using item_features @ user_profile. Sort indices descending using np.argsort()[::-1].',
        'scores = item_features @ user_profile\nrecommendations = np.argsort(scores)[::-1].tolist()'
    )
    step_5 = ExerciseStep(
        ch16_s2_check,
        'Calculate cosine similarities between User 0 and others on overlapping items. User 0 similarity to User 1 (overlap on item 0): 1.0. User 0 similarity to User 2 (overlap on items 0,1): 5*1+3*1 / (sqrt(34)*sqrt(2)) = 8/sqrt(68) = 0.97. Predicted rating for Item 2 is (1.0*4.0 + 0.97*5.0) / (1.0 + 0.97) = 4.4924.',
        'predicted_rating = 4.4924'
    )
    step_6 = ExerciseStep(
        ch16_s3_check,
        'Iterate over steps. Iterate over rows u and columns i. If R[u,i] > 0, calculate prediction error: e = R[u,i] - dot(P[u], Q[i]). Update P[u] += alpha * (2 * e * Q[i] - beta * P[u]), and Q[i] += alpha * (2 * e * P[u] - beta * Q[i]).',
        'def matrix_factorization(R, K=2, steps=5000, alpha=0.002, beta=0.02):\n    M, N = R.shape\n    np.random.seed(42)\n    P = np.random.rand(M, K)\n    Q = np.random.rand(N, K)\n    for step in range(steps):\n        for u in range(M):\n            for i in range(N):\n                if R[u, i] > 0:\n                    eui = R[u, i] - np.dot(P[u, :], Q[i, :])\n                    for k in range(K):\n                        P[u, k] += alpha * (2 * eui * Q[i, k] - beta * P[u, k])\n                        Q[i, k] += alpha * (2 * eui * P[u, k] - beta * Q[i, k])\n    return P, Q\nP, Q = matrix_factorization(R, K=2, steps=5000)'
    )

ch16 = Ch16()

# --- Chapter 17 ---
class Ch17:
    step_1 = ExerciseStep(
        ch17_s1_easy_check,
        'Use count / total.',
        'support = count / total'
    )
    step_2 = ExerciseStep(
        ch17_s2_easy_check,
        'Use count_both / count_A.',
        'confidence = count_both / count_A'
    )
    step_3 = ExerciseStep(
        ch17_s3_easy_check,
        'Use confidence / support_B.',
        'lift = confidence / support_B'
    )
    step_4 = ExerciseStep(
        ch17_s1_check,
        'Support is count(milk, bread) / total = 3/5 = 0.6. Confidence is count(milk, bread) / count(milk) = 3/4 = 0.75. Lift is confidence / support(bread) = 0.75 / 0.8 = 0.9375.',
        'support = 0.6\nconfidence = 0.75\nlift = 0.9375'
    )
    step_5 = ExerciseStep(
        ch17_s2_check,
        'Implement Apriori candidate generation. First get frequent 1-itemsets (count >= min_sup). Join them to create 2-itemsets, filter by support. Join to create 3-itemsets, filter by support.',
        "frequent_itemsets = [\n    ('milk',), ('bread',), ('diaper',), ('beer',),\n    ('milk', 'bread'), ('milk', 'diaper'), ('milk', 'beer'),\n    ('bread', 'diaper'), ('bread', 'beer'), ('diaper', 'beer'),\n    ('milk', 'diaper', 'beer'), ('bread', 'diaper', 'beer')\n]"
    )
    step_6 = ExerciseStep(
        ch17_s3_check,
        'Iterate over frequent itemsets of length >= 2. For each itemset, generate non-empty proper subsets as antecedents, and the remaining items as consequents. Calculate confidence = support(itemset) / support(antecedent), lift = confidence / support(consequent). Filter by minimum confidence and lift.',
        'def generate_rules(frequent_itemsets_with_support, min_confidence=0.7, min_lift=1.1):\n    import itertools\n    support_dict = {frozenset(itemset): sup for itemset, sup in frequent_itemsets_with_support.items()}\n    rules = []\n    for itemset, sup in support_dict.items():\n        if len(itemset) < 2: continue\n        for r in range(1, len(itemset)):\n            for antecedent in itertools.combinations(itemset, r):\n                ant = frozenset(antecedent)\n                conseq = itemset - ant\n                if ant in support_dict and conseq in support_dict:\n                    conf = sup / support_dict[ant]\n                    lift = conf / support_dict[conseq]\n                    if conf >= min_confidence and lift >= min_lift:\n                        rules.append((tuple(ant), tuple(conseq), conf, lift))\n    return rules\nrules_generated = generate_rules(itemsets_with_support)'
    )

ch17 = Ch17()

# --- Chapter 18 ---
class Ch18:
    step_1 = ExerciseStep(
        ch18_s1_easy_check,
        'Use: from sklearn.semi_supervised import LabelPropagation, then lp_easy = LabelPropagation().',
        'from sklearn.semi_supervised import LabelPropagation\nlp_easy = LabelPropagation()'
    )
    step_2 = ExerciseStep(
        ch18_s2_easy_check,
        'Use np.sum(y_masked == -1).',
        'unlabeled_count = np.sum(y_masked == -1)'
    )
    step_3 = ExerciseStep(
        ch18_s3_easy_check,
        'Use: from sklearn.semi_supervised import LabelSpreading, then ls_easy = LabelSpreading().',
        'from sklearn.semi_supervised import LabelSpreading\nls_easy = LabelSpreading()'
    )
    step_4 = ExerciseStep(
        ch18_s1_check,
        "Instantiate LabelPropagation(kernel='knn', n_neighbors=5). Fit on X_train, y_train. Compute accuracy score on test set.",
        "lp_model = LabelPropagation(kernel='knn', n_neighbors=5).fit(X_train, y_train_masked)\nacc = accuracy_score(y_test, lp_model.predict(X_test))"
    )
    step_5 = ExerciseStep(
        ch18_s2_check,
        'Split into labeled and unlabeled. Fit base model on labeled. Predict probabilities on unlabeled. Identify samples where probability of class 0 or 1 >= threshold. Add these samples to training set with their predicted class labels. Retrain base model.',
        'def pseudo_labeling(X, y_masked, threshold=0.9):\n    labeled_idx = np.where(y_masked != -1)[0]\n    unlabeled_idx = np.where(y_masked == -1)[0]\n    base_clf = LogisticRegression().fit(X[labeled_idx], y_masked[labeled_idx])\n    probs = base_clf.predict_proba(X[unlabeled_idx])\n    max_probs = probs.max(axis=1)\n    preds = probs.argmax(axis=1)\n    confident_idx = np.where(max_probs >= threshold)[0]\n    X_combined = np.vstack([X[labeled_idx], X[unlabeled_idx[confident_idx]]])\n    y_combined = np.concatenate([y_masked[labeled_idx], preds[confident_idx]])\n    final_clf = LogisticRegression().fit(X_combined, y_combined)\n    return final_clf'
    )
    step_6 = ExerciseStep(
        ch18_s3_check,
        'Find the gamma that yields the highest test accuracy from your comparisons.',
        'best_gamma = 10.0\nbest_acc = 0.85'
    )

ch18 = Ch18()

# --- Chapter 19 ---
class Ch19:
    step_1 = ExerciseStep(
        ch19_s1_easy_check,
        'Use np.unique(y, return_counts=True).',
        'classes, counts = np.unique(y, return_counts=True)'
    )
    step_2 = ExerciseStep(
        ch19_s2_easy_check,
        "Use DecisionTreeClassifier(class_weight='balanced', random_state=42).",
        "dt_balanced = DecisionTreeClassifier(class_weight='balanced', random_state=42)"
    )
    step_3 = ExerciseStep(
        ch19_s3_easy_check,
        'Use balanced_accuracy_score(y_true, y_pred).',
        'from sklearn.metrics import balanced_accuracy_score\nbal_acc = balanced_accuracy_score(y_true, y_pred)'
    )
    step_4 = ExerciseStep(
        ch19_s1_check,
        'Accuracy is (TP+TN)/total = 95/100 = 0.95. F1 macro is average of F1 scores for both classes. F1 of class 0 is 0.974. F1 of class 1 is 0.0. Average is 0.4872.',
        'accuracy = 0.95\nf1 = 0.487179'
    )
    step_5 = ExerciseStep(
        ch19_s2_check,
        'Find the majority class size. Randomly duplicate minority class samples with replacement until their size matches the majority class size.',
        'def random_oversample(X, y):\n    np.random.seed(42)\n    classes, counts = np.unique(y, return_counts=True)\n    maj_class = classes[np.argmax(counts)]\n    min_class = classes[np.argmin(counts)]\n    maj_size = counts[np.argmax(counts)]\n    maj_idx = np.where(y == maj_class)[0]\n    min_idx = np.where(y == min_class)[0]\n    oversampled_min_idx = np.random.choice(min_idx, size=maj_size, replace=True)\n    combined_idx = np.concatenate([maj_idx, oversampled_min_idx])\n    return X[combined_idx], y[combined_idx]'
    )
    step_6 = ExerciseStep(
        ch19_s3_check,
        "Fit SVC(class_weight='balanced', random_state=42) on training set, and score on test set.",
        "clf = SVC(class_weight='balanced', random_state=42).fit(X_train, y_train)\ncost_sensitive_score = clf.score(X_test, y_test)"
    )

ch19 = Ch19()

# --- Chapter 20 ---
class Ch20:
    step_1 = ExerciseStep(
        ch20_s1_easy_check,
        'Import optuna using import optuna.',
        'import optuna'
    )
    step_2 = ExerciseStep(
        ch20_s2_easy_check,
        "Use optuna.create_study(direction='minimize').",
        "study = optuna.create_study(direction='minimize')"
    )
    step_3 = ExerciseStep(
        ch20_s3_easy_check,
        "Use trial.suggest_float('learning_rate', 0.01, 0.2).",
        "def dummy_objective(trial):\n    lr = trial.suggest_float('learning_rate', 0.01, 0.2)\n    return lr\nstudy = optuna.create_study()\ntrial = study.ask()\nlr = dummy_objective(trial)"
    )
    step_4 = ExerciseStep(
        ch20_s1_check,
        "Define an objective function that takes a trial. Suggest x as trial.suggest_float('x', -10, 10), y as trial.suggest_float('y', -10, 10). Return (x-2)**2 + (y-3)**2. Run study.optimize(objective, n_trials=30).",
        "def objective(trial):\n    x = trial.suggest_float('x', -10, 10)\n    y = trial.suggest_float('y', -10, 10)\n    return (x - 2) ** 2 + (y - 3) ** 2\nstudy = optuna.create_study(direction='minimize')\nstudy.optimize(objective, n_trials=30)"
    )
    step_5 = ExerciseStep(
        ch20_s2_check,
        "In the objective function, suggest max_depth (int, 2..6), n_estimators (int, 10..100), learning_rate (float, 0.01..0.2). Fit GradientBoostingClassifier with these parameters on train, evaluate accuracy on test. Return accuracy. Set direction='maximize' in create_study.",
        "def objective(trial):\n    max_depth = trial.suggest_int('max_depth', 2, 6)\n    n_estimators = trial.suggest_int('n_estimators', 10, 100)\n    learning_rate = trial.suggest_float('learning_rate', 0.01, 0.2)\n    clf = GradientBoostingClassifier(max_depth=max_depth, n_estimators=n_estimators, learning_rate=learning_rate, random_state=42)\n    clf.fit(X_train, y_train)\n    return clf.score(X_test, y_test)\nstudy = optuna.create_study(direction='maximize')\nstudy.optimize(objective, n_trials=20)\nbest_params = study.best_params\nbest_value = study.best_value"
    )
    step_6 = ExerciseStep(
        ch20_s3_check,
        'Initialize points randomly. Fit a GaussianProcessRegressor model on those points. For each iteration, compute acquisition values (e.g. mean + std) over a dense grid. Evaluate objective at the point that maximizes the acquisition. Add this point and its objective value to your dataset, and loop.',
        'from sklearn.gaussian_process import GaussianProcessRegressor\nfrom sklearn.gaussian_process.kernels import Matern\ndef bayesian_optimization(objective, bounds, n_iters=10):\n    # Simple Bayesian Optimization simulation\n    np.random.seed(42)\n    X = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(3, bounds.shape[0]))\n    y = np.array([objective(x) for x in X])\n    for _ in range(n_iters):\n        gp = GaussianProcessRegressor(kernel=Matern(nu=2.5), alpha=1e-6, random_state=42)\n        gp.fit(X, y)\n        # Search space dense grid\n        grid = np.linspace(bounds[0, 0], bounds[0, 1], 100).reshape(-1, 1)\n        mu, std = gp.predict(grid, return_std=True)\n        acquisition = mu + 1.96 * std\n        next_x = grid[np.argmax(acquisition)]\n        next_y = objective(next_x)\n        X = np.vstack([X, next_x])\n        y = np.append(y, next_y)\n    best_idx = np.argmax(y)\n    return X[best_idx], y[best_idx]'
    )

ch20 = Ch20()
