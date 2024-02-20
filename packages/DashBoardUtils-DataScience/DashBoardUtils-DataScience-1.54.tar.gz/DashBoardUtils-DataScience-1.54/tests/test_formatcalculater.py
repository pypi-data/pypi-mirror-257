import pytest
from package.formatcalculator import FormatCalculator, Mitter, Ordring
from typing import Generator
from package.variationcalculator import VERIATIONS
import pandas as pd

def test_format_df_hash():
    import pandas as pd
    import re

    df = pd.DataFrame(
        {"var1": ["a", "b", "c"], "other_var": [4, 7, 3], "yet_another": [8, 0, 2]}
    )
    dfq = FormatCalculator.hash_df_formats(df)
    tests = re.compile(dfq.iloc[0, 0])
    result = tests.match(df.iloc[0, 0])
    validation = False
    if result:
        validation = True
    assert isinstance(df, pd.DataFrame)
    assert isinstance(dfq, pd.DataFrame)
    assert isinstance(result, re.Match)
    assert len(dfq) == len(df)
    assert dfq.columns.to_list() == df.columns.to_list()
    assert validation


def test_datamiter_column_wise():
    import pandas as pd

    df = pd.DataFrame(
        {"var1": ["a", "b", "c"], "other_var": [4, 7, 3], "yet_another": [8, 0, 2]}
    )
    mitter = FormatCalculator.generate_datamiter(df)
    assert isinstance(mitter, Mitter)
    assert isinstance(df, pd.DataFrame)
    assert isinstance(mitter._df, pd.DataFrame)
    assert isinstance(mitter.dataset, pd.DataFrame)
    assert isinstance(mitter.colhashes, Generator)
    assert len(mitter._df) == 1
    assert len(df) == len(mitter.dataset)
    assert len(df.iloc[:, 0].to_list()) >= len(list(mitter.colhashes)[0][1])


def test_split_all_labels_to_words_with_new_cols():
    import pandas as pd

    df = pd.DataFrame(
        {
            "var1": ["a c", "b w c", "c x"],
            "other_var": [4, 7, 3],
            "yet_another": [8, 0, 2],
        }
    )
    splitdf = FormatCalculator.split_all_labels_to_words_with_new_cols(df, exer=[" "])
    assert len(df.columns.to_list()) < len(splitdf.columns.to_list())
    assert len(df) == len(splitdf)
    assert isinstance(splitdf, pd.DataFrame)


def test_formatwise_mitter():
    import pandas as pd

    df = pd.DataFrame(
        {
            "var1": ["a c", "b w c", "c x"],
            "other_var": [4, 7, 3],
            "yet_another": [8, 0, 2],
        }
    )
    mitter = FormatCalculator.generate_datamiter(df)
    formit = mitter.formatwise_mitter()
    assert isinstance(mitter, Mitter)
    assert isinstance(formit, pd.DataFrame)


def test_row_patterns():
    import pandas as pd

    df = pd.DataFrame(
        {
            "var1": ["a c", "b w c", "c x"],
            "other_var": [4, 7, 3],
            "yet_another": [8, 0, 2],
        }
    )
    mitter       = FormatCalculator.generate_datamiter(df)
    row_patterns = mitter.row_patterns(df)
    assert isinstance(row_patterns, list)
    assert isinstance(row_patterns[0], str)


def test_columnwise_data_pattern_ordring_seq():
    import pandas as pd

    df = pd.DataFrame(
        {
            "var1": ["a c", "b w c", "c x"],
            "other_var": [4, 7, 3],
            "yet_another": [8, 0, 2],
        }
    )
    mitter = FormatCalculator.generate_datamiter(df)
    mitter = mitter.columnwise_data_pattern_ordring_seq()
    assert isinstance(mitter, dict)


def test_get_row_ordring_seq_from_dataset():
    import pandas as pd

    df = pd.DataFrame(
        {
            "var1": ["a c", "b w c", "c x"],
            "other_var": [4, 7, 3],
            "yet_another": [8, 0, 2],
        }
    )
    mitter = FormatCalculator.generate_datamiter(df)
    mi     = mitter.get_row_ordring_seq_from_dataset(df, 3)
    assert isinstance(mi, list)


def test_hash_str_patterns():
    import pandas as pd

    df = pd.DataFrame(
        {
            "var1": ["a c", "b w c", "c x"],
            "other_var": [4, 7, 3],
            "yet_another": [8, 0, 2],
        }
    )
    mitter      = FormatCalculator.generate_datamiter(df)
    mitter      = mitter.formatwise_mitter()
    mitter_hash = Mitter.hash_str_patterns(mitter)
    assert isinstance(mitter_hash, pd.DataFrame)





