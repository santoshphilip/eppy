# Copyright (c) 2026 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Unit-aware attribute access for EpBunch objects.

This module provides :class:`UnitsProxy`, a thin proxy that lets callers
read (and write) EnergyPlus object fields in either SI or IP units
without having to call conversion helpers explicitly.

Typical usage
-------------
After the proxy is attached to an :class:`~eppy.bunch_subclass.EpBunch`
via the ``ip``, ``ipv``, ``si`` and ``siv`` properties:

    site = idf.idfobjects["Site:Location"][0]

    site.ip.Elevation      # numeric value in IP units
    site.ipv.Elevation     # same value plus an IDF-style comment
    site.si.Elevation      # numeric value in SI units (identical to
                           # ordinary attribute access)
    site.siv.Elevation     # SI value plus an IDF-style comment

Assignment works the same way: writing through ``.ip`` / ``.ipv``
converts the supplied IP number back to SI before storing it; writing
through ``.si`` / ``.siv`` stores the value unchanged.

The proxy also supports dictionary-style access
(``obj.ip["Elevation"]``) and tab-completion of field names.
"""

class UnitsProxy:
    """Proxy that lets you do:
        obj.ip.FieldName   → numeric IP value
        obj.ipv.FieldName  → verbose IP string  (value + !- comment)
        obj.si.FieldName   → numeric SI value
        obj.siv.FieldName  → verbose SI string  (value + !- comment)
    """

    def __init__(self, epbunch, mode="ip"):
        # mode is "ip", "ipv", "si" or "siv"
        object.__setattr__(self, "_epbunch", epbunch)
        object.__setattr__(self, "_mode", mode)

    def __getattr__(self, name):
        if self._mode == "ip":
            return self._epbunch.get_ipvalue(name)
        elif self._mode == "ipv":
            return self._epbunch.get_ipvalue(name, verbose=True)
        elif self._mode == "siv":
            return self._epbunch.get_sivalue(name, verbose=True)
        else:
            # si mode → normal (SI) value
            return getattr(self._epbunch, name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return
        if self._mode in ("ip", "ipv"):
            self._epbunch.set_ipvalue(name, value)
        else:
            # si / siv → normal attribute assignment
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