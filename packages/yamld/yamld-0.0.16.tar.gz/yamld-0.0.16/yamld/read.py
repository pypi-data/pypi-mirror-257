import pandas as pd
from ast import literal_eval
import warnings

if __name__ == "__main__":
    from common import Entry, NaN
else:
    from .common import Entry, NaN


class Read():
    FIRST_CHAR2TYPES = {
        '[': list,
        '"': str,
        "'": str,
    }

    LIST_CAST_TYPES = {
        (int, float): float,
        (float, int): float
    }


    def __init__(self, is_onelist=False, tgt_parent=None):
        self.is_onelist = is_onelist
        self.tgt_parent = tgt_parent
        
        #init read
        self.out = None
        self.current_parent = None
        self.prev_parent = None
        self.list_counter = 0
        self.yaml_obj = dict()
        self.yaml_obj_types = dict()
        self.all_types = dict()
        self.list_counter = 0
        self.block_seq_len = 0
        self.is_mini_data = False
        self.columns = {}
        self.is_data_1straw = False

        #line state
        self.key = None
        self.value = None
        self.is_parent = False
        self.is_child = False
        self.is_entry_minus = False
        self.is_double_minus = False
        self.is_obj_parsing_done = False
        self.is_single_value = False
        self.is_obj_still_parsing = False
    
    @classmethod
    def _ylist_type_cast(cls, old_types, new_types):
        def c(fromto):
            from_type, to_type = fromto
            if to_type is None or from_type is None:
                return from_type if from_type else to_type

            if from_type == to_type:
                return from_type
            else:
                new_type =  cls.LIST_CAST_TYPES.get(fromto, False)
                if not new_type:
                    raise warnings.warn(f'Unsuported mixed datatypes, tyring to cast {from_type} to {to_type}. Will default to general object type')
                    new_type = object
                return new_type
        
        return map(c, zip(old_types.values(), new_types.values()))

    @classmethod
    def infer_type(cls, value):
        ytype = cls.FIRST_CHAR2TYPES.get(value[0], False)
        if not ytype:
            if value == NaN:
                ytype = None
            else:
                ytype = float if '.' in value else int
        return ytype

    def _reset(self):
        #reset and skip
        if self.is_parent:
            if self.is_onelist and self.list_counter:
                raise Exception("You specified a one list('-') yaml2d file but a key was found after parsing the list")
            else:
                self.current_parent = self.key
            #TODO onelist is the default
            #self.list_counter = 0
            
        if self.is_obj_parsing_done:
            self.yaml_obj = dict()
            self.yaml_obj_types = dict()
            


    def process_line(self, line):
        striped_line = line.strip()
        if not striped_line:
            return True

        self.is_child = line[0].isspace()
        self.is_parent = not self.is_child
        line = striped_line

        keyvalue = line.strip().split(':', 1)
        if len(keyvalue) == 1:
            is_colon = False
            self.key, self.value =  keyvalue[0], None
        else:
            #note: relying on `len(':'.split(':')) == 2`
            is_colon = True
            self.key, self.value = keyvalue
            self.key, self.value = self.key.strip(), self.value.strip()
        
        
        if self.is_parent and not self.current_parent:
            self.current_parent = self.key

        self.is_single_value = self.is_parent and bool(self.value)

        minus_counter = int(self.key[0:2] == '- ')
        if minus_counter:
            self.key = self.key[1:].strip()
            minus_counter +=  int(self.key[0:2] == '- ')
            if minus_counter > 1:
                self.key = self.key[1:].strip()
            
        if minus_counter > 1:
            self.is_mini_data = True
            
        self.is_double_minus = minus_counter == 2
        self.is_entry_minus = self.is_double_minus or \
                            (minus_counter == 1 and \
                             not self.is_mini_data)

        self.is_obj_parsing_done = (self.is_parent or self.is_entry_minus) and bool(self.yaml_obj)
        self.list_counter += self.is_entry_minus
        self.is_data_1straw = self.list_counter == 1

        if self.is_double_minus:
            self.block_seq_len = 0
        if self.block_seq_len or self.is_double_minus:
            self.block_seq_len += 1
            if self.is_data_1straw and is_colon:
                self.columns[self.block_seq_len - 1] = self.key
                return True
            else:
                self.value = self.key
                try:
                    self.key = self.columns[self.block_seq_len - 1]
                except KeyError as e:
                    raise Exception('Probably violated fixed set of features: ' + str(e)) from e

        #states
        if self.is_child:
            self.is_obj_still_parsing = True
        if self.is_parent:
            self.is_obj_still_parsing = False
        
        
    def parsing_obj(self):
        self.yaml_obj[self.key] = self.value
        ytype = self.infer_type(self.value)        
        self.yaml_obj_types[self.key] = ytype


    def read_obj(self):
        if self.list_counter and self.current_parent in self.all_types:
            #casting
            new_obj_types = self.all_types[self.current_parent]
            new_obj_types = self._ylist_type_cast(self.all_types[self.current_parent], self.yaml_obj_types)
            self.yaml_obj_types = dict(zip(self.yaml_obj_types.keys(), new_obj_types))
        self.all_types[self.current_parent] = self.yaml_obj_types
        return True


    def read_generator(self, lines):
        line_num = 0
        for line in lines:
            line_num += 1
            if self.process_line(line):
                continue
            if self.is_obj_parsing_done:
                if self.read_obj():
                    yield Entry(
                        parent=self.current_parent,
                        obj=self.yaml_obj,
                        ytype=self.yaml_obj_types,
                        is_ylist= bool(self.list_counter),
                        is_single_value= False,
                    ), line_num
            if self.is_single_value:
                    yield Entry(
                        parent= self.key,
                        obj=self.value,
                        ytype= self.infer_type(self.value),
                        is_single_value= True,
                        is_ylist= False,
                    ), line_num

            self._reset()
            if self.is_obj_still_parsing:
                self.parsing_obj()
        if self.is_obj_still_parsing:
            if self.read_obj():
                yield Entry(
                    obj=self.yaml_obj,
                    ytype=self.yaml_obj_types,
                    is_ylist= bool(self.list_counter),
                    is_single_value= False,
                ), line_num
            yield Entry(is_last=True), line_num


