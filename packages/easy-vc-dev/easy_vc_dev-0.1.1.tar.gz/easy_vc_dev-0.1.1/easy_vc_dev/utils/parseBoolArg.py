def parseBoolArg(arg: str | bool) -> bool:
    return arg.lower() in ("true", "1", "yes", "y") if isinstance(arg, str) else arg
