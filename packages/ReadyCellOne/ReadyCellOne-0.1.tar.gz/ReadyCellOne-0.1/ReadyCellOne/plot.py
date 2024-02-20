import anndata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scanpy as sc
import seaborn as sns

from sklearn.metrics import precision_recall_curve, auc, f1_score, confusion_matrix, multilabel_confusion_matrix, roc_curve

# @title Visualization functions
def barplot_classifier_f1(adata, ground_truth: str = "celltype", class_prediction: str = "SCN_class"):
  '''

  Barplot of F1 scores.

  '''
  fscore = f1_score(adata.obs[ground_truth], adata.obs[class_prediction], average=None, labels = adata.obs[ground_truth].cat.categories)
  cates = list(adata.obs[ground_truth].cat.categories)
  f1_score_dict = {class_label: f1_score_x for class_label, f1_score_x in zip(cates, fscore)}

  # Calculate the number of observations per class
  class_counts = adata.obs[ground_truth].value_counts().to_dict()

  plt.rcParams['figure.constrained_layout.use'] = True
  sns.set_theme(style="whitegrid")
  ax = sns.barplot(x=list(f1_score_dict.values()), y=list(f1_score_dict.keys()))
  plt.xlabel('F1-Score')
  plt.title('F1-Scores per Class')
  plt.xlim(0, 1.1) # Set x-axis limits to ensure visibility of all bars

  # Add the number of observations per class as text within the barplot
  for i, bar in enumerate(ax.containers[0]):
      width = bar.get_width()
      print(f"{width}")
      label = f"n = {class_counts[cates[i]]}"
      fcolor = "white"
      if width < 0.20:
          fcolor = "black"

      ax.text( 0.03, bar.get_y() + bar.get_height() / 2, label, ha='left', va='center', color = fcolor)

  plt.show()


def plot_confusion_matrix(clf, y_test, y_pred, cls_mapping=None, figsize=(8,6), cmap="Blues", multilabel_idx=[1], xticklabels=None, yticklabels=None):
  '''
  Plot multi-class confusion matrix of the results

  @param clf: classifier
  @param y_test: np.array of shape (n, c)
  @param y_pred: np.array of shape (m, c)
  @param figsize: tuple of shape (h,w)
  @param multilabel: bool, whether to plot a multilabel confusion matrix

  @return Matplotlib figure

  '''

  if cls_mapping:
    v = np.vectorize(lambda x: cls_mapping[x])
    y_pred = v(y_pred)


  if multilabel_idx:
    cm = multilabel_confusion_matrix(y_test, y_pred)[multilabel_idx]
  else:
    cm = confusion_matrix(y_test, y_pred)

  if xticklabels is None:
    xticklabels = clf.classes_

  if yticklabels is None:
    yticklabels = clf.classes_

  plt.figure(figsize=figsize)
  sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", annot_kws={"size": 16}, xticklabels=xticklabels, yticklabels=yticklabels)
  plt.title('Confusion Matrix, Albumin')
  plt.xlabel('Predicted')
  plt.ylabel('Actual')
  plt.show()

def plot_pr_curves(y_test, y_scores, cls, figsize=(8,6)):
  '''

  @param y_test: output of train_rco_model, expects to be label-binarized
  @param y_scores: output of predict_cell_state_similarity_scores
  @param cls: categorical labels for each of the classes/cell states.
  @param: figsize: figure size (mpl)

  '''
  plt.figure(figsize=figsize)

  for i in range(y_test.shape[1]):
      precision, recall, _ = precision_recall_curve(y_test[:, i], y_scores[:, i])
      auprc = auc(recall, precision)
      plt.plot(recall, precision, label=f'{cls[i]} (AUPRC = {auprc:.2f})')

  plt.xlabel('Recall')
  plt.ylabel('Precision')
  plt.title('Precision-Recall Curves for OvR Random Forest Classifier')
  plt.legend()
  plt.show()

def plot_single_pr_curve(y_true, y_scores, expression_program, cls=None, plot_ideal=True, figsize=(8,6)):
  '''
  Plot a precision-recall curve.

  @param cls: list, names of classes to assign to the true class labels instead 
              of binarized encoding.
  @param y_scores: np.array, cell state similarity scores for which to compute 
                  precision and recall at various decision thresholds.
  @param expression_program: str, 

  '''
  # Compute Precision-Recall curve and AUPRC
  if cls:
    precision, recall, thresholds = precision_recall_curve(y_true.map({cls[0]: 0, cls[1]: 1}), y_scores)
    auprc = auc(recall, precision)
  else:
    precision, recall, thresholds = precision_recall_curve(y_true[:, 1], y_scores)
    auprc = auc(recall, precision)

  # Plot the Precision-Recall curve
  plt.figure(figsize=figsize)
  plt.plot(recall, precision, lw=2, label=f'PR curve (AUPRC = {auprc:.2f})')

  if plot_ideal:
    # An idealized PR curve
    ideal_precision = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ideal_recall = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.0, 1.0]

    # Plot ideal
    plt.step(ideal_recall, ideal_precision, color='darkgreen', where='post', label='Ideal PR curve (AUPRC = 1.0)')

    # Add a dark green vertical line at recall = 1.0 that stops at the precision-recall curve
    plt.axvline(x=1.0, ymin=0.05, ymax=0.95, color='darkgreen')

  plt.xlabel('Recall (Sensitivity)')
  plt.ylabel('Precision (Positive Predictive Value)')
  plt.title(f'PR Curve, {expression_program}')
  plt.legend(loc='best')
  plt.show()

