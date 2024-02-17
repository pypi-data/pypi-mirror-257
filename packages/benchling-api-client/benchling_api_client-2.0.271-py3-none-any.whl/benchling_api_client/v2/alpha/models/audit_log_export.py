from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.audit_log_export_format import AuditLogExportFormat
from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditLogExport")


@attr.s(auto_attribs=True, repr=False)
class AuditLogExport:
    """  """

    _api_id: str
    _format: AuditLogExportFormat

    def __repr__(self):
        fields = []
        fields.append("api_id={}".format(repr(self._api_id)))
        fields.append("format={}".format(repr(self._format)))
        return "AuditLogExport({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        api_id = self._api_id
        format = self._format.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if api_id is not UNSET:
            field_dict["apiId"] = api_id
        if format is not UNSET:
            field_dict["format"] = format

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_api_id() -> str:
            api_id = d.pop("apiId")
            return api_id

        try:
            api_id = get_api_id()
        except KeyError:
            if strict:
                raise
            api_id = cast(str, UNSET)

        def get_format() -> AuditLogExportFormat:
            _format = d.pop("format")
            try:
                format = AuditLogExportFormat(_format)
            except ValueError:
                format = AuditLogExportFormat.of_unknown(_format)

            return format

        try:
            format = get_format()
        except KeyError:
            if strict:
                raise
            format = cast(AuditLogExportFormat, UNSET)

        audit_log_export = cls(
            api_id=api_id,
            format=format,
        )

        return audit_log_export

    @property
    def api_id(self) -> str:
        """ API ID of the Benchling object to export audit logs for. """
        if isinstance(self._api_id, Unset):
            raise NotPresentError(self, "api_id")
        return self._api_id

    @api_id.setter
    def api_id(self, value: str) -> None:
        self._api_id = value

    @property
    def format(self) -> AuditLogExportFormat:
        """ The format of the exported file. """
        if isinstance(self._format, Unset):
            raise NotPresentError(self, "format")
        return self._format

    @format.setter
    def format(self, value: AuditLogExportFormat) -> None:
        self._format = value
