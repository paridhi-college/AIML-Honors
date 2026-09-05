from __future__ import annotations
import sys
from abc import ABC, abstractmethod
from typing import Dict, Type

## Task 1 :

class PaymentMethod(ABC):
    @abstractmethod
    def get_details(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def pay(self, amount: float) -> bool:
        raise NotImplementedError


class RazorpayCardPayment(PaymentMethod):
    def __init__(self, card_number: str, **kwargs):
        self._card_number = card_number

    def get_details(self) -> str:
        return f"Razorpay Card [**** **** **** {self._card_number[-4:]}]"

    def pay(self, amount: float) -> bool:
        print(f"[Razorpay] Charging {self.get_details()} Rs.{amount:.2f} ...")
        print("[Razorpay] Card payment successful.")
        return True


class RazorpayUPIPayment(PaymentMethod):
    def __init__(self, upi_id: str, **kwargs):
        self._upi_id = upi_id

    def get_details(self) -> str:
        return f"Razorpay UPI [{self._upi_id}]"

    def pay(self, amount: float) -> bool:
        print(f"[Razorpay] Requesting Rs.{amount:.2f} via {self.get_details()} ...")
        print("[Razorpay] UPI payment successful.")
        return True


class StripeCardPayment(PaymentMethod):
    def __init__(self, card_number: str, **kwargs):
        self._card_number = card_number

    def get_details(self) -> str:
        return f"Stripe Card [**** **** **** {self._card_number[-4:]}]"

    def pay(self, amount: float) -> bool:
        print(f"[Stripe] Charging {self.get_details()} ${amount:.2f} ...")
        print("[Stripe] Card payment successful.")
        return True


class StripeUPIPayment(PaymentMethod):

    def __init__(self, upi_id: str, token: str = "N/A", **kwargs):
        self._upi_id = upi_id
        self._token = token

    def get_details(self) -> str:
        return f"Stripe UPI Bridge [{self._upi_id}, token={self._token}]"

    def pay(self, amount: float) -> bool:
        print(f"[Stripe] Requesting ${amount:.2f} via {self.get_details()} ...")
        print("[Stripe] UPI payment successful.")
        return True

    ## Task 2 :

class FactoryPaymentMethod(ABC):
    factory: Dict[str, Type[PaymentMethod]] = {}

    @classmethod
    def get_payment_object(cls, method_type: str, **kwargs) -> PaymentMethod:
        method_type = method_type.lower().strip()
        if method_type not in cls.factory:
            raise ValueError(
                f"Unsupported payment method '{method_type}' for {cls.__name__}. "
                f"Available: {list(cls.factory.keys())}"
            )
        payment_cls = cls.factory[method_type]
        return payment_cls(**kwargs)

    @classmethod
    def register_method(cls, method_type: str, payment_cls: Type[PaymentMethod]) -> None:

        cls.factory[method_type.lower().strip()] = payment_cls


class RazorpayFactory(FactoryPaymentMethod):
    factory: Dict[str, Type[PaymentMethod]] = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment,
    }


class StripeFactory(FactoryPaymentMethod):
    factory: Dict[str, Type[PaymentMethod]] = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment,
    }

## Task 3 :

class Aggregator(ABC):

    def __init__(self, name: str, processing_fee: float):
        self.name: str = name
        self.processing_fee: float = processing_fee  # percent

    @property
    @abstractmethod
    def payment_factory(self) -> Type[FactoryPaymentMethod]:
        raise NotImplementedError

    def call_get_payment_object(self, method_type: str, amount: float, **kwargs) -> bool:
        
        try:
            payment_method = self.payment_factory.get_payment_object(method_type, **kwargs)
        except ValueError as exc:
            print(f"[{self.name}] Error: {exc}")
            return False

        print(f"[{self.name}] Routing payment through {payment_method.get_details()}")
        success = payment_method.pay(amount)

        if success:
            fee = amount * (self.processing_fee / 100)
            print(f"[{self.name}] Processing fee ({self.processing_fee}%): {fee:.2f}")
            print(f"[{self.name}] Net settled amount: {amount - fee:.2f}")

        return success


class RazorpayAggregator(Aggregator):
    def __init__(self):
        super().__init__(name="Razorpay", processing_fee=2.0)

    @property
    def payment_factory(self) -> Type[FactoryPaymentMethod]:
        return RazorpayFactory


