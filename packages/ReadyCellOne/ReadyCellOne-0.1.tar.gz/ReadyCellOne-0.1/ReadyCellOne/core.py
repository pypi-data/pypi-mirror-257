import anndata
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize

from ReadyCellOne.utils import *

# Core functions
def train_rco_model(train_adata, train_cell_state_obs_column, test_adata, expression_program, species='human',
                    n_trees=1000, max_depth=3, random_state=100, class_weight='balanced',
                    num_random_samples=0, train_order=None, test_cell_state_obs_column=None, test_order=None):
  '''

  High level function to train a ReadyCellOne model.

  @param train_adata: AnnData, training matrix, expects scRNA-seq.
  @param test_adata: AnnData, testing matrix, can be bulk or single-cell.
  @param cell_state_obs_column: str, name of the observation column in train_adata for cell state annotations. 
          This is the target variable for classification.
  @param expression_program: str or list, if str, name of GOBP, BioCarta, KEGG, or Reactome functional gene set from MSigDB. 
          If list, custom gene set. The model features will be restricted to these genes during training.
  @param species: 'human' or 'mouse'
  @param n_trees (default:1000): number of estimators in random forest classifier.
  @param max_depth (default:3): max depth for each decision tree in the random forest.
  @param random_state (default:100): seed for the random state.
  @param class_weight (default:'balanced'): whether or not to balance the classes.
  @param num_random_samples (optional; default: 0): This is to add a negative control class in the training process. 
          The idea is that any query samples that are dissimilar to the cell states trained on will be predicted as a random expression profile.
  @param order (optional): 

  @return
          clf: trained classifier
          train_ranked_expression_reduced: the
          test_ranked_expression_reduced:
          y_train
          cgenes

  '''

  train_adata_common, test_adata_common, cgenes = restrict_to_cgenes(train_adata, test_adata)

  train_df = train_adata_common.to_df()
  test_df = test_adata_common.to_df()

  train_cell_state_obs = train_adata.obs[train_cell_state_obs_column]

  y_train = None
  y_test = None

  train_ranked_expression = pd.DataFrame()

  # Rank-based feature transformation
  if num_random_samples > 0:
    train_cell_state_obs = np.concatenate([train_cell_state_obs, np.array(['random'] * num_random_samples)])
    train_ranked_expression = transcriptome_rank_transform(train_df)

  else:
    train_ranked_expression = transcriptome_rank_transform(train_df, add_random_samples=False)

  train_unique_cell_states = np.unique(train_cell_state_obs)

  # Processing of target variable
  if train_order:
    sorted_indices = np.argsort([train_order.index(x) for x in train_unique_cell_states])
    train_unique_cell_states = train_unique_cell_states[sorted_indices]

  y_train = label_binarize(train_cell_state_obs, classes=train_unique_cell_states)

  if test_cell_state_obs_column:
    test_cell_state_obs = test_adata.obs[test_cell_state_obs_column]
    test_unique_cell_states = np.unique(test_cell_state_obs)

    if test_order:
      if 'random' in train_unique_cell_states:
        test_unique_cell_states = np.concatenate([test_unique_cell_states, np.array(['random'])])

      sorted_indices = np.argsort([test_order.index(x) for x in test_unique_cell_states])
      test_unique_cell_states = test_unique_cell_states[sorted_indices]

    if num_random_samples > 0:
      y_test = label_binarize(test_cell_state_obs, classes=test_unique_cell_states)
    else:
      y_test = label_binarize(test_cell_state_obs, classes=test_unique_cell_states)

  # Gene annotation based feature selection
  gene_set = []

  if isinstance(expression_program, list):
    gene_set = expression_program
  else:
    gene_set = get_expression_program(expression_program, species=species)

  train_ranked_expression_reduced = select_expression_program_genes(train_ranked_expression, gene_set)

  # Process test dataset
  test_ranked_expression = transcriptome_rank_transform(test_df, add_random_samples=False)
  test_ranked_expression_reduced = select_expression_program_genes(test_ranked_expression, gene_set)

  # Train the RCO model
  clf = make_classifier(n_trees=n_trees, max_depth=max_depth, random_state=random_state, class_weight=class_weight)

  print('training...')

  clf.fit(train_ranked_expression_reduced, y_train)

  if test_cell_state_obs_column:
    return clf, train_ranked_expression_reduced, test_ranked_expression_reduced, y_train, y_test, cgenes

  return clf, train_ranked_expression_reduced, test_ranked_expression_reduced, y_train, cgenes


