"""
--------------------------------------------------------------------------------

    evidence_ctx.py

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

from .alea import coerce
from .exceptions import LeaError


class EvidenceCtx(object):
    """
    EvidenceCtx is a class which instance represents global conditions
    that can be activated or deactivated. At any given time, all active
    EvidenceCtx instances define implicit conditions that are enforced
    on all calculated probabilities; these become then automatically
    conditional probabilities (see Ilea class).
    An EvidenceCtx is defined by a sequence of conditions (boolean Lea
    instances) and bindings dictionary for binding Alea instances to
    given values ("observations"). Both data are optional. Semantically,
    these are combined together with a conjunction (AND); the bindings
    {x:v) are equivalent to conditions (x==v) but these can be treated
    faster, especially if x's domain is large.
    An EvidenceCtx can be used as a Python context manager, using
    the 'with' keyword, making the activation/deactivation automatic.
    """

    _active_evidence_contexts = []

    __slots__ = ('_conditions', '_bindings')

    def __init__(self, *conditions, bindings=None):
        """ initializes an evidence context with the given conditions
            (boolean Lea instances) and bindings dictionary for binding
            Alea instances to given values ("observations")
        """
        self._conditions = tuple(coerce(condition) for condition in conditions)
        self._bindings = None if bindings is None else dict(bindings)

    def __enter__(self):
        """ activate the evidence context and return self;
            automatically called when entering the scoped block if self is
            used as a context manager (with statement)
        """
        self.activate()
        return self

    def __exit__(self, *exc):
        """ deactivate the evidence context;
            automatically called when exiting the scoped block if self is
            used as a context manager (with statement)
        """
        self.deactivate()

    def activate(self):
        """ activate the evidence context 
        """
        if self._bindings is not None:
            for (x, v) in self._bindings.items():
                if not x.is_bindable(v):
                    raise LeaError("cannot bind %s because dependent or already bound" % (x._id(),))
            for (x, v) in self._bindings.items():
                x.observe(v)
        EvidenceCtx._active_evidence_contexts.append(self)

    def deactivate(self):
        """ deactivate the evidence context 
        """
        EvidenceCtx._active_evidence_contexts.pop()
        if self._bindings is not None:
            for x in self._bindings:
                x.free(check=False)


def get_active_conditions():
    return tuple(c for ectx in EvidenceCtx._active_evidence_contexts
                 for c in ectx._conditions)


def has_evidence():
    """ returns True iff there is at least one active evidence context
    """
    return len(EvidenceCtx._active_evidence_contexts) > 0


def add_evidence(*conditions, bindings=None):
    """ adds given evidences as a new evidence context;
        these evidences are boolean Lea instances or coerced booleans
    """
    evidence_context = EvidenceCtx(*conditions, bindings=bindings)
    evidence_context.activate()


def pop_evidence():
    """ removes the last added evidence context and returns it;
        requires that there is at least one evidence context
    """
    if len(EvidenceCtx._active_evidence_contexts) == 0:
        raise LeaError("no evidence context")
    return EvidenceCtx._active_evidence_contexts.pop()


def clear_evidence():
    """ removes all evidence contexts
    """
    EvidenceCtx._active_evidence_contexts.clear()


evidence = EvidenceCtx

__all__ = ("evidence", "get_active_conditions", "has_evidence", "add_evidence",
           "pop_evidence", "clear_evidence")
