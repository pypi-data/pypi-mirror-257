import itertools 

if __name__ == "__main__":
    from common import Entry, TAB, MINUS_TAB, NL, SEP, NaN
else:
    from .common import Entry, TAB, MINUS_TAB, NL, SEP, NaN


class Write():
    def __init__(self):
        self.buffer = ""
        self.last_keys = None
        self.max_buffer_size = 400
        self.is_1stentry = False
    
    def write_entry(self, entry, is_mini=False):
        if entry.is_single_value:
            self.buffer += entry.parent + SEP + entry.obj + NL
            self.buffer += NL
        elif entry.is_ylist:
            if not self.is_1stentry:  
                self.buffer += entry.parent + SEP + NL
                if is_mini:
                    for i, key in enumerate(entry.obj.keys()):
                        if i==0:
                            item = 2*MINUS_TAB + key + SEP 
                        else:
                            item = TAB + MINUS_TAB + key + SEP 
                        self.buffer += TAB + item + NL
            if is_mini:
                for i, val in enumerate(entry.obj.values()):
                    if i == 0:
                        head = 2*MINUS_TAB
                    else:
                        head = TAB + MINUS_TAB
                    item = TAB + head +  val
                    self.buffer += item + NL
            else:
                for i, keyval in enumerate(entry.obj.items()):
                    key, val = keyval
                    if i == 0:
                        key = MINUS_TAB + key
                    else:
                        key = TAB + key
                    item = TAB + key + SEP + val
                    self.buffer += item + NL
        else:
            self.buffer += entry.parent + SEP + NL
            self.last_keys = entry.obj.keys()
            for i, keyval in enumerate(entry.obj.items()):
                key, val = keyval
                item = TAB + key + SEP  + val
                self.buffer += item + NL
            self.buffer += NL
            
        self.is_1stentry = entry.is_ylist


    def write(self, f, entries, is_mini=False):
        config_entry_num = 0
        data_entry_num = 0
        try:
            for entry in entries:
                data_entry_num +=  int(entry.is_ylist)
                config_entry_num += int(not entry.is_ylist)
                self.write_entry(entry, is_mini=is_mini)
                if len(self.buffer) > self.max_buffer_size:
                    f.write(self.buffer)
                    self.buffer = ""
        except Exception as e:
            if data_entry_num:
                raise type(e)("Exception! while writing the {}-th entry in the provided data:\n".format(data_entry_num) + \
                                repr(e)) from e
            else:
                raise type(e)("Exception! while writing the {}-th entry in the provided meta/attrs/config data:\n".format(config_entry_num) + \
                                repr(e)) from e
        f.write(self.buffer)

def write_dataframe(f, df, is_mini=False, name='data'):
    itr = df.iterrows()
    itr = df.to_dict(orient="records")
    itr = map(lambda x: Entry.from_dict(parent=name, obj=x, is_ylist=True), itr)
    
    if df.attrs:
        itr = itertools.chain(Entry.dict2d_to_entries(df.attrs), itr)

    write = Write()
    write.write(f, itr, is_mini=is_mini)

def write_dataframe_from_path(path, df, is_mini=False, name='data', encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as f:
        write_dataframe(f, df, is_mini=is_mini, name=name)


def write_dict2d(path, dict2d):
    itr = Entry.dict2d_to_entries(df.attrs)
    write = Write()
    write.write(path, itr)

def append_write(path, dict1d):
    entry = Entry.from_dict(dict1d, parent=None, is_ylist=True)
    write = Write()
    write.write(path, [entry], flag='a')

if __name__ == "__main__":
    import pandas as pd

    data = {'Name': ['Alice', 'Bob', 'Charlie'],
            'Age2': [25, 30, 22],
            'Age':  [25, 30, 22],
            'City': ['New York', 'San Francisco', 'Los Angeles']}

    df = pd.DataFrame(data)
    df.attrs = {'x': 32323.3}
    df.attrs['liest'] = [12,33,45,353]
    write_dataframe('./out.yaml', df, "dataie")
    write_dict2d('./dict2d.yaml', df.attrs)
    append_write('./out.yaml', {"Appended": "Appended",
    "Age2": 22,
    "Age": 22,
    "City": "Los Angeles"})
