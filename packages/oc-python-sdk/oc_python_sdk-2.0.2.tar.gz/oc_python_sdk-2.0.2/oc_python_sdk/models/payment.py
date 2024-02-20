import datetime
import functools
import json
from enum import Enum
from json import JSONEncoder
from typing import List, Optional
from uuid import UUID

from dateutil import parser
from pydantic import BaseModel, ValidationError, constr, validator

from ..utils.logger import payment_logger as logger


def check_iso_format(v: str):
    try:
        return parser.parse(v)
    except Exception:
        raise ValidationError('date must be ISO8601 format')


def check_isoformat_none_case(v: Optional[str]):
    if v is not None:
        try:
            return parser.parse(v)
        except Exception:
            raise ValidationError('date must be ISO8601 format')


class HttpMethodType(Enum):
    HTTP_METHOD_GET = 'GET'
    HTTP_METHOD_POST = 'POST'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class CurrencyType(Enum):
    CURRENCY_EUR = 'EUR'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentStatus(Enum):
    STATUS_CREATION_PENDING = 'CREATION_PENDING'
    STATUS_CREATION_FAILED = 'CREATION_FAILED'
    STATUS_PAYMENT_PENDING = 'PAYMENT_PENDING'
    STATUS_PAYMENT_STARTED = 'PAYMENT_STARTED'
    STATUS_PAYMENT_CONFIRMED = 'PAYMENT_CONFIRMED'
    STATUS_PAYMENT_FAILED = 'PAYMENT_FAILED'
    STATUS_NOTIFICATION_PENDING = 'NOTIFICATION_PENDING'
    STATUS_COMPLETE = 'COMPLETE'
    STATUS_EXPIRED = 'EXPIRED'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentType(Enum):
    TYPE_PAGOPA = 'PAGOPA'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PayerType(Enum):
    TYPE_HUMAN = 'human'
    TYPE_LEGAL = 'legal'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentDataSplit(BaseModel):
    code: str
    amount: Optional[float]
    meta: dict

    class Config:
        validate_all = True
        validate_assignment = True

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentData(BaseModel):
    transaction_id: Optional[str]
    paid_at: Optional[str]
    expire_at: str
    amount: float
    currency: CurrencyType
    notice_code: Optional[str]
    iud: str
    iuv: Optional[str]
    split: List[Optional[PaymentDataSplit]]

    class Config:
        validate_all = True
        validate_assignment = True

    paid_at_must_be_iso8601 = validator('paid_at', allow_reuse=True)(check_isoformat_none_case)
    expire_at_must_be_iso8601 = validator('expire_at', allow_reuse=True)(check_iso_format)

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class OnlinePaymentBegin(BaseModel):
    url: Optional[str]
    last_opened_at: Optional[str]
    method: Optional[HttpMethodType]

    last_opened_at_must_be_iso8601 = validator('last_opened_at', allow_reuse=True)(check_isoformat_none_case)

    class Config:
        validate_all = True
        validate_assignment = True

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class OnlinePaymentLanding(OnlinePaymentBegin):
    pass


class OfflinePayment(OnlinePaymentBegin):
    pass


class Receipt(OnlinePaymentBegin):
    pass


