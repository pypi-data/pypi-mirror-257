class TimerInitError(ValueError):
    """Raised when the Timer is initialized with invalid parameters"""


class TimerChangeError(ValueError):
    """Raised when the Timer is called with an invalid status"""


class Timer:
    """A timer that can be slowed down or sped up by calling it with a boolean value."""

    def __init__(
        self,
        default: int = 30,
        min_: int | None = None,
        max_: int | None = None,
        change_rate: float | None = None,
    ):
        self.default = default
        self.min_ = min_
        self.max_ = max_
        self.change_rate = change_rate
        self.next: int = self.default
        self.check_init()

    def check_init(self):
        if self.min_ is not None and self.max_ is not None:
            if self.min_ > self.max_:
                raise TimerInitError(
                    f"min_ must be smaller than max_, got {self.min_} and {self.max_}"
                )
        if self.change_rate is not None:
            if self.change_rate <= 1:
                raise TimerInitError(
                    f"change_rate must be greater than 1, got {self.change_rate}"
                )
        if self.min_ is None and self.max_ is None and self.change_rate is None:
            raise TimerInitError(
                "At least one of min_, max_, or change_rate must be set"
            )

    def __call__(self, status: bool | None = None) -> int:
        if status is None:
            return self.next
        if status:
            if self.max_:
                self.next = (self.next + self.max_) >> 1
            elif self.change_rate:
                self.next = int(self.next * self.change_rate)
            else:
                raise TimerChangeError(
                    "Cannot slow down the heartbeat without setting max_ or change_rate"
                )
        else:
            if self.min_:
                self.next = (self.next + self.min_) >> 1
            elif self.change_rate:
                self.next = int(self.next // self.change_rate)
            else:
                raise TimerChangeError(
                    "Cannot speed up the heartbeat without setting min_ or change_rate"
                )
        return self.next

    def __str__(self) -> str:
        return str(self.next)

    def __repr__(self) -> str:
        return f"Timer(default={self.default}, min_={self.min_}, max_={self.max_}, change_rate={self.change_rate})"

    def reset(self):
        self.next = self.default
