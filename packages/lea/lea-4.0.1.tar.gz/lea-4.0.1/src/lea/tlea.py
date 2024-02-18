"""
--------------------------------------------------------------------------------

    tlea.py

--------------------------------------------------------------------------------
Copyright 2013-2024 Pierre Denis

This file is part of Lea.

Lea is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lea is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Lea.  If not, see <http://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------
"""

from .lea import Lea
from .exceptions import LeaError
from .alea import coerce, pmf
from collections import defaultdict


class Tlea(Lea):
    """
    Tlea is a Lea subclass, which instance represents a conditional probability
    table (CPT) giving a Lea instance C and a dictionary associating each
    possible value of C to a specific Lea instance.
    A Tlea instance is a "table pex", as defined in the paper on Statues algorithm
    (see http://arxiv.org/abs/1806.09997).
    """

    __slots__ = ('_lea_c', '_lea_dict', '_default_lea')

    def __init__(self, lea_c, lea_dict, default_lea=Lea._DUMMY_VAL):
        if isinstance(lea_dict, defaultdict):
            raise LeaError('defaultdict not supported for Tlea, use default_lea argument instead')
        Lea.__init__(self)
        self._lea_c = coerce(lea_c)
        self._lea_dict = {c: coerce(lea1) for (c, lea1) in lea_dict.items()}
        if default_lea is Lea._DUMMY_VAL:
            self._default_lea = Lea._DUMMY_VAL
        else:
            self._default_lea = coerce(default_lea)
            self._lea_dict = defaultdict(lambda: self._default_lea, self._lea_dict)

    @staticmethod
    def build(lea_c, lea_dict, default_lea=Lea._DUMMY_VAL, prior_lea=Lea._DUMMY_VAL):
        if default_lea is not Lea._DUMMY_VAL and prior_lea is not Lea._DUMMY_VAL:
            raise LeaError('default_lea and prior_lea arguments cannot be defined together')
        if prior_lea is not Lea._DUMMY_VAL:
            # determine default_lea from prior_lea
            dummy_lea = []
            tlea = Tlea(lea_c, lea_dict, dummy_lea)
            alea1 = tlea.given(tlea != dummy_lea).calc(normalization=False)
            default_lea_support = set(alea1.support())
            default_lea_support.update(prior_lea.support())
            vps = []
            for v in default_lea_support:
                p = prior_lea._p(v) - alea1._p(v)
                try:
                    is_valid = bool(p >= 0)
                except Exception:
                    # comparison impossible due to probability type (e.g. symbolic type as in sympy)
                    # no probability check possible
                    is_valid = True
                if not is_valid:
                    raise LeaError('impossible to calculate probabilities from input data')
                vps.append((v, p))
            default_lea = pmf(vps)
        return Tlea(lea_c, lea_dict, default_lea)

    def _get_lea_children(self, restricted=False):
        lea_children = [self._lea_c]
        if not restricted:
            for lea1 in self._lea_dict.values():
                lea_children.append(lea1)
            if self._default_lea is not Lea._DUMMY_VAL:
                lea_children.append(self._default_lea)
        return lea_children

    def _clone_by_type(self, clone_table):
        default_lea = self._default_lea
        if default_lea is not Lea._DUMMY_VAL:
            default_lea = default_lea._clone(clone_table)
        return Tlea(self._lea_c._clone(clone_table),
                    {v: lea1._clone(clone_table) for (v, lea1) in self._lea_dict.items()},
                    default_lea)

    def _gen_vp(self):
        lea_dict = self._lea_dict
        for (vc, pc) in self._lea_c.gen_vp():
            try:
                lea_v = lea_dict[vc]
            except KeyError:
                # value missing in CPT: nothing to yield
                pass
            else:
                # value present in CPT
                for (vd, pd) in lea_v.gen_vp():
                    yield (vd, pc * pd)

    def _gen_one_random_mc(self):
        lea_dict = self._lea_dict
        for vc in self._lea_c.gen_one_random_mc():
            try:
                lea_v = lea_dict[vc]
            except KeyError:
                # value missing in CPT: nothing to yield
                pass
            else:
                # value present in CPT
                for vd in lea_v.gen_one_random_mc():
                    yield vd

    def _em_step(self, model_lea, cond_lea, obs_pmf_tuple, conversion_dict):
        lea_c = self._lea_c
        lea2_c = lea_c.em_step(model_lea, cond_lea, obs_pmf_tuple, conversion_dict)
        lea2_dict = {vc: d.em_step(model_lea, cond_lea & (lea_c == vc), obs_pmf_tuple, conversion_dict)
                     for (vc, d) in self._lea_dict.items()}
        return Tlea(lea2_c, lea2_dict)