def plot_roc_curve(y_test, y_pred_positive_class, cls, figsize=(8,6),
                   title='Receiver Operating Characteristic (ROC) Curve',
                   xlabel='False Positive Rate',
                   ylabel='True Positive Rate',
                   loc='lower right',
                   fontsize='xx-large'):

  '''

  Plots Receiver Operating Characteristic (ROC) plot for binary classification.

  Can also be extended to the multiclass case by adopting a One vs. Rest scheme.

  '''

  # Calculate the ROC curve
  fpr, tpr, thresholds = roc_curve(y_test.map({cls[0]: 0, cls[1]: 1}), y_pred_positive_class)

  # Calculate the Area Under the Curve (AUC)
  roc_auc = auc(fpr, tpr)

  # Plot the ROC curve
  plt.figure(figsize=figsize)
  plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
  plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
  plt.xlabel(xlabel, fontsize=fontsize)
  plt.ylabel(ylabel, fontsize=fontsize)
  plt.title(title, fontsize=fontsize)
  plt.legend(loc=loc, fontsize=fontsize)
  plt.show()



def plot_bulk_rnaseq_samples(y_scores, sample_names, classes, xlabel, ylabel, title, loc='best', rotation=45):
  '''
  Plot grouped barplot of cell state similarity scores for query bulk RNA-Seq samples.

  @param y_scores: np.array, cell state similarity scores
  @param sample_names: list, names of the bulk RNA-seq samples.
  @param classes: list, cell state training classes to plot cell state scores for. 
          Should be same classes + order as they appear in the training data.
  @param xlabel: str, x-axis label of grouped barplot
  @param ylabel: str, y-axis label of grouped barplot
  @param title: str, title of barplot

  @return MPL barplot of predicted cell state similarity scores for bulk RNA-seq samples.

  '''
  # Create the grouped barplot using seaborn
  sns.set(style="whitegrid")
  df = pd.DataFrame(y_scores, index=sample_names, columns=classes).plot(kind='bar')

  # Customize the plot
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)
  plt.legend(loc=loc)
  plt.xticks(rotation=rotation)

  # Show the plot
  plt.show()

def heatmap_rco_scores(y_scores, predictions, groupby=None, cls=None, vmin: float = 0, vmax: float = 1, title=None, xlabel=None, ylabel=None, rotation=45):
  '''
  Plots a heatmap of RCO cell state similarity scores for single-cell RNA-Seq samples.

  @param y_scores: np.array, cell state similarity score predictions 
                    from predict_cell_state_similarity_scores()
  @param predictions: anndata.AnnData, prediction anndata generated
                    from predict_cell_state_similarity_scores()
  @param groupby (optional): query anndata observational group column.
                    If given, will be passed into sc.pl.heatmap to group cells.
                    else will leave the x-axis empty unless xlabel is given.
  @param cls (optional): list, class names of train cell states to assign
                    to y-axis of the heatmap.
  @param title
  @param xlabel
  @param ylabel

  @return sc.pl.heatmap of single-cells and their predicted RCO cell state 
          similarity scores for each of the train classes

  '''
  temp_predictions = anndata.AnnData(y_scores, obs=predictions.obs)

  # guess at appropriate dimensions
  fsize = [5, 6]
  plt.rcParams['figure.subplot.bottom'] = 0.25

  if cls is not None:
    temp_predictions.var_names = cls

  if groupby:
    temp_predictions.obs[groupby] = predictions.obs[groupby]
    ax_dict = sc.pl.heatmap(temp_predictions, temp_predictions.var_names.values, groupby=groupby, dendrogram=False, swap_axes=True, vmin = vmin, vmax = vmax, figsize=fsize, cmap='viridis', show=False)
  else:
    temp_predictions.obs['groupby'] = 'groupby'
    ax_dict = sc.pl.heatmap(temp_predictions, temp_predictions.var_names.values, groupby='groupby', dendrogram=False, swap_axes=True, vmin = vmin, vmax = vmax, figsize=fsize, cmap='viridis', show=False)

  heatmap_ax = ax_dict['heatmap_ax']

  # Modify the axes
  heatmap_ax.set_title(title)
  heatmap_ax.set_xlabel(xlabel)
  heatmap_ax.set_ylabel(ylabel)

  heatmap_ax.set_xticklabels(heatmap_ax.get_xticklabels(), rotation=rotation)

  plt.show()