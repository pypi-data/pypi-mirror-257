from typing import Union, Iterable


def prompt(string: str, p_t: Union[str, Iterable[str]], p_f: Union[str, Iterable[str]]) -> str:
    """Prompt for input and return the selected answer.

    Args:
        string: Prefix string to input
        p_t: Any of the :code:`True` prompts
        p_f: Any of the :code:`False` prompts

    """
    x = input(string).strip()
    if isinstance(p_t, str):
        p_t = {p_t}
    if isinstance(p_f, str):
        p_f = {p_f}
    valid_inputs = {*p_t, *p_f}
    while x not in valid_inputs:
        x = input(string + f"\n\nPlease type one of {p_t} \nOr one of {p_f} ").strip()
    return x


def prompt_p(string: str, p_t: Union[str, set], p_f: Union[str, set]) -> bool:
    """Prompt for input and return a boolean value.

    Args:
        string: Prefix string to input
        p_t: Any of the `True` prompts
        p_f: Any of the `False` prompts

    """
    x = input(string).strip()
    if isinstance(p_t, str):
        p_t = {p_t}
    if isinstance(p_f, str):
        p_f = {p_f}
    valid_inputs = {*p_t, *p_f}
    while x not in valid_inputs:
        x = input(string + f"\nPlease type one of {valid_inputs} ").strip()
    if x in p_t:
        return True
    elif x in p_f:
        return False


def prompt_yes_no(string: str) -> bool:
    return prompt_p(string + " (yes or no) ", "yes", "no")


def prompt_y_n(string: str) -> bool:
    return prompt_p(string + " (y, n) ", {"yes", "y"}, {"no", "n"})
