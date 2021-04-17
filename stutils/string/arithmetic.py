# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com


def add_strings(num1: str, num2: str) -> str:
    """给定两个字符串形式的非负整数，返回它们的和"""
    chars = []
    carry, i, j = 0, len(num1) - 1, len(num2) - 1
    while i >= 0 or j >= 0 or carry:
        if i >= 0:
            carry += ord(num1[i]) - ord('0')
            i -= 1
        if j >= 0:
            carry += ord(num2[j]) - ord('0')
            j -= 1
        chars.insert(0, str(int(carry % 10)))
        carry //= 10
    return ''.join(chars)


def multiply_strings(num1: str, num2: str) -> str:
    """给定两个字符串形式的非负整数，返回它们的积"""
    m, n = len(num1), len(num2)
    if m == 0 or n == 0:
        return '0'
    if num1 == '0' or num2 == '0':
        return '0'
    # 乘积的长度最多为m+n
    ans = [0] * (m + n)
    # 从后往前依次和每一位数相乘
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # 两数第i位和第j位的乘积暂时放到数组的i+j+1位
            ans[i + j + 1] += int(num1[i]) * int(num2[j])
    # 统一处理进位
    for i in range(m + n - 1, 0, -1):
        ans[i - 1] += ans[i] // 10
        ans[i] %= 10
    # ans数组第一位可能位0
    return ''.join(map(str, ans)).lstrip('0')


def check_expr(expr: str):
    """检查表达式的合法性，只包含空格数字和英文小括号

    返回值1：括号不匹配 2：异常字符 0：正常
    """
    stack = list()
    for char in expr:
        if char.isdigit() or char.isspace() or char in '+-*/':
            continue
        if char == ')':
            if not stack or stack[-1] != '(':
                return 1
            stack.pop()
        elif char == '(':
            stack.append(char)
        else:
            return 2
    return 0 if not stack else 1


def infix2suffix(expr: str) -> str:
    """中缀表达式转成后缀表达式（逆波兰表达式 Reverse Polish Notation）"""
    code = check_expr(expr)
    if code == 1:
        raise ValueError('Invalid bracket.')
    elif code == 2:
        raise ValueError('Invalid character.')
    s1, s2 = [], []  # 两个栈
    p = {'+': 1, '-': 1, '*': 2, '/': 2}  # 运算符优先级
    for c in expr:
        if c.isspace():
            continue
        # 遇到操作数时，将其压入S2
        if c.isdigit():
            s2.append(c)
        # 遇到运算符时，比较其与S1栈顶运算符的优先级
        elif c in p:
            while True:
                # 如果S1为空，或栈顶运算符为左括号(，则直接将此运算符入栈
                if not s1 or s1[-1] == '(':
                    s1.append(c)
                    break
                else:
                    # 否则，若优先级比栈顶运算符的高，也将运算符压入S1
                    if p[c] > p[s1[-1]]:
                        s1.append(c)
                        break
                    # 否则，将S1栈顶的运算符弹出并压入到S2中
                    # 再次循环与S1中新的栈顶运算符相比较
                    else:
                        s2.append(s1.pop())
        # 遇到括号时
        elif c in '()':
            # 如果是左括号(，则直接压入S1
            if c == '(':
                s1.append(c)
            # 如果是右括号)，则依次弹出S1栈顶的运算符，并压入S2
            # 直到遇到左括号为止，此时将这一对括号丢弃
            elif c == ')':
                while True:
                    t = s1.pop()
                    if t == '(':
                        break
                    s2.append(t)
    # 将s1剩余的运算符一次加入s2
    while s1:
        s2.append(s1.pop())
    return ''.join(s2)


def calculate(expr: str) -> float:
    """字符串表达式计算，支持+-*/()符号"""
    s = []
    suffix = infix2suffix(expr)
    if not suffix:
        raise ValueError('Empty Reverse Polish Notation.')
    for c in suffix:
        if c.isdigit():
            s.append(c)
        else:
            a = float(s.pop())
            b = float(s.pop())
            if c == '+':
                s.append(a + b)
            elif c == '-':
                s.append(b - a)
            elif c == '*':
                s.append(a * b)
            elif c == '/':
                s.append(b / a)
    return s.pop()
