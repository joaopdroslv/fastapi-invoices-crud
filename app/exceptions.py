class NotFound(Exception):
    def __init__(self, name: str):
        self.name = name


class InvoiceAlready(Exception):
    def __init__(self, invoice_id: int, already: str):
        self.invoice_id = invoice_id
        self.already = already


class InvalidPaymentMethod(Exception):
    def __init__(self, method: str):
        self.method = method