class StripeAggregator(Aggregator):
    def __init__(self):
        super().__init__(name="Stripe", processing_fee=2.9)

    @property
    def payment_factory(self) -> Type[FactoryPaymentMethod]:
        return StripeFactory

    
## Task 4 :

class AggregatorFactory:
    factory: Dict[str, Type[Aggregator]] = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator,
    }

    @classmethod
    def get_aggregator_object(cls, aggregator_name: str) -> Aggregator:
        aggregator_name = aggregator_name.lower().strip()
        if aggregator_name not in cls.factory:
            raise ValueError(
                f"Unsupported aggregator '{aggregator_name}'. "
                f"Available: {list(cls.factory.keys())}"
            )
        return cls.factory[aggregator_name]()

    @classmethod
    def register_aggregator(cls, aggregator_name: str, aggregator_cls: Type[Aggregator]) -> None:
        cls.factory[aggregator_name.lower().strip()] = aggregator_cls


## Task 5 :

def _prompt(text: str) -> str:
    return input(text).strip()


def run_cli() -> None:
    print("=" * 55)
    print("   Multi-Gateway Payment Processing Engine")
    print("=" * 55)

    # 1. Select Aggregator 
    aggregator = None
    while aggregator is None:
        aggregator_name = _prompt(f"Select Aggregator {list(AggregatorFactory.factory.keys())}: ")
        try:
            aggregator = AggregatorFactory.get_aggregator_object(aggregator_name)
        except ValueError as exc:
            print(f"Error: {exc}. Please try again.")

    # 2. Select Method 
    method_type = None
    while method_type not in ("card", "upi"):
        method_type = _prompt("Select Method (card / upi): ").lower().strip()
        if method_type not in ("card", "upi"):
            print(f"Error: unknown method type '{method_type}'. Please try again.")

    # 3. Enter Payment Details
    kwargs = {}
    try:
        if method_type == "card":
            card_number = _prompt("Enter Card Number: ")
            if not card_number.isdigit() or len(card_number) < 4:
                raise ValueError("Card number must be at least 4 digits.")
            kwargs["card_number"] = card_number
        else:  # upi
            upi_id = _prompt("Enter UPI ID: ")
            if "@" not in upi_id:
                raise ValueError("UPI ID must be in the form name@bank.")
            kwargs["upi_id"] = upi_id
            if isinstance(aggregator, StripeAggregator):
                kwargs["token"] = _prompt("Enter Stripe UPI bridge token: ")
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    # 4. Enter Amount 
    amount = None
    while amount is None:
        amount_raw = _prompt("Enter Amount: ")
        try:
            amount = float(amount_raw)
            if amount <= 0:
                print("Amount must be positive. Please try again.")
                amount = None
        except ValueError:
            print(f"Error: '{amount_raw}' is not a valid amount. Please try again.")

    # 5. Route execution dynamically: Aggregator -> its Factory -> PaymentMethod.pay()
    print("-" * 55)
    try:
        success = aggregator.call_get_payment_object(method_type, amount, **kwargs)
    except Exception as exc:  # pragma: no cover - defensive catch-all for CLI use
        print(f"An unexpected error occurred while processing payment: {exc}")
        success = False
    print("-" * 55)
    print("Payment SUCCEEDED" if success else "Payment FAILED")


def _demo_extensibility() -> None:
    class PayPalCardPayment(PaymentMethod):
        def __init__(self, card_number: str, **kwargs):
            self._card_number = card_number

        def get_details(self) -> str:
            return f"PayPal Card [**** **** **** {self._card_number[-4:]}]"

        def pay(self, amount: float) -> bool:
            print(f"[PayPal] Charging {self.get_details()} ${amount:.2f} ...")
            return True

    class PayPalFactory(FactoryPaymentMethod):
        factory: Dict[str, Type[PaymentMethod]] = {}

    PayPalFactory.register_method("card", PayPalCardPayment)

    class PayPalAggregator(Aggregator):
        def __init__(self):
            super().__init__(name="PayPal", processing_fee=3.5)

        @property
        def payment_factory(self) -> Type[FactoryPaymentMethod]:
            return PayPalFactory

    AggregatorFactory.register_aggregator("paypal", PayPalAggregator)

    paypal = AggregatorFactory.get_aggregator_object("paypal")
    paypal.call_get_payment_object("card", 100.0, card_number="4242424242424242")


if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nCancelled by user. Exiting.")
        sys.exit(1)