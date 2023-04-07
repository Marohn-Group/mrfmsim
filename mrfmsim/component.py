from collections import defaultdict
import numpy as np


class ComponentBase:
    """The base component class defines the __repr__ method."""

    _units = {}
    # _parameters = () # list the accessible parameters

    def attrs_to_dict(self):
        """Output attributes to dictionary format."""

        return {
            key: value
            for key, value in sorted(
                vars(self).items(), key=lambda pair: pair[0].lower()
            )
            if not key.startswith("_")
        }

    def __str__(self):
        """Modify the string representation of Components.

        In the format of key=value unit description.
        For int and float, the format is set in the units.yaml
        For lists or numpy arrays, the format is set first with
        np.printoptions.
        """

        name = self.__class__.__name__
        str_list = []
        for key, value in self.attrs_to_dict().items():
            u_dict = self._units.get(key, defaultdict(str))

            des = u_dict["description"]
            if des:
                des = f" # {u_dict['description']}"
            unit = u_dict["unit"]
            if unit:
                unit = f" {unit}"

            formatter = "{{{}}}".format(u_dict["format"]).format
            if isinstance(value, list):
                # convert list to numpy array for representation
                # normally carries integers, exclude the tuple cases
                value = np.array(value)
            if isinstance(value, np.ndarray):
                with np.printoptions(formatter={"all": formatter}):
                    s = "\t{}={}{}{}".format(key, value, unit, des)
            else:
                value_str = formatter(value)
                s = "\t{}={}{}{}".format(key, value_str, unit, des)

            str_list.append(s.expandtabs(2))


        return f"{name}(\n" + "\n".join(str_list) + "\n)"
