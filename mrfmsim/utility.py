from types import MappingProxyType
from inspect import signature, Signature


class ConfigBase:
    """Store constructor information for class instances.

    The stored values help recreate the instance when needed.
    """

    def __new__(cls, *args, **kwargs):

        sig = Signature(list(signature(cls.__init__).parameters.values())[1:])
        instance = super().__new__(cls)

        instance._constructor_args = args
        instance._constructor_kwargs = kwargs
        instance._constructor_signature = sig
        return instance

    @property
    def _mapped_parameters(self):
        """Create a mapping of constructor arguments to their values.

        The mapping assumes that there is no positional only and
        variable positional arguments.
        """
        sig = self._constructor_signature
        args = self._constructor_args
        kwargs = self._constructor_kwargs
        arg_dict = dict(zip(sig.parameters.keys(), args))
        return {**arg_dict, **kwargs}
