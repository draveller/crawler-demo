import csv
import os
from datetime import datetime
from typing import Dict
from typing import List, Tuple, Any

from openpyxl import load_workbook, Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet
from typing_extensions import Literal


def generate_unique_filename(prefix: str = "data", extension: str = ".xlsx") -> str:
    """
    生成一个包含当前时间戳的唯一文件名。

    :param prefix: 文件名前缀。
    :param extension: 文件扩展名。
    :return: 生成的文件名。
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
    return f"{prefix}_{timestamp}{extension}"


def get_default_path(store_folder: str = "acer_store") -> str:
    """
    获取默认的 Excel 文件存储路径，包含时间戳，并确保存储目录存在。

    :param store_folder: 存储文件的文件夹名称。
    :return: 完整的 Excel 文件路径。
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    store_dir = os.path.join(current_dir, store_folder)
    # 确保指定的目录存在。如果不存在，则创建该目录。
    os.makedirs(store_dir, exist_ok=True)
    file_name = generate_unique_filename()
    return os.path.join(store_dir, file_name)


def load_or_create_workbook(excel_path: str, sheet_name: str) -> Workbook:
    """
    加载现有的工作簿或创建一个新的工作簿

    :param excel_path: Excel 文件路径。
    :param sheet_name: 工作表名称。
    :return: 打开的或新创建的 Workbook 对象。
    """
    if os.path.exists(excel_path):
        workbook = load_workbook(excel_path)
    else:
        workbook = Workbook()
        # 重命名默认创建的 'Sheet' 工作表为指定的 sheet_name
        default_sheet = workbook.active
        default_sheet.title = sheet_name
    return workbook

def _append_row_with_images(worksheet: Worksheet, row: List[Any], row_num: int) -> None:
    """
    将一行数据追加到工作表中，处理可能存在的 OpenpyxlImage 类型，并根据图片大小自动调整行列宽高。

    :param worksheet: 目标 Worksheet 对象。
    :param row: 要追加的行数据。
    :param row_num: 行号, 从1开始。
    """

    # 遍历行中的每个单元格
    for col_num, cell_value in enumerate(row, start=1):
        if isinstance(cell_value, Image):
            # 如果是 Openpyxl 的 Image 类型，将图像添加到工作表中
            cell_ref = worksheet.cell(row=row_num, column=col_num).coordinate
            cell_value.anchor = cell_ref
            worksheet.add_image(cell_value)

            # 根据图片大小调整列宽和行高
            _adjust_column_width(worksheet, col_num, cell_value.width)
            _adjust_row_height(worksheet, row_num, cell_value.height)
        else:
            # 否则，直接写入单元格
            worksheet.cell(row=row_num, column=col_num, value=cell_value)


def _adjust_column_width(worksheet: Worksheet, col_num: int, image_width: float) -> None:
    """
    根据图片宽度调整列宽。

    :param worksheet: 目标 Worksheet 对象。
    :param col_num: 列号。
    :param image_width: 图片的宽度（以像素为单位）。
    """
    # 将像素转换为 Excel 列宽单位（1 单位 ≈ 7 像素）
    width_units = image_width / 7

    # 获取当前列宽
    column_letter = get_column_letter(col_num)
    current_width = worksheet.column_dimensions[column_letter].width

    # 如果当前列宽小于图片宽度，则调整列宽
    if current_width is None or current_width < width_units:
        worksheet.column_dimensions[column_letter].width = width_units


def _adjust_row_height(worksheet: Worksheet, row_num: int, image_height: float) -> None:
    """
    根据图片高度调整行高。

    :param worksheet: 目标 Worksheet 对象。
    :param row_num: 行号。
    :param image_height: 图片的高度（以像素为单位）。
    """
    # 将像素转换为 Excel 行高单位（1 单位 ≈ 1.33 像素）
    height_units = image_height / 1.33

    # 获取当前行高
    current_height = worksheet.row_dimensions[row_num].height

    # 如果当前行高小于图片高度，则调整行高
    if current_height is None or current_height < height_units:
        worksheet.row_dimensions[row_num].height = height_units


def save(
        data: List[List[Any]] | Tuple[Tuple[Any, ...], ...],
        excel_path: str | None = None,
        sheet_name: str = 'Sheet1',
        clean_mode: Literal['wb', 'ws', 'no'] = 'ws'
) -> None:
    """
    将数据保存到指定的 Excel 文件中。

    :param data: 要保存的数据，可以是列表的列表、元组的元组或字典的列表/单个字典。
                 - 列表的列表或元组的元组表示多行数据（可以包含表头）
                 - 字典的列表或单个字典表示带有表头的数据
    :param excel_path: Excel 文件路径。如果为 None，则使用默认路径。
    :param sheet_name: 工作表名称。
    :param clean_mode: 清除策略，第1位表示是否清除文件内容（1-清除，0-追加），第2位表示工作表层面的策略。
    """
    # 动态生成默认路径
    if excel_path is None:
        excel_path = get_default_path()

    # 加载或创建工作簿
    wb = load_or_create_workbook(excel_path, sheet_name)

    # 策略=wb时删除所有sheet; 策略=ws时删除指定sheet; 策略=no时不删除
    [wb.remove(sheet) for sheet in wb.worksheets[:] if clean_mode == 'wb']
    [wb.remove(sheet) for sheet in wb.worksheets[:] if clean_mode == 'ws' and sheet.title == sheet_name]

    # 获取或创建sheet
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.create_sheet(sheet_name)
    # 写入数据到sheet中
    [_append_row_with_images(ws, row, i + 1) for i, row in enumerate(data) if data]
    # 将sheet移动到最前
    wb.move_sheet(ws, offset=-wb.index(ws))
    # 保存工作簿
    wb.save(excel_path)


def save_csv(data: List[List[Any]] | Tuple[Tuple[Any, ...], ...], csv_path: str):
    """
    将二维列表或二维元组保存为 CSV 文件。

    :param data: 要保存的数据，可以是二维列表或二维元组。
    :param csv_path: CSV 文件路径。如果为 None，则保存为 'output.csv'。
    """
    # 如果未提供 csv_path，使用默认文件名
    if csv_path is None:
        csv_path = "output.csv"

    # 写入 CSV 文件
    try:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print(f"数据已成功保存到 {csv_path}")
    except Exception as e:
        print(f"保存 CSV 文件时出错: {e}")
