import argparse
import sys

from dhapi.configuration.logger import set_logger
from dhapi.domain_object.lotto645_buy_request import Lotto645BuyRequest
from dhapi.meta.version_provider import get_installed_version
from dhapi.router.credentials_provider import get_credentials


class HelpOnErrorParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"🚨 입력 파라미터 에러 발생: {message}\n")
        sys.exit(1)


class ArgParser:
    def __init__(self):
        parser = HelpOnErrorParser(description="동행복권 비공식 API", formatter_class=argparse.RawTextHelpFormatter)

        # -v
        parser.add_argument("-v", "--version", action="version", version=get_installed_version())

        command_subparser = parser.add_subparsers(title="명령어 구분", dest="command", required=True)

        ## buy_lotto645 section

        buy_lotto645 = command_subparser.add_parser(
            "buy_lotto645",
            help="로또6/45 구매",
            epilog="""

[buy_lotto645 명령어 사용 예시]

dhapi buy_lotto645
\t\t\t# ~/.dhapi/credentials 을 읽어 ID/PW 를 자동으로 입력받고, 확인 후 자동모드로 5장 구매 (프로필 파일 포맷은 README.md 참고)
dhapi buy_lotto645 -q
\t\t\t# 확인 절차 없이 자동모드로 5장 구매
dhapi buy_lotto645 -u $USER_ID
\t\t\t# ID/PW 를 직접 입력받아 자동모드로 5장 구매 (deprecated)
dhapi buy_lotto645 -g
\t\t\t# 자동모드로 1장 구매 (1 game)
dhapi buy_lotto645 -g 1,2,3,4,5,6 -g 5,6,7 -g -g
\t\t\t# 1장 수동모드, 1장 반자동모드, 2장 자동모드

""",
        )

        buy_lotto645.formatter_class = argparse.RawTextHelpFormatter

        # -g
        buy_lotto645.add_argument(
            "-g",
            "--game",
            required=False,
            action="append",
            dest="games",
            nargs="?",
            const=None,
            help="""
구매할 번호 6개를 콤마로 구분해 입력합니다.
옵션을 여러번 사용하여 여러 게임을 구매할 수 있습니다 (매주 최대 5 게임).
'-g' 형태로 제시하면 해당 게임의 모든 번호를 자동으로 선택합니다 (자동 모드).
6개 미만의 번호를 입력하면 나머지 번호는 자동으로 구매할 수 있습니다 (반자동 모드).
옵션을 아예 입력하지 않으면 '자동으로 5장 구매'를 수행합니다.""",
        )

        # -p
        buy_lotto645.add_argument(
            "-p",
            "--profile",
            required=False,
            default="default",
            help="지정하지 않으면 'default' 프로필을 사용합니다.",
        )

        # -q
        buy_lotto645.add_argument("-q", "--quiet", action="store_true", help="플래그 설정 시 구매 전 확인 절차를 스킵합니다.")  # "store_true" means "set default to False"

        # -e
        buy_lotto645.add_argument("-e", "--email", required=False, help="구매 결과를 콘솔로 출력하는 대신, 입력된 이메일로 전송합니다.")

        # -d
        buy_lotto645.add_argument("-d", "--debug", action="store_true", help="로그 출력 레벨을 debug로 세팅합니다.")  # "store_true" means "set default to False"

        ## show_balance section # TODO(roeniss): Better way for DRY?

        show_balance = command_subparser.add_parser(
            "show_balance",
            help="예치금 현황 조회",
            epilog="""

[show_balance 명령어 사용 예시]

dhapi show_balance

""",
        )

        show_balance.formatter_class = argparse.RawTextHelpFormatter

        # -p
        show_balance.add_argument(
            "-p",
            "--profile",
            required=False,
            default="default",
            help="지정하지 않으면 'default' 프로필을 사용합니다.",
        )

        # -d
        show_balance.add_argument("-d", "--debug", action="store_true", help="로그 출력 레벨을 debug로 세팅합니다.")  # "store_true" means "set default to False"

        ## assign_virtual_account section # TODO(roeniss): Better way for DRY???

        assign_virtual_account = command_subparser.add_parser(
            "assign_virtual_account",
            help="예치금 현황 조회",
            epilog="""

[assign_virtual_account 명령어 사용 예시]

dhapi assign_virtual_account -a 10000

        """,
        )

        assign_virtual_account.formatter_class = argparse.RawTextHelpFormatter

        # -a
        assign_virtual_account.add_argument("-a", "--amount", help="충전할 금액을 입력합니다. (선택지: 5000, 10000, 20000, 30000, 50000, 100000, 200000, 300000, 500000, 700000, 1000000)")

        # -p
        assign_virtual_account.add_argument(
            "-p",
            "--profile",
            required=False,
            default="default",
            help="지정하지 않으면 'default' 프로필을 사용합니다.",
        )

        # -d
        assign_virtual_account.add_argument("-d", "--debug", action="store_true", help="로그 출력 레벨을 debug로 세팅합니다.")  # "store_true" means "set default to False"

        ## common section

        self._args = parser.parse_args()

        set_logger(self.is_debug())

        credentials = get_credentials(self.profile())
        self._args.username = credentials.get("username")
        self._args.password = credentials.get("password")

        if self._safe_arg_get(lambda: self._args.email):
            credentials = get_credentials(self.profile())
            self._args.mailjet_api_key = credentials.get("mailjet_api_key")
            self._args.mailjet_api_secret = credentials.get("mailjet_api_secret")
            self._args.mailjet_sender_email = credentials.get("mailjet_sender_email")
            if not self._args.mailjet_api_key or not self._args.mailjet_api_secret or not self._args.mailjet_sender_email:
                raise RuntimeError("Mailjet API Key/Secret 정보가 없습니다.")
        else:
            self._args.mailjet_api_key = None
            self._args.mailjet_api_secret = None
            self._args.mailjet_sender_email = None

    def profile(self):
        return self._args.profile

    def is_debug(self):
        return self._args.debug

    def user_source(self):
        return {
            "user_id": self._args.username,
            "user_pw": self._args.password,
        }

    def email_source(self):
        return {
            "recipient_email": self._safe_arg_get(lambda: self._args.email),
            "sender_email": self._safe_arg_get(lambda: self._args.mailjet_sender_email),
            "api_key": self._safe_arg_get(lambda: self._args.mailjet_api_key),
            "api_secret": self._safe_arg_get(lambda: self._args.mailjet_api_secret),
        }

    def send_result_to_email(self):
        return self._args.email is not None

    def is_quiet(self):
        return self._args.quiet

    def amount(self):
        return int(self._args.amount)

    def command(self):
        return self._args.command.upper()

    def transform_games(self):
        if self.command() == "BUY_LOTTO645":
            if self._args.games is None:
                self._args.games = [None for _ in range(Lotto645BuyRequest.MAX_GAME_COUNT)]

            req_bucket = []
            for game in self._args.games:
                req_bucket.append([] if game is None else [*map(int, game.split(","))])

            self._args.games = req_bucket

    def buy_lotto645_req(self):
        self.transform_games()
        return Lotto645BuyRequest(self._args.games)

    def _safe_arg_get(self, func):  # TODO(roeniss): Is this the best...?
        try:
            return func()
        except AttributeError:
            return None
