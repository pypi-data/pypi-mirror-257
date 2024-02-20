from gseapy import Msigdb

# Utility functions to select gene annotations
def get_expression_program(expression_program, species="human"):
  '''

  Get the expression program BioCarta, KEGG

  '''
  msig = initialize_msigdb()

  gene_set_collection = expression_program.split('_')[0]

  print('expression program', expression_program)
  print('gene set collection', gene_set_collection)

  if gene_set_collection == "KEGG":
    return get_kegg(expression_program, msig, species)

  elif gene_set_collection == "GOBP":
    return get_gobp(expression_program, msig, species)

  elif gene_set_collection == "BIOCARTA":
    return get_biocarta(expression_program, msig, species)

  else:
    return get_reactome(expression_program, msig, species)


def initialize_msigdb():
  '''

  Initializes Molecular Signatures Database.

  '''

  return Msigdb()

def get_gobp(gene_set_name, msig, species="human",
             human_db_category="c5.go.bp", human_db_ver="2023.2.Hs",
             mouse_db_category="m5.go.bp", mouse_db_ver="2023.2.Mm"):
    '''
    Returns the user-specified GO:Biological Process gene annotation set.

    @param species, "human" or "mouse"

    '''

    db_config = {
        "human": [human_db_category, human_db_ver],
        "mouse": [mouse_db_category, mouse_db_ver]
    }

    gmt = msig.get_gmt(category=db_config[species][0], dbver=db_config[species][1])
    return gmt[gene_set_name]


def get_biocarta(gene_set_name, msig, species="human",
                 human_db_category="c2.cp.biocarta", human_db_ver="2023.2.Hs",
                 mouse_db_category="m2.cp.biocarta", mouse_db_ver="2023.2.Mm"):
    '''
    Returns the user-specified BioCarta gene annotation set.

    '''

    db_config = {
        "human": [human_db_category, human_db_ver],
        "mouse": [mouse_db_category, mouse_db_ver]
    }

    gmt = msig.get_gmt(category=db_config[species][0], dbver=db_config[species][1])
    return gmt[gene_set_name]


def get_reactome(gene_set_name, msig, species="human",
                 human_db_category="c2.cp.reactome", human_db_ver="2023.2.Hs",
                 mouse_db_category="m2.cp.reactome", mouse_db_ver="2023.2.Mm"):
    '''
    Returns the user-specified BioCarta gene annotation set.

    '''

    db_config = {
        "human": [human_db_category, human_db_ver],
        "mouse": [mouse_db_category, mouse_db_ver]
    }

    gmt = msig.get_gmt(category=db_config[species][0], dbver=db_config[species][1])
    return gmt[gene_set_name]


def get_kegg(gene_set_name, species='mouse', db_category="c2.all", db_ver="2023.2.Hs"):
    '''
    Returns the user-specified KEGG or KEGG Medicus gene annotation set and returns the mouse orthologs.

    '''
    msig = initialize_msigdb()
    gmt = msig.get_gmt(category=db_category, dbver=db_ver)
    human_kegg_genes = gmt[gene_set_name]

    if species == 'human':
        return human_kegg_genes

    mouse_orthologs = [gene.lower().capitalize() for gene in human_kegg_genes]
    return mouse_orthologs

def get_alb_gene_set(species='mouse', db_category="c8.all", db_ver="2023.2.Hs"):
    '''
    Returns albumin gene set. Specifically for demonstrating albumin as a 
    hepatocyte specific marker gene for cell type classification.

    '''
    msig = initialize_msigdb()
    gmt = msig.get_gmt(category=db_category, dbver=db_ver)
    human_alb_genes = gmt['DESCARTES_MAIN_FETAL_AFP_ALB_POSITIVE_CELLS']

    if species == 'human':
        return human_alb_genes

    mouse_orthologs = [gene.lower().capitalize() for gene in human_alb_genes]
    return mouse_orthologs
