from mcp.server.fastmcp import FastMCP
import disk_util

# 定数の準備

mcp = FastMCP("Server-disk-info")

# サーバのdisk容量を取得する
def get_disk_usage() -> str:
    usage = disk_util.get_disk_usage()
    return usage


@mcp.tool()
def disk_info() -> str:
    return get_disk_usage()


# サーバのメモリ使用量を取得する
def get_memory_usage() -> str:
    usage = disk_util.get_memory_usage()
    return usage


@mcp.tool()
def memory_info() -> str:
    return get_memory_usage()

if __name__ == "__main__":
    mcp.run()
