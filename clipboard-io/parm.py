class Parm():
    def __init__(self, name, args: list):
        self.name = name
        self.args = args

    def set(self, value: str|int|float|list[ str|int|float ], index: int|None=None):
        arg_len = len(self.args)

        # single element inputs
        if isinstance(value, (str, int, float)):
            if index and index > arg_len:
                print(f"WARNING: setting value out of index range. Parm {self.name} Val {value} Max Args {arg_len}")
                self.args[index] = value
                return
            else:
                value = [value]
                self.args = value
                return

        # multi element input
        elif isinstance(value, (list, tuple)):
            # list inputs
            if len(value) > arg_len:
                print("WARNING: new parm {self.name} is longer than previous parm.",
                      f"NEW: {value}:{len(value)} old {self.args}:{arg_len}")
            self.args = value

        # unkown input
        else:
            print(f"WARNING: can't set parm {self.name} to type {type(value)}")

        return self
    
    def export(self):
        name = self.name
        locks = "[ 0	locks=0 ]"
        args = "\t".join(self.args)
        export = name+"\t"+locks+"\t(\t"+args+"\t)"

        return export

    def __str__(self):
        return f"{self.name}:{self.args}"
