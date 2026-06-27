# Interactive Machine Learning Curriculum

Welcome to your interactive Machine Learning curriculum! This workspace contains 24 comprehensive Jupyter notebooks designed to take you from data manipulation fundamentals all the way to building deep neural networks, time-series forecasting, NLP, recommender systems, association rule mining, Bayesian optimization, reinforcement learning, computer vision, graph machine learning, and explainable AI.

Each notebook is structured like a Kaggle course chapter and contains:
- **Theory & Mathematical Foundations**: Concise guides with LaTeX mathematical formulas.
- **Example Code**: Concrete implementations using `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `optuna`, `pillow`, and `scikit-learn`.
- **Exercises**: At least 6 exercises per chapter, stepping up from **Easy** to **Medium** to **Hard**.
- **Self-Checking API**: Check your answers, get hints, or view reference code solutions interactively inside your notebook environment.

---

## 📚 Curriculum Sitemap

Below is the complete list of interactive notebooks in this workspace:

### 1. Fundamentals & Preprocessing
1. 📊 **[Chapter 1: Data Manipulation](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_01_Data_Manipulation.ipynb)**
   - Topics: NumPy arrays, vectorization, Pandas indexing, slicing, filtering, Groupby aggregations, and matrix multiplication.
2. 🧹 **[Chapter 2: Data Preprocessing & Cleaning](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_02_Data_Cleaning.ipynb)**
   - Topics: Imputing missing values, Ordinal & One-Hot categorical encoding, and custom outlier-clipping scaling.
3. 📈 **[Chapter 3: Data Visualization & Plotting](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_03_Data_Plotting.ipynb)**
   - Topics: Histograms, scatter plots with regression lines and hue, and masked correlation heatmaps using Matplotlib and Seaborn.

### 2. Classical Machine Learning
4. 📉 **[Chapter 4: Linear & Logistic Regression](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_04_Regression.ipynb)**
   - Topics: Linear regression model fitting, implementing gradient descent optimization from scratch, and L1 (Lasso) vs. L2 (Ridge) regularization.
5. 🌲 **[Chapter 5: Decision Trees & Random Forests](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_05_Decision_Trees.ipynb)**
   - Topics: Constrained Decision Tree Classifiers, Random Forest hyperparameter tuning, feature importance extraction, and feature selection.
6. 🛡️ **[Chapter 6: Support Vector Machines & Naive Bayes](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_06_SVM_and_Naive_Bayes.ipynb)**
   - Topics: Text classification via TF-IDF and Naive Bayes, Linear SVM decision boundaries, and Kernel RBF vs. Linear SVM moon classification.

### 3. Clustering & Feature Engineering
7. 🧩 **[Chapter 7: Unsupervised Learning & Clustering](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_07_Unsupervised_Learning.ipynb)**
   - Topics: PCA dimension reduction, K-Means clustering, the Elbow Method, and implementing K-Means from scratch in NumPy.
8. ⚙️ **[Chapter 8: Feature Engineering & Selection](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_08_Feature_Engineering.ipynb)**
   - Topics: Polynomial and interaction features, cyclical time representation (sine/cosine hour transforms), and Recursive Feature Elimination (RFE).
9. 🎯 **[Chapter 9: Model Evaluation & Hyperparameter Tuning](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_09_Model_Evaluation.ipynb)**
   - Topics: K-Fold cross-validation, GridSearchCV vs. RandomizedSearchCV, and F1-score classification threshold tuning.

### 4. Advanced Topics
10. 🧠 **[Chapter 10: Introduction to Deep Learning](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_10_Deep_Learning.ipynb)**
    - Topics: Multi-Layer Perceptrons (MLPs), single Perceptron prediction & training rules from scratch, and building a 2-layer Neural Network with backpropagation from scratch to solve XOR.
11. ⏱️ **[Chapter 11: Time Series Analysis & Forecasting](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_11_Time_Series.ipynb)**
    - Topics: Rolling statistics, time-series stationarity testing (Augmented Dickey-Fuller Test), differencing, and fitting ARIMA models with MAPE evaluation.
12. 🗣️ **[Chapter 12: Natural Language Processing (NLP)](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_12_NLP.ipynb)**
    - Topics: Text preprocessing (tokenization, cleaning, stopword filtering), Bag-of-Words vs. TF-IDF vectorization, Cosine Similarity matrices, and sentence embeddings from word vectors.
13. 🚨 **[Chapter 13: Anomaly Detection](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_13_Anomaly_Detection.ipynb)**
    - Topics: Statistical outlier limits (Z-score & IQR), Isolation Forests, and calculating Mahalanobis Distance from scratch in NumPy.
14. 🤝 **[Chapter 14: Ensemble Learning & Gradient Boosting](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_14_Ensemble_Learning.ipynb)**
    - Topics: Soft Voting Classifier ensembles, AdaBoost learning curves (boosting estimators), and implementing a custom Stacking Classifier.
15. 🌌 **[Chapter 15: Dimensionality Reduction & Manifold Learning](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_15_Manifold_Learning.ipynb)**
    - Topics: Linear Discriminant Analysis (LDA), non-linear Kernel PCA mapping, t-SNE clustering projections, and Silhouette Score evaluations.

### 5. Highly Specialized ML Fields
16. 🎬 **[Chapter 16: Recommender Systems](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_16_Recommender_Systems.ipynb)**
    - Topics: Content-Based genre matching, Cosine Similarity User-Based Collaborative Filtering, and Matrix Factorization (Latent Factors) using SGD from scratch.
17. 🛒 **[Chapter 17: Association Rule Learning](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_17_Association_Rule_Learning.ipynb)**
    - Topics: Support, Confidence, Lift metric logic, the Apriori Frequent Itemsets algorithm, and rule extraction.
18. 🌓 **[Chapter 18: Semi-Supervised Learning](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_18_Semi_Supervised_Learning.ipynb)**
    - Topics: Graph-based Label Propagation (KNN kernel), Pseudo-Labeling (self-training loops), and RBF kernel parameter tuning in Label Spreading.
19. ⚖️ **[Chapter 19: Classification on Imbalanced Data](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_19_Imbalanced_Classification.ipynb)**
    - Topics: Accuracy vs. Macro F1 score metrics traps, random oversampling from scratch, and cost-sensitive SVC.
20. 🔧 **[Chapter 20: Hyperparameter Optimization with Optuna](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_20_Hyperparameter_Optimization.ipynb)**
    - Topics: Optuna multi-parameter studies, tuning Gradient Boosting hyper-parameters, and custom Gaussian Process Bayesian Optimization from scratch.

### 6. Reinforcement, Vision, and Explainable AI
21. 🤖 **[Chapter 21: Reinforcement Learning](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_21_Reinforcement_Learning.ipynb)**
    - Topics: Markov Decision Processes (MDPs), Q-learning updates, exploration-exploitation (epsilon-greedy), and training a Gridworld Q-learning agent from scratch in NumPy.
22. 🖼️ **[Chapter 22: Deep Computer Vision](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_22_Deep_Computer_Vision.ipynb)**
    - Topics: Image representations, 2D Convolution layers from scratch, Max Pooling, image augmentations, Sobel filter edge detection, and simple CNN forward pass inference.
23. 🕸️ **[Chapter 23: Graph Machine Learning](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_23_Graph_Machine_Learning.ipynb)**
    - Topics: Adjacency/Degree matrices, Graph Laplacians, PageRank iteration updates, Jaccard coefficients for link prediction, graph label propagation, and random walk generation.
24. 🔍 **[Chapter 24: Model Interpretability (XAI)](file:///root/notebooks/Python/Jupyter-Exercises/Chapter_24_Model_Interpretability.ipynb)**
    - Topics: Permutation feature importance, Partial Dependence Plots, mean absolute SHAP feature attributions, linear model weight scaling, and custom 3-feature Shapley value estimates from scratch.


### 7. Practical Case Studies & Projects
- 📉 **[Project 1: Predict Customer Churn (Classification Case Study)](file:///root/notebooks/Python/Jupyter-Exercises/Project_01_Customer_Churn.ipynb)**
  - Dataset: `data/customer_churn.csv`
  - Topics: Binary classification, exploratory data analysis, feature scaling, model training, and precision-recall/F1 decision threshold tuning.
- 🏡 **[Project 2: Housing Price Prediction (Regression Case Study)](file:///root/notebooks/Python/Jupyter-Exercises/Project_02_Housing_Prices.ipynb)**
  - Dataset: `data/housing.csv`
  - Topics: Feature engineering, regularized Ridge regression grid search, and hyperparameter tuning with Optuna.
- 💬 **[Project 3: Sentiment Analysis on Customer Reviews (NLP Case Study)](file:///root/notebooks/Python/Jupyter-Exercises/Project_03_Sentiment_Analysis.ipynb)**
  - Dataset: `data/text_sentiment.csv`
  - Topics: Text cleaning, tokenization, TF-IDF vectorization, Naive Bayes sentiment classifiers, and permutation feature importance.

---

## 🛠️ How to Use the Verification System

At the end of each exercise, you'll see a verification cell. You can use the local **[learntools.py](file:///root/notebooks/Python/Jupyter-Exercises/learntools.py)** module to guide you.

For example, in Chapter 1:
```python
# Import the chapter's checker
from learntools import ch1

# 1. Check your solution
ch1.step_1.check(result_df)

# 2. Get a hint if you are stuck
ch1.step_1.hint()

# 3. View the reference solution
ch1.step_1.solution()
```

When you call `.check(...)`, it will output a green **🎉 Correct!** message if your variable matches, or a descriptive red **❌ Incorrect: ...** message with the reason it failed.
