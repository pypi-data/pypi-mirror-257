import json
from datetime import datetime, timedelta, timezone
from unittest import TestCase

from freezegun import freeze_time
from pydantic.error_wrappers import ValidationError
from pydantic.types import UUID

from oc_python_sdk.models.payment import (
    CurrencyType,
    HttpMethodType,
    Links,
    Notify,
    OnlinePaymentBegin,
    Payer,
    PayerType,
    Payment,
    PaymentData,
    PaymentDataSplit,
    PaymentStatus,
    PaymentType,
    Update,
)

from ._helpers import (
    get_empty_notify_data,
    get_links_data,
    get_notify_data,
    get_online_payment_begin_data,
    get_payer_data,
    get_payment_data,
    get_payment_event_data,
    get_split_data,
    get_split_data_complete,
    get_split_data_invalid,
    get_update_data,
)

NOW = datetime(2022, 9, 19, 16, 0, 0, tzinfo=timezone.utc)


class PaymentTestCase(TestCase):
    def test_creation(self):
        payment = Payment(**get_payment_event_data())
        self.assertEqual(payment.id, UUID('bb7044e4-066c-4bf7-915e-87ee97270eae'))

    def test_payment_reason_length(self):
        with self.assertRaises(ValidationError):
            Payment(
                **get_payment_event_data(
                    reason='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt '
                    'ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco '
                    'laboris nisi ut aliquip ex ea commodo consequat.',
                ),
            )

    def test_payment_event_version(self):
        with self.assertRaises(ValidationError):
            Payment(**get_payment_event_data(event_version='X'))

    def test_iso_date(self):
        with self.assertRaises(ValidationError):
            Payment(**get_payment_event_data(created_at='non-valid-datetime'))

    def test_iso_date_null(self):
        with self.assertRaises(ValidationError):
            PaymentData(**get_payment_data(paid_at='non-valid-datetime'))

    def test_payment_creation(self):
        self.assertTrue(
            Payment(
                **get_payment_event_data(status=PaymentStatus.STATUS_CREATION_PENDING),
            ).is_payment_creation_needed(),
        )
        self.assertFalse(
            Payment(**get_payment_event_data(status=PaymentStatus.STATUS_COMPLETE)).is_payment_creation_needed(),
        )

    def test_update_time(self):
        payment = Payment(**get_payment_event_data())
        with freeze_time(NOW):
            payment.update_time('updated_at')
            self.assertEqual(payment.updated_at, NOW)

    def test_payment_update_time(self):
        payment = Payment(**get_payment_event_data())
        with freeze_time(NOW):
            payment.update_time('links.update.last_check_at')
            self.assertEqual(payment.links.update.last_check_at, NOW)

    def test_payment_update_check_time_missing_last_check_at(self):
        payment = Payment(**get_payment_event_data(created_at=NOW.isoformat()))
        with freeze_time(NOW):
            payment.update_check_time()
            self.assertEqual(payment.links.update.last_check_at, None)

    def test_payment_update_check_time(self):
        payment = Payment(**get_payment_event_data(created_at=NOW.isoformat()))
        with freeze_time(NOW):
            payment.update_time('links.update.last_check_at')
            payment.update_check_time()
            self.assertEqual(payment.links.update.next_check_at, NOW + timedelta(minutes=1))
        with freeze_time(NOW + timedelta(minutes=1)):
            payment.update_time('links.update.last_check_at')
            payment.update_check_time()
            self.assertEqual(payment.links.update.next_check_at, NOW + timedelta(minutes=1 + 1))
        with freeze_time(NOW + timedelta(minutes=15)):
            payment.update_time('links.update.last_check_at')
            payment.update_check_time()
            self.assertEqual(payment.links.update.next_check_at, NOW + timedelta(minutes=15 + 5))
        with freeze_time(NOW + timedelta(days=7)):
            payment.update_time('links.update.last_check_at')
            payment.update_check_time()
            self.assertEqual(payment.links.update.next_check_at, NOW + timedelta(days=7, hours=1))
        with freeze_time(NOW + timedelta(days=30)):
            payment.update_time('links.update.last_check_at')
            payment.update_check_time()
            self.assertEqual(payment.links.update.next_check_at, NOW + timedelta(days=30, hours=6))
        with freeze_time(NOW + timedelta(days=366)):
            payment.update_time('links.update.last_check_at')
            payment.update_check_time()
            self.assertEqual(payment.links.update.next_check_at, None)
            self.assertEqual(payment.status, PaymentStatus.STATUS_EXPIRED)

    def test_payer_country(self):
        with self.assertRaises(ValidationError):
            Payer(**get_payer_data(country='XX'))

    def test_encoders(self):
        payment = Payment(**get_payment_event_data())
        empty_split = payment.payment.split

        payment_empty_notify = Payment(**get_payment_event_data())
        payment_empty_notify.links.notify = None

        payment_data_with_split = payment.payment
        payment_data_with_split.split = get_split_data_complete()
        payment_with_split = Payment(**get_payment_event_data(payment=payment_data_with_split))

        payment_data = PaymentData(**get_payment_data())
        split = PaymentDataSplit(**get_split_data())
        online_payment_begin = OnlinePaymentBegin(**get_online_payment_begin_data())
        notify = Notify(**get_notify_data())
        notify_no_data = Notify(**get_empty_notify_data())
        update = Update(**get_update_data())
        links = Links(**get_links_data())
        payer = Payer(**get_payer_data())

        self.assertEqual(json.loads(payment.json())['id'], 'bb7044e4-066c-4bf7-915e-87ee97270eae')
        self.assertEqual(empty_split, [])
        self.assertEqual(
            json.loads(payment_with_split.json())['payment']['split'],
            [
                {
                    'code': 'c_1',
                    'amount': 16.0,
                    'meta': {
                        'split_type': 'Tipo c1',
                        'split_code': 'Codice c1',
                        'split_description': 'Descrizione c1',
                        'split_budget_chapter': 'Capitolo di bilancio c1',
                        'split_assessment': 'Accertamento c1',
                    },
                },
                {
                    'code': 'c_2',
                    'amount': 0.5,
                    'meta': {
                        'split_type': 'Tipo c2',
                        'split_code': 'Codice c2',
                        'split_description': 'Descrizione c12',
                        'split_budget_chapter': 'Capitolo di bilancio c2',
                        'split_assessment': 'Accertamento c2',
                    },
                },
            ],
        )
        self.assertEqual(json.loads(payment.json())['created_at'], '2022-06-08T08:28:42+00:00')
        self.assertEqual(json.loads(payment.status.json()), PaymentStatus.STATUS_CREATION_PENDING.value)
        self.assertEqual(json.loads(payment.type.json()), PaymentType.TYPE_PAGOPA.value)
        self.assertEqual(json.loads(payment.payer.type.json()), PayerType.TYPE_HUMAN.value)
        self.assertEqual(json.loads(payment.payment.currency.json()), CurrencyType.CURRENCY_EUR.value)
        self.assertEqual(json.loads(payment.links.notify[0].method.json()), HttpMethodType.HTTP_METHOD_POST.value)
        self.assertEqual(json.loads(payment_empty_notify.json())['links']['notify'], None)
        self.assertEqual(json.loads(split.json())['code'], 'CODE')
        self.assertEqual(json.loads(payment_data.json())['amount'], 1)
        self.assertEqual(json.loads(online_payment_begin.json())['url'], None)
        self.assertEqual(
            json.loads(notify.json())['url'],
            'https://devsdc.opencontent.it/'
            'comune-di-bugliano/api/applications/'
            'a51cc065-4fb1-4ace-8d3f-e3a70c867472/payment',
        )
        self.assertEqual(json.loads(notify_no_data.json()), {'url': None, 'method': None, 'sent_at': None})
        self.assertEqual(json.loads(update.json())['url'], None)
        self.assertEqual(len(json.loads(links.json())['notify']), 1)
        self.assertEqual(json.loads(payer.json())['type'], PayerType.TYPE_HUMAN.value)
        with self.assertRaises(ValidationError):
            PaymentData(**get_payment_data(split=None))
        with self.assertRaises(ValidationError):
            PaymentData(**get_payment_data(split=get_split_data_invalid()))
        with self.assertRaises(ValidationError):
            PaymentData(**get_payment_data(split='Lorem ipsum'))
