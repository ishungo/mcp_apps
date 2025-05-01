from mcp.server.fastmcp import FastMCP
import psutil

# 定数の準備

mcp = FastMCP("Server-disk-info")

# サーバのdisk容量を取得する
def get_disk_usage() -> str:
    disk = psutil.disk_usage("/")
    total = disk.total / (1024 ** 3)
    used = disk.used / (1024 ** 3)
    free = disk.free / (1024 ** 3)
    percent = disk.percent
    usage = f"Total: {total:.2f} GB\nUsed: {used:.2f} GB\nFree: {free:.2f} GB\nPercent: {percent}%"
    return usage


@mcp.tool()
def disk_info() -> str:
    return get_disk_usage()

if __name__ == "__main__":
    mcp.run()