def restrict_to_cgenes(train_adata, test_adata):
  '''
  Computes the common set of genes for RF classification

  '''
  cgenes = list(set(train_adata.var_names).intersection(set(test_adata.var_names)))
  train_adata_common = train_adata[:,cgenes]
  test_adata_common = test_adata[:,cgenes]

  return train_adata_common, test_adata_common, cgenes

def transcriptome_rank_transform(df, add_random_samples=True):
  '''
  Assign transcriptome-wide rankings for each gene within each sample

  @param df: pd.DataFrame, training data
  @param add_random_samples: bool, whether or not to create and add random expression profiles during training.

  @return: ranked_expression: a feature-transformed, rank-normalized expression matrix where the expression
            value of each gene in a sample is replaced with its transcriptome-wide ranking for that sample.

  '''

  ranked_expression = np.argsort(df.to_numpy(), axis=1).argsort(axis=1) + 1
  ranked_expression = pd.DataFrame(ranked_expression, index=df.index, columns=df.columns)

  if add_random_samples:
    ranked_expression = pd.concat([ranked_expression, randomize(ranked_expression)])

  return ranked_expression

def select_expression_program_genes(ranked_expression, gene_set):
  '''
  Subset by a gene set functional annotation.

  @param ranked_expression: pd.DataFrame, rank-transformed expression matrix.
  @param gene_set: list, list of genes to perform feature selection with.

  '''

  # Get the intersection of gene_set and variable names in the DataFrame
  valid_genes = list(set(gene_set) & set(ranked_expression.columns))

  # Subsample based on the valid genes
  return ranked_expression[valid_genes]

def make_classifier(n_trees=1000, max_depth=3, random_state=100, class_weight='balanced'):
  '''
  Makes a OvR classifier for multi-class classification

  @param n_trees: int
  @param max_depth: int
  @param random_state: int
  @param class_weight: str

  '''

  return OneVsRestClassifier(RandomForestClassifier(n_estimators=n_trees, max_depth=max_depth, random_state=random_state, class_weight=class_weight))


def randomize(expDat: pd.DataFrame, num: int = 100) -> pd.DataFrame:
    """
    Randomize the rows and columns of a pandas DataFrame.

    Args:
        expDat (pd.DataFrame): the input DataFrame
        num (int): the number of rows to return (default 50)

    Returns:
        pd.DataFrame: the randomized DataFrame with num rows and the same columns as expDat
    """

    # Convert DataFrame to NumPy array
    temp = expDat.to_numpy()

    # Randomize the rows of the array
    temp = np.array([np.random.choice(x, len(x), replace=False) for x in temp])

    # Transpose the array and randomize the columns
    temp = temp.T
    temp = np.array([np.random.choice(x, len(x), replace=False) for x in temp]).T

    # Convert the array back to a DataFrame and return the first num rows
    return pd.DataFrame(data=temp, columns=expDat.columns).iloc[0:num, :]


def predict_cell_states(clf, X):
  '''
  Predict discrete (categorical) cell states given input expression samples.

  This calls random forest predict function.

  '''
  return clf.predict(X)

def predict_cell_state_similarity_scores(clf, X, y=None, col='cell state'):
  '''
  Predict cell state similarity scores for RNA-seq expression profiles. 
  
  This is essentially the majority vote of the individual estimators in the 
  random forest along the natural axis of variation or an averaged probability 
  of the query sample being predicted as each discrete cell state class observed in training.

  '''
  y_scores = clf.predict_proba(X)

  # Store predictions as an AnnData object
  xpreds = pd.DataFrame(y_scores, columns=clf.classes_, index=X.index.astype(str))
  prediction_adata = anndata.AnnData(X)
  if y is not None:
    prediction_adata.obs[col] = y
  prediction_adata.obsm['prediction'] = xpreds

  return y_scores, prediction_adata