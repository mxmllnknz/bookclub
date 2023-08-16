import typing

def numberedStrIterable(strlist: typing.Union[list[str], tuple[str,...]]) -> str:
    ans = ""
    for i, s in enumerate(strlist):
        ans +=  f"{i+1}. {s}"
        if i != len(strlist) - 1:
            ans +=  "\n"
    return ans