def _python_eval(value):
    if value == NaN:
        return None
    return literal_eval(value)


def read_onelist_meta(lines):
    read = Read(is_onelist=True, tgt_parent=None)
    out = {}
    try:
        for entry, line_num in read.read_generator(lines):
            if entry.is_ylist:
                return out
            if entry.is_single_value:
                out[entry.parent] = _python_eval(entry.obj)
            else:
                out[entry.parent] = {k: _python_eval(v) for k, v in entry.obj.items()}
        return out
    except Exception as e:
        raise Exception("Exception was raised. Last parsed line in the provided YAML was: {} \n".format(line_num) + \
                         str(e)) from e
                 
def read_onelist_meta_from_file(path):
    with open(path, 'r') as f:
        return read_onelist_meta(f)

def read_onelist_generator(lines, transform=None):
    read = Read(is_onelist=True, tgt_parent=None)
    def gen():
        try:
            for entry, line_num in read.read_generator(lines):
                if not entry.is_ylist:
                    continue
                tmp = {k: _python_eval(v) for k, v in entry.obj.items()}
                if transform:
                    tmp = transform(tmp)
                yield tmp
        except Exception as e:
            raise type(e)("Exception! last parsed line was {} in the provided YAML:\n".format(line_num) + \
                            repr(e)) from e
                     
    return gen

def read_onelist_generator_from_file(path):
    def gen():
        with open(path, 'r') as f:
            readgen =  read_onelist_generator(f)
            for item in readgen():
                yield item
    return gen

def read_onelist_dataframe(lines):
    read = Read(is_onelist=True, tgt_parent=None)
    data = {}
    gen = read_onelist_generator(lines)
    test = -1
    for entrydict in gen():
        if not data:
            data = {k:[v] for k,v in entrydict.items()}
            test = len(data)
        else:
            try:
                for k, v in entrydict.items():
                    data[k].append(v)
                assert len(entrydict) == test
            except KeyError as e:
                raise Exception('Probably violated YAML (-)list must contain fixed features, KeyError was raised: ' + str(e)) from e
    df = pd.DataFrame(data)
    return df

def read_onelist_dataframe_from_file(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        meta =  read_onelist_meta(f)
    with open(path, 'r', encoding=encoding) as f:
        df = read_onelist_dataframe(f)
    if hasattr(df, 'attrs'):
        df.attrs.update(meta)
    return df



if __name__ == "__main__":
    yamlf = """
config1:
  key1: 'value1'
  key2: 'value2'
  key3: 'value3'

config2:
  keyA: 'valueA'
  keyB: 'valueB'
  keyC: 'valueC'

data:
  - name: 'John Doe'
    age: 30
    city: 'New York'
  - name: 'Jane Smith'
    age: 25
    city: 'San Francisco'
  - name: 'Bob Johnson'
    age: 35
    city: 'Chicago'
  - name: 'Test'
    age: 35.0
    city: 'Chicago'
    """

    out = read_onelist_meta(yamlf.splitlines())
    print(out)
    gen = read_onelist_generator(yamlf.splitlines())

    for item in gen():
        print(item)
