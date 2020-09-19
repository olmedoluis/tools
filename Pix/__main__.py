class ArgumentManager:
    def __init__(self, argv):
        self.user_routes = argv
        self.actual_route = argv[0]
        self.left_keys = argv[1:]

    def get_good_routes(self):
        good_routes = []

        for route in self.user_routes:
            if route != self.actual_route:
                good_routes.append(route)
            else:
                break

        return good_routes

    def get_next_route(self):
        return "" if 0 == len(self.left_keys) else self.left_keys[0]


def get_concatenated_routes(routes):
    indexes = [i for i, e in enumerate(routes) if e == "n"]
    last_route = routes[indexes[-1] + 1 :]
    all_routes = []
    last_index = 0

    for index in indexes:
        all_routes.append(routes[last_index:index])
        last_index = index + 1

    all_routes.append(last_route)

    return all_routes


def main():
    from sys import argv

    arg = argv[1:]

    if len(arg) == 0:
        return

    from Configuration import ALIASES
    from .Data.Routes import KEYS
    from .Modules import PIX_STORE
    from .Modules.Helpers import check_pix_shortcut, check_route

    allRoutes = get_concatenated_routes(arg) if "n" in arg else [arg]

    for arguments in allRoutes:
        argument_manager = ArgumentManager(arguments)

        route_name = check_pix_shortcut(argument_manager.actual_route, KEYS, ALIASES)

        if route_name == False:
            from .Modules.Helpers import MessageControl

            good_routes = f"pix {' '.join(argument_manager.get_good_routes())}"
            wrong_routes = f"{argument_manager.actual_route} {' '.join(argument_manager.left_keys)}"

            return MessageControl().log(
                "error-unknown_route",
                {"pm_goodRoutes": good_routes, "pm_wrongRoutes": wrong_routes},
            )

        next_route = argument_manager.get_next_route()
        sub_route = check_route(next_route, KEYS[route_name], ALIASES[route_name])

        requiredRouter = PIX_STORE[route_name]
        requiredRouter(argument_manager, sub_route)


if __name__ == "__main__":
    main()
