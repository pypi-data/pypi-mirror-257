import ast
import itertools
from typing import Optional, List
import pandas as pd

from package.formatcalculator import FormatCalculator


class VERIATIONS:
    """_summary_"""

    def __init__(
        self,
        columnsTable: pd.DataFrame,
        RowTable: pd.DataFrame,
        keyboard: Optional[List] = None,
        Mitter: object = None,
    ) -> None:
        """_summary_

        Args:
            columnsTable (pd.DataFrame): _description_.
            RowTable (pd.DataFrame): _description_.
        """
        self.columnsTable = columnsTable
        self.RowTable = RowTable
        self.keyboard = keyboard
        self.Mitter = Mitter

    def formats_and_no_of_patterns(self):
        col = {}
        for i, v in self.columnsTable.iterrows():
            cd = self.columnsTable.columns.to_list()
            for c in cd:
                sw = None
                try:
                    sw = ast.literal_eval(v[c])
                except Exception:
                    sw = v[c]
                if isinstance(sw, list):
                    col[c] = len(sw)
                else:
                    col[c] = 1
        return col

    def row_sequance_veriations(self):
        """_summary_

        Returns:
            columns: list of columns seq veriations
        """
        veriations = []
        for i, v in enumerate(self.RowTable.columns.to_list()):
            s, d = v.split("|")
            s = s.split("+")
            d = d.split("+")
            s = [x.split("?") if "?" in x else [x] for x in s]
            d = [x.split("?") if "?" in x else [x] for x in d]
            veriations.append({i: [s, d]})
        return veriations

    def solve_iteration(self, string, filter_params=[]):
        """_summary_

        Args:
            string (str): _description_.
            filter_params (list, optional): _description_. Defaults to [].

        Returns:
            _type_: _description_.
        """
        if filter_params != []:
            raise NotImplementedError("filter mitter not implemented")
        d = string.split("?")
        d = [[x[0]] * int(x.split("(")[-1][0:-1]) for x in d]
        flat_list = []
        for inner_list in d:
            flat_list.extend(inner_list)
        return flat_list

    def add_data_slices(self, datalist):
        """_summary_

        Args:
            datalist (_type_): _description_

        Returns:
            _type_: _description_
        """
        rows = []
        for x in range(len(datalist[0])):
            data = [d[x] for d in datalist]
            rows.append("".join(data))
        return rows

    def get_column_row_pattern(self, formatpattern, patternseq):
        """_summary_

        Args:
            formatpattern (_type_): _description_
            patternseq (_type_): _description_

        Returns:
            _type_: _description_
        """
        return "|".join([formatpattern, patternseq])[1:]

    def replace_empty_vals(self, rows):
        """_summary_

        Args:
            rows (_type_): _description_

        Yields:
            _type_: _description_
        """
        for x in rows:
            if "*" in x:
                x = x.replace("*", "")
            yield x

    def generate_row_patterns(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        rowcolslist = []
        for x in self.RowTable.columns.to_list():
            x = x.split("|")
            x = [z.split("+") for z in x]
            r = []
            for s in x:
                w = []
                for q in s:
                    q = self.solve_iteration(q)
                    w.append(q)
                r.append(self.add_data_slices(w))
            x = [list(self.replace_empty_vals(a)) for a in r]
            rowcolslist.append(x)
        return rowcolslist

    def merge(self, list1, list2):
        """_summary_

        Args:
            list1 (_type_): _description_
            list2 (_type_): _description_

        Returns:
            _type_: _description_
        """
        merged_list = ["|".join((list1[i], list2[i])) for i in range(0, len(list1))]
        return merged_list

    def get_columnswise_rowpatterns(self):
        """_summary_

        Returns:
            _type_: _description_.
        """
        colrows = self.generate_row_patterns()
        col = []
        for x in colrows:
            x = self.merge(x[0], x[1])
            col.append(x)
        dataframeconst = dict(enumerate(col))
        return pd.DataFrame.from_dict(dataframeconst)

    def transform_sequences_to_keyboard_values(self):
        """_summary_

        Yields:
            _type_: _description_
        """
        for x, y in self.get_columnswise_rowpatterns().iterrows():
            ye = []
            for z in self.get_columnswise_rowpatterns().columns.to_list():
                val = y[z]
                val = val.split("|")
                data = self.columnsTable.iloc[0, int(val[0])]
                try:
                    data = ast.literal_eval(data)
                except ValueError:
                    pass
                if isinstance(data, list):
                    data = data[int(val[1])]
                data2 = []
                for p in data.split("+"):
                    p = self.solve_iteration(p)
                    data2.append(p)
                data2 = self.add_data_slices(data2)
                ye.append(data2)
            yield ye

    def format_keyboard_values(self):
        """_summary_

        Returns:
            _type_: _description_.
        """
        rows = []
        for x in list(self.transform_sequences_to_keyboard_values()):
            wq = []
            for z in x:
                pds = []
                for p in z:
                    if "*" in p:
                        p = p.replace("*", "")
                        pds.append(p)
                    else:
                        pds.append(p)
                wq.append(pds)
            rows.append(wq)
        return pd.DataFrame(rows, columns=list(range(len(rows[0]))))

    def transform_keybord_seq_to_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        df = self.format_keyboard_values()
        result = []
        for k, _v in df.iterrows():
            data = _v.values.tolist()
            datas = []
            if data != [] and self.keyboard is not None:
                for _g in data:
                    try:
                        _d = ast.literal_eval(_g)
                    except ValueError:
                        _d = _g
                    da = "".join([self.keyboard[int(e)] for e in _d])
                    datas.append(da)
            result.append(datas)
        return pd.DataFrame(result, columns=list(range(len(result[0]))))

    def clssifiy_column_mitterdata(self):
        """_summary_"""
        mitter = self.Mitter.formatwise_mitter()
        formatteddata = []
        for x in mitter.iloc[0].values.tolist():
            if isinstance(ast.literal_eval(x), list):
                x = [
                    (
                        ast.literal_eval(a[0])
                        if isinstance(ast.literal_eval(a[0]), list)
                        else a[0]
                    )
                    for a in ast.literal_eval(x)
                ]
            else:
                try:
                    x = ast.literal_eval(ast.literal_eval(x)[0])
                except SyntaxError as E:
                    print(E)
            formatteddata.append(x)
        mumerixconf = []
        for z in formatteddata:
            datadict = {}
            if isinstance(z[0], list):
                datadict["datalength"] = len(z[0])
                z = list(itertools.chain(*z))
                iterlen = FormatCalculator.find_max_length(z)
                splitdata = []
                for f in range(iterlen):
                    sw = []
                    for p in z:
                        d = None
                        try:
                            d = p[f]
                        except IndexError as E:
                            d = "*"
                        if d is not None:
                            sw.append(d)
                    splitdata.append(sw)
                addslices = []
                for q in splitdata:
                    hashc = ""
                    groups = (
                        (key, sum(1 for _ in values))
                        for (key, values) in itertools.groupby(q)
                    )
                    for color, count in groups:
                        hashc += "?"
                        hashc += color
                        hashc += "({})".format(count)
                    addslices.append(hashc[1:])
                datadict["format"] = "+".join(addslices)
            else:
                datadict["datalength"] = 1
                iterlen = FormatCalculator.find_max_length(z)
                splitdata = []
                for f in range(iterlen):
                    sw = []
                    for p in z:
                        d = None
                        try:
                            d = p[f]
                        except IndexError as E:
                            d = "*"
                        if d is not None:
                            sw.append(d)
                    splitdata.append(sw)
                addslices = []
                for q in splitdata:
                    hashc = ""
                    groups = (
                        (key, sum(1 for _ in values))
                        for (key, values) in itertools.groupby(q)
                    )
                    for color, count in groups:
                        hashc += "?"
                        hashc += color
                        hashc += "({})".format(count)
                    addslices.append(hashc[1:])
                datadict["format"] = "+".join(addslices)
            mumerixconf.append(datadict)
        return pd.DataFrame([mumerixconf], columns=mitter.columns.to_list())

    def divide_chunks(self, l, n):
        """_summary_

        Args:
            l (_type_): _description_
            n (_type_): _description_

        Yields:
            _type_: _description_
        """
        for i in range(0, len(l), n):
            yield l[i : i + n]

    def regenerate_data_from_optimised_mitter(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        data = self.get_columnswise_rowpatterns()
        classifieddata = self.clssifiy_column_mitterdata()
        datalist = []
        for x, y in data.iterrows():
            for s in data.columns.to_list():
                val = y[s]
                val = val.split("|")
                format = classifieddata.columns.to_list()[int(val[0])]
                pattern = classifieddata.iloc[0, int(val[0])]
                wq=None
                if pattern["datalength"] > 1:
                    dataslices = []
                    for q in pattern["format"].split("+"):
                        dataslices.append(self.solve_iteration(q))
                    daa = self.add_data_slices(dataslices)
                    daa = [w.replace("*", "") if "*" in w else w for w in daa]
                    chunckslist = list(self.divide_chunks(daa,pattern['datalength']))
                    wq = chunckslist[int(val[1])]

                else:
                    dataslices = []
                    for q in pattern["format"].split("+"):
                        dataslices.append(self.solve_iteration(q))
                    daa = self.add_data_slices(dataslices)
                    wq = [w.replace("*", "") if "*" in w else w for w in daa][int(val[1])]
                if isinstance(wq,str):
                    y[s]=self.keyboard[int(wq)]
                else:
                    y[s]="".join([self.keyboard[int(o)] for o in wq])
            datalist.append(y.to_dict())
        return pd.DataFrame.from_records(datalist)
