import psutil

# サーバのdisk容量を取得する
def get_disk_usage() -> str:
    header = ["Mountpoint", "Total[GB]", "Used[GB]", "Free[GB]", "Percent[%]"]
    body = []
    all_partitions = psutil.disk_partitions()
    for partition in all_partitions:
        mountpoint = partition.mountpoint
        partition = psutil.disk_usage(mountpoint)
        # print(partition)

        used = partition.used / (1024 ** 3)
        free = partition.free / (1024 ** 3)
        total = used + free
        percent = partition.percent
        body.append([mountpoint, f"{total:.2f}", f"{used:.2f}", f"{free:.2f}", str(percent)])
    table = [header] + body
    # print(to_markdown_table(table))
    return to_markdown_table(table)

def get_memory_usage() -> str:
    header = ["Total[GB]", "Used[GB]", "Free[GB]", "Percent[%]"]
    mem = psutil.virtual_memory()
    total = mem.total / (1024 ** 3)
    used = mem.used / (1024 ** 3)
    free = mem.available / (1024 ** 3)
    percent = mem.percent
    body = [[f"{total:.2f}", f"{used:.2f}", f"{free:.2f}", str(percent)]]
    table = [header] + body
    return to_markdown_table(table)

def to_markdown_table(table: list[list[str]], header: bool = True) -> str:
    col_num = len(table[0])
    # 各列の最大文字数を取得
    max_width = []
    for col_idx in range(col_num):
        max_width.append(max(len(row[col_idx]) for row in table))
    # print(max_width)

    table_str = ""
    for idx, row in enumerate(table):
        row_str = "|"
        for col_idx, col in enumerate(row):
            if col_idx == 0:
                row_str += f" {col.ljust(max_width[col_idx])} |"
            else:
                row_str += f" {col.rjust(max_width[col_idx])} |"
        table_str += row_str + "\n"
        if idx == 0 and header:
            row_str = "|"
            for col_idx, col in enumerate(row):
                if col_idx == 0:
                    row_str += ":" + "-" * max_width[col_idx] + " |"
                else:
                    row_str += " " + "-" * max_width[col_idx] + ":|"
            table_str += row_str + "\n"
    return table_str

if __name__ == "__main__":
    # print(get_disk_usage())
    print(get_memory_usage())
