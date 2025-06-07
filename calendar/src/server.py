"""
    Googleカレンダーにイベントを取得、追加、削除するMCPサーバ
"""
from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
import google_calendar


# 定数の準備

mcp = FastMCP("Google-Calendar-Operation")


@mcp.tool()
def get_calendar_events(
    extract_num: Annotated[int, Field(ge=1, le=30), "取得するイベントの数"] = 10
    ) -> str:
    """ Googleカレンダーのイベントを取得する """
    return google_calendar.get_calendar_events(extract_num)


@mcp.tool()
def add_calendar_event_timeboxed(
        summary    : Annotated[str, Field(max_length=30), "イベントタイトル"],
        start_time : Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$"), "開始日時 (YYYY-MM-DDTHH:MM:SS)"],
        end_time   : Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$"), "終了日時 (YYYY-MM-DDTHH:MM:SS)"],
        description: Annotated[str, Field(max_length=100), "イベントの説明"] = "",
        location   : Annotated[str, Field(max_length=100), "イベントの場所"] = ""
    ) -> str:
    """
    Googleカレンダーに時間指定の予定を追加 (start_time/end_timeは "YYYY-MM-DDTHH:MM:SS" 形式)
    """
    return google_calendar.add_calendar_event_timeboxed(
        summary, start_time, end_time, description, location
    )


@mcp.tool()
def add_calendar_event_allday(
        summary    : Annotated[str, Field(max_length=30), "イベントタイトル"],
        start_date : Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$"), "開始日 (YYYY-MM-DD)"],
        end_date   : Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$"), "終了日 (YYYY-MM-DD)"],
        description: Annotated[str, Field(max_length=100), "イベントの説明"] = "",
        location   : Annotated[str, Field(max_length=100), "イベントの場所"] = ""
    ) -> str:
    """
    Googleカレンダーに終日予定を追加 (start_date/end_dateは "YYYY-MM-DD" 形式)
    """
    return google_calendar.add_calendar_event_allday(
        summary, start_date, end_date, description, location
    )

if __name__ == "__main__":
    mcp.run()
