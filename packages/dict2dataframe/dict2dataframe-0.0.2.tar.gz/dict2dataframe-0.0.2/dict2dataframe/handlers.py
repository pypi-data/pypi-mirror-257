#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

"""
Data handlers.
"""

from typing import Iterator, List, Tuple
from collections import OrderedDict
from benedict import benedict
from copy import deepcopy
import pandas as pd
import logging
import json

try:
    from collections.abc import Mapping
except:
    from collections import Mapping


LOGGER = logging.getLogger(__name__)


def sort_dict_by_hierarchy(d: dict, ascending: bool = True) -> dict:
    """
    Sorts the dictionary by hierarchy level.

    Parameters
    ----------
    d : dict
        The dictionary to be sorted.
    ascending : bool, optional
        If True, sorts in ascending order, otherwise sorts in descending order.
        Defaults to True.

    Returns
    -------
    dict
        The sorted dictionary.

    Examples
    --------
    >>> d = {'b': 2, 'a': 1, 'c': {'z': 26, 'y': 25}}
    >>> sort_dict_by_hierarchy(d)
    {'a': 1, 'b': 2, 'c': {'y': 25, 'z': 26}}

    """
    sorted_items = []

    for key, value in d.items():
        if isinstance(value, (list, tuple)):
            new_value = [sort_dict_by_hierarchy(v, ascending) for v in value]
            sorted_items.append((1, (key, new_value)))
        elif isinstance(value, dict):
            new_value = sort_dict_by_hierarchy(value, ascending)
            sorted_items.append((1, (key, new_value)))
        else:
            sorted_items.append((0, (key, value)))

    sorted_items.sort(key=lambda x: x[0], reverse=not ascending)
    sorted_dict = dict([item[1] for item in sorted_items])

    return sorted_dict


def flatten_dict(data: dict, prefix: str = "", sep: str = "_", keep_breadcrumb: bool = True) -> dict:
    """
    Flattens a dictionary, causing all its keys to be moved to the root, at the first hierarchical level.

    Parameters
    ----------
    data: dic
        Dictionary.
    prefix: str
        Prefix added to the keys of the first hierarchy level.
    sep: str
        Hierarchical key separator.
    keep_breadcrumb: bool
        Whether to keep hierarchical level in keys.

    Returns
    -------
    dict
        Flatten dictionary.
    """
    leaf_items = {}

    for key, value in data.items():
        new_prefix = f"{prefix}{sep}{key}" if keep_breadcrumb and prefix else key

        if isinstance(value, dict):
            leaf_items.update(flatten_dict(data=value, prefix=new_prefix, sep=sep, keep_breadcrumb=keep_breadcrumb))
        else:
            leaf_items[new_prefix] = value

    return leaf_items


def merge_dict(a: dict, b: dict) -> dict:
    """
    Merges two simple and non-hierarchical dictionaries.

    Parameters
    ----------
    a: dict
        Dictionary.
    b: dict
        Dictionary.

    Returns
    -------
    dict
        Merged dictionary.

    Notes
    -----
    To merge complex/hierarchical dictionaries, use the `merge()` method from `gpa_orchestrator.handlers.Dict` class.
    """
    x, y = a, b

    if not isinstance(a, dict):
        x = a.__json__()

    if not isinstance(b, dict):
        y = b.__json__()

    x.update(y)

    return x


