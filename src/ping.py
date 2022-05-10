from datetime import datetime
from my_resource import Argument, MyResource


class Ping(MyResource):
    def __init__(self) -> None:
        super().__init__(
            args=[
                Argument(name="number", type=int),
                Argument(name="string", type=str, is_required=True)
            ]
        )

    def get(self, name=None):
        return {"message": f"Hello! It's {datetime.now().isoformat()}"}

    def post(self, name=None):
        args = self.request_args.parse_args()
        return {
            "name": name,
            "number": args.number,
            "string": args.string
        }