class Notify(BaseModel):
    url: Optional[str]
    method: Optional[HttpMethodType]
    sent_at: Optional[str]

    sent_at_must_be_iso8601 = validator('sent_at', allow_reuse=True)(check_isoformat_none_case)

    class Config:
        validate_all = True
        validate_assignment = True

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class Update(BaseModel):
    url: Optional[str]
    last_check_at: Optional[str]
    next_check_at: Optional[str]
    method: Optional[HttpMethodType]

    last_check_at_must_be_iso8601 = validator('last_check_at', allow_reuse=True)(check_isoformat_none_case)
    next_check_at_must_be_iso8601 = validator('next_check_at', allow_reuse=True)(check_isoformat_none_case)

    class Config:
        validate_all = True
        validate_assignment = True

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class Links(BaseModel):
    online_payment_begin: OnlinePaymentBegin
    online_payment_landing: OnlinePaymentLanding
    offline_payment: OfflinePayment
    receipt: Receipt
    notify: Optional[List[Notify]]
    update: Update

    class Config:
        validate_all = True
        validate_assignment = True

    def append_notify(self, notify):
        for item in notify:
            self.notify.append(Notify(**item))

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class Payer(BaseModel):
    type: PayerType
    tax_identification_number: str
    name: str
    family_name: Optional[str]
    street_name: Optional[str]
    building_number: Optional[str]
    postal_code: Optional[str]
    town_name: Optional[str]
    country_subdivision: Optional[str]
    country: Optional[str]
    email: Optional[str]

    class Config:
        validate_all = True
        validate_assignment = True

    @validator('country')
    def country_must_be_it(cls, v):
        if 'IT' not in v:
            raise ValidationError('country must be IT')
        return v

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class Payment(BaseModel):
    id: UUID
    user_id: UUID
    type: PaymentType
    tenant_id: UUID
    service_id: UUID
    created_at: str
    updated_at: str
    status: PaymentStatus
    reason: constr(max_length=140)
    remote_id: UUID
    payment: PaymentData
    links: Links
    payer: Payer
    locale: str
    event_id: UUID
    event_version: str
    event_created_at: str
    app_id: str

    class Config:
        validate_all = True
        validate_assignment = True

    created_at_must_be_iso8601 = validator('created_at', allow_reuse=True)(check_iso_format)
    updated_at_must_be_iso8601 = validator('updated_at', allow_reuse=True)(check_iso_format)

    @validator('event_version')
    def event_version_must_be_two(cls, v):
        if float(v) != 2.0:
            raise ValidationError('event must have 2.0 as version')
        return v.title()

    event_created_at_must_be_iso8601 = validator('event_created_at', allow_reuse=True)(check_iso_format)

    def update_time(self, field):
        self._rsetattr(
            field,
            datetime.datetime.now().replace(microsecond=0).astimezone().isoformat(),
        )
        return self

    def update_check_time(self):
        if not self.links.update.last_check_at:
            return

        last_check = self.links.update.last_check_at
        next_check = datetime.datetime.now()

        minutes_checkpoint = self.created_at + datetime.timedelta(minutes=5)
        quarter_checkpoint = self.created_at + datetime.timedelta(minutes=15)
        week_checkpoint = self.created_at + datetime.timedelta(days=7)
        month_checkpoint = self.created_at + datetime.timedelta(days=30)
        year_checkpoint = self.created_at + datetime.timedelta(days=365)

        if last_check <= minutes_checkpoint:
            next_check = next_check + datetime.timedelta(minutes=1)
        elif last_check <= quarter_checkpoint:
            next_check = next_check + datetime.timedelta(minutes=5)
        elif last_check <= week_checkpoint:
            next_check = next_check + datetime.timedelta(hours=1)
        elif last_check <= month_checkpoint:
            next_check = next_check + datetime.timedelta(hours=6)
        elif last_check <= year_checkpoint:
            days_ahead = 6 - next_check.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            next_check = next_check + datetime.timedelta(days=days_ahead)
        else:
            next_check = None
            self.status = PaymentStatus.STATUS_EXPIRED

        self.links.update.next_check_at = (
            next_check.replace(microsecond=0).astimezone().isoformat() if next_check else None
        )

        return self

    def _rsetattr(self, attr, val):
        pre, _, post = attr.rpartition('.')
        return setattr(self._rgetattr(pre) if pre else self, post, val)

    def _rgetattr(self, attr, *args):
        def _getattr(obj, attr):
            return getattr(obj, attr, *args)

        return functools.reduce(_getattr, [self] + attr.split('.'))

    def is_payment_creation_needed(self):
        if self.status != PaymentStatus.STATUS_CREATION_PENDING:
            logger.info(f'Event {self.id} from application {self.remote_id}: Payment creation not required')
            return False
        return True

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        elif isinstance(o, UUID):
            return str(o)
        elif isinstance(o, (PaymentType, PayerType, PaymentStatus, HttpMethodType, CurrencyType)):
            return o.value
        return o.__dict__
