import numpy as np
import pandas as pd
import re

def check_code_history(pattern):
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None:
            history = ip.user_ns.get('_ih', [])
            for code in history:
                if re.search(pattern, code):
                    return True
    except Exception:
        pass
    return False

_plot_history = {
    'line_plots': [],
    'scatter_plots': [],
    'histograms': [],
    'lmplots': [],
    'heatmaps': [],
    'title_set': None,
    'xlabel_set': None,
    'ylabel_set': None,
}

try:
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes
    import seaborn as sns

    # Plot
    _orig_plt_plot = plt.plot
    def _custom_plt_plot(*args, **kwargs):
        _plot_history['line_plots'].append((args, kwargs))
        return _orig_plt_plot(*args, **kwargs)
    plt.plot = _custom_plt_plot

    _orig_axes_plot = Axes.plot
    def _custom_axes_plot(self, *args, **kwargs):
        _plot_history['line_plots'].append((args, kwargs))
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
        _plot_history['scatter_plots'].append((args, kwargs))
        return _orig_plt_scatter(*args, **kwargs)
    plt.scatter = _custom_plt_scatter

    _orig_axes_scatter = Axes.scatter
    def _custom_axes_scatter(self, *args, **kwargs):
        _plot_history['scatter_plots'].append((args, kwargs))
        return _orig_axes_scatter(self, *args, **kwargs)
    Axes.scatter = _custom_axes_scatter

    _orig_sns_scatterplot = sns.scatterplot
    def _custom_sns_scatterplot(*args, **kwargs):
        _plot_history['scatter_plots'].append((args, kwargs))
        return _orig_sns_scatterplot(*args, **kwargs)
    sns.scatterplot = _custom_sns_scatterplot

    # Histogram
    _orig_plt_hist = plt.hist
    def _custom_plt_hist(*args, **kwargs):
        _plot_history['histograms'].append((args, kwargs))
        return _orig_plt_hist(*args, **kwargs)
    plt.hist = _custom_plt_hist

    _orig_axes_hist = Axes.hist
    def _custom_axes_hist(self, *args, **kwargs):
        _plot_history['histograms'].append((args, kwargs))
        return _orig_axes_hist(self, *args, **kwargs)
    Axes.hist = _custom_axes_hist

    if hasattr(sns, 'histplot'):
        _orig_sns_histplot = sns.histplot
        def _custom_sns_histplot(*args, **kwargs):
            _plot_history['histograms'].append((args, kwargs))
            return _orig_sns_histplot(*args, **kwargs)
        sns.histplot = _custom_sns_histplot

    # lmplot
    _orig_sns_lmplot = sns.lmplot
    def _custom_sns_lmplot(*args, **kwargs):
        _plot_history['lmplots'].append((args, kwargs))
        return _orig_sns_lmplot(*args, **kwargs)
    sns.lmplot = _custom_sns_lmplot

    # heatmap
    _orig_sns_heatmap = sns.heatmap
    def _custom_sns_heatmap(*args, **kwargs):
        _plot_history['heatmaps'].append((args, kwargs))
        return _orig_sns_heatmap(*args, **kwargs)
    sns.heatmap = _custom_sns_heatmap
except Exception:
    pass

def check_plotted_data(plot_type, expected_x, expected_y=None):
    plots = _plot_history.get(plot_type, [])
    for args, kwargs in plots:
        # 1. Positional arguments
        if expected_y is not None:
            if len(args) >= 2:
                try:
                    if np.allclose(args[0], expected_x) and np.allclose(args[1], expected_y):
                        return True
                except Exception:
                    pass
        else:
            if len(args) >= 1:
                try:
                    if np.allclose(args[0], expected_x):
                        return True
                except Exception:
                    pass
        
        # 2. Keyword arguments
        x_val = kwargs.get('x', None)
        y_val = kwargs.get('y', None)
        if x_val is not None:
            if expected_y is not None:
                if y_val is not None:
                    try:
                        if np.allclose(x_val, expected_x) and np.allclose(y_val, expected_y):
                            return True
                    except Exception:
                        pass
            else:
                try:
                    if np.allclose(x_val, expected_x):
                        return True
                except Exception:
                    pass

        # 3. DataFrame kwargs: data=df, x='col1', y='col2'
        data = kwargs.get('data', None)
        x_col = kwargs.get('x', None)
        y_col = kwargs.get('y', None)
        if data is not None and isinstance(data, pd.DataFrame):
            if isinstance(x_col, str) and expected_y is not None and isinstance(y_col, str):
                try:
                    if x_col in data.columns and y_col in data.columns:
                        x_data = data[x_col].values
                        y_data = data[y_col].values
                        if np.allclose(x_data, expected_x) and np.allclose(y_data, expected_y):
                            return True
                except Exception:
                    pass
            elif isinstance(x_col, str) and expected_y is None:
                try:
                    if x_col in data.columns:
                        x_data = data[x_col].values
                        if np.allclose(x_data, expected_x):
                            return True
                except Exception:
                    pass
    return False

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
    has_hist = False
    for args, kwargs in _plot_history.get('histograms', []):
        if len(args) >= 1:
            try:
                if len(args[0]) == 500:
                    has_hist = True
                    break
            except Exception:
                pass
        x_val = kwargs.get('x', None)
        if x_val is not None:
            try:
                if len(x_val) == 500:
                    has_hist = True
                    break
            except Exception:
                pass
    
    hist_correct = has_hist or check_code_history(r'\b(hist|histplot)\s*\(\s*data\b')
    if not hist_correct:
        return "Could not find correct histogram plot of 'data'."
        
    title = _plot_history['title_set']
    xlabel = _plot_history['xlabel_set']
    ylabel = _plot_history['ylabel_set']
    
    title_correct = (title and str(title).strip().lower() == "feature distribution") or check_code_history(r'\b(title|set_title)\s*\(\s*[\'"]Feature Distribution[\'"]\s*\)')
    xlabel_correct = (xlabel and str(xlabel).strip().lower() == "value") or check_code_history(r'\b(xlabel|set_xlabel)\s*\(\s*[\'"]Value[\'"]\s*\)')
    ylabel_correct = (ylabel and str(ylabel).strip().lower() == "frequency") or check_code_history(r'\b(ylabel|set_ylabel)\s*\(\s*[\'"]Frequency[\'"]\s*\)')
    grid_correct = check_code_history(r'\bgrid\s*\(') or check_code_history(r'\bgrid\s*=\s*True\b')
    
    if not title_correct: return "Plot is missing or has incorrect title. Expected 'Feature Distribution'."
    if not xlabel_correct: return "Plot is missing or has incorrect X-axis label. Expected 'Value'."
    if not ylabel_correct: return "Plot is missing or has incorrect Y-axis label. Expected 'Frequency'."
    if not grid_correct: return "Make sure to turn on the grid."
    return True


def ch3_s2_check():
    has_lmplot = False
    for args, kwargs in _plot_history.get('lmplots', []):
        x_val = kwargs.get('x', None)
        y_val = kwargs.get('y', None)
        hue_val = kwargs.get('hue', None)
        if x_val == 'total_bill' and y_val == 'tip' and hue_val == 'smoker':
            has_lmplot = True
            break
    if has_lmplot or check_code_history(r'\blmplot\s*\('):
        return True
    return "Could not find correct scatter plot with a regression line. Make sure you used sns.lmplot with total_bill, tip, and smoker."


def ch3_s3_check():
    has_heatmap = False
    for args, kwargs in _plot_history.get('heatmaps', []):
        annot = kwargs.get('annot', None)
        cmap = kwargs.get('cmap', None)
        if annot is True and cmap == 'coolwarm':
            has_heatmap = True
            break
    if has_heatmap or check_code_history(r'\bheatmap\s*\('):
        return True
    return "Could not find correct heatmap. Make sure you used sns.heatmap with annot=True and cmap='coolwarm'."


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
    expected_x = [1, 2, 3, 4]
    expected_y = [10, 20, 25, 30]
    if check_plotted_data('line_plots', expected_x, expected_y):
        return True
    if check_code_history(r'\b(plot|lineplot)\s*\(\s*x\s*,\s*y\s*\)'):
        return True
    return "No correct line plot was drawn. Use plt.plot(x, y)."

def ch3_s2_easy_check():
    expected_x = [1, 2, 3, 4]
    expected_y = [1, 4, 9, 16]
    data_correct = check_plotted_data('line_plots', expected_x, expected_y) or check_code_history(r'\b(plot|lineplot)\s*\(\s*x\s*,\s*y\s*\)')
    if not data_correct:
        return "Plot data seems incorrect. Make sure you plot x vs y."
        
    title = _plot_history['title_set']
    xlabel = _plot_history['xlabel_set']
    ylabel = _plot_history['ylabel_set']
    
    title_correct = (title and str(title).strip().lower() == "my first plot") or check_code_history(r'\b(title|set_title)\s*\(\s*[\'"]My First Plot[\'"]\s*\)')
    xlabel_correct = (xlabel and str(xlabel).strip().lower() == "x axis") or check_code_history(r'\b(xlabel|set_xlabel)\s*\(\s*[\'"]X Axis[\'"]\s*\)')
    ylabel_correct = (ylabel and str(ylabel).strip().lower() == "y axis") or check_code_history(r'\b(ylabel|set_ylabel)\s*\(\s*[\'"]Y Axis[\'"]\s*\)')
    
    if not title_correct: return "Plot is missing or has incorrect title. Expected 'My First Plot'."
    if not xlabel_correct: return "Plot is missing or has incorrect X-axis label. Expected 'X Axis'."
    if not ylabel_correct: return "Plot is missing or has incorrect Y-axis label. Expected 'Y Axis'."
    return True

def ch3_s3_easy_check():
    expected_x = [1, 2, 3, 4]
    expected_y = [10, 15, 13, 18]
    if check_plotted_data('scatter_plots', expected_x, expected_y):
        return True
    if check_code_history(r'\b(scatterplot|scatter)\s*\(\s*(x_coords\s*,\s*y_coords|x\s*=\s*x_coords\s*,\s*y\s*=\s*y_coords)\b'):
        return True
    return "No correct scatter plot was found. Make sure you used sns.scatterplot with x_coords and y_coords."

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


def ch1_s4_easy_check(mean_val):
    if not isinstance(mean_val, (float, np.floating)): return "Output should be a float."
    if not np.isclose(mean_val, 30.0): return f"Expected mean of 30.0, but got {mean_val}."
    return True

def ch1_s5_easy_check(df):
    if not isinstance(df, pd.DataFrame): return "Output should be a pandas DataFrame."
    if list(df.columns) != ['A', 'B']: return f"Expected columns ['A', 'B'], but got {list(df.columns)}."
    if list(df['A'].values) != [1, 2] or list(df['B'].values) != [3, 4]: return "DataFrame values are incorrect."
    return True

def ch2_s4_easy_check(s):
    if not isinstance(s, pd.Series): return "Output should be a pandas Series."
    if list(s.values) != [1.0, 3.0, 3.0, 4.0, 5.0]: return f"Expected [1.0, 3.0, 3.0, 4.0, 5.0], but got {list(s.values)}."
    return True

def ch2_s5_easy_check(arr):
    if not isinstance(arr, np.ndarray): return "Output should be a numpy array."
    if arr.min() != 0.0 or arr.max() != 1.0: return "Values are not scaled to [0, 1] range."
    if not np.allclose(arr, [0.0, 0.5, 1.0]): return f"Expected [0.0, 0.5, 1.0], but got {arr}."
    return True

def ch3_s4_easy_check():
    if check_code_history(r'\\b(boxplot|box)\\s*\\('):
        return True
    return "No correct boxplot was found. Use sns.boxplot(x=data_to_box)."

def ch3_s5_easy_check():
    if check_code_history(r'\\b(bar|barplot)\\s*\\('):
        return True
    return "No correct bar chart was found. Use plt.bar or sns.barplot."

def ch4_s4_easy_check(val):
    if not isinstance(val, (float, np.floating)): return "Output should be a float."
    if not np.isclose(val, 0.94, atol=1e-2): return f"Expected R2 score around 0.94, but got {val}."
    return True

def ch4_s5_easy_check(model):
    from sklearn.linear_model import LogisticRegression
    if not isinstance(model, LogisticRegression): return "Output should be a LogisticRegression instance."
    if model.C != 1.0: return f"Expected C=1.0, got {model.C}."
    return True

def ch5_s4_easy_check(model):
    from sklearn.tree import DecisionTreeRegressor
    if not isinstance(model, DecisionTreeRegressor): return "Output should be a DecisionTreeRegressor instance."
    if model.max_depth != 5: return f"Expected max_depth=5, got {model.max_depth}."
    return True

