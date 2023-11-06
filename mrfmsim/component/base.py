"""Base component."""

from dataclasses import dataclass, asdict


@dataclass
class ComponentBase:
    def __str__(self):
        """Reformat the dataclass string output.
        
        The default format is 3 decimal places for floats.
        For custom format, define format in the field metadata.
        """

        str_lines = []
        for k, v in asdict(self).items():
            unit = self.get_unit(k)
            format = self._get_metadata(k).get("format", ".3f")
            if isinstance(v, float):
                # round the float values
                str_lines.append(f"\t{k}={v:{format}} {unit}".rstrip())
            else:
                str_lines.append(f"\t{k}={str(v)} {unit}".rstrip())

        return "{}({})".format(self.__class__.__name__, "\n".join(str_lines).strip())

    def _get_metadata(self, attr):
        """Get the metadata for the attribute.

        The metadata are defined in the fields of the
        dataclass attributes.
        """

        if attr in self.__dataclass_fields__:
            return self.__dataclass_fields__[attr].metadata
        else:
            return {}

    def get_unit(self, attr):
        """Get the units of the attributes.

        If the units are undefined, None is returned.
        """

        if hasattr(self, attr):
            return self._get_metadata(attr).get("unit", "")
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")
