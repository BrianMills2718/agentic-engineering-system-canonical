def greet(name: str) -> str:
    """Say hello.

    [[[cog import lockstep.cogtext as c; c.docstring("ART-GREET")]]]
    [[[end]]]
    """
    return f"Hello, {name}!"
