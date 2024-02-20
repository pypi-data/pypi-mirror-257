from typing import List, Optional


class LOGSErrorResponse:
    title: Optional[str] = None
    details: Optional[str] = None
    status: Optional[int] = None
    type: Optional[str] = None

    errors: List[str] = []

    def __init__(self, ref=None, errors: Optional[List[str]] = None):
        if ref:
            self._fromRef(ref)

        if errors:
            self.errors = errors

    def override(self, ref=dict):
        self._fromRef(ref)

    def _fromRef(self, ref=None):
        if not isinstance(ref, dict):
            ref = {"title": str(ref)}

        for k in dir(self):
            if k in ref and hasattr(self, k) and not callable(getattr(self, k)):
                try:
                    setattr(self, k, ref[k])
                except AttributeError:
                    pass