class Dict:
    """Dictionary handler with indexing based on nested keys."""

    _data: dict
    """Dictionary."""

    def __init__(self, data: dict = None):
        """
        Instantiates a dictionary object with nested keys-based indexing.

        Parameters
        ----------
        data: dict
            Dictionary.

        References
        ----------
        .. [1] Class `Dict`: https://stackoverflow.com/a/70908985/16109419

        .. [2] Package `Benedict`: https://github.com/fabiocaccamo/python-benedict

        .. [3] Dictionary nested iteration: https://stackoverflow.com/a/10756615/16109419
        """
        self._data = deepcopy(data) if data else {}

    @property
    def data(self) -> dict:
        """
        Data.

        Returns
        -------
        dict
            Data.
        """
        return self._data

    def get(self, keys: list, **kwargs) -> (object, bool):
        """
        Get dictionary item value based on nested keys.

        Parameters
        ----------
        keys: list
            Nested keys to get item value based on.
        **kwargs
            Keyword-based arguments.

        Returns
        -------
        (object, bool)
            Item value, and whether the target item was found.
        """
        data = kwargs.get('data', self._data)
        path = kwargs.get('path', [])
        value, found = None, False

        # Looking for item location on dictionary:
        for outer_key, outer_value in data.items():
            trace = path + [outer_key]

            # Getting item value from dictionary:
            if trace == keys:
                value, found = outer_value, True
                break

            if trace == keys[:len(trace)] and isinstance(outer_value, Mapping):  # Recursion cutoff.
                value, found = self.get(
                    data=outer_value,
                    keys=keys,
                    path=trace
                )

        return value, found

    def set(self, keys: list, value: object, **kwargs) -> bool:
        """
        Set dictionary item value based on nested keys.

        Parameters
        ----------
        keys: list
            Nested keys to set item value based on.
        value: object
            Item value.
        **kwargs
            Keyword-based arguments.

        Returns
        -------
        bool
            Whether the target item was updated.
        """
        data = kwargs.get('data', self._data)
        path = kwargs.get('path', [])
        updated = False

        # Looking for item location on dictionary:
        for outer_key, outer_value in data.items():
            trace = path + [outer_key]

            # Setting item value on dictionary:
            if trace == keys:
                data[outer_key] = value
                updated = True
                break

            if trace == keys[:len(trace)] and isinstance(outer_value, Mapping):  # Recursion cutoff.
                updated = self.set(
                    data=outer_value,
                    keys=keys,
                    value=value,
                    path=trace
                )

        return updated

    def add(self, keys: list, value: object, **kwargs) -> bool:
        """
        Add dictionary item value based on nested keys.

        Parameters
        ----------
        keys: list
            Nested keys to add item based on.
        value: object
            Item value.
        **kwargs
            Keyword-based arguments.

        Returns
        -------
        bool
            Whether the target item was added.
        """
        data = kwargs.get('data', self._data)
        added = False

        # Adding item on dictionary:
        if keys[0] not in data:
            if len(keys) == 1:
                data[keys[0]] = value
                added = True
            else:
                data[keys[0]] = {}

        # Looking for item location on dictionary:
        for outer_key, outer_value in data.items():
            if outer_key == keys[0]:  # Recursion cutoff.
                if len(keys) > 1 and isinstance(outer_value, Mapping):
                    added = self.add(
                        data=outer_value,
                        keys=keys[1:],
                        value=value
                    )

        return added

    def remove(self, keys: list, **kwargs) -> bool:
        """
        Remove dictionary item based on nested keys.

        Parameters
        ----------
        keys: list
            Nested keys to remove item based on.
        **kwargs
            Keyword-based arguments.

        Returns
        -------
        bool
            Whether the target item was removed.
        """
        data = kwargs.get('data', self._data)
        path = kwargs.get('path', [])
        removed = False

        # Looking for item location on dictionary:
        for outer_key, outer_value in data.items():
            trace = path + [outer_key]

            # Removing item from dictionary:
            if trace == keys:
                del data[outer_key]
                removed = True
                break

            if trace == keys[:len(trace)] and isinstance(outer_value, Mapping):  # Recursion cutoff.
                removed = self.remove(
                    data=outer_value,
                    keys=keys,
                    path=trace
                )

        return removed

    def items(self, **kwargs) -> Iterator[List[Tuple[List, object]]]:
        """
        Get dictionary items based on nested keys.

        Returns
        -------
        keys, value: Iterator[List[Tuple[List, object]]]
            List of nested keys and list of values.
        **kwargs
            Keyword-based arguments.
        """
        data = kwargs.get('data', self._data)
        path = kwargs.get('path', [])

        for outer_key, outer_value in data.items():
            if isinstance(outer_value, Mapping):
                for inner_key, inner_value in self.items(data=outer_value, path=path + [outer_key]):
                    yield inner_key, inner_value
            else:
                yield path + [outer_key], outer_value

    @staticmethod
    def merge(dict_list: [dict], overwrite: bool = False, concat: bool = False, default_value: object = None) -> dict:
        """
        Merges dictionaries, with value assignment based on order of occurrence. Overwrite values if and only if:
            - The key does not yet exist on merged dictionary;
            - The current value of the key on merged dictionary is the default value.

        Parameters
        ----------
        dict_list: [dict]
            List of dictionaries.
        overwrite: bool
            Overwrites occurrences of values. If false, keep the first occurrence of each value found.
        concat: bool
            Concatenates occurrences of values for the same key.
        default_value: object
            Default value used as a reference to override dictionary attributes.

        Returns
        -------
        dict
            Merged dictionary.
        """
        dict_list = [d for d in dict_list if d and isinstance(d, dict)] if dict_list else []
        assert len(dict_list), f"no dictionaries given."

        # Keeping the first occurrence of each value:
        if not overwrite:
            dict_list = [Dict(d) for d in dict_list]

            for i, d in enumerate(dict_list[:-1]):
                for keys, value in d.items():
                    if value != default_value:
                        for j, next_d in enumerate(dict_list[i+1:], start=i+1):
                            next_d.remove(keys=keys)

            dict_list = [d._data for d in dict_list]

        md = benedict()
        md.merge(*dict_list, overwrite=True, concat=concat)

        return md


