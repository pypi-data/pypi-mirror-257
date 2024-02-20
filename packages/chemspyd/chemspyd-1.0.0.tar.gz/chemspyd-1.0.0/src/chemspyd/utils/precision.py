from decimal import Decimal

PRECISION: Decimal = Decimal(str(10**-3))


def decimal_precision(func, precision: int = 3):
    precision = Decimal(str(10**-precision))

    def wrapper(self, *args, **kwargs):
        args = [Decimal(str(arg)).quantize(precision) for arg in args]
        kwargs = {
            key: Decimal(str(value)).quantize(precision)
            for key, value in kwargs.items()
        }
        func_return = func(self, *args, **kwargs)
        if isinstance(func_return, (float, Decimal)):
            return Decimal(str(func_return)).quantize(precision)
        else:
            return func_return

    return wrapper
