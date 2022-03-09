import re
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
from sklearn.feature_extraction.text import TfidfVectorizer

def ngrams(string, n=3):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

def preprocessing(df, column_name, generated_column_name):
    #convert to lower text
    df[generated_column_name] =df[column_name].str.lower()
    
    #remove all text inside () with blank space
    df[generated_column_name] =df[generated_column_name].str.replace(r'\([^)]*\)', '', regex=True)
    
    #removec punctuations with space
    df[generated_column_name] =df[generated_column_name].str.replace(r'[-*,+()/<>|@#:"]', ' ', regex=True)
    
    #remove &.' with blank space
    df[generated_column_name] =df[generated_column_name].str.replace(r"[&.']", "", regex=True)
    
    #remove multiple space into single space
    df[generated_column_name] =df[generated_column_name].str.replace(r"\s+", " ", regex=True)
    
    #strip or trim
    df[generated_column_name] =df[generated_column_name].str.strip()
    
    #remove added column
    L = df[generated_column_name].tolist()
    
    for idx, string in enumerate(L):
        if str(string) == 'nan':
            L[idx] = ''
        else:
            L[idx] = string
    df.drop(columns=[generated_column_name], inplace=True)
    return L

def awesome_cossim_top(A, B, ntop, threshold):
        A = A.tocsr()
        B = B.tocsr()
        M, _ = A.shape
        _, N = B.shape
        
        idx_dtype = np.int32
        
        nnz_max = M*ntop
        indptr = np.zeros(M+1, dtype=idx_dtype)
        indices = np.zeros(nnz_max, dtype=idx_dtype)
        data = np.zeros(nnz_max, dtype=A.dtype)

        ct.sparse_dot_topn(
            M, N, np.asarray(A.indptr, dtype=idx_dtype),
            np.asarray(A.indices, dtype=idx_dtype),
            A.data,
            np.asarray(B.indptr, dtype=idx_dtype),
            np.asarray(B.indices, dtype=idx_dtype),
            B.data,
            ntop,
            threshold,
            indptr, indices, data)

        return csr_matrix((data,indices,indptr),shape=(M,N))

def return_match_pair(match,name_vector,dict_vendor,limit,col1,col2):
    non_zero = match.nonzero()
    sparse_rows = non_zero[0]
    sparse_columns = non_zero[1]
    key1 = list()
    key2 = list()
    score = list()
    for i, j in zip(sparse_rows, sparse_columns):
        if i == limit:
            break
        score_array = match[i,:].toarray()
        key1.append(name_vector[i])
        key2.append(dict_vendor[j])
        score.append(int(score_array[0][j]*100))
        
    dataframe = pd.DataFrame({
        col1:key1,
        col2:key2,
        "similarity_score":score,
    })
    return dataframe

def get_vectorize(lookup_list, table_array_list):
    vectorizer = TfidfVectorizer(min_df = 0,token_pattern='(?u)\\b\\w+\\b', analyzer=ngrams)
    train_matrix = vectorizer.fit_transform(lookup_list+table_array_list)
    #For Lookup
    lookup_matrix = train_matrix[0:len(lookup_list)]
    #For Table Array
    table_array_matrix = vectorizer.transform(table_array_list)
    return [lookup_matrix, table_array_matrix]