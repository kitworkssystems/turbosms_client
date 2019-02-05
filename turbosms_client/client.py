import logging

_logger = logging.getLogger(__name__)

try:
    from zeep import Client
except (ImportError, IOError) as err:
    _logger.debug(err)
    _logger.info(
        "ERROR IMPORTING zeep, if not installed, please install it:"
        " e.g.: pip install zeep")

AUTH_SUCCESS = 'Вы успешно авторизировались'

NO_AUTH = 'Вы не авторизированы'

SEND_SUCCESS = 'Сообщения успешно отправлены'

STATUS_SUCCESS = 'Сообщение доставлено получателю'

STATUS_DEPART = [
    'Отправлено', 'В очереди', 'Сообщение передано в мобильную сеть']


class TurboSmsClient(object):
    url = 'http://turbosms.in.ua/api/wsdl.html'
    auth = False
    balance = 0
    sender = 'sender'
    min_balance = 1

    def __init__(self, username, password) -> None:
        super().__init__()
        self.error = ''
        self.sms_error = ''
        self.sms_id = False
        self.username = username
        self.password = password
        self.client = Client(wsdl=self.url)

    def authenticate(self):
        result = self.client.service.Auth(
            login=self.username, password=self.password)
        if result == AUTH_SUCCESS:
            self.error = ''
            self.auth = True
            return True
        self.error = result
        self.auth = False
        return False

    def get_balance(self):
        if not self.authenticate():
            return False
        result = self.client.service.GetCreditBalance()
        try:
            balance = float(result)
        except Exception as e:
            self.error = 'Balance status {} error {}'.format(result, e)
            _logger.error(self.error)
            return False
        self.balance = balance
        if self.balance < self.min_balance:
            self.error = 'Not enough money. Replenish the balance.'
            _logger.info(self.error)
            return False
        self.error = ''
        return True

    def send_sms(self, to, text):
        """
        Send SMS to one phone number ONLY ONE, NOT list
        :param to: Phone number, digits only
        :param text: SMS text
        :return: True if success
        """
        if not self.get_balance():
            return False
        if not (isinstance(to, str) and to.isdigit()):
            self.error = '\'to\' must string value of ' \
                         'phone number with digits only'
            _logger.error(self.error)
            return False
        result = self.client.service.SendSMS(
            sender=self.sender, destination=to, text=text)
        if not (isinstance(result, list) and len(result)):
            self.error = 'Response result must be list of values, ' \
                         'not {}'.format(result)
            _logger.error(self.error)
            return False
        if result[0] != SEND_SUCCESS:
            self.error = result[0]
            self.sms_id = False
            if len(result) > 1:
                self.sms_error = result[1]
            return False
        self.error = ''
        if len(result) == 1:
            self.error = 'Success sending has no sms id'
            _logger.error(self.error)
            return False
        self.sms_error = ''
        self.sms_id = result[1]
        return True

    def status(self, sms_id):
        if not self.authenticate():
            return False
        result = self.client.service.GetMessageStatus(sms_id)
        if result == STATUS_SUCCESS:
            return 'success'
        if result in STATUS_DEPART:
            return 'depart'
        self.sms_error = result
        return 'error'
