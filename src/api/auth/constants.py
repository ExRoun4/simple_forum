from enums import Enum

class Routes(str, Enum):
    PREFIX = "/auth"

    REGISTER = "/register"
    LOGIN = "/login"
    LOGOUT = "/logout"

    REFRESH = "/refresh"

    @staticmethod
    def get_refresh_full_route():
        return Routes.PREFIX + Routes.REFRESH

tags = ["Tags"]