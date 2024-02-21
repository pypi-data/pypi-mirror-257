from ..common import Any, Optional, Union, datetime


def input_int(print_str: str, unit: str = "") -> int:
    """
    int入力

    Parameters
    ----------
    print_str : str
        表示文字列
    unit : str
        単位 by default ""

    Returns
    -------
    int
        入力数字
    """
    return int(_input(print_str=print_str, type=int, unit=unit))


def input_float(print_str: str, unit: str = "") -> float:
    """
    float入力

    Parameters
    ----------
    print_str : str
        表示文字列
    unit : str
        単位 by default ""

    Returns
    -------
    float
        入力数字
    """
    return float(_input(print_str=print_str, type=float, unit=unit))


def input_str(print_str: str, unit: str = "") -> str:
    """
    文字列出力

    Parameters
    ----------
    print_str : str
        表示文字列
    unit : str
        単位 by default ""

    Returns
    -------
    str
        入力文字列
    """
    return str(_input(print_str=print_str, type=str, unit=unit))


def input_min_sec(print_str: str) -> datetime:
    """
    入力時間からdatetimeオブジェクトを出力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    int
        _description_
    """
    return _input(print_str=print_str, type=datetime)


def input_bool(print_str: str) -> bool:
    """
    bool入力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    bool
        入力bool
    """
    return bool(_input(print_str=print_str, type=bool))


def _input(
    print_str: str,
    type: type,
    over_count: int = 1024,
    unit: str = "",
) -> Any:
    """
    コンソール入力処理

    Parameters
    ----------
    print_str : str
        表示文字列
    type : Union[int, str, float, datetime]
        出力タイプ
    over_count : int
        オーバーフロー回数 by default 1024
    unit : str
        単位 by default ""

    Returns
    -------
    Union[int, str, float]
        入力されたデータ

    Raises
    ------
    TypeError
        予期しないタイプ
    OverflowError
        無限ループ対策
    """
    result: Union[int, str, float, datetime, bool]
    if unit:
        unit = f"[{unit}]"
    for _ in range(over_count):
        try:
            if type == bool:
                data = input(print_str + "入力[Yn]:")
                if data.lower() == "y":
                    result = True
                elif data.lower() == "n":
                    result = False
                else:
                    raise ValueError
                if result:
                    if input("Y? [Yn]:").lower() == "y":
                        break
                else:
                    if input("n? [Yn]:").lower() == "y":
                        break
            elif type == datetime:
                date = _datetime_input(print_str)
                if date:
                    result = date
                    if input(str(date) + "? [Yn]:").lower() == "y":
                        break
            else:
                data = input(print_str + f"入力{unit}:")
                if type == int:
                    result = int(data)
                elif type == float:
                    result = float(data)
                elif type == str:
                    result = data
                elif type == datetime:
                    result = datetime.strptime(data, "%M:%S")
                else:
                    raise TypeError
                if input(data + "? [Yn]:").lower() == "y":
                    break
        except ValueError:
            pass
    else:
        raise OverflowError
    return result


def _datetime_input(print_str: str) -> Optional[datetime]:
    need_date = ["西暦", "月", "日", "時", "分", "秒", "ミリ秒"]
    data = []
    for date in need_date:
        data.append(input(f"{print_str}の{date}を入力(空白で現在時刻):"))
    result = datetime.now()
    try:
        if data[0]:
            result = result.replace(year=int(data[0]))
        if data[1]:
            result = result.replace(month=int(data[1]))
        if data[2]:
            result = result.replace(day=int(data[2]))
        if data[3]:
            result = result.replace(hour=int(data[3]))
        if data[4]:
            result = result.replace(minute=int(data[4]))
        if data[5]:
            result = result.replace(second=int(data[5]))
        if data[6]:
            result = result.replace(microsecond=int(data[6]))
        return result
    except ValueError:
        return None