def test_columnwise_datasets_org():
    import pandas as pd
    from package.keyborddata import alphabets,alphabets_upper,simbols,numbers
    import ast
    data             =  pd.DataFrame(
        {"var1": ["a", "b", "c"], "other_var": [4, 7, 3], "yet_another": [8, 0, 2]}
    )
    format_hashed_df = FormatCalculator.hash_df_formats(data)
    finaldata        = []
    for x in format_hashed_df.columns.to_list():    
        colms          = format_hashed_df[x].values.tolist()
        my_list_count1 = {i: colms.count(i) for i in colms}
        finaldata.append({x: my_list_count1})

    # keyboards data
    keyboards = alphabets + alphabets_upper + simbols + [str(x) for x in numbers]
    # formatwisedata org
    formatdataset = []
    hashed=[]
    for x in finaldata:
        hashed_x=x
        for z in list(list(x.values())[0].keys()):
            datas = data[list(x.keys())[0]].apply(FormatCalculator.regex_filter, regex=z)
            datas = datas[datas != False].values.tolist()
            x[list(x.keys())[0]][z] = datas
            hashd=[]
            for sa in datas:
                if len(str(sa))==1:
                    hashd.append(str(keyboards.index(str(sa))))
                else:
                    pairs=[]
                    for xs in list(str(sa)):
                        pairs.append(str(keyboards.index(xs)))
                    hashd.append(str(pairs))

            hashed_x[list(hashed_x.keys())[0]][z] = {i:hashd.count(i) for i in hashd}

        formatdataset.append(x)
        hashed.append(hashed_x)
        # multindex columns
    tuplesd=[list(FormatCalculator.dict_mapped_tup(x)) for x in hashed]
    tuplesd=[x for xs in tuplesd for x in xs]
    multindextuples=[]
    valueslist=[]
    for x in tuplesd:
        multindextuples.append(x[:-1])
        valueslist.append(x[-1])

    multindex=pd.MultiIndex.from_tuples(multindextuples)
    output_df_before_optimizing_unique_lists=pd.DataFrame([valueslist],columns=multindex)
    valueslis=[]
    for x in output_df_before_optimizing_unique_lists.columns.to_list():
        datasq=None
        try:
            datasq=int(x[-1])
        except Exception as E:
            datasq=ast.literal_eval(x[-1])
        if type(datasq)==int:
            generowscount=output_df_before_optimizing_unique_lists[x].values.tolist()[0]
            datagen=[keyboards[int(datasq)] for d in range(generowscount)]
            valueslis.append(datagen)
        else:
            generowscount=output_df_before_optimizing_unique_lists[x].values.tolist()[0]
            datagen=["".join([keyboards[int(z)] for z in datasq]) for d in range(generowscount)]
            valueslis.append(datagen)
    assert isinstance(output_df_before_optimizing_unique_lists,pd.DataFrame)
    assert isinstance(valueslis,list)
    

def test_data_regeneration_process():
    import pandas as pd
    from package.variationcalculator import VERIATIONS
    from package.keyborddata import alphabets,alphabets_upper,simbols,numbers
    data             =  pd.DataFrame(
        {"var1": ["a", "b", "c"], "other_var": [4, 7, 3], "yet_another": [8, 0, 2]}
    )
    format_hashed_df = FormatCalculator.hash_df_formats(data)
    mitter           = FormatCalculator.generate_datamiter(data)
    mitter2          = mitter.formatwise_mitter()
    formateld        = Mitter.hash_str_patterns(mitter2)
    keyboards        = (
            alphabets + alphabets_upper + simbols + [str(x) for x in numbers] + [" "]
        )
    veri             = VERIATIONS(formateld,pd.DataFrame(columns=mitter.get_row_ordring_seq_from_dataset(data,iterlen=1)),keyboard=keyboards)
    result           = veri.transform_keybord_seq_to_data()
    assert result[0].values.tolist()==["a", "b", "c"]
    assert isinstance(data,pd.DataFrame)
    assert isinstance(format_hashed_df,pd.DataFrame)
    assert isinstance(veri,VERIATIONS)


def test_veriations_functions():
    df             = pd.DataFrame(
        {
            "var1": ["a c", "b w c", "c x"],
            "other_var": [4, 7, 3],
            "yet_another": [8, 0, 2],
        }
    )
    mitter         = FormatCalculator.generate_datamiter(df)
    mitter2        = mitter.formatwise_mitter()
    formateld      = Mitter.hash_str_patterns(mitter2)
    veri           = VERIATIONS(formateld,pd.DataFrame(columns=mitter.get_row_ordring_seq_from_dataset(df,iterlen=3)))
    cols           = veri.formats_and_no_of_patterns()
    sw             = veri.row_sequance_veriations()
    assert isinstance(cols,dict)
    assert isinstance(sw,list)

