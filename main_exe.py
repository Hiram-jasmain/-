from borax.calendars.lunardate import LunarDate
import datetime

# 六宫定义（含五行属性）
LIU_GONG = [
    ('大安', '吉', '木', '安稳清吉，贵人扶持'),
    ('留连', '凶', '土', '反复拖延，纠缠不休'),
    ('速喜', '吉', '火', '喜讯速至，合作有利'),
    ('赤口', '凶', '金', '官非口舌，金属血光'),
    ('小吉', '吉', '水', '谋事可成，出行有利'),
    ('空亡', '凶', '土', '事有不成，财防落空')
]

# 时辰对照表
SHI_CHEN = [
    ('子', '23:00-01:00'), ('丑', '01:00-03:00'),
    ('寅', '03:00-05:00'), ('卯', '05:00-07:00'),
    ('辰', '07:00-09:00'), ('巳', '09:00-11:00'),
    ('午', '11:00-13:00'), ('未', '13:00-15:00'),
    ('申', '15:00-17:00'), ('酉', '17:00-19:00'),
    ('戌', '19:00-21:00'), ('亥', '21:00-23:00')
]


def get_input(prompt, default=None, input_type=int):
    """获取用户输入"""
    while True:
        try:
            if default is not None:
                user_input = input(f"{prompt} (默认: {default}): ") or default
            else:
                user_input = input(f"{prompt}: ")

            return input_type(user_input)
        except ValueError:
            print("输入无效，请重新输入！")


def calculate_divination(year, month, day, hour):
    """计算小六壬卦象"""
    try:
        # 计算农历和时辰
        dt = datetime.datetime(year, month, day, hour)
        lunar_date = LunarDate.from_solar_date(year, month, day)

        # 时辰计算
        shi_chen_idx = (hour + 1) // 2 % 12
        sc_name, sc_range = SHI_CHEN[shi_chen_idx]

        # 三宫定位算法
        month_index = (lunar_date.month - 1) % 6
        day_index = (month_index + lunar_date.day - 1) % 6
        hour_index = (day_index + shi_chen_idx) % 6

        # 构建结果
        result = {
            '公历': dt.strftime('%Y-%m-%d %H:%M'),
            '农历': f'{lunar_date.month}月{lunar_date.day}日' + ('(闰)' if lunar_date.leap else ''),
            '时辰': f'{sc_name}时 ({sc_range})',
            '卦象': {
                '月宫': LIU_GONG[month_index],
                '日宫': LIU_GONG[day_index],
                '时宫': LIU_GONG[hour_index]
            }
        }

        return result

    except Exception as e:
        raise ValueError(f"计算错误: {str(e)}")


def show_result(result):
    """逐步显示结果"""
    print("\n✨ 小六壬卦象报告")
    print("====================")
    print(f"公历时间：{result['公历']}")
    print(f"农历时间：{result['农历']}")
    print(f"当前时辰：{result['时辰']}")
    input("\n按Enter键查看卦象...")

    for pos in ['月宫', '日宫', '时宫']:
        name, jx, wx, desc = result['卦象'][pos]
        print(f"\n▍{pos}卦象")
        print(f"• 名称：{name}")
        print(f"• 吉凶：{jx}")
        print(f"• 五行：{wx}")
        print(f"• 解读：{desc}")
        if pos != '时宫':
            input("\n按Enter键查看下一卦象...")


def main():
    print("欢迎使用小六壬占卜系统")
    print("====================\n")

    # 获取当前时间作为默认值
    now = datetime.datetime.now()

    while True:
        print("\n请输入占卜时间：")
        year = get_input("年份", now.year)
        month = get_input("月份", now.month)
        day = get_input("日期", now.day)
        hour = get_input("小时", now.hour)

        try:
            result = calculate_divination(year, month, day, hour)
            show_result(result)
        except ValueError as e:
            print(f"\n错误: {str(e)}")

        choice = input("\n是否继续占卜？(y/n): ").lower()
        if choice != 'y':
            print("\n感谢使用，再见！")
            break


if __name__ == "__main__":
    main()