from typing import Tuple, Union


def pop_from_dict(data, keys: Union[str, Tuple[str, ...]]):
    if isinstance(keys, str):
        keys = (keys,)
    if not isinstance(keys, tuple):
        keys = tuple(keys)
    main = data.copy()
    for key in keys:
        if key in main:
            main.pop(key)
    return main
    # return {k: data[k] for k in data.keys() - keys}


class LabelDict(dict):
    def __init__(self, data, **kwargs):
        super().__init__(data)
        for k, d in kwargs.items():
            obj = self.copy()
            obj.update(d)
            setattr(self, k, obj)

    def __sub__(self, other):
        if isinstance(other, (tuple, str)):
            return LabelDict(pop_from_dict(self, other))
        return super().__sub__(other)  # pylint: disable=E1101

    def __and__(self, other):
        if isinstance(other, str):
            other = (other,)
        if isinstance(other, tuple):
            return LabelDict({k: self.get(k) for k in other if k in self})
        return super().__sub__(other)  # pylint: disable=E1101

    def __or__(self, other):
        main = self.copy()
        for k, v in other.items():
            main.setdefault(k, v)
        return LabelDict(main)

    def __ror__(self, other):
        main = other.copy()
        for k, v in self.items():
            main.setdefault(k, v)
        return LabelDict(main)
