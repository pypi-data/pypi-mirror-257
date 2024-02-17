class CredentialsMissingError(Exception):
    def __init__(self, token):
        assert token in ["Conductor API Key",
                         "Conductor Shared Secret"], "Not a valid token arg"
        message = f"{token} required. If you have one " \
                  f"either add it to environment as {token.replace(' ', '_').upper()} " \
                  "or pass it as the api_key parameter. If you do " \
                  "not have one you can request one here: " \
                  "https://developers.conductor.com/"
        Exception.__init__(self, message)
