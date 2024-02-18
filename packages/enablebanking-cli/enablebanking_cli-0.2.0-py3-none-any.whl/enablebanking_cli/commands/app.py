import json
import os

from datetime import datetime
from enum import Enum

from ..cp_client import CpClient
from ..cp_store import CpStore
from .base import BaseCommand


class Environment(str, Enum):
    PRODUCTION = "PRODUCTION"
    SANDBOX = "SANDBOX"

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class AppCommand(BaseCommand):
    def __init__(self, parent_subparsers):
        self.parser = parent_subparsers.add_parser("app", help="Application commands")
        self.parser.add_argument(
            "-u",
            "--user",
            type=str,
            help="ID of an authenticated user to be used (using default if not provided)",
            required=False,
        )
        self.subparsers = self.parser.add_subparsers(
            title="Application Commands",
            dest="app_command")
        default_parser = self.subparsers.add_parser(
            "default",
            help="Set an application to be used by default",
        )
        default_parser.add_argument("app", type=str, help="Application ID")
        list_parser = self.subparsers.add_parser("list", help="List locally available applications")
        requests_parser = self.subparsers.add_parser(
            "requests",
            help="Fetch logs of requests made by an application",
        )
        requests_parser.add_argument(
            "-a",
            "--app",
            type=str,
            help="Application ID (using default if not provided)",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-account-id",
            metavar="ACCOUNT_ID",
            type=str,
            help="Filtering requests associated with an account by its ID",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-aspsp-country",
            metavar="ASPSP_COUNTRY",
            type=str,
            help="Filtering requests by a country (ISO 3166 code)",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-aspsp-name",
            metavar="ASPSP_NAME",
            type=str,
            help="Filtering requests by ASPSP name",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-auth-approach",
            metavar="AUTH_APPROACH",
            type=str,
            help="Filtering requests by an authorization approach",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-auth-method",
            metavar="AUTH_METHOD",
            type=str,
            help="Filtering requests by an authorization method",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-authorization-id",
            metavar="AUTHORIZATION_ID",
            type=str,
            help="Filtering requests associated with an authorization by its ID",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-endpoint-name",
            metavar="ENDPOINT_NAME",
            type=str,
            help="Filtering requests by an endpoint name",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-payment-id",
            metavar="PAYMENT_ID",
            type=str,
            help="Filtering requests associated with a payment by its ID",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-psu-type",
            metavar="PSU_TYPE",
            type=str,
            help="Filtering requests by PSU type",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-response-code",
            metavar="RESPONSE_CODE",
            type=str,
            help="Filtering requests by a response code",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-session-id",
            metavar="SESSION_ID",
            type=str,
            help="Filtering requests associated with a session by its ID",
            required=False,
        )
        requests_parser.add_argument(
            "--filter-session-status",
            metavar="",
            type=str,
            help="Filtering requests by a session status",
            required=False,
        )
        requests_parser.add_argument(
            "-o",
            "--outfile",
            nargs="?",
            const="default",
            type=str,
            help="Outputing requests to a file instead of printing to console",
            required=False,
        )
        register_parser = self.subparsers.add_parser("register", help="Register an application")
        register_parser.add_argument(
            "-e",
            "--environment",
            type=Environment,
            choices=[*Environment],
            help=f"Environment, which the application will use",
            required=True,
        )
        register_parser.add_argument(
            "-n",
            "--name",
            type=str,
            help="Name of the application being registered",
            required=True,
        )
        register_parser.add_argument(
            "-r",
            "--redirect-urls",
            type=str,
            nargs="+",
            help=f"Redirect URL(s) allowed for the application",
            required=True,
        )
        register_parser.add_argument(
            "-d",
            "--description",
            type=str,
            help="Description of the application being registered",
            required=False,
        )
        register_parser.add_argument(
            "--gdpr-email",
            type=str,
            help=f"Email of data protection matters",
            required=False,
        )
        register_parser.add_argument(
            "--privacy-url",
            type=str,
            help=f"URL of the application's privacy policy",
            required=False,
        )
        register_parser.add_argument(
            "--terms-url",
            type=str,
            help=f"URL of the application's terms of service",
            required=False,
        )
        register_parser.add_argument(
            "-c",
            "--cert-path",
            type=str,
            help=f"Path to a certificate or a public key of the application",
            required=True,
        )
        register_parser.add_argument(
            "-k",
            "--key-path",
            type=str,
            help=f"Path to a private key of the application (used to generate or verify public key)",
            required=False,
        )
        self.subparsers.add_parser("share", help="Share an application")

    def register(self, args):
        print("Registering an application...")
        cp_store = CpStore(args.root_path)
        cp_client = CpClient(args.cp_domain, cp_store.get_user_path(args.user))
        with open(args.cert_path, "r") as f:
            cert_content = f.read()
        response = cp_client.register_application({
            "name": args.name,
            "certificate": cert_content,
            "environment": args.environment,
            "redirect_urls": args.redirect_urls,
            "description": args.description,
            "gdpr_email": args.gdpr_email,
            "privacy_url": args.privacy_url,
            "terms_url": args.terms_url,
        })
        if response.status != 200:
            print(f"{response.status} response from the applications API: {response.read().decode()}")
            return 1
        response_data = json.loads(response.read().decode())
        print(f"The application is registered under ID {response_data['app_id']}")
        cp_store = CpStore(args.root_path)
        os.makedirs(cp_store.cp_apps_path, exist_ok=True)
        app_filename = cp_store.get_app_filename(response_data["app_id"])
        with open(os.path.join(cp_store.cp_apps_path, app_filename), "w") as f:
            f.write(json.dumps({
                "kid": response_data["app_id"],
                "name": args.name,
                "description": args.description,
                "certificate": cert_content,
                "key_path": args.key_path,
                "environment": args.environment,
                "redirect_urls": args.redirect_urls,
            }, indent=4))
        cp_store.set_default_app_filename(app_filename)
        print("Done!")

    def list(self, args):
        cp_store = CpStore(args.root_path)
        apps_data = cp_store.load_app_files()
        for app_data in apps_data:
            print("*" if app_data["_default"] else " ", app_data["kid"], app_data["name"])

    def default(self, args):
        cp_store = CpStore(args.root_path)
        apps_data = cp_store.load_app_files()
        is_app_found = False
        for app_data in apps_data:
            if app_data["kid"] == args.app:
                is_app_found = True
                break
        if not is_app_found:
            print(f"Application with ID '{args.app}' is not available")
            return 1
        cp_store.set_default_app_filename(cp_store.get_app_filename(args.app))
        print(f"Default application switched to {args.app} ({app_data['name']})")

    def requests(self, args):
        cp_store = CpStore(args.root_path)
        cp_client = CpClient(args.cp_domain, cp_store.get_user_path(args.user))
        app_id = args.app if args.app is not None else cp_store.load_app_file()["kid"]
        print("Fetching requests...")
        response = cp_client.fetch_requests(
            app_id,
            account_id=args.filter_account_id,
            aspsp_country=args.filter_aspsp_country,
            aspsp_name=args.filter_aspsp_name,
            auth_approach=args.filter_auth_approach,
            auth_method=args.filter_auth_method,
            authorization_id=args.filter_authorization_id,
            endpoint_name=args.filter_endpoint_name,
            payment_id=args.filter_payment_id,
            psu_type=args.filter_psu_type,
            response_code=args.filter_response_code,
            session_id=args.filter_session_id,
            session_status=args.filter_session_status,
        )
        if response.status != 200:
            print(f"{response.status} response from the requests API: {response.read().decode()}")
            return 1
        response_data = json.loads(response.read().decode())
        requests = response_data["requests"]
        print(f"Fetched {len(requests)} request" + ("s" if len(requests) != 1 else "") + ".")
        if len(requests):
            requests_text = json.dumps(requests, indent=4)
            if args.outfile is None:
                print(requests_text)
            else:
                if args.outfile == "default":
                    now = datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"{app_id}-{now}.json"
                else:
                    filename = args.outfile
                print(f"Saving requests to {filename}...")
                with open(filename, "w") as f:
                    f.write(requests_text)
        print("Done!")