class JSON:
    """JSON file handler."""

    _dict_list: [dict]
    """List of dictionaries."""
    _key_sep: str
    """Separator for merging nested keys."""
    _dump_objects: bool
    """Whether to dump objects."""

    def __init__(self, dict_list: [dict], key_sep: str = "_", dump_objects: bool = False):
        """
        Instantiates a JSON processing object.

        Parameters
        ----------
        dict_list: [dict]
            List of dictionaries.
        key_sep: str
            Nested keys separator.
        dump_objects: bool
            Whether to dump objects.

        References
        ----------
        .. [1] Class `JSON`: https://stackoverflow.com/a/70791993/16109419

        .. [2] Class `Dict`: https://stackoverflow.com/a/70908985/16109419
        """
        self._key_sep = key_sep
        self._dump_objects = dump_objects

        # Sorting dictionaries by hierarchy level (requirement):
        dict_list = [sort_dict_by_hierarchy(d) for d in dict_list]

        # Serializing dictionaries before processing them (requirement):
        self._dict_list = [self._serialize(data=d, dump_objects=dump_objects) for d in dict_list]

    @property
    def dict_list(self) -> [dict]:
        """
        Dictionaries list.

        Returns
        -------
        dict_list: [dict]
            Dictionaries list.
        """
        return self._dict_list

    @property
    def key_sep(self) -> str:
        """
        Dictionary keys separator.

        Returns
        -------
        key_sep: str
            Dictionary keys separator.
        """
        return self._key_sep

    @staticmethod
    def _serialize(data: dict, dump_objects: bool = False) -> [dict]:
        """
        Serializes the objects contained in the dictionary.

        Parameters
        ----------
        data: dict
            Dictionary.
        dump_objects: bool
            Whether to dump objects.

        Returns
        -------
        dict
            Dictionary.

        Notes
        -----
        This method is required to handle data types not supported by the JSON standard.
        For instance, only native data types are supported in Python (e.g., str, int).
        Custom objects values are dumped into the dictionaries structure.
        """
        serialized_d = Dict(data=data)

        for keys, value in serialized_d.items():
            parsed, parsed_value = False, None

            if hasattr(value, 'isoformat'):  # Date/Datetime object.
                parsed = True
                parsed_value = value.isoformat() if dump_objects else value
            elif hasattr(value, '__dict__'):  # Custom object.
                parsed = True
                value_vars = vars(value)
                value_vars_str = str(value_vars)
                value_str = str(value)

                if value_vars_str == value_str:  # Dict-based object.
                    parsed_value = JSON._serialize(data=value_vars, dump_objects=dump_objects)
                else:  # Not dict-based object.
                    if dump_objects:
                        parsed_value = JSON._serialize(data=value_vars, dump_objects=dump_objects)
                    else:
                        parsed_value = value_str

            if parsed:
                serialized_d.set(keys=keys, value=parsed_value)

        data = serialized_d.data

        return data

    def _dict_to_list(
            self,
            sub_tree: dict,
            current_list: [str],
            items_list: [list]
    ) -> [list]:
        """
        Convert dictionary to items list.

        Parameters
        ----------
        sub_tree : dict
            The subtree of the dictionary to process.
        current_list : list
            The current list representing the path in the dictionary.
        items_list : list
            The list to which items are added.

        Returns
        -------
        list
            The list of items list.

        Notes
        -----
        This function converts a dictionary into a list of items list. Each item list
        represents a path through the dictionary, ending with a leaf value.

        """
        try:  # Tree branches.
            for key in sub_tree:
                if isinstance(sub_tree[key], (list, tuple)):
                    for sub_item in sub_tree[key]:
                        self._dict_to_list(
                            sub_tree=sub_item,
                            current_list=current_list + [key],
                            items_list=items_list
                        )
                elif isinstance(sub_tree[key], dict):
                    self._dict_to_list(
                        sub_tree=sub_tree[key],
                        current_list=current_list + [key],
                        items_list=items_list
                    )
                else:
                    items_list.append(current_list + [key] + [sub_tree[key]])
        except:  # Tree leaf.
            items_list.append(current_list + [sub_tree])

        return items_list

    def _extract_entries(self) -> [[(str, object)]]:
        """
        Extracts entries from a dictionary.

        Returns
        -------
        [[(str, object)]]
            List of key-value items list.
        """
        entries = []

        for parent in self._dict_list:
            key_value_tuples = []
            items_list = self._dict_to_list(sub_tree=parent, current_list=[], items_list=[])

            for child in items_list:
                key_parts = child[:-1]
                key = self._key_sep.join([str(i) for i in key_parts])
                value = child[-1]
                key_value_tuples.append((key, value))

            entries.append(key_value_tuples)

        return entries

    @staticmethod
    def _get_nth_element(
        items: [(str, object)],
        element: str,
        nth: int = 1
    ) -> ((str, object), bool):
        """
        Get nth element (occurrence) from items list.

        Parameters
        ----------
        items: [(str, object)]
            Items list.
        element: str
            Item key.
        nth: int
            Nth element position.

        Returns
        -------
        ((str, object), bool)
            Nth element, and whether it was not found.
        """
        assert nth >= 1, f"'nth' ({nth}) must be >= 1."

        occurrences = [i for i in items if i[0] == element]
        n_occurrences = len(occurrences)

        if n_occurrences:
            index_out_of_bounds = True if nth > n_occurrences else False
            nth_element = occurrences[min(nth, n_occurrences) - 1]
        else:
            nth_element = None
            index_out_of_bounds = True

        return nth_element, index_out_of_bounds

    def _to_tuples(self) -> ([str], [tuple]):
        """
        Convert JSON semi-structured data into structured tuples data.

        Returns
        -------
        ([str], [tuple])
            List of keys and values.

        Examples
        --------
        >>> data = {"values":[{"A": 0,"B": 1,"C": 2},{"C": {"E": 3,"F": 4},"D": [{"G": 5},{"H": 6}]}]}
        >>> JSON(data['values'])._to_tuples()
        (["A", "B", "C", "C_E", "C_F", "D_G", "D_H"],[(0, 1, 2, None, None, None, None),(None, None, None, 3, 4, 5, 6)])
        """
        LOGGER.debug(f"Extracting values tuples from dictionary...")
        entries = self._extract_entries()
        keys = list(
            OrderedDict.fromkeys(
                [
                    key_value_tuple[0]
                    for samples in entries
                    for key_value_tuple in samples
                ]
            )
        )

        # Ensuring that all dict hierarchical levels have the same features/columns:
        key_index = 0

        for i, entry_list in enumerate(entries):
            for j, entry in enumerate(entry_list):
                if entry[0] != keys[key_index]:
                    entries[i].insert(j, (keys[key_index], None))

                key_index += 1

                if key_index == len(keys):
                    key_index = 0

            if entry_list[i][-1] != keys[key_index]:
                while True:
                    entries[i].append((keys[key_index], None))

                    key_index += 1

                    if key_index == len(keys):
                        key_index = 0
                        break

        n_entries = len(entries)
        n_keys = len(keys)
        values = []

        for tuples, index in zip(entries, range(1, n_entries + 1)):
            LOGGER.debug(f"Processing values from entry {index}/{n_entries} ({((index / n_entries) * 100):.2f}%)...")

            for i in range(1, len(tuples) + 1):
                index_out_of_bounds_count = 0
                row = []

                for c in keys:
                    key_value_tuple, index_out_of_bounds = self._get_nth_element(items=tuples, element=c, nth=i)
                    row.append(key_value_tuple[1]) if key_value_tuple else row.append(None)

                    if index_out_of_bounds:
                        index_out_of_bounds_count += 1

                if index_out_of_bounds_count == n_keys:
                    break

                if row.count(None) != n_keys:
                    values.append(row)

        return keys, values

    @staticmethod
    def _fill_values(values_list: list) -> list:
        """
        Fills missing values in a list with the last non-missing value.

        Parameters
        ----------
        values_list : list
            A list of values.

        Returns
        -------
        list
            The list with missing values filled.

        Examples
        --------
        >>> _fill_values([1, None, 2, None, 3, None])
        [1, 1, 2, 2, 3, 3]
        """
        if values_list[0] is None:
            return values_list

        current_value = values_list[0]

        for i, value in enumerate(values_list):
            if value is None:
                values_list[i] = current_value
            else:
                current_value = value

        return values_list

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert JSON semi-structured data to a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            A DataFrame representation of the object.

        Notes
        -----
        The method internally calls _to_tuples to get the columns and rows,
        then constructs a DataFrame using these columns and rows.

        Examples
        --------
        >>> data = {"values": [{"a": 1, "b": {"x": 10, "y": 20 }, "c": 2, "d": [{"z": 30 } ] }, {"a": 5, "b": {"x": 15, "y": 25 }, "c": 6, "d": [{"z": 35 } ] }, {"a": 9, "b": {"x": 20, "y": 30 }, "c": 10, "d": [{"z": 40 } ] } ] }
        >>> df = JSON(dict_list=data['values'], dump_objects=False).to_dataframe()
        >>> print(df)
           a   c  b_x  b_y  d_z
        0  1   2   10   20   30
        1  5   6   15   25   35
        2  9  10   20   30   40
        """
        LOGGER.debug(f"Converting Dictionary to Pandas Dataframe...")
        columns, rows = self._to_tuples()
        df = pd.DataFrame(rows, columns=columns)

        for column in df.columns:
            df[column] = self._fill_values(df[column].to_list())

        return df


def extract_json_from_text(text: str) -> dict:
    """
    Extract JSON content from text.

    Parameters
    ----------
    text: str
        Text.

    Returns
    -------
    dict
        JSON content.
    """
    json_content = None

    text = " ".join(text.replace("\n", " ").split()).replace("'", "\"")

    try:
        # Find the starting position of the first '{' (opening of the JSON)
        opening_position = text.find('{')

        # Check if the opening of the JSON is found
        if opening_position != -1:
            # Find the closing position of the corresponding '}'
            closing_position = text.find('}', opening_position + 1)

            # Check if the closing brace is found
            if closing_position != -1:
                # Extract the JSON substring
                json_string = text[opening_position:closing_position + 1]

                # Load the JSON
                json_object = json.loads(json_string)
                json_content = json_object
            else:
                logging.warning("Closing brace '}' not found.")
        else:
            logging.warning("Opening brace '{' not found.")
    except json.JSONDecodeError as e:
        logging.warning(f"Error decoding the JSON: {str(e)}")
        pass

    return json_content