def ch5_s5_easy_check(probs):
    if not isinstance(probs, np.ndarray): return "Output should be a numpy array."
    if probs.shape != (2, 2): return f"Expected probability shape (2, 2), got {probs.shape}."
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
        "agg_df = sales_df.groupby('Category').agg(
    Avg_Revenue=('Revenue', 'mean'),
    Total_Quantity=('Quantity', 'sum')
)"
    )
    step_6 = ExerciseStep(
        ch1_s3_check,
        'Use np.sum(A, axis=1, keepdims=True) to compute row sums. Divide A by these sums to normalize. Then use np.dot or @ for multiplication.',
        'def normalize_and_multiply(A, B):
    row_sums = np.sum(A, axis=1, keepdims=True)
    A_norm = A / row_sums
    return A_norm @ B'
    )
    step_7 = ExerciseStep(
        ch1_s4_easy_check,
        'Use np.mean(arr_to_mean).',
        'arr_mean = np.mean(arr_to_mean)'
    )
    step_8 = ExerciseStep(
        ch1_s5_easy_check,
        'Use pd.DataFrame(data_dict).',
        'df_created = pd.DataFrame(data_dict)'
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
        "df['Size_Encoded'] = df['Size'].map({'Small': 0, 'Medium': 1, 'Large': 2})
encoded_df = pd.get_dummies(df, columns=['Color'])"
    )
    step_6 = ExerciseStep(
        ch2_s3_check,
        'Calculate percentiles using np.percentile(arr, 10) and np.percentile(arr, 90). Clip the array using np.clip. Then do min-max scaling.',
        'def custom_scale(arr, min_val, max_val):
    p10 = np.percentile(arr, 10)
    p90 = np.percentile(arr, 90)
    clipped = np.clip(arr, p10, p90)
    scaled = (clipped - clipped.min()) / (clipped.max() - clipped.min()) * (max_val - min_val) + min_val
    return scaled'
    )
    step_7 = ExerciseStep(
        ch2_s4_easy_check,
        'Use s_to_fill.fillna(s_to_fill.median()).',
        's_median_filled = s_to_fill.fillna(s_to_fill.median())'
    )
    step_8 = ExerciseStep(
        ch2_s5_easy_check,
        'Use standard min-max scaling formula: (arr - arr.min()) / (arr.max() - arr.min()).',
        'arr_scaled_01 = (arr_to_scale - arr_to_scale.min()) / (arr_to_scale.max() - arr_to_scale.min())'
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
        "plt.title('My First Plot')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')"
    )
    step_3 = ExerciseStep(
        ch3_s3_easy_check,
        'Use sns.scatterplot(x=x_coords, y=y_coords).',
        'sns.scatterplot(x=x_coords, y=y_coords)'
    )
    step_4 = ExerciseStep(
        ch3_s1_check,
        'Use plt.hist(data) or sns.histplot(data). Remember to add plt.title(), plt.xlabel(), plt.ylabel().',
        "plt.figure(figsize=(8, 5))
plt.hist(data, bins=20, color='skyblue', edgecolor='black')
plt.title('Feature Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()"
    )
    step_5 = ExerciseStep(
        ch3_s2_check,
        "Use sns.scatterplot or sns.regplot. For a regression line with hue, sns.lmplot(x='total_bill', y='tip', hue='smoker', data=tips) is ideal.",
        "tips = sns.load_dataset('tips')
sns.lmplot(x='total_bill', y='tip', hue='smoker', data=tips, height=6, aspect=1.2)
plt.title('Relationship between total_bill and tip by smoker')
plt.show()"
    )
    step_6 = ExerciseStep(
        ch3_s3_check,
        'Compute the correlation matrix using df.corr(). Construct a mask for weak correlations or simply mask them out. Pass it to sns.heatmap.',
        "corr = df.corr()
# Mask out weak correlations
corr_filtered = corr.copy()
corr_filtered[corr_filtered.abs() < 0.3] = np.nan
sns.heatmap(corr_filtered, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
plt.title('Correlation Heatmap (|r| >= 0.3)')
plt.show()"
    )
    step_7 = ExerciseStep(
        ch3_s4_easy_check,
        'Use sns.boxplot(x=data_to_box).',
        'ax_box = sns.boxplot(x=data_to_box)'
    )
    step_8 = ExerciseStep(
        ch3_s5_easy_check,
        'Use plt.bar(categories, values).',
        'plt.bar(categories, values)'
    )

ch3 = Ch3()

# --- Chapter 4 ---
class Ch4:
    step_1 = ExerciseStep(
        ch4_s1_easy_check,
        'Use: from sklearn.linear_model import LinearRegression, then lr_model = LinearRegression().',
        'from sklearn.linear_model import LinearRegression
lr_model = LinearRegression()'
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
        'model = LinearRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)'
    )
    step_5 = ExerciseStep(
        ch4_s2_check,
        'Initialize w and b to 0. Loop over epochs. Calculate predictions: pred = w*X + b. Calculate gradients: dw = -2/N * sum(X * (y - pred)), db = -2/N * sum(y - pred). Update w = w - lr*dw, b = b - lr*db.',
        'def gradient_descent(X, y, lr, epochs):
    w, b = 0.0, 0.0
    N = len(X)
    for _ in range(epochs):
        pred = w * X + b
        dw = -2/N * np.sum(X * (y - pred))
        db = -2/N * np.sum(y - pred)
        w -= lr * dw
        b -= lr * db
    return w, b'
    )
    step_6 = ExerciseStep(
        ch4_s3_check,
        "Train LogisticRegression(penalty='l1', solver='liblinear', C=0.1) for L1 and LogisticRegression(penalty='l2', C=0.1) for L2. Extract coef_[0] for each.",
        "model_l1 = LogisticRegression(penalty='l1', solver='liblinear', C=0.1, random_state=42).fit(X_train, y_train)
model_l2 = LogisticRegression(penalty='l2', C=0.1, random_state=42).fit(X_train, y_train)
coef_l1 = model_l1.coef_[0]
coef_l2 = model_l2.coef_[0]"
    )
    step_7 = ExerciseStep(
        ch4_s4_easy_check,
        'Use r2_score(y_true_r2, y_pred_r2).',
        'r2_val = r2_score(y_true_r2, y_pred_r2)'
    )
    step_8 = ExerciseStep(
        ch4_s5_easy_check,
        'Use LogisticRegression(C=1.0, random_state=42).',
        'log_reg_model = LogisticRegression(C=1.0, random_state=42)'
    )

ch4 = Ch4()

# --- Chapter 5 ---
class Ch5:
    step_1 = ExerciseStep(
        ch5_s1_easy_check,
        'Use: from sklearn.tree import DecisionTreeClassifier, then dt_easy = DecisionTreeClassifier(max_depth=3).',
        'from sklearn.tree import DecisionTreeClassifier
dt_easy = DecisionTreeClassifier(max_depth=3)'
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
        'dt_model = DecisionTreeClassifier(max_depth=3, random_state=42)
dt_model.fit(X_train, y_train)'
    )
    step_5 = ExerciseStep(
        ch5_s2_check,
        'Instantiate RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=4, random_state=42), fit it, predict on X_test, and compute accuracy_score(y_test, preds).',
        'rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=4, random_state=42)
rf_model.fit(X_train, y_train)
preds = rf_model.predict(X_test)
rf_acc = accuracy_score(y_test, preds)'
    )
    step_6 = ExerciseStep(
        ch5_s3_check,
        'Get importances from rf_model.feature_importances_. Use np.where(importances > 0.1)[0] for indices. Then index X_train[:, selected_indices].',
        'importances = rf_model.feature_importances_
selected_indices = np.where(importances > 0.1)[0]
X_train_filtered = X_train[:, selected_indices]'
    )
    step_7 = ExerciseStep(
        ch5_s4_easy_check,
        'Use DecisionTreeRegressor(max_depth=5, random_state=42).',
        'dtr_model = DecisionTreeRegressor(max_depth=5, random_state=42)'
    )
    step_8 = ExerciseStep(
        ch5_s5_easy_check,
        'Use trained_dt.predict_proba(X_new_probs).',
        'pred_probs = trained_dt.predict_proba(X_new_probs)'
    )

ch5 = Ch5()

# --- Chapter 6 ---


def ch6_s4_easy_check(model):
    from sklearn.naive_bayes import ComplementNB
    if not isinstance(model, ComplementNB): return 'Output should be a ComplementNB instance.'
    return True

def ch6_s5_easy_check(dec):
    if not isinstance(dec, np.ndarray): return 'Output should be a numpy array.'
    if dec.shape != (2,): return f'Expected shape (2,), got {dec.shape}.'
    return True

def ch7_s4_easy_check(val):
    if not isinstance(val, (float, np.floating)): return 'Output should be a float.'
    if val < 0: return 'Inertia must be positive.'
    return True

def ch7_s5_easy_check(arr):
    if not isinstance(arr, np.ndarray): return 'Output should be a numpy array.'
    if len(arr) != 2: return f'Expected 2 variance ratios, got {len(arr)}.'
    return True

def ch8_s4_easy_check(col):
    if not isinstance(col, pd.Series): return 'Output should be a pandas Series.'
    if not np.allclose(col.values, np.log1p([30000, 50000, 90000, 0])): return 'Values are incorrect.'
    return True

def ch8_s5_easy_check(col):
    if not isinstance(col, pd.Series): return 'Output should be a pandas Series.'
    if list(col.values) != [6, 20, 42]: return f'Expected [6, 20, 42], got {list(col.values)}.'
    return True

def ch9_s4_easy_check(cm):
    if not isinstance(cm, np.ndarray): return 'Output should be a numpy array.'
    if cm.shape != (2, 2): return f'Expected shape (2, 2), got {cm.shape}.'
    return True

def ch9_s5_easy_check(val):
    if not isinstance(val, (float, np.floating)): return 'Output should be a float.'
    if not np.isclose(val, 0.666666666): return f'Expected precision 0.67, got {val}.'
    return True

def ch10_s4_easy_check(model):
    from tensorflow.keras.models import Sequential
    if not isinstance(model, Sequential): return 'Output should be a Keras Sequential model.'
    return True

def ch10_s5_easy_check(model):
    from tensorflow.keras.models import Sequential
    if not isinstance(model, Sequential): return 'Output should be a Keras Sequential model.'
    if not model.optimizer: return 'Model has not been compiled yet. Use model.compile().'
    return True

def ch11_s4_easy_check(s):
    if not isinstance(s, pd.Series): return 'Output should be a pandas Series.'
    if not np.isnan(s.iloc[0]): return 'Expected first value to be NaN due to shifting.'
    return True

def ch11_s5_easy_check(s):
    if not isinstance(s, pd.Series): return 'Output should be a pandas Series.'
    if len(s) != 2: return f'Expected 2 monthly data points, got {len(s)}.'
    return True

def ch12_s4_easy_check(col):
    if not isinstance(col, pd.Series): return 'Output should be a pandas Series.'
    if list(col.values) != [11, 19, 3]: return f'Expected [11, 19, 3], got {list(col.values)}.'
    return True

def ch12_s5_easy_check(lst):
    if not isinstance(lst, list): return 'Output should be a list.'
    if lst != ['Tokenize', 'this', 'simple', 'sentence']: return f'Unexpected tokens: {lst}.'
    return True

def ch13_s4_easy_check(model):
    from sklearn.ensemble import IsolationForest
    if not isinstance(model, IsolationForest): return 'Output should be an IsolationForest model.'
    if model.contamination != 0.05: return f'Expected contamination=0.05, got {model.contamination}.'
    return True

def ch13_s5_easy_check(arr):
    if not isinstance(arr, np.ndarray): return 'Output should be a numpy array.'
    if not np.isclose(np.mean(arr, axis=0), 0.0).all(): return 'Features are not standard scaled to 0 mean.'
    return True

def ch14_s4_easy_check(model):
    from sklearn.ensemble import VotingClassifier
    if not isinstance(model, VotingClassifier): return 'Output should be a VotingClassifier model.'
    if model.voting != 'soft': return f'Expected voting=soft, got {model.voting}.'
    return True

def ch14_s5_easy_check(model):
    from sklearn.ensemble import AdaBoostClassifier
    if not isinstance(model, AdaBoostClassifier): return 'Output should be an AdaBoostClassifier model.'
    if model.n_estimators != 50: return f'Expected n_estimators=50, got {model.n_estimators}.'
    return True

def ch15_s4_easy_check(model):
    from sklearn.manifold import TSNE
    if not isinstance(model, TSNE): return 'Output should be a TSNE instance.'
    if model.n_components != 2: return f'Expected n_components=2, got {model.n_components}.'
    return True

def ch15_s5_easy_check(arr):
    if not isinstance(arr, np.ndarray): return 'Output should be a numpy array.'
    if arr.shape[1] != 2: return f'Expected output shape to have 2 columns, got {arr.shape[1]}.'
    return True

def ch16_s4_easy_check(val):
    if not isinstance(val, (float, np.floating)): return 'Output should be a float.'
    if not np.isclose(val, 0.985, atol=1e-2): return f'Expected similarity near 0.985, got {val}.'
    return True

def ch16_s5_easy_check(val):
    if not isinstance(val, (float, np.floating)): return 'Output should be a float.'
    if not np.isclose(val, 0.962, atol=1e-2): return f'Expected correlation near 0.962, got {val}.'
    return True

def ch17_s4_easy_check(model):
    from mlxtend.preprocessing import TransactionEncoder
    if not isinstance(model, TransactionEncoder): return 'Output should be a TransactionEncoder.'
    return True

def ch17_s5_easy_check(df):
    if not isinstance(df, pd.DataFrame): return 'Output should be a pandas DataFrame.'
    return True

def ch18_s4_easy_check(model):
    from sklearn.semi_supervised import LabelSpreading
    if not isinstance(model, LabelSpreading): return 'Output should be a LabelSpreading instance.'
    if model.kernel != 'knn': return f'Expected kernel=knn, got {model.kernel}.'
    return True

def ch18_s5_easy_check(arr):
    if not isinstance(arr, np.ndarray): return 'Output should be a numpy array.'
    if list(arr) != [1, 0, -1, 1, -1]: return f'Unexpected labels: {list(arr)}.'
    return True

def ch19_s4_easy_check(weights):
    if not isinstance(weights, np.ndarray): return 'Output should be a numpy array.'
    if not np.isclose(weights[0], 0.6) or not np.isclose(weights[1], 3.0): return 'Weights are incorrect.'
    return True

def ch19_s5_easy_check(arr):
    if not isinstance(arr, np.ndarray): return 'Output should be a numpy array.'
    if len(arr) != 4: return f'Expected 4 indices, got {len(arr)}.'
    return True

def ch20_s4_easy_check(model):
    from sklearn.model_selection import GridSearchCV
    if not isinstance(model, GridSearchCV): return 'Output should be a GridSearchCV instance.'
    return True

def ch20_s5_easy_check(model):
    from sklearn.model_selection import RandomizedSearchCV
    if not isinstance(model, RandomizedSearchCV): return 'Output should be a RandomizedSearchCV instance.'
    return True

def ch21_s4_easy_check(q):
    if not isinstance(q, np.ndarray): return 'Output should be a numpy array.'
    if q.shape != (5, 3): return f'Expected shape (5, 3), got {q.shape}.'
    return True

def ch21_s5_easy_check(act):
    if not isinstance(act, (int, np.integer)): return 'Output should be an integer.'
    rng = np.random.RandomState(42)
    expected = rng.choice(3)
    if act != expected: return f'Expected {expected}, got {act}.'
    return True

def ch22_s4_easy_check(model):
    from tensorflow.keras.models import Sequential
    if not isinstance(model, Sequential): return 'Output should be a Keras Sequential model.'
    return True

def ch22_s5_easy_check(model):
    from tensorflow.keras.models import Sequential
    if not isinstance(model, Sequential): return 'Output should be a Keras Sequential model.'
    if len(model.layers) < 2: return 'Model is missing layers.'
    return True

def ch23_s4_easy_check(dc):
    if not isinstance(dc, dict): return 'Output should be a dictionary.'
    if len(dc) != 4: return f'Expected 4 node centralities, got {len(dc)}.'
    return True

def ch23_s5_easy_check(adj):
    if not isinstance(adj, np.ndarray): return 'Output should be a numpy array.'
    if adj.shape != (4, 4): return f'Expected shape (4, 4), got {adj.shape}.'
    return True

def ch24_s4_easy_check(coef):
    if not isinstance(coef, np.ndarray): return 'Output should be a numpy array.'
    if not np.isclose(coef[0], 2.0): return f'Expected coef 2.0, got {coef[0]}.'
    return True

def ch24_s5_easy_check(exp):
    import shap
    if not isinstance(exp, shap.explainers._tree.Tree): return 'Output should be a SHAP Tree Explainer.'
    return True

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

    step_7 = ExerciseStep(
        ch6_s4_easy_check,
        'Use: cnb_model = ComplementNB().',
        'from sklearn.naive_bayes import ComplementNB\ncnb_model = ComplementNB()'
    )
    step_8 = ExerciseStep(
        ch6_s5_easy_check,
        'Call trained_svm.decision_function(X_new_svm).',
        'decision_values = trained_svm.decision_function(X_new_svm)'
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

    step_7 = ExerciseStep(
        ch7_s4_easy_check,
        'Fit model = KMeans(n_clusters=2, random_state=42).fit(X_kmeans) and return model.inertia_.',
        'model = KMeans(n_clusters=2, random_state=42).fit(X_kmeans)\ninertia_val = model.inertia_'
    )
    step_8 = ExerciseStep(
        ch7_s5_easy_check,
        'Fit PCA(n_components=2).fit(X_pca) and extract explained_variance_ratio_.',
        'explained_variance = PCA(n_components=2).fit(X_pca).explained_variance_ratio_'
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

    step_7 = ExerciseStep(
        ch8_s4_easy_check,
        "Use: np.log1p(df_log['Salary']).",
        "df_log['Salary_Log'] = np.log1p(df_log['Salary'])"
    )
    step_8 = ExerciseStep(
        ch8_s5_easy_check,
        "Use: df_inter['A'] * df_inter['B'].",
        "df_inter['A_x_B'] = df_inter['A'] * df_inter['B']"
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

    step_7 = ExerciseStep(
        ch9_s4_easy_check,
        'Use: confusion_matrix(y_true_cm, y_pred_cm).',
        'cm = confusion_matrix(y_true_cm, y_pred_cm)'
    )
    step_8 = ExerciseStep(
        ch9_s5_easy_check,
        'Use: precision_score(y_true_cm, y_pred_cm).',
        'precision_val = precision_score(y_true_cm, y_pred_cm)'
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

    step_7 = ExerciseStep(
        ch10_s4_easy_check,
        "Use: keras_model = Sequential([Dense(1, activation='sigmoid')]) or Sequential().add(Dense(1, activation='sigmoid')).",
        "keras_model = Sequential([Dense(1, activation='sigmoid', input_shape=(10,))])"
    )
    step_8 = ExerciseStep(
        ch10_s5_easy_check,
        "Call model_to_compile.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']).",
        "model_to_compile.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])\ncompiled_model = model_to_compile"
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

    step_7 = ExerciseStep(
        ch11_s4_easy_check,
        'Use: ts_series.shift(1).',
        'ts_lagged = ts_series.shift(1)'
    )
    step_8 = ExerciseStep(
        ch11_s5_easy_check,
        "Use: daily_ts.resample('ME').mean() or daily_ts.resample('M').mean().",
        "monthly_mean = daily_ts.resample('ME').mean()"
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

    step_7 = ExerciseStep(
        ch12_s4_easy_check,
        'Use: text_series.str.len().',
        'char_counts = text_series.str.len()'
    )
    step_8 = ExerciseStep(
        ch12_s5_easy_check,
        'Use: sentence.split().',
        'tokens = sentence.split()'
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
        'def mahalanobis_distance(X):\n    mean = X.mean(axis=0)\n    cov = np.cov(X.T)\n    inv_cov = np.linalg.pinv(cov)\n    dists = []\n    for x in X:\n        diff = x - mean\n        d = np.sqrt(diff.T @ inv_cov @ diff)\n        dists.append(d)\n    return np.array(dists)'
<<<<<<< HEAD
    )

    step_7 = ExerciseStep(
        ch13_s4_easy_check,
        'Use: IsolationForest(contamination=0.05, random_state=42).',
        'if_model = IsolationForest(contamination=0.05, random_state=42)'
    )
    step_8 = ExerciseStep(
        ch13_s5_easy_check,
        'Instantiate and apply StandardScaler().fit_transform(X_anom).',
        'X_scaled_anom = StandardScaler().fit_transform(X_anom)'
=======
>>>>>>> 90675cf0021a5b7b7a4ac10f4d93c6d191dbcdf9
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

    step_7 = ExerciseStep(
        ch14_s4_easy_check,
        "Use: VotingClassifier(estimators=[('rf', rf_clf), ('lr', lr_clf)], voting='soft').",
        "voting_model = VotingClassifier(estimators=[('rf', rf_clf), ('lr', lr_clf)], voting='soft')"
    )
    step_8 = ExerciseStep(
        ch14_s5_easy_check,
        'Use: AdaBoostClassifier(n_estimators=50, random_state=42).',
        'adaboost_model = AdaBoostClassifier(n_estimators=50, random_state=42)'
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

    step_7 = ExerciseStep(
        ch15_s4_easy_check,
        'Use: TSNE(n_components=2, random_state=42).',
        'X_tsne = tsne_model.fit_transform(X_manifold)'
    )
    step_8 = ExerciseStep(
        ch15_s5_easy_check,
        'Call tsne_model.fit_transform(X_manifold).',
        'X_tsne = tsne_model.fit_transform(X_manifold)'
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

    step_7 = ExerciseStep(
        ch16_s4_easy_check,
        'Use: np.dot(u1, u2) / (np.linalg.norm(u1) * np.linalg.norm(u2)).',
        'sim_val = np.dot(u1, u2) / (np.linalg.norm(u1) * np.linalg.norm(u2))'
    )
    step_8 = ExerciseStep(
        ch16_s5_easy_check,
        'Use: np.corrcoef(ratings_A, ratings_B)[0, 1].',
        'pearson_corr = np.corrcoef(ratings_A, ratings_B)[0, 1]'
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

    step_7 = ExerciseStep(
        ch17_s4_easy_check,
        'Use: te_encoder = TransactionEncoder().',
        'te_encoder = TransactionEncoder()'
    )
    step_8 = ExerciseStep(
        ch17_s5_easy_check,
        "Call: association_rules(frequent_itemsets, metric='confidence', min_threshold=0.6).",
        "rules_df = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.6)"
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

    step_7 = ExerciseStep(
        ch18_s4_easy_check,
        "Use: LabelSpreading(kernel='knn', n_neighbors=5).",
        "ls_model = LabelSpreading(kernel='knn', n_neighbors=5)"
    )
    step_8 = ExerciseStep(
        ch18_s5_easy_check,
        "Copy y_raw, replace 'unknown' with -1, and return values array.",
        "y_semi = y_raw.copy().replace('unknown', -1).values.astype(int)"
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

    step_7 = ExerciseStep(
        ch19_s4_easy_check,
        "Use: class_weight.compute_class_weight(class_weight='balanced', classes=np.unique(y_imb), y=y_imb).",
        "class_weights = class_weight.compute_class_weight(class_weight='balanced', classes=np.unique(y_imb), y=y_imb)"
    )
    step_8 = ExerciseStep(
        ch19_s5_easy_check,
        'Identify idx_0 and idx_1, select len(idx_1) elements from idx_0 with rng.choice, then concatenate.',
        'idx_0 = np.where(y_binary == 0)[0]\nidx_1 = np.where(y_binary == 1)[0]\nrng = np.random.RandomState(42)\nidx_0_sampled = rng.choice(idx_0, size=len(idx_1), replace=False)\nbalanced_indices = np.concatenate([idx_0_sampled, idx_1])'
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

    step_6 = ExerciseStep(
        ch20_s3_check,
        'Initialize points randomly. Fit a GaussianProcessRegressor model on those points. For each iteration, compute acquisition values (e.g. mean + std) over a dense grid. Evaluate objective at the point that maximizes the acquisition. Add this point and its objective value to your dataset, and loop.',
        'from sklearn.gaussian_process import GaussianProcessRegressor\nfrom sklearn.gaussian_process.kernels import Matern\ndef bayesian_optimization(objective, bounds, n_iters=10):\n    # Simple Bayesian Optimization simulation\n    np.random.seed(42)\n    X = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(3, bounds.shape[0]))\n    y = np.array([objective(x) for x in X])\n    for _ in range(n_iters):\n        gp = GaussianProcessRegressor(kernel=Matern(nu=2.5), alpha=1e-6, random_state=42)\n        gp.fit(X, y)\n        # Search space dense grid\n        grid = np.linspace(bounds[0, 0], bounds[0, 1], 100).reshape(-1, 1)\n        mu, std = gp.predict(grid, return_std=True)\n        acquisition = mu + 1.96 * std\n        next_x = grid[np.argmax(acquisition)]\n        next_y = objective(next_x)\n        X = np.vstack([X, next_x])\n        y = np.append(y, next_y)\n    best_idx = np.argmax(y)\n    return X[best_idx], y[best_idx]'
    )

    step_7 = ExerciseStep(
        ch20_s4_easy_check,
        "Use: GridSearchCV(estimator=DecisionTreeClassifier(), param_grid={'max_depth': [3, 5]}, cv=3).",
        "grid_search = GridSearchCV(estimator=DecisionTreeClassifier(), param_grid={'max_depth': [3, 5]}, cv=3)"
    )
    step_8 = ExerciseStep(
        ch20_s5_easy_check,
        "Use: RandomizedSearchCV(estimator=DecisionTreeClassifier(), param_distributions={'max_depth': [2, 4, 6]}, n_iter=3, cv=3, random_state=42).",
        "random_search = RandomizedSearchCV(estimator=DecisionTreeClassifier(), param_distributions={'max_depth': [2, 4, 6]}, n_iter=3, cv=3, random_state=42)"
    )

ch20 = Ch20()


# ==========================================
# --- CHAPTER 21: REINFORCEMENT LEARNING ---
# ==========================================

def ch21_s1_easy_check(func):
    if not callable(func): return "Input must be a function."
    res1 = func(np.array([1.0, 5.0, 2.0, 0.5]), epsilon=0.0)
    if res1 != 1: return f"Expected greedy action 1, got {res1}."
    res2 = func(np.array([1.0, 5.0, 2.0, 0.5]), epsilon=1.0, random_state=42)
    if res2 is None: return "Function returned None."
    return True

def ch21_s2_easy_check(func):
    if not callable(func): return "Input must be a function."
    res = func(q_val=2.0, reward=10.0, max_next_q=5.0, alpha=0.1, gamma=0.9)
    if not np.isclose(res, 3.25):
        return f"Expected Q-value of 3.25, got {res}."
    return True

def ch21_s3_easy_check(func):
    if not callable(func): return "Input must be a function."
    res = func(16, 4)
    if not isinstance(res, np.ndarray): return "Expected a numpy array."
    if res.shape != (16, 4): return f"Expected shape (16, 4), got {res.shape}."
    if not np.all(res == 0): return "Expected Q-table to be initialized with all zeros."
    return True

def ch21_s1_check(func):
    if not callable(func): return "Input must be a function."
    # Test boundary transitions and step updates
    s, r, d = func(0, 1, grid_size=4)
    if s != 4 or r != -1 or d is not False:
        return f"From state 0 taking action 1 (down): expected (4, -1, False), got ({s}, {r}, {d})."
    s, r, d = func(0, 0, grid_size=4)
    if s != 0 or r != -1 or d is not False:
        return f"From state 0 taking action 0 (up): expected (0, -1, False), got ({s}, {r}, {d})."
    s, r, d = func(14, 3, grid_size=4)
    if s != 15 or r != 10 or d is not True:
        return f"From state 14 taking action 3 (right): expected (15, 10, True), got ({s}, {r}, {d})."
    return True

def ch21_s2_check(func):
    if not callable(func): return "Input must be a function."
    q_table = np.array([[1.0, 2.0, 1.5, 0.5]])
    rng = np.random.RandomState(42)
    act = func(q_table, 0, epsilon=0.0, rng=rng)
    if act != 1: return f"Greedy action selection: expected action 1, got {act}."
    act2 = func(q_table, 0, epsilon=1.0, rng=rng)
    if act2 not in [0, 1, 2, 3]: return f"Random action selection: expected action in [0, 3], got {act2}."
    return True

def ch21_s3_check(func):
    if not callable(func): return "Input must be a function."
    try:
        q_table = func(epochs=100, alpha=0.1, gamma=0.9, epsilon=0.1)
    except Exception as e:
        return f"Error executing train_q_learning: {str(e)}"
    if not isinstance(q_table, np.ndarray):
        return "Expected Q-table to be a numpy array."
    if q_table.shape != (16, 4):
        return f"Expected shape (16, 4), got {q_table.shape}."
    if np.all(q_table == 0.0):
        return "Q-table is still all zeros. Check if your training updates are functioning."
    # The action that moves down/right from state 0 should have non-zero value
    if np.sum(q_table[0]) == 0.0:
        return "Q-values for initial state (state 0) are still 0.0."
    return True

class Ch21:
    step_1 = ExerciseStep(
        ch21_s1_easy_check,
        'Use np.random.RandomState(random_state) to select actions randomly or greedily based on epsilon.',
        'def epsilon_greedy(q_values, epsilon, random_state=None):\n    rng = np.random.RandomState(random_state)\n    if rng.rand() < epsilon:\n        return rng.randint(len(q_values))\n    else:\n        return np.argmax(q_values)'
    )
    step_2 = ExerciseStep(
        ch21_s2_easy_check,
        'Implement: q_val + alpha * (reward + gamma * max_next_q - q_val)',
        'def bellman_update(q_val, reward, max_next_q, alpha, gamma):\n    return q_val + alpha * (reward + gamma * max_next_q - q_val)'
    )
    step_3 = ExerciseStep(
        ch21_s3_easy_check,
        'Use np.zeros((num_states, num_actions))',
        'def init_q_table(num_states, num_actions):\n    return np.zeros((num_states, num_actions))'
    )
    step_4 = ExerciseStep(
        ch21_s1_check,
        'Convert the state to row and col, adjust based on action (0: up, 1: down, 2: left, 3: right), keep inside the grid boundary, and return the reward (-1 for normal steps, +10 for goal) and done.',
        'def gridworld_step(state, action, grid_size=4):\n    row, col = state // grid_size, state % grid_size\n    if action == 0 and row > 0: row -= 1\n    elif action == 1 and row < grid_size - 1: row += 1\n    elif action == 2 and col > 0: col -= 1\n    elif action == 3 and col < grid_size - 1: col += 1\n    next_state = row * grid_size + col\n    done = (next_state == grid_size * grid_size - 1)\n    reward = 10.0 if done else -1.0\n    return next_state, reward, done'
    )
    step_5 = ExerciseStep(
        ch21_s2_check,
        'Check if rng.rand() < epsilon; if so select randomly, else select using np.argmax on q_table[state].',
        'def select_action(q_table, state, epsilon, rng):\n    if rng.rand() < epsilon:\n        return rng.randint(q_table.shape[1])\n    else:\n        return np.argmax(q_table[state])'
    )
    step_6 = ExerciseStep(
        ch21_s3_check,
        'Loop over epochs. For each epoch, run environment steps, select epsilon-greedy actions, and perform Bellman Q-value updates.',
        'def train_q_learning(epochs=100, alpha=0.1, gamma=0.9, epsilon=0.1):\n    q_table = np.zeros((16, 4))\n    for epoch in range(epochs):\n        rng = np.random.RandomState(epoch)\n        state = 0\n        done = False\n        steps = 0\n        while not done and steps < 50:\n            action = select_action(q_table, state, epsilon, rng)\n            next_state, reward, done = gridworld_step(state, action)\n            max_next_q = np.max(q_table[next_state])\n            q_table[state, action] = bellman_update(q_table[state, action], reward, max_next_q, alpha, gamma)\n            state = next_state\n            steps += 1\n    return q_table'
    )

    step_7 = ExerciseStep(
        ch21_s4_easy_check,
        'Use: np.zeros((num_states, num_actions)).',
        'q_table = np.zeros((num_states, num_actions))'
    )
    step_8 = ExerciseStep(
        ch21_s5_easy_check,
        'Since rand_val < epsilon (0.05 < 0.2), choose a random action using rng.choice(num_actions). Otherwise argmax(q_values).',
        'rng = np.random.RandomState(42)\nif rand_val < epsilon:\n    selected_action = rng.choice(num_actions)\nelse:\n    selected_action = np.argmax(q_values)'
    )

ch21 = Ch21()


# ====================================================
# --- CHAPTER 22: COMPUTER VISION & CONVOLUTIONS ---
# ====================================================

def ch22_s1_easy_check(func):
    if not callable(func): return "Input must be a function."
    from PIL import Image
    import os
    img = Image.new('RGB', (10, 10), color='blue')
    temp_path = 'temp_dummy_ch22.png'
    img.save(temp_path)
    try:
        arr = func(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    if not isinstance(arr, np.ndarray): return "Expected a numpy array."
    if arr.ndim != 2: return "Expected a 2D grayscale image array."
    if arr.shape != (10, 10): return f"Expected shape (10, 10), got {arr.shape}."
    if not (0.0 <= arr.min() <= arr.max() <= 1.0): return "Values should be scaled between 0.0 and 1.0."
    return True

def ch22_s2_easy_check(func):
    if not callable(func): return "Input must be a function."
    img = np.array([[1.0, 2.0], [3.0, 4.0]])
    res = func(img, pool_size=2)
    if not np.isclose(res[0, 0], 4.0):
        return f"Expected max value of 4.0, got {res[0, 0]}."
    return True

def ch22_s3_easy_check(func):
    if not callable(func): return "Input must be a function."
    img = np.arange(12).reshape(2, 2, 3)
    res = func(img)
    if not np.allclose(res[:, 0, :], img[:, 1, :]):
        return "Horizontal flip does not correctly swap the columns."
    return True

def ch22_s1_check(func):
    if not callable(func): return "Input must be a function."
    img = np.ones((10, 10))
    res = func(img)
    if not np.allclose(res[1:-1, 1:-1], 0.0):
        return "Sobel horizontal filter on a constant region should output zeros."
    return True


def ch22_s2_check(func):
    if not callable(func): return "Input must be a function."
    img = np.array([
        [0.0, 1.0, 2.0],
        [3.0, 4.0, 5.0],
        [6.0, 7.0, 8.0]
    ])
    kernel = np.array([[1.0, 0.0], [0.0, 1.0]])
    # conv2d_scratch with stride=1, padding=0:
    # element (0,0): 0*1 + 4*1 = 4
    # element (0,1): 1*1 + 5*1 = 6
    # element (1,0): 3*1 + 7*1 = 10
    # element (1,1): 4*1 + 8*1 = 12
    expected = np.array([[4.0, 6.0], [10.0, 12.0]])
    res = func(img, kernel, stride=1, padding=0)
    if not np.allclose(res, expected):
        return f"Expected convolution output \n{expected}\n, got \n{res}\n"
    return True

def ch22_s3_check(func):
    if not callable(func): return "Input must be a function."
    img = np.ones((6, 6))
    conv_kernel = np.ones((3, 3))
    pool_size = 2
    dense_weights = np.ones((4, 2))
    dense_bias = np.zeros(2)
    try:
        res = func(img, conv_kernel, pool_size, dense_weights, dense_bias)
    except Exception as e:
        return f"Error executing cnn_forward: {str(e)}"
    if not np.allclose(res, np.array([0.5, 0.5])):
        return f"Expected [0.5, 0.5] softmax outputs, got {res}."
    return True

class Ch22:
    step_1 = ExerciseStep(
        ch22_s1_easy_check,
        'Use Image.open(img_path).convert("L"), then cast to np.array and divide by 255.0.',
        'from PIL import Image\ndef to_grayscale(img_path):\n    img = Image.open(img_path).convert("L")\n    return np.array(img, dtype=float) / 255.0'
    )
    step_2 = ExerciseStep(
        ch22_s2_easy_check,
        'Determine output shape, slide a pool_size window with stride equal to pool_size, and take np.max of the window.',
        'def max_pooling_2d(img, pool_size=2):\n    h, w = img.shape\n    out_h = h // pool_size\n    out_w = w // pool_size\n    pooled = np.zeros((out_h, out_w))\n    for i in range(out_h):\n        for j in range(out_w):\n            window = img[i*pool_size:(i+1)*pool_size, j*pool_size:(j+1)*pool_size]\n            pooled[i, j] = np.max(window)\n    return pooled'
    )
    step_3 = ExerciseStep(
        ch22_s3_easy_check,
        'Use horizontal indexing: img[:, ::-1, :] or img[:, ::-1].',
        'def horizontal_flip(img):\n    return img[:, ::-1, ...]'
    )
    step_4 = ExerciseStep(
        ch22_s1_check,
        'Create the Sobel horizontal kernel and use scipy.signal.convolve2d with mode="same".',
        'from scipy.signal import convolve2d\ndef apply_sobel_horizontal(img):\n    kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])\n    return convolve2d(img, kernel, mode="same")'
    )
    step_5 = ExerciseStep(
        ch22_s2_check,
        'Pad the image if needed, slide the kernel over the image by the stride, perform element-wise multiplication and sum.',
        'def conv2d_scratch(img, kernel, stride=1, padding=0):\n    if padding > 0:\n        img = np.pad(img, padding, mode="constant")\n    h_in, w_in = img.shape\n    k_h, k_w = kernel.shape\n    h_out = (h_in - k_h) // stride + 1\n    w_out = (w_in - k_w) // stride + 1\n    out = np.zeros((h_out, w_out))\n    for i in range(h_out):\n        for j in range(w_out):\n            r = i * stride\n            c = j * stride\n            window = img[r:r+k_h, c:c+k_w]\n            out[i, j] = np.sum(window * kernel)\n    return out'
    )
    step_6 = ExerciseStep(
        ch22_s3_check,
        'Perform convolve2d, ReLU (np.maximum(0, x)), max_pooling_2d, flattening, dense layer calculation, and softmax.',
        'from scipy.signal import convolve2d\ndef cnn_forward(img, conv_kernel, pool_size, dense_weights, dense_bias):\n    conv_out = convolve2d(img, conv_kernel, mode="valid")\n    relu_out = np.maximum(0, conv_out)\n    # Reuse max pool logic\n    h, w = relu_out.shape\n    out_h, out_w = h // pool_size, w // pool_size\n    pooled = np.zeros((out_h, out_w))\n    for i in range(out_h):\n        for j in range(out_w):\n            pooled[i, j] = np.max(relu_out[i*pool_size:(i+1)*pool_size, j*pool_size:(j+1)*pool_size])\n    flat = pooled.flatten()\n    dense_out = np.dot(flat, dense_weights) + dense_bias\n    exp_vals = np.exp(dense_out - np.max(dense_out))\n    return exp_vals / np.sum(exp_vals)'
    )

    step_7 = ExerciseStep(
        ch22_s4_easy_check,
        "Use: Sequential([Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1))]).",
        "cnn_model = Sequential([Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1))])"
    )
    step_8 = ExerciseStep(
        ch22_s5_easy_check,
        'Call maxpool_model.add(MaxPooling2D(pool_size=(2, 2))).',
        "maxpool_model = Sequential([\n    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1))\n])\nmaxpool_model.add(MaxPooling2D(pool_size=(2, 2)))"
    )

ch22 = Ch22()


# ===============================================
# --- CHAPTER 23: GRAPH MACHINE LEARNING --------
# ===============================================

def ch23_s1_easy_check(func):
    if not callable(func): return "Input must be a function."
    adj = np.array([[0, 1], [1, 0]])
    res = func(adj)
    if not np.allclose(res, np.array([1, 1])):
        return f"Expected node degrees [1, 1], got {res}."
    return True

def ch23_s2_easy_check(func):
    if not callable(func): return "Input must be a function."
    adj = np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ])
    # Node 0 neighbors: {1, 2}. Node 1 neighbors: {0, 2}.
    # Intersection: {2} (size 1)
    # Union: {0, 1, 2} (size 3)
    # Jaccard = 1/3
    res = func(adj, 0, 1)
    if not np.isclose(res, 1.0/3.0):
        return f"Expected Jaccard 1/3, got {res}."
    return True

def ch23_s3_easy_check(func):
    if not callable(func): return "Input must be a function."
    adj = np.array([[0, 1], [1, 0]])
    res = func(adj)
    expected = np.array([[1, -1], [-1, 1]])
    if not np.allclose(res, expected):
        return f"Expected Laplacian \n{expected}\n, got \n{res}\n"
    return True

def ch23_s1_check(func):
    if not callable(func): return "Input must be a function."
    M = np.array([[0.5, 0.5], [0.5, 0.5]])
    r = np.array([0.5, 0.5])
    res = func(M, r, d=0.8)
    # 0.8 * [0.5, 0.5] + 0.2 / 2 * [1, 1] = [0.4, 0.4] + [0.1, 0.1] = [0.5, 0.5]
    if not np.allclose(res, np.array([0.5, 0.5])):
        return f"Expected PageRank output [0.5, 0.5], got {res}."
    return True

def ch23_s2_check(func):
    if not callable(func): return "Input must be a function."
    T = np.array([[0, 1], [1, 0]], dtype=float)
    Y = np.array([[1.0, 0.0], [0.0, 0.0]])
    Y_orig = Y.copy()
    res = func(T, Y, Y_orig, [0])
    # T * Y = [ [0, 0], [1, 0] ]
    # Reset labeled [0]: row 0 is reset to [1, 0]
    # Expected: [ [1, 0], [1, 0] ]
    if not np.allclose(res, np.array([[1.0, 0.0], [1.0, 0.0]])):
        return f"Expected labels \n[[1, 0], [1, 0]]\n, got \n{res}\n"
    return True

def ch23_s3_check(func):
    if not callable(func): return "Input must be a function."
    adj = np.array([
        [0, 1],
        [1, 0]
    ])
    walks = func(adj, walk_length=3, num_walks=2, random_state=42)
    if walks.shape != (4, 3):
        return f"Expected walks shape (4, 3), got {walks.shape}."
    return True

class Ch23:
    step_1 = ExerciseStep(
        ch23_s1_easy_check,
        'Sum the columns or rows of the adjacency matrix.',
        'def get_degrees(adj_matrix):\n    return np.sum(adj_matrix, axis=1)'
    )
    step_2 = ExerciseStep(
        ch23_s2_easy_check,
        'Find neighbors of u and v, compute their intersection and union size, and return intersection / union.',
        'def jaccard_coefficient(adj_matrix, u, v):\n    n_u = set(np.where(adj_matrix[u] > 0)[0])\n    n_v = set(np.where(adj_matrix[v] > 0)[0])\n    if not n_u or not n_v: return 0.0\n    union = n_u.union(n_v)\n    if len(union) == 0: return 0.0\n    return len(n_u.intersection(n_v)) / len(union)'
    )
    step_3 = ExerciseStep(
        ch23_s3_easy_check,
        'Compute degree matrix D and return D - adj_matrix.',
        'def graph_laplacian(adj_matrix):\n    D = np.diag(np.sum(adj_matrix, axis=1))\n    return D - adj_matrix'
    )
    step_4 = ExerciseStep(
        ch23_s1_check,
        'Implement: d * np.dot(M, r) + (1 - d) / N * np.ones(N).',
        'def pagerank_iteration(M, r, d=0.85):\n    N = len(r)\n    return d * np.dot(M, r) + (1.0 - d) / N'
    )
    step_5 = ExerciseStep(
        ch23_s2_check,
        'Perform matrix multiplication np.dot(T, Y), then reset row values for labeled nodes using Y_orig.',
        'def label_prop_step(T, Y, Y_orig, labeled_indices):\n    Y_new = np.dot(T, Y)\n    Y_new[labeled_indices] = Y_orig[labeled_indices]\n    return Y_new'
    )
    step_6 = ExerciseStep(
        ch23_s3_check,
        'For each node, generate walks using random neighbor transition choices. If a node has no neighbors, stay on the current node.',
        'def generate_random_walks(adj_matrix, walk_length=5, num_walks=10, random_state=42):\n    rng = np.random.RandomState(random_state)\n    N = adj_matrix.shape[0]\n    walks = []\n    for node in range(N):\n        for _ in range(num_walks):\n            walk = [node]\n            curr = node\n            for _ in range(walk_length - 1):\n                neighbors = np.where(adj_matrix[curr] > 0)[0]\n                if len(neighbors) > 0:\n                    curr = rng.choice(neighbors)\n                walk.append(curr)\n            walks.append(walk)\n    return np.array(walks)'
    )

    step_7 = ExerciseStep(
        ch23_s4_easy_check,
        'Use: nx.degree_centrality(G).',
        'deg_centrality = nx.degree_centrality(G)'
    )
    step_8 = ExerciseStep(
        ch23_s5_easy_check,
        'Use: nx.adjacency_matrix(G).toarray().',
        'adj_matrix = nx.adjacency_matrix(G).toarray()'
    )

ch23 = Ch23()


# ====================================================
# --- CHAPTER 24: MODEL INTERPRETABILITY (XAI) -------
# ====================================================

def ch24_s1_easy_check(func):
    if not callable(func): return "Input must be a function."
    from sklearn.linear_model import LinearRegression
    X = np.array([[1.0], [2.0], [3.0], [4.0]])
    y = np.array([2.0, 4.0, 6.0, 8.0])
    model = LinearRegression().fit(X, y)
    res = func(model, X, y, random_state=42)
    if not hasattr(res, 'importances_mean'):
        return "Expected output to have 'importances_mean' attribute."
    return True

def ch24_s2_easy_check(func):
    if not callable(func): return "Input must be a function."
    shap = np.array([[1.0, -2.0], [-3.0, 4.0]])
    res = func(shap)
    if not np.allclose(res, np.array([2.0, 3.0])):
        return f"Expected mean absolute SHAP values [2.0, 3.0], got {res}."
    return True

def ch24_s3_easy_check(func):
    if not callable(func): return "Input must be a function."
    coefs = np.array([3.0, -4.0])
    stds = np.array([2.0, 0.5])
    res = func(coefs, stds)
    if not np.allclose(res, np.array([6.0, 2.0])):
        return f"Expected linear importance [6.0, 2.0], got {res}."
    return True

def ch24_s1_check(func):
    if not callable(func): return "Input must be a function."
    class DummyModel:
        def predict(self, X):
            return X[:, 0]
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]])
    y = np.array([1.0, 3.0, 5.0, 7.0])
    metric_fn = lambda y_true, y_pred: -np.mean((y_true - y_pred)**2)
    res = func(DummyModel(), X, y, metric_fn)
    if not isinstance(res, dict): return "Expected output to be a dictionary."
    if 0 not in res or 1 not in res: return "Keys must be feature indices 0 and 1."
    if not np.isclose(res[1], 0.0): return "Feature 1 is unused, its importance should be 0.0."
    if res[0] <= 0.0: return "Feature 0 is key, its importance should be positive."
    return True

def ch24_s2_check(func):
    if not callable(func): return "Input must be a function."
    class DummyModel:
        def predict(self, X):
            return X[:, 0] * 3.0 + X[:, 1]
    X = np.array([[2.0, 10.0], [4.0, 20.0]])
    res = func(DummyModel(), X, 0, [1.0, 2.0])
    # For feature 0 set to 1.0: predictions are 1*3+10=13, 1*3+20=23. Mean = 18.0
    # For feature 0 set to 2.0: predictions are 2*3+10=16, 2*3+20=26. Mean = 21.0
    if not np.allclose(res, np.array([18.0, 21.0])):
        return f"Expected partial dependencies [18.0, 21.0], got {res}."
    return True

def ch24_s3_check(func):
    if not callable(func): return "Input must be a function."
    def val_fn(subset):
        s = set(subset)
        if len(s) == 0: return 0.0
        if s == {0}: return 5.0
        if s == {1}: return 2.0
        if s == {2}: return 1.0
        if s == {0, 1}: return 8.0
        if s == {0, 2}: return 6.0
        if s == {1, 2}: return 4.0
        if s == {0, 1, 2}: return 12.0
        return 0.0
    # Shapley for 0:
    # S = empty: 1/3 * (v({0}) - v(empty)) = 1/3 * 5 = 5/3
    # S = {1}: 1/6 * (v({0,1}) - v({1})) = 1/6 * (8 - 2) = 1.0
    # S = {2}: 1/6 * (v({0,2}) - v({2})) = 1/6 * (6 - 1) = 5/6
    # S = {1,2}: 1/3 * (v({0,1,2}) - v({1,2})) = 1/3 * (12 - 4) = 8/3
    # Total = 5/3 + 1.0 + 5/6 + 8/3 = 10/6 + 6/6 + 5/6 + 16/6 = 37/6 = 6.1667
    res = func(val_fn)
    if not np.isclose(res, 37.0/6.0):
        return f"Expected Shapley value {37.0/6.0:.4f}, got {res}."
    return True

class Ch24:
    step_1 = ExerciseStep(
        ch24_s1_easy_check,
        'Use permutation_importance(model, X_test, y_test, random_state=random_state).',
        'from sklearn.inspection import permutation_importance\ndef get_permutation_importances(model, X_test, y_test, random_state=42):\n    return permutation_importance(model, X_test, y_test, random_state=random_state)'
    )
    step_2 = ExerciseStep(
        ch24_s2_easy_check,
        'Use np.mean(np.abs(shap_values), axis=0).',
        'def mean_absolute_shap(shap_values):\n    return np.mean(np.abs(shap_values), axis=0)'
    )
    step_3 = ExerciseStep(
        ch24_s3_easy_check,
        'Use np.abs(coefs) * stds.',
        'def linear_feature_importance(coefs, stds):\n    return np.abs(coefs) * stds'
    )
    step_4 = ExerciseStep(
        ch24_s1_check,
        'Shuffle feature column of a copied X, evaluate model predictions, compute metrics, and subtract from baseline metric.',
        'def permutation_importance_scratch(model, X, y, metric_fn):\n    baseline_metric = metric_fn(y, model.predict(X))\n    importances = {}\n    rng = np.random.RandomState(42)\n    for col in range(X.shape[1]):\n        X_temp = X.copy()\n        shuffled_col = X_temp[:, col].copy()\n        rng.shuffle(shuffled_col)\n        X_temp[:, col] = shuffled_col\n        shuffled_metric = metric_fn(y, model.predict(X_temp))\n        importances[col] = baseline_metric - shuffled_metric\n    return importances'
    )
    step_5 = ExerciseStep(
        ch24_s2_check,
        'Iterate over grid values, modify the feature column in a copy of X, run predictions, and calculate the mean prediction.',
        'def partial_dependence_scratch(model, X, feature_idx, grid_values):\n    dependencies = []\n    for val in grid_values:\n        X_temp = X.copy()\n        X_temp[:, feature_idx] = val\n        preds = model.predict(X_temp)\n        dependencies.append(np.mean(preds))\n    return np.array(dependencies)'
    )
    step_6 = ExerciseStep(
        ch24_s3_check,
        'Compute the weighted difference of model predictions across the 4 subsets of features: empty, {1}, {2}, and {1, 2}.',
        'def shapley_value_feature_0(val_fn):\n    # v(S U {0}) - v(S) for subsets of {1, 2}\n    val_empty = (val_fn((0,)) - val_fn(())) * (1.0/3.0)\n    val_1 = (val_fn((0, 1)) - val_fn((1,))) * (1.0/6.0)\n    val_2 = (val_fn((0, 2)) - val_fn((2,))) * (1.0/6.0)\n    val_1_2 = (val_fn((0, 1, 2)) - val_fn((1, 2))) * (1.0/3.0)\n    return val_empty + val_1 + val_2 + val_1_2'
    )

    step_7 = ExerciseStep(
        ch24_s4_easy_check,
        'Use: trained_linear_model.coef_.',
        'coef_weights = trained_linear_model.coef_'
    )
    step_8 = ExerciseStep(
        ch24_s5_easy_check,
        'Use: shap.TreeExplainer(trained_rf_interpret).',
        'import shap\nexplainer = shap.TreeExplainer(trained_rf_interpret)'
    )

ch24 = Ch24()


# ==========================================
# --- PROJECT 1: CUSTOMER CHURN (CLASS) ----
# ==========================================

def proj1_s1_check(func):
    if not callable(func): return "Input must be a function."
    try:
        rate = func("data/customer_churn.csv")
    except Exception as e:
        return f"Error executing function: {str(e)}"
    df = pd.read_csv("data/customer_churn.csv")
    expected = df['Churn'].mean()
    if not np.isclose(rate, expected):
        return f"Expected churn rate {expected:.4f}, but got {rate}."
    return True

def proj1_s2_check(func):
    if not callable(func): return "Input must be a function."
    df = pd.DataFrame({
        'CustomerID': [1, 2, 3],
        'Age': [20, 30, 40],
        'Tenure': [5, 10, 15],
        'UsageFrequency': [2, 4, 6],
        'SupportCalls': [1, 0, 2],
        'Churn': [0, 1, 0]
    })
    try:
        X_scaled, y = func(df)
    except Exception as e:
        return f"Error running preprocess_churn_data: {str(e)}"
    if not isinstance(X_scaled, np.ndarray): return "X_scaled should be a numpy array."
    if X_scaled.shape != (3, 4): return f"Expected shape (3, 4), got {X_scaled.shape}."
    if not np.isclose(np.mean(X_scaled, axis=0), 0.0).all():
        return "Features are not scaled to 0 mean."
    if not np.allclose(y, np.array([0, 1, 0])):
        return "Target array y is incorrect."
    return True

def proj1_s3_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(100, 4)
    y_train = np.random.randint(0, 2, 100)
    X_test = np.random.randn(20, 4)
    y_test = np.random.randint(0, 2, 20)
    try:
        model, score = func(X_train, X_test, y_train, y_test)
    except Exception as e:
        return f"Error running train_churn_model: {str(e)}"
    from sklearn.ensemble import RandomForestClassifier
    if not isinstance(model, RandomForestClassifier):
        return "Model should be a RandomForestClassifier."
    if not isinstance(score, (float, np.floating)):
        return "Score should be a float."
    return True

def proj1_s4_check(func):
    if not callable(func): return "Input must be a function."
    y_true = np.array([0, 0, 1, 1, 1])
    probs = np.array([0.1, 0.2, 0.4, 0.6, 0.8])
    try:
        best_thresh, best_f1 = func(y_true, probs)
    except Exception as e:
        return f"Error running tune_threshold: {str(e)}"
    if not np.isclose(best_f1, 1.0):
        return f"Expected max F1 of 1.0, got {best_f1}."
    if not np.isclose(best_thresh, 0.3) and not np.isclose(best_thresh, 0.4) and not np.isclose(best_thresh, 0.2):
        return f"Expected threshold around 0.3 or 0.4, got {best_thresh}."
    return True

def proj1_s5_check(func):
    if not callable(func): return "Input must be a function."
    try:
        X, y = func("data/titanic.csv")
    except Exception as e:
        return f"Error executing preprocess_titanic: {str(e)}"
    df = pd.read_csv("data/titanic.csv")
    expected_age = df['Age'].fillna(df['Age'].median())
    expected_sex = df['Sex'].map({'male': 0, 'female': 1})
    expected_y = df['Survived'].values
    if not isinstance(X, pd.DataFrame): return "X must be a pandas DataFrame."
    if 'PassengerId' in X.columns or 'Embarked' in X.columns or 'Survived' in X.columns:
        return "X should not contain PassengerId, Embarked, or Survived columns."
    if not np.allclose(X['Age'].values, expected_age.values, equal_nan=True):
        return "Imputed Age values are incorrect."
    if not np.allclose(X['Sex'].values, expected_sex.values):
        return "Sex mapping is incorrect."
    if not np.array_equal(y, expected_y):
        return "Target array y is incorrect."
    return True

def proj1_s6_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(80, 4)
    y_train = np.random.randint(0, 2, 80)
    X_test = np.random.randn(20, 4)
    y_test = np.random.randint(0, 2, 20)
    try:
        model, acc = func(X_train, X_test, y_train, y_test)
    except Exception as e:
        return f"Error executing train_titanic_svm: {str(e)}"
    from sklearn.svm import SVC
    if not isinstance(model, SVC): return "Model must be a Support Vector Classifier (SVC)."
    if model.kernel != 'rbf': return "SVC must use the RBF kernel."
    if not isinstance(acc, (float, np.floating)): return "test_accuracy must be a float."
    return True

class Proj1:
    step_1 = ExerciseStep(
        proj1_s1_check,
        'Use pd.read_csv(file_path), then compute the mean of the Churn column.',
        'def get_churn_rate(file_path):\n    df = pd.read_csv(file_path)\n    return df["Churn"].mean()'
    )
    step_2 = ExerciseStep(
        proj1_s2_check,
        'Drop CustomerID and Churn for features X, use Churn for y. Fit and transform X using StandardScaler.',
        'from sklearn.preprocessing import StandardScaler\ndef preprocess_churn_data(df):\n    X = df.drop(columns=["CustomerID", "Churn"])\n    y = df["Churn"].values\n    scaler = StandardScaler()\n    X_scaled = scaler.fit_transform(X)\n    return X_scaled, y'
    )
    step_3 = ExerciseStep(
        proj1_s3_check,
        'Fit a RandomForestClassifier(random_state=42) on training set, calculate classification_report or f1_score on test predictions.',
        'from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import f1_score\ndef train_churn_model(X_train, X_test, y_train, y_test):\n    model = RandomForestClassifier(random_state=42)\n    model.fit(X_train, y_train)\n    preds = model.predict(X_test)\n    score = f1_score(y_test, preds)\n    return model, score'
    )
    step_4 = ExerciseStep(
        proj1_s4_check,
        'Loop over thresholds from 0.1 to 0.9. Convert probs to predictions, calculate f1_score, and keep track of the max.',
        'from sklearn.metrics import f1_score\ndef tune_threshold(y_true, probs):\n    best_f1 = -1\n    best_thresh = None\n    for t in np.arange(0.1, 1.0, 0.1):\n        preds = (probs >= t).astype(int)\n        score = f1_score(y_true, preds)\n        if score > best_f1:\n            best_f1 = score\n            best_thresh = t\n    return best_thresh, best_f1'
    )
    step_5 = ExerciseStep(
        proj1_s5_check,
        'Load csv, fillna Age with median, map Sex, drop PassengerId and Embarked, return X (df) and y (array).',
        'def preprocess_titanic(file_path):\n    df = pd.read_csv(file_path)\n    df["Age"] = df["Age"].fillna(df["Age"].median())\n    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})\n    X = df.drop(columns=["PassengerId", "Embarked", "Survived"])\n    y = df["Survived"].values\n    return X, y'
    )
    step_6 = ExerciseStep(
        proj1_s6_check,
        'Fit SVC(kernel="rbf", C=1.0, random_state=42) on X_train and evaluate accuracy on test.',
        'from sklearn.svm import SVC\nfrom sklearn.metrics import accuracy_score\ndef train_titanic_svm(X_train, X_test, y_train, y_test):\n    model = SVC(kernel="rbf", C=1.0, random_state=42)\n    model.fit(X_train, y_train)\n    preds = model.predict(X_test)\n    acc = accuracy_score(y_test, preds)\n    return model, acc'
    )

proj1 = Proj1()


# ==========================================
# --- PROJECT 2: HOUSING PRICES (REG) ------
# ==========================================

def proj2_s1_check(func):
    if not callable(func): return "Input must be a function."
    try:
        df = func('data/housing.csv')
    except Exception as e:
        return f"Error running engineer_housing_features: {str(e)}"
    if not isinstance(df, pd.DataFrame): return "Expected output to be a pandas DataFrame."
    if 'Price_per_SqFt' not in df.columns or 'Bedrooms_per_Area' not in df.columns:
        return "Missing engineered columns 'Price_per_SqFt' and 'Bedrooms_per_Area'."
    first_row = df.iloc[0]
    expected_ppsf = first_row['Price'] / first_row['Area']
    expected_bpa = first_row['Bedrooms'] / first_row['Area']
    if not np.isclose(first_row['Price_per_SqFt'], expected_ppsf) or not np.isclose(first_row['Bedrooms_per_Area'], expected_bpa):
        return "Calculated engineered features values are incorrect."
    return True

def proj2_s2_check(func):
    if not callable(func): return "Input must be a function."
    X = np.random.randn(50, 3)
    y = X[:, 0] * 2.0 + np.random.randn(50) * 0.1
    try:
        best_alpha = func(X, y)
    except Exception as e:
        return f"Error running tune_ridge: {str(e)}"
    if best_alpha not in [0.1, 1.0, 10.0, 100.0]:
        return f"Returned alpha {best_alpha} is not in the grid list [0.1, 1.0, 10.0, 100.0]."
    return True

def proj2_s3_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(60, 4)
    y_train = np.random.randn(60)
    try:
        best_params = func(X_train, y_train)
    except Exception as e:
        return f"Error running optuna_tune_rf: {str(e)}"
    if not isinstance(best_params, dict):
        return "Expected output to be a dictionary."
    if 'n_estimators' not in best_params or 'max_depth' not in best_params:
        return "Expected keys 'n_estimators' and 'max_depth' in best_params."
    if not (10 <= best_params['n_estimators'] <= 50):
        return f"n_estimators {best_params['n_estimators']} is out of bounds [10, 50]."
    if not (3 <= best_params['max_depth'] <= 10):
        return f"max_depth {best_params['max_depth']} is out of bounds [3, 10]."
    return True

def proj2_s4_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(50, 4)
    y_train = X_train[:, 0] * 3.0 + np.random.randn(50) * 0.1
    X_test = np.random.randn(15, 4)
    y_test = X_test[:, 0] * 3.0 + np.random.randn(15) * 0.1
    try:
        model, r2 = func(X_train, X_test, y_train, y_test)
    except Exception as e:
        return f"Error executing baseline_regression: {str(e)}"
    from sklearn.linear_model import LinearRegression
    if not isinstance(model, LinearRegression): return "Model must be a LinearRegression instance."
    if not isinstance(r2, (float, np.floating)): return "R2 score must be a float."
    return True

def proj2_s5_check(func):
    if not callable(func): return "Input must be a function."
    X = np.array([
        [1.0, 0.0, 100.0],
        [2.0, 0.0, 200.0],
        [3.0, 0.0, 300.0],
        [4.0, 0.0, 400.0]
    ])
    y = np.array([10.0, 20.0, 30.0, 40.0])
    feature_names = ['feat1', 'feat2', 'feat3']
    try:
        selected = func(X, y, feature_names)
    except Exception as e:
        return f"Error executing lasso_feature_selection: {str(e)}"
    if not isinstance(selected, list): return "Expected output to be a list."
    from sklearn.linear_model import Lasso
    m = Lasso(alpha=10.0, random_state=42).fit(X, y)
    expected = [feature_names[i] for i in np.where(m.coef_ != 0)[0]]
    if selected != expected:
        return f"Expected {expected}, got {selected}."
    return True

def proj2_s6_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(50, 4)
    y_train = np.random.randn(50)
    X_test = np.random.randn(15, 4)
    y_test = np.random.randn(15)
    try:
        model, r2 = func(X_train, X_test, y_train, y_test)
    except Exception as e:
        return f"Error executing train_gbdt: {str(e)}"
    from sklearn.ensemble import GradientBoostingRegressor
    if not isinstance(model, GradientBoostingRegressor): return "Model must be a GradientBoostingRegressor."
    if model.n_estimators != 50 or model.max_depth != 4:
        return "GradientBoostingRegressor must have n_estimators=50 and max_depth=4."
    if not isinstance(r2, (float, np.floating)): return "R2 score must be a float."
    return True

class Proj2:
    step_1 = ExerciseStep(
        proj2_s1_check,
        'Use pd.read_csv(file_path) and assign df["Price_per_SqFt"] = df["Price"] / df["Area"], etc.',
        'def engineer_housing_features(file_path):\n    df = pd.read_csv(file_path)\n    df["Price_per_SqFt"] = df["Price"] / df["Area"]\n    df["Bedrooms_per_Area"] = df["Bedrooms"] / df["Area"]\n    return df'
    )
    step_2 = ExerciseStep(
        proj2_s2_check,
        'Use GridSearchCV(Ridge(), param_grid={"alpha": [0.1, 1.0, 10.0, 100.0]}, cv=5, scoring="neg_mean_squared_error").',
        'from sklearn.linear_model import Ridge\nfrom sklearn.model_selection import GridSearchCV\ndef tune_ridge(X, y):\n    grid = GridSearchCV(Ridge(), param_grid={"alpha": [0.1, 1.0, 10.0, 100.0]}, cv=5, scoring="neg_mean_squared_error")\n    grid.fit(X, y)\n    return grid.best_params_["alpha"]'
    )
    step_3 = ExerciseStep(
        proj2_s3_check,
        'Define objective taking a trial. Suggest n_estimators (10..50) and max_depth (3..10). Cross-validate and return mean R2 or negative MSE. Optimize study for 20 trials.',
        'import optuna\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.model_selection import cross_val_score\ndef optuna_tune_rf(X_train, y_train):\n    def objective(trial):\n        n_est = trial.suggest_int("n_estimators", 10, 50)\n        depth = trial.suggest_int("max_depth", 3, 10)\n        model = RandomForestRegressor(n_estimators=n_est, max_depth=depth, random_state=42)\n        score = np.mean(cross_val_score(model, X_train, y_train, cv=3))\n        return score\n    study = optuna.create_study(direction="maximize")\n    study.optimize(objective, n_trials=20)\n    return study.best_params'
    )
    step_4 = ExerciseStep(
        proj2_s4_check,
        'Fit default LinearRegression() and evaluate R2 score on test.',
        'from sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import r2_score\ndef baseline_regression(X_train, X_test, y_train, y_test):\n    model = LinearRegression()\n    model.fit(X_train, y_train)\n    preds = model.predict(X_test)\n    r2 = r2_score(y_test, preds)\n    return model, r2'
    )
    step_5 = ExerciseStep(
        proj2_s5_check,
        'Fit Lasso(alpha=10.0, random_state=42) and return list of features with non-zero coefficients.',
        'from sklearn.linear_model import Lasso\ndef lasso_feature_selection(X, y, feature_names):\n    model = Lasso(alpha=10.0, random_state=42)\n    model.fit(X, y)\n    non_zero = np.where(model.coef_ != 0)[0]\n    return [feature_names[i] for i in non_zero]'
    )
    step_6 = ExerciseStep(
        proj2_s6_check,
        'Fit GradientBoostingRegressor(n_estimators=50, max_depth=4, random_state=42) and evaluate R2 on test.',
        'from sklearn.ensemble import GradientBoostingRegressor\nfrom sklearn.metrics import r2_score\ndef train_gbdt(X_train, X_test, y_train, y_test):\n    model = GradientBoostingRegressor(n_estimators=50, max_depth=4, random_state=42)\n    model.fit(X_train, y_train)\n    preds = model.predict(X_test)\n    r2 = r2_score(y_test, preds)\n    return model, r2'
    )

proj2 = Proj2()


# ==========================================
# --- PROJECT 3: SENTIMENT ANALYSIS (NLP) --
# ==========================================

def proj3_s1_check(func):
    if not callable(func): return "Input must be a function."
    try:
        words = func("Hello, World! This is a test.")
    except Exception as e:
        return f"Error running clean_text: {str(e)}"
    if not isinstance(words, list): return "Expected a list of strings."
    expected = ["hello", "world", "this", "is", "a", "test"]
    if words != expected:
        return f"Expected {expected}, got {words}."
    return True

def proj3_s2_check(func):
    if not callable(func): return "Input must be a function."
    try:
        X, y = func('data/text_sentiment.csv')
    except Exception as e:
        return f"Error running extract_tfidf_features: {str(e)}"
    df = pd.read_csv('data/text_sentiment.csv')
    if X.shape[0] != len(df) or X.shape[1] > 100:
        return f"Expected feature matrix shape ({len(df)}, <=100), got {X.shape}."
    if len(y) != len(df):
        return f"Expected labels length {len(df)}, got {len(y)}."
    return True

def proj3_s3_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.rand(80, 50)
    y_train = np.random.randint(0, 2, 80)
    X_test = np.random.rand(20, 50)
    y_test = np.random.randint(0, 2, 20)
    try:
        acc = func(X_train, X_test, y_train, y_test)
    except Exception as e:
        return f"Error running train_sentiment_model: {str(e)}"
    if not isinstance(acc, (float, np.floating)):
        return "Expected accuracy to be a float."
    if not (0.0 <= acc <= 1.0):
        return f"Expected accuracy in [0.0, 1.0], got {acc}."
    return True

def proj3_s4_check(func):
    if not callable(func): return "Input must be a function."
    class DummyModel:
        def predict(self, X):
            return (X[:, 0] > 0.5).astype(int)
    X_test = np.array([
        [0.8, 0.1],
        [0.2, 0.9],
        [0.9, 0.4],
        [0.1, 0.7]
    ])
    y_test = np.array([1, 0, 1, 0])
    try:
        importances = func(DummyModel(), X_test, y_test)
    except Exception as e:
        return f"Error running sentiment_feature_importance: {str(e)}"
    if not isinstance(importances, dict):
        return "Expected a dictionary."
    if 0 not in importances or 1 not in importances:
        return "Dictionary keys should be feature indices 0 and 1."
    if importances[1] != 0.0:
        return f"Feature 1 is not used by the model, its drop should be 0.0, got {importances[1]}."
    if importances[0] <= 0.0:
        return f"Feature 0 is key, its drop should be positive, got {importances[0]}."
    return True

def proj3_s5_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(80, 20)
    y_train = np.random.randint(0, 2, 80)
    X_test = np.random.randn(20, 20)
    y_test = np.random.randint(0, 2, 20)
    try:
        model, acc = func(X_train, X_test, y_train, y_test)
    except Exception as e:
        return f"Error executing train_logistic_regression: {str(e)}"
    from sklearn.linear_model import LogisticRegression
    if not isinstance(model, LogisticRegression): return "Model must be a LogisticRegression instance."
    if not isinstance(acc, (float, np.floating)): return "Accuracy must be a float."
    return True

def proj3_s6_check(func):
    if not callable(func): return "Input must be a function."
    class DummyLR:
        coef_ = np.array([[0.1, 0.9, -0.4, 1.2, 0.5]])
    feature_names = ['word0', 'word1', 'word2', 'word3', 'word4']
    try:
        top_words = func(DummyLR(), feature_names, top_n=3)
    except Exception as e:
        return f"Error executing get_top_positive_words: {str(e)}"
    expected = ['word3', 'word1', 'word4']
    if top_words != expected:
        return f"Expected {expected}, got {top_words}."
    return True

class Proj3:
    step_1 = ExerciseStep(
        proj3_s1_check,
        'Use text.lower(), re.sub(r"[^\\w\\s]", "", text), and text.split().',
        'import re\ndef clean_text(text):\n    text_clean = re.sub(r"[^\\w\\s]", "", text.lower())\n    return text_clean.split()'
    )
    step_2 = ExerciseStep(
        proj3_s2_check,
        'Load csv, instantiate TfidfVectorizer(max_features=100), call fit_transform(df["Text"]) and convert to dense array.',
        'from sklearn.feature_extraction.text import TfidfVectorizer\ndef extract_tfidf_features(file_path):\n    df = pd.read_csv(file_path)\n    vec = TfidfVectorizer(max_features=100)\n    X = vec.fit_transform(df["Text"]).toarray()\n    y = df["Sentiment"].values\n    return X, y'
    )
    step_3 = ExerciseStep(
        proj3_s3_check,
        'Instantiate MultinomialNB(), call fit(X_train, y_train), compute score(X_test, y_test) accuracy.',
        'from sklearn.naive_bayes import MultinomialNB\ndef train_sentiment_model(X_train, X_test, y_train, y_test):\n    clf = MultinomialNB()\n    clf.fit(X_train, y_train)\n    return clf.score(X_test, y_test)'
    )
    step_4 = ExerciseStep(
        proj3_s4_check,
        'Calculate baseline accuracy, shuffle each column index in a copy of X_test, calculate accuracy, and record the difference.',
        'from sklearn.metrics import accuracy_score\ndef sentiment_feature_importance(model, X_test, y_test):\n    baseline_acc = accuracy_score(y_test, model.predict(X_test))\n    importances = {}\n    rng = np.random.RandomState(42)\n    for col in range(X_test.shape[1]):\n        X_temp = X_test.copy()\n        shuffled_col = X_temp[:, col].copy()\n        rng.shuffle(shuffled_col)\n        X_temp[:, col] = shuffled_col\n        shuffled_acc = accuracy_score(y_test, model.predict(X_temp))\n        importances[col] = baseline_acc - shuffled_acc\n    return importances'
    )
    step_5 = ExerciseStep(
        proj3_s5_check,
        'Fit LogisticRegression(random_state=42) on X_train and evaluate accuracy on test.',
        'from sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import accuracy_score\ndef train_logistic_regression(X_train, X_test, y_train, y_test):\n    model = LogisticRegression(random_state=42)\n    model.fit(X_train, y_train)\n    preds = model.predict(X_test)\n    acc = accuracy_score(y_test, preds)\n    return model, acc'
    )
    step_6 = ExerciseStep(
        proj3_s6_check,
        'Extract coefficients, find top positive words, and return their names in sorted list.',
        'def get_top_positive_words(model, feature_names, top_n=5):\n    coefs = model.coef_[0]\n    top_indices = np.argsort(coefs)[::-1][:top_n]\n    return [feature_names[i] for i in top_indices]'
    )

proj3 = Proj3()




# ==========================================
# --- PROJECT 4: IRIS CLASSIFICATION -------
# ==========================================

def proj4_s1_check(func):
    if not callable(func): return "Input must be a function."
    try:
        shape, counts = func("data/iris.csv")
    except Exception as e:
        return f"Error executing load_iris_data: {str(e)}"
    import pandas as pd
    df = pd.read_csv("data/iris.csv")
    expected_shape = df.shape
    expected_counts = df['Species'].value_counts()
    if shape != expected_shape:
        return f"Expected shape {expected_shape}, got {shape}."
    if not counts.equals(expected_counts):
        return f"Expected species counts:\n{expected_counts}\n\nGot:\n{counts}"
    return True

def proj4_s2_check(func):
    if not callable(func): return "Input must be a function."
    import pandas as pd
    df = pd.DataFrame({'Species': ['setosa', 'versicolor', 'virginica', 'setosa']})
    try:
        encoded = func(df)
    except Exception as e:
        return f"Error running encode_species: {str(e)}"
    expected = np.array([0, 1, 2, 0])
    if not np.array_equal(encoded, expected):
        return f"Expected {expected}, got {encoded}."
    return True

def proj4_s3_check(func):
    if not callable(func): return "Input must be a function."
    import pandas as pd
    df = pd.DataFrame({
        'SepalLength': [5.0, 6.0, 7.0],
        'SepalWidth': [3.0, 2.5, 3.2],
        'PetalLength': [1.5, 4.0, 6.0],
        'PetalWidth': [0.2, 1.3, 2.0],
        'Species': ['setosa', 'versicolor', 'virginica']
    })
    try:
        X_scaled, y = func(df)
    except Exception as e:
        return f"Error running scale_iris_features: {str(e)}"
    if not isinstance(X_scaled, np.ndarray): return "X_scaled must be a numpy array."
    if X_scaled.shape != (3, 4): return f"Expected feature shape (3, 4), got {X_scaled.shape}."
    if not np.isclose(np.mean(X_scaled, axis=0), 0.0).all():
        return "Features are not standard scaled to 0 mean."
    if not np.array_equal(y, np.array(['setosa', 'versicolor', 'virginica'])):
        return "Species labels array y is incorrect."
    return True

def proj4_s4_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(80, 4)
    y_train = np.random.randint(0, 3, 80)
    X_test = np.random.randn(20, 4)
    y_test = np.random.randint(0, 3, 20)
    try:
        model, acc = func(X_train, X_test, y_train, y_test)
    except Exception as e:
        return f"Error running train_iris_dt: {str(e)}"
    from sklearn.tree import DecisionTreeClassifier
    if not isinstance(model, DecisionTreeClassifier): return "Model must be a DecisionTreeClassifier."
    if model.max_depth != 3: return "DecisionTreeClassifier must have max_depth=3."
    if not isinstance(acc, (float, np.floating)): return "Accuracy must be a float."
    return True

def proj4_s5_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(80, 4)
    y_train = np.random.randint(0, 3, 80)
    X_test = np.random.randn(20, 4)
    y_test = np.random.randint(0, 3, 20)
    try:
        acc = func(X_train, X_test, y_train, y_test)
    except Exception as e:
        return f"Error running train_iris_nb: {str(e)}"
    if not isinstance(acc, (float, np.floating)): return "Accuracy must be a float."
    return True

def proj4_s6_check(func):
    if not callable(func): return "Input must be a function."
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([0, 1, 1, 1, 2, 0])
    try:
        f1s = func(y_true, y_pred)
    except Exception as e:
        return f"Error running get_multiclass_metrics: {str(e)}"
    if not isinstance(f1s, dict): return "Expected a dictionary mapping class label to F1-score."
    from sklearn.metrics import precision_recall_fscore_support
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, average=None)
    expected = {0: f[0], 1: f[1], 2: f[2]}
    for k in expected:
        if k not in f1s or not np.isclose(f1s[k], expected[k]):
            return f"Mismatch for class {k}. Expected F1 {expected[k]:.4f}, got {f1s.get(k)}."
    return True

class Proj4:
    step_1 = ExerciseStep(
        proj4_s1_check,
        'Use pd.read_csv(file_path), then return df.shape and df["Species"].value_counts().',
        'def load_iris_data(file_path):\n    df = pd.read_csv(file_path)\n    return df.shape, df["Species"].value_counts()'
    )
    step_2 = ExerciseStep(
        proj4_s2_check,
        'Use df["Species"].map({"setosa": 0, "versicolor": 1, "virginica": 2}).values.',
        'def encode_species(df):\n    return df["Species"].map({"setosa": 0, "versicolor": 1, "virginica": 2}).values'
    )
    step_3 = ExerciseStep(
        proj4_s3_check,
        'Separate features X and target y. Fit and transform features with StandardScaler and return (X_scaled, y).',
        'from sklearn.preprocessing import StandardScaler\ndef scale_iris_features(df):\n    X = df.drop(columns=["Species"])\n    y = df["Species"].values\n    scaler = StandardScaler()\n    X_scaled = scaler.fit_transform(X)\n    return X_scaled, y'
    )
    step_4 = ExerciseStep(
        proj4_s4_check,
        'Fit DecisionTreeClassifier(max_depth=3, random_state=42) on train data and return (model, accuracy_score(y_test, preds)).',
        'from sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\ndef train_iris_dt(X_train, X_test, y_train, y_test):\n    model = DecisionTreeClassifier(max_depth=3, random_state=42)\n    model.fit(X_train, y_train)\n    preds = model.predict(X_test)\n    acc = accuracy_score(y_test, preds)\n    return model, acc'
    )
    step_5 = ExerciseStep(
        proj4_s5_check,
        'Fit GaussianNB() on train data and return accuracy score on test set.',
        'from sklearn.naive_bayes import GaussianNB\ndef train_iris_nb(X_train, X_test, y_train, y_test):\n    model = GaussianNB()\n    model.fit(X_train, y_train)\n    return model.score(X_test, y_test)'
    )
    step_6 = ExerciseStep(
        proj4_s6_check,
        'Compute precision, recall, f1-score using precision_recall_fscore_support and map class integers to f1-scores.',
        'from sklearn.metrics import precision_recall_fscore_support\ndef get_multiclass_metrics(y_true, y_pred):\n    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, average=None)\n    return {i: f[i] for i in range(len(f))}'
    )

proj4 = Proj4()


# ==========================================
# --- PROJECT 5: CUSTOMER SEGMENTATION -----
# ==========================================

def proj5_s1_check(func):
    if not callable(func): return "Input must be a function."
    try:
        scaled = func("data/customer_churn.csv")
    except Exception as e:
        return f"Error executing get_clustering_data: {str(e)}"
    if not isinstance(scaled, np.ndarray): return "Output must be a numpy array."
    import pandas as pd
    df = pd.read_csv("data/customer_churn.csv")
    expected_cols = df.shape[1] - 2
    if scaled.shape[1] != expected_cols:
        return f"Expected {expected_cols} feature columns, got {scaled.shape[1]}."
    if not np.isclose(scaled.min(), 0.0) or not np.isclose(scaled.max(), 1.0):
        return "Features do not appear to be MinMaxScaler scaled to [0, 1] range."
    return True

def proj5_s2_check(func):
    if not callable(func): return "Input must be a function."
    X = np.random.rand(50, 4)
    try:
        inertias = func(X, max_k=4)
    except Exception as e:
        return f"Error running calculate_elbow_inertia: {str(e)}"
    if not isinstance(inertias, list): return "Expected a list of inertias."
    if len(inertias) != 4: return f"Expected 4 inertia values, got {len(inertias)}."
    return True

def proj5_s3_check(func):
    if not callable(func): return "Input must be a function."
    X = np.random.rand(50, 4)
    try:
        labels = func(X, k=3)
    except Exception as e:
        return f"Error running train_kmeans: {str(e)}"
    if not isinstance(labels, np.ndarray): return "Output labels must be a numpy array."
    if len(labels) != 50: return f"Expected 50 labels, got {len(labels)}."
    unique = np.unique(labels)
    if not set(unique).issubset({0, 1, 2}):
        return f"Cluster labels should be integers from 0 to 2, got {unique}."
    return True

def proj5_s4_check(func):
    if not callable(func): return "Input must be a function."
    X = np.array([[1.0, 1.0], [1.1, 1.1], [5.0, 5.0], [5.1, 5.1]])
    labels = np.array([0, 0, 1, 1])
    try:
        score = func(X, labels)
    except Exception as e:
        return f"Error running evaluate_silhouette: {str(e)}"
    from sklearn.metrics import silhouette_score
    expected = silhouette_score(X, labels)
    if not np.isclose(score, expected):
        return f"Expected silhouette score {expected:.4f}, got {score}."
    return True

def proj5_s5_check(func):
    if not callable(func): return "Input must be a function."
    X = np.random.rand(50, 4)
    try:
        X_pca = func(X, n_components=2)
    except Exception as e:
        return f"Error running apply_pca: {str(e)}"
    if not isinstance(X_pca, np.ndarray): return "Output must be a numpy array."
    if X_pca.shape != (50, 2): return f"Expected shape (50, 2), got {X_pca.shape}."
    return True

def proj5_s6_check(func):
    if not callable(func): return "Input must be a function."
    import pandas as pd
    df = pd.DataFrame({
        'Age': [20, 30, 40],
        'Tenure': [5, 10, 15]
    })
    labels = np.array([0, 1, 0])
    try:
        profiles = func(df, labels)
    except Exception as e:
        return f"Error running get_cluster_profiles: {str(e)}"
    if not isinstance(profiles, pd.DataFrame): return "Expected a pandas DataFrame."
    if profiles.shape[0] != 2: return f"Expected 2 rows (for 2 clusters), got {profiles.shape[0]}."
    return True

class Proj5:
    step_1 = ExerciseStep(
        proj5_s1_check,
        'Load csv, drop CustomerID and Churn, apply MinMaxScaler and return dense scaled array.',
        'from sklearn.preprocessing import MinMaxScaler\ndef get_clustering_data(file_path):\n    df = pd.read_csv(file_path)\n    X = df.drop(columns=["CustomerID", "Churn"])\n    scaler = MinMaxScaler()\n    return scaler.fit_transform(X)'
    )
    step_2 = ExerciseStep(
        proj5_s2_check,
        'Loop k from 1 to max_k, train KMeans(n_clusters=k, random_state=42) and record inertia_.',
        'from sklearn.cluster import KMeans\ndef calculate_elbow_inertia(X, max_k=6):\n    return [KMeans(n_clusters=k, random_state=42).fit(X).inertia_ for k in range(1, max_k + 1)]'
    )
    step_3 = ExerciseStep(
        proj5_s3_check,
        'Fit KMeans(n_clusters=k, random_state=42) and return its labels_ array.',
        'from sklearn.cluster import KMeans\ndef train_kmeans(X, k=3):\n    model = KMeans(n_clusters=k, random_state=42)\n    model.fit(X)\n    return model.labels_'
    )
    step_4 = ExerciseStep(
        proj5_s4_check,
        'Compute silhouette_score using sklearn.metrics.',
        'from sklearn.metrics import silhouette_score\ndef evaluate_silhouette(X, labels):\n    return silhouette_score(X, labels)'
    )
    step_5 = ExerciseStep(
        proj5_s5_check,
        'Fit PCA(n_components=n_components) and transform features.',
        'from sklearn.decomposition import PCA\ndef apply_pca(X, n_components=2):\n    return PCA(n_components=n_components).fit_transform(X)'
    )
    step_6 = ExerciseStep(
        proj5_s6_check,
        'Assign Cluster labels to df, group by Cluster, and return the feature means DataFrame.',
        'def get_cluster_profiles(df, labels):\n    df_copy = df.copy()\n    df_copy["Cluster"] = labels\n    return df_copy.groupby("Cluster").mean()'
    )

proj5 = Proj5()


# ==========================================
# --- PROJECT 6: DAILY SALES FORECASTING ---
# ==========================================

def proj6_s1_check(func):
    if not callable(func): return "Input must be a function."
    try:
        series = func("data/daily_sales.csv")
    except Exception as e:
        return f"Error executing load_sales_data: {str(e)}"
    import pandas as pd
    if not isinstance(series, pd.Series): return "Expected output to be a pandas Series."
    if not isinstance(series.index, pd.DatetimeIndex): return "Series index must be a DatetimeIndex."
    if len(series) != 365: return f"Expected 365 sales records, got {len(series)}."
    return True

def proj6_s2_check(func):
    if not callable(func): return "Input must be a function."
    import pandas as pd
    s = pd.Series([10.0, 20.0, 30.0, 40.0])
    try:
        mean, std = func(s, window=2)
    except Exception as e:
        return f"Error running compute_rolling_sales: {str(e)}"
    if not isinstance(mean, pd.Series) or not isinstance(std, pd.Series):
        return "Outputs must be pandas Series."
    expected_mean = s.rolling(window=2).mean()
    expected_std = s.rolling(window=2).std()
    if not np.allclose(mean.dropna().values, expected_mean.dropna().values):
        return "Rolling mean values are incorrect."
    if not np.allclose(std.dropna().values, expected_std.dropna().values):
        return "Rolling standard deviation values are incorrect."
    return True

def proj6_s3_check(func):
    if not callable(func): return "Input must be a function."
    s = pd.Series(np.random.normal(0, 1, 100))
    try:
        p_val = func(s)
    except Exception as e:
        return f"Error running check_sales_stationarity: {str(e)}"
    from statsmodels.tsa.stattools import adfuller
    expected = adfuller(s)[1]
    if not np.isclose(p_val, expected):
        return f"Expected p-value {expected:.4f}, got {p_val}."
    return True

def proj6_s4_check(func):
    if not callable(func): return "Input must be a function."
    s = pd.Series([1, 2, 4, 7])
    try:
        diff = func(s, order=1)
    except Exception as e:
        return f"Error running difference_sales: {str(e)}"
    expected = s.diff(1).dropna()
    if not np.array_equal(diff.values, expected.values):
        return f"Expected {expected.values}, got {diff.values}."
    return True

def proj6_s5_check(func):
    if not callable(func): return "Input must be a function."
    s = pd.Series(np.random.normal(10, 1, 50))
    try:
        model = func(s, order=(1,0,0))
    except Exception as e:
        return f"Error running fit_arima_sales: {str(e)}"
    from statsmodels.tsa.arima.model import ARIMAResultsWrapper
    if not isinstance(model, ARIMAResultsWrapper):
        return "Expected fitted ARIMA model results."
    return True

def proj6_s6_check(func):
    if not callable(func): return "Input must be a function."
    y_true = np.array([100.0, 200.0])
    y_pred = np.array([90.0, 220.0])
    try:
        mape = func(y_true, y_pred)
    except Exception as e:
        return f"Error running evaluate_forecast_mape: {str(e)}"
    expected = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    if not np.isclose(mape, expected):
        return f"Expected MAPE {expected:.4f}%, got {mape:.4f}%."
    return True

class Proj6:
    step_1 = ExerciseStep(
        proj6_s1_check,
        'Load csv, parse Date, set index Date, and return the Sales Series.',
        'def load_sales_data(file_path):\n    df = pd.read_csv(file_path)\n    df["Date"] = pd.to_datetime(df["Date"])\n    df.set_index("Date", inplace=True)\n    return df["Sales"]'
    )
    step_2 = ExerciseStep(
        proj6_s2_check,
        'Use rolling(window=window).mean() and rolling(window=window).std().',
        'def compute_rolling_sales(series, window=7):\n    return series.rolling(window).mean(), series.rolling(window).std()'
    )
    step_3 = ExerciseStep(
        proj6_s3_check,
        'Use adfuller(series) from statsmodels.tsa.stattools and return p-value at index 1.',
        'from statsmodels.tsa.stattools import adfuller\ndef check_sales_stationarity(series):\n    return adfuller(series)[1]'
    )
    step_4 = ExerciseStep(
        proj6_s4_check,
        'Use series.diff(order).dropna().',
        'def difference_sales(series, order=1):\n    return series.diff(order).dropna()'
    )
    step_5 = ExerciseStep(
        proj6_s5_check,
        'Instantiate ARIMA(series, order=order) and call fit().',
        'from statsmodels.tsa.arima.model import ARIMA\ndef fit_arima_sales(series, order=(1,1,1)):\n    model = ARIMA(series, order=order)\n    return model.fit()'
    )
    step_6 = ExerciseStep(
        proj6_s6_check,
        'Calculate mean absolute percentage error as float percentage value.',
        'def evaluate_forecast_mape(y_true, y_pred):\n    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100'
    )

proj6 = Proj6()


# ==========================================
# --- PROJECT 7: FRAUD DETECTION -----------
# ==========================================

def proj7_s1_check(func):
    if not callable(func): return "Input must be a function."
    try:
        ratio = func("data/credit_card_fraud.csv")
    except Exception as e:
        return f"Error executing get_fraud_ratio: {str(e)}"
    import pandas as pd
    df = pd.read_csv("data/credit_card_fraud.csv")
    expected = (df['Class'] == 1).mean()
    if not np.isclose(ratio, expected):
        return f"Expected ratio {expected:.4f}, but got {ratio}."
    return True

def proj7_s2_check(func):
    if not callable(func): return "Input must be a function."
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([0, 0, 0, 1])
    try:
        X_res, y_res = func(X, y)
    except Exception as e:
        return f"Error running random_oversample: {str(e)}"
    if len(X_res) != 6 or len(y_res) != 6:
        return f"Expected oversampled dataset to have 6 rows, got {len(X_res)} and {len(y_res)}."
    counts = np.bincount(y_res)
    if counts[0] != 3 or counts[1] != 3:
        return f"Dataset is not balanced. Class counts: {counts.tolist()}."
    return True

def proj7_s3_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(50, 4)
    y_train = np.random.randint(0, 2, 50)
    try:
        model = func(X_train, y_train)
    except Exception as e:
        return f"Error running train_fraud_rf: {str(e)}"
    from sklearn.ensemble import RandomForestClassifier
    if not isinstance(model, RandomForestClassifier): return "Model must be a RandomForestClassifier."
    if model.n_estimators != 10: return "RandomForestClassifier must have n_estimators=10."
    return True

def proj7_s4_check(func):
    if not callable(func): return "Input must be a function."
    class DummyModel:
        def predict_proba(self, X):
            return np.column_stack([1 - X[:, 0], X[:, 0]])
    X_test = np.array([[0.1], [0.8], [0.2], [0.9]])
    y_test = np.array([0, 1, 0, 1])
    try:
        auc_val = func(DummyModel(), X_test, y_test)
    except Exception as e:
        return f"Error running get_pr_auc: {str(e)}"
    from sklearn.metrics import precision_recall_curve, auc
    probs = DummyModel().predict_proba(X_test)[:, 1]
    p, r, _ = precision_recall_curve(y_test, probs)
    expected = auc(r, p)
    if not np.isclose(auc_val, expected):
        return f"Expected PR-AUC {expected:.4f}, got {auc_val}."
    return True

def proj7_s5_check(func):
    if not callable(func): return "Input must be a function."
    X_train = np.random.randn(60, 4)
    y_train = np.random.randint(0, 2, 60)
    X_test = np.random.randn(20, 4)
    y_test = np.random.randint(0, 2, 20)
    try:
        f1 = func(X_train, X_test, y_train, y_test)
    except Exception as e:
        return f"Error running train_cost_sensitive_svm: {str(e)}"
    if not isinstance(f1, (float, np.floating)): return "Expected F1 score to be a float."
    return True

def proj7_s6_check(func):
    if not callable(func): return "Input must be a function."
    y_true = np.array([0, 0, 1, 1, 1])
    probs = np.array([0.1, 0.2, 0.4, 0.6, 0.8])
    try:
        best_thresh, best_f1 = func(y_true, probs)
    except Exception as e:
        return f"Error running optimize_fraud_threshold: {str(e)}"
    if not isinstance(best_f1, (float, np.floating)): return "Expected best F1 score to be a float."
    if not any(np.isclose(best_thresh, val) for val in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]):
        return f"Best threshold {best_thresh} is not in the list [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]."
    return True

class Proj7:
    step_1 = ExerciseStep(
        proj7_s1_check,
        'Load csv, select Class, and return fraction of 1s.',
        'def get_fraud_ratio(file_path):\n    df = pd.read_csv(file_path)\n    return (df["Class"] == 1).mean()'
    )
    step_2 = ExerciseStep(
        proj7_s2_check,
        'Identify indices of 0 and 1 classes. Sample from 1s with replacement until len matches 0s. Concatenate and return.',
        'def random_oversample(X, y):\n    idx_0 = np.where(y == 0)[0]\n    idx_1 = np.where(y == 1)[0]\n    rng = np.random.RandomState(42)\n    idx_1_resampled = rng.choice(idx_1, size=len(idx_0), replace=True)\n    idx_all = np.concatenate([idx_0, idx_1_resampled])\n    return X[idx_all], y[idx_all]'
    )
    step_3 = ExerciseStep(
        proj7_s3_check,
        'Fit RandomForestClassifier(n_estimators=10, random_state=42) on X_train and y_train.',
        'from sklearn.ensemble import RandomForestClassifier\ndef train_fraud_rf(X_train, y_train):\n    model = RandomForestClassifier(n_estimators=10, random_state=42)\n    model.fit(X_train, y_train)\n    return model'
    )
    step_4 = ExerciseStep(
        proj7_s4_check,
        'Use model.predict_proba(X_test)[:, 1] to calculate precision, recall, and auc from sklearn.metrics.',
        'from sklearn.metrics import precision_recall_curve, auc\ndef get_pr_auc(model, X_test, y_test):\n    probs = model.predict_proba(X_test)[:, 1]\n    p, r, _ = precision_recall_curve(y_test, probs)\n    return auc(r, p)'
    )
    step_5 = ExerciseStep(
        proj7_s5_check,
        'Fit SVC(class_weight="balanced", random_state=42) on train and return test macro F1-score.',
        'from sklearn.svm import SVC\nfrom sklearn.metrics import f1_score\ndef train_cost_sensitive_svm(X_train, X_test, y_train, y_test):\n    model = SVC(class_weight="balanced", random_state=42)\n    model.fit(X_train, y_train)\n    preds = model.predict(X_test)\n    return f1_score(y_test, preds, average="macro")'
    )
    step_6 = ExerciseStep(
        proj7_s6_check,
        'Loop thresholds [0.1..0.9], convert probs to predictions, calculate f1_score, and return (best_thresh, best_f1).',
        'from sklearn.metrics import f1_score\ndef optimize_fraud_threshold(y_true, probs):\n    best_f1 = -1\n    best_thresh = None\n    for t in np.arange(0.1, 1.0, 0.1):\n        preds = (probs >= t).astype(int)\n        score = f1_score(y_true, preds)\n        if score > best_f1:\n            best_f1 = score\n            best_thresh = t\n    return best_thresh, best_f1'
    )

proj7 = Proj7()
