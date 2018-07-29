'''
Aggregates paper information dictionaries into scoring tables/statistics to
display pass to the front-end (Draw flower or display statistics).

date:   26.06.18
author: Alexander Soen
'''

import pandas as pd
from core.utils.entity_type import Entity_type
from core.score.agg_utils   import get_name_mapping
from core.score.agg_utils   import apply_name_mapping
from core.score.agg_utils   import is_self_cite


def score_paper_info(paper_info, self=list()):
    ''' Generates a dictionary with score values and relevant information to be
        aggregated.
    '''
    # Score results
    score_list = list()

    # Iterate through references
    for reference in paper_info['References']:
        # Check if it is a self citation
        self_cite = is_self_cite(reference, self)

        # Get venue value
        conf_name = reference['ConferenceName'] \
                if 'ConferenceName' in reference else None
        jour_name = reference['JournalName'] \
                if 'JournalName' in reference else None

        # Get author combinations
        author_list = list()
        for paa in reference['Authors']:
            auth_name = paa['AuthorName'] \
                    if 'AuthorName' in paa else None
            affi_name = paa['AffiliationName'] \
                    if 'AffiliationName' in paa else None
            author_list.append((auth_name, affi_name))

        if not author_list:
            author_list = [(None, None)]

        for auth_name, affi_name in author_list:
            inst_res = dict()

            # Entity Names
            inst_res['AuthorName']      = auth_name
            inst_res['AffiliationName'] = affi_name
            inst_res['ConferenceName']  = conf_name
            inst_res['JournalName']     = jour_name

            # Additional Properties
            inst_res['self_cite'] = self_cite

            # Scoring
            inst_res['influenced_count']  = 0
            inst_res['influencing_count'] = 1
            
            inst_res['influenced_paa']  = 0
            inst_res['influencing_paa'] = 1 / len(author_list)

            # Year information
            try:
                inst_res['publication_year'] = paper_info['Year']
                inst_res['influence_year']   = paper_info['Year']
            except KeyError:
                inst_res['publication_year'] = None
                inst_res['influence_year']   = None
            try:
                inst_res['link_year'] = reference['Year']
            except:
                inst_res['link_year'] = None

            # Paper information
            inst_res['ego_paper_id']     = paper_info['PaperId']
            inst_res['link_paper_id']    = reference['PaperId']
            inst_res['link_paper_title'] = reference['PaperTitle']

            score_list.append(inst_res)

    # Iterate through citations
    for citation in paper_info['Citations']:
        # Check if it is a self citation
        self_cite = is_self_cite(citation, self)

        # Get venue value
        conf_name = citation['ConferenceName'] \
                if 'ConferenceName' in citation else None
        jour_name = citation['JournalName'] \
                if 'JournalName' in citation else None

        # Get author combinations
        author_list = list()
        for paa in citation['Authors']:
            auth_name = paa['AuthorName'] \
                    if 'AuthorName' in paa else None
            affi_name = paa['AffiliationName'] \
                    if 'AffiliationName' in paa else None
            author_list.append((auth_name, affi_name))

        if not author_list:
            author_list = [(None, None)]

        for auth_name, affi_name in author_list:
            inst_res = dict()

            # Entity Names
            inst_res['AuthorName']      = auth_name
            inst_res['AffiliationName'] = affi_name
            inst_res['ConferenceName']  = conf_name
            inst_res['JournalName']     = jour_name

            # Additional Properties
            inst_res['self_cite'] = self_cite

            # Scoring
            inst_res['influenced_count']  = 1
            inst_res['influencing_count'] = 0
            
            inst_res['influenced_paa']  = 1 / len(author_list)
            inst_res['influencing_paa'] = 0

            # Year information
            try:
                inst_res['publication_year'] = paper_info['Year']
            except KeyError:
                inst_res['publication_year'] = None
            try:
                inst_res['influence_year'] = citation['Year']
                inst_res['link_year']     = citation['Year']
            except KeyError:
                inst_res['influence_year'] = None
                inst_res['link_year'] = None

            # Paper information
            inst_res['ego_paper_id']     = paper_info['PaperId']
            inst_res['link_paper_id']    = citation['PaperId']
            inst_res['link_paper_title'] = citation['PaperTitle']

            score_list.append(inst_res)

    return score_list


def get_influence_index(entity_type, influence_dir='influenced'):
    ''' Function to get the score index from the scoring dictionaries.
    '''
    # Author
    if entity_type == Entity_type.AUTH:
        return influence_dir + '_paa'

    # Affiliation
    if entity_type == Entity_type.AFFI:
        return influence_dir + '_paa'

    # Conference
    if entity_type == Entity_type.CONF:
        #return influence_dir + '_count'
        return influence_dir + '_paa' #Should be equiv to count once agg

    # Journal
    if entity_type == Entity_type.JOUR:
        #return influence_dir + '_count'
        return influence_dir + '_paa'

    return None


def get_name_index(entity_type):
    ''' Function to get the name index from the scoring dictionaries.
    '''
    # Author
    if entity_type == Entity_type.AUTH:
        return 'AuthorName'

    # Affiliation
    if entity_type == Entity_type.AFFI:
        return 'AffiliationName'

    # Conference
    if entity_type == Entity_type.CONF:
        return 'ConferenceName'

    # Journal
    if entity_type == Entity_type.JOUR:
        return 'JournalName'

    return None


def score_paper_info_list(paper_info_list, self=list()):
    '''
    '''
    # Query results
    score_list = list()

    # Turn paper information into score dictionary
    for paper_info in paper_info_list:
        score_list += score_paper_info(paper_info, self)

    # Score dataframe
    return pd.DataFrame(score_list)

    
def score_leaves(score_df, leaves):
    '''
    '''
    # Set entity names and influence to specified
    res_list = list()
    for leaf in leaves:
        leaf_df = score_df.copy()
        leaf_df['entity_name'] = leaf_df[get_name_index(leaf)]
        leaf_df['entity_type'] = leaf
        leaf_df['influenced']  = leaf_df[get_influence_index(leaf)]
        leaf_df['influencing'] = leaf_df[get_influence_index(leaf,
            influence_dir='influencing')]

        res_list.append(leaf_df)

    return pd.concat(res_list)