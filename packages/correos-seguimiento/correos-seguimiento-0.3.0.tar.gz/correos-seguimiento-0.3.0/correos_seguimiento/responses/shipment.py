from correos_seguimiento.errors import UnknownApiResponse


class ShipmentResponse:
    DELIVERED_CODE = "Entregado"
    RELABELED_CODE = "Reetiquetado"
    RETURNED_CODE = "En proceso de devolución"

    def __init__(self, raw_response):
        self.json_response = raw_response
        try:
            self.eventos = set(
                [c["desTextoResumen"] for c in self.json_response[0]["eventos"]]
            )
        except (IndexError, KeyError):
            raise UnknownApiResponse
        if not self.eventos:
            raise UnknownApiResponse

    def _get_bried_associate_event(self):
        return self.json_response[0]["enviosAsociados"][0]

    def is_delivered(self):
        return self.DELIVERED_CODE in self.eventos

    def is_relabeled(self):
        return self.RELABELED_CODE in self.eventos

    def is_returned(self):
        return self.RETURNED_CODE in self.eventos

    def get_relabeled_shipment_code(self):
        try:
            return self._get_bried_associate_event()["codEnvio"]
        except (IndexError, KeyError):
            raise UnknownApiResponse
