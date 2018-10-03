from flask_restful import reqparse


# validation parsers
registration_parser = reqparse.RequestParser()
create_verification_parser = reqparse.RequestParser()
update_verification_parser = reqparse.RequestParser()
login_parser = reqparse.RequestParser()
logout_parser = reqparse.RequestParser()
edituserdetails_parser = reqparse.RequestParser()

edituserdetails_parser.add_argument(
    'email',
    help='This field is required',
    required=False
)

edituserdetails_parser.add_argument(
    'firstName',
    help='This field is required',
    required=False
)

edituserdetails_parser.add_argument(
    'lastName',
    help='This field is required',
    required=False
)

# register user validation parser
registration_parser.add_argument(
    'email',
    help='This field is required',
    required=True
)
registration_parser.add_argument(
    'firstName',
    help='This field is required',
    required=True
)
registration_parser.add_argument(
    'lastName',
    help='This field is required',
    required=True
)
registration_parser.add_argument(
    'tokenId',
    help='This field is required',
    required=True
)

# create verification validation parser
create_verification_parser.add_argument(
    'tokenId',
    help='This field is required',
    required=True
)
create_verification_parser.add_argument(
    'userId',
    help='This field is required',
    required=True
)
create_verification_parser.add_argument(
    'issuedTimestamp',
    help='This field is required',
    required=True
)
create_verification_parser.add_argument(
    'state',
    help='This field is required',
    required=True
)

# update verification parser
update_verification_parser.add_argument(
    'tokenId',
    help='This field is required',
    required=True
)
update_verification_parser.add_argument(
    'state',
    help='This field is required',
    required=True
)

login_parser.add_argument(
    'tokenId',
    help='This field is required',
    required=True
)
login_parser.add_argument(
    'loginState',
    help='This field is required',
    required=True
)
login_parser.add_argument(
    'loginDate',
    help='This field is required',
)

logout_parser.add_argument(
    'logoutDate',
    help='This field is required',
    required=True
)
