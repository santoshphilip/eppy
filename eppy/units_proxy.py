# Copyright (c) 2026 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# TODO module docstring

class UnitsProxy:
    """Proxy that lets you do obj.ip.FieldName or obj.si.FieldName."""

    def __init__(self, epbunch, mode="ip"):
        # mode is "ip" or "si"
        object.__setattr__(self, "_epbunch", epbunch)
        object.__setattr__(self, "_mode", mode)

    def __getattr__(self, name):
        if self._mode == "ip":
            return self._epbunch.get_ipvalue(name)
        else:
            # si mode → just return the normal (SI) value
            return getattr(self._epbunch, name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return
        if self._mode == "ip":
            self._epbunch.set_ipvalue(name, value)
        else:
            setattr(self._epbunch, name, value)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        self.__setattr__(name, value)

    def __dir__(self):
        """Make tab-completion show the field names."""
        return list(self._epbunch.fieldnames)

    def __repr__(self):
        return f"<UnitsProxy mode={self._mode!r} for {self._epbunch.key}>"