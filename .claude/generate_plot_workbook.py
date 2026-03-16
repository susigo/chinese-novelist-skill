from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
from datetime import datetime, timezone
from xml.sax.saxutils import escape

out_path = Path(r"E:/pratice/AITest/chinese-novelist-skill/novels/修真之创世纪/大纲/剧情推进总表.xlsx")

sheet_names = [
    "使用说明",
    "总览",
    "第1卷-魂入边荒",
    "第2卷-坊市试道",
    "第3卷-遗迹启明",
    "第4卷-宗门争锋",
    "第5卷-玄始战场",
    "第6卷-离星之门",
    "第7卷-初入星海",
    "第8卷-百道学宫",
]

volume_meta = [
    ("第1卷-魂入边荒", "底层求生逆袭", "黑巷反杀、矿难突围、夜市收网", "女性反馈以底层烟火气为主，先埋高位关注", "黑巷 / 矿场 / 鬼市 / 夜市", "避免只有生存，没有情绪回报"),
    ("第2卷-坊市试道", "立足坊市、方法出圈", "公开压场、拆台夺势、底层翻身", "辛红绡等底层女性反馈；开始有人因名声关注林渊", "坊市 / 工坊 / 灰市 / 动乱", "避免只有经营，没有炸场面"),
    ("第3卷-遗迹启明", "副本探索与体系启明", "抢理解权、抢资产、深层逃生", "姬清微开始真正注意到林渊", "遗迹外层 / 中层 / 深层 / 崩塌逃生", "避免全程解谜，缺人味和冲突"),
    ("第4卷-宗门争锋", "公开舞台打脸", "资格卡脖子、论道压场、秘境翻盘", "姬清微正面对撞，暧昧正式起势", "宗门 / 论道台 / 试炼秘境 / 评定场", "避免只讲理念，不给情绪拉扯"),
    ("第5卷-玄始战场", "战争体系升级", "散修成军、矿脉决战、战场反杀", "战时互救、立场裂缝、认知松动", "战场 / 废墟 / 矿脉 / 后勤据点", "避免主线太硬，情绪线断温"),
    ("第6卷-离星之门", "战后收拢与离星抉择", "资源兑现、内奸泄密、抢门突围", "姬清微暧昧爆发，去留抉择最强", "战后据点 / 古门遗址 / 突围战场", "保持秘密感与高压感并存"),
    ("第7卷-初入星海", "换地图压制后重构", "星海吃瘪、模型重构、小胜反杀", "商月绮可入场；姬清微进入异乡竞合", "星港 / 底层区 / 黑市 / 废矿 / 中立港", "避免连续吃瘪、空间气质过灰"),
    ("第8卷-百道学宫", "学宫争标准与解释权", "讲席压场、项目夺势、实证翻盘", "学宫追随者入场；姬清微关系继续升温", "学宫 / 实验场 / 工坊 / 外部试验地", "避免像一直在开会，缺实战和场景变化"),
]

line_rows = [
    ("主线", "主剧情推进", "本章主事件，用最短关键词概括。", 5),
    ("主线", "男主成长/升级", "修为、方法论、认知、组织力任一推进即可记。", 5),
    ("主线", "爽点兑现", "打脸 / 反杀 / 压场 / 夺势 / 抢资源等。", 5),
    ("主线", "悬念/伏笔", "新谜题、埋伏线、下章钩子来源。", 9),
    ("主线", "反派动作", "施压、试探、布局、反扑、换人。", 5),
    ("势力", "资源/势力扩张", "人手、渠道、矿脉、标准、话语权。", 8),
    ("世界", "世界观/遗迹/远古秘密", "设定推进必须服务剧情，不写成纯说明。", 7),
    ("情绪", "姬清微线", "关注、对撞、互救、嘴硬、立场拉扯。", 6),
    ("情绪", "苏半夏线", "共患难、照拂、经营配合、情绪承接。", 6),
    ("情绪", "裴丹青线", "专业合作、试药疗伤、成熟克制张力。", 6),
    ("情绪", "商月绮线", "交易试探、危险撩拨、资源互换。", 6),
    ("情绪", "其他女性反馈", "辛红绡、学宫追随者、阶段女性角色。", 6),
    ("人物", "核心配角成长", "顾七、段星罗等人的立功、背叛或转变。", 10),
    ("体验", "场景类型", "避免连续多章空间气质重复。", 9),
    ("体验", "章末钩子", "每章结尾要有追读驱动力。", 9),
    ("体验", "本章功能评价", "爽 / 暧昧 / 铺垫 / 爆点 / 刀 / 名场面。", 10),
]

chapter_prefill = {
    "第1卷-魂入边荒": {
        "主剧情推进": {
            1: "魂穿惊醒",
            2: "债主堵门",
            3: "摸清烂账",
            4: "残功险试",
            5: "黑巷逃命",
            6: "灰市换路",
            7: "破器控灵",
            8: "黑巷反杀",
        },
        "男主成长/升级": {
            1: "识灵流异常",
            2: "判断旧伤根源",
            3: "建立求生顺序",
            4: "首次结构观测",
            5: "学会压伤稳息",
            6: "学灰色生存术",
            7: "控灵入门",
            8: "首次实战成型",
        },
        "爽点兑现": {
            1: "生死开局",
            2: "顶住压迫",
            3: "看穿账局",
            4: "险中止崩",
            5: "甩尾脱身",
            6: "以技换命",
            7: "预判压场",
            8: "精准反杀",
        },
        "悬念/伏笔": {
            1: "原身为何将死",
            2: "杜横山背后人",
            3: "残功为何异常",
            4: "结构视野来源",
            5: "黑巷还有眼线",
            6: "残器藏古纹",
            7: "杜横山何时动手",
            8: "祸根未除",
        },
        "反派动作": {
            1: "债务催命",
            2: "杜横山逼债",
            3: "爪牙搜巷",
            4: "继续封路",
            5: "黑巷设卡",
            6: "杜横山放话",
            7: "暗盯住处",
            8: "首次吃瘪",
        },
        "资源/势力扩张": {
            1: "无",
            2: "无",
            3: "梳理欠账",
            4: "记下药材缺口",
            5: "发现藏身点",
            6: "换到残器/药粉",
            7: "备下陷阱材料",
            8: "夺回喘息空间",
        },
        "世界观/遗迹/远古秘密": {
            1: "边荒底层亮相",
            2: "黑巷规矩初显",
            3: "散修欠债生态",
            4: "残功/经脉负荷",
            5: "边荒生存逻辑",
            6: "灰市交换规则",
            7: "破器灵路常识",
            8: "方法可用于实战",
        },
        "姬清微线": {
            1: "未出场",
            2: "未出场",
            3: "未出场",
            4: "未出场",
            5: "未出场",
            6: "未出场",
            7: "未出场",
            8: "未出场",
        },
        "苏半夏线": {
            1: "未出场",
            2: "未出场",
            3: "未出场",
            4: "未出场",
            5: "未出场",
            6: "未出场",
            7: "未出场",
            8: "未出场",
        },
        "裴丹青线": {
            1: "未出场",
            2: "未出场",
            3: "未出场",
            4: "未出场",
            5: "未出场",
            6: "未出场",
            7: "未出场",
            8: "未出场",
        },
        "商月绮线": {
            1: "未出场",
            2: "未出场",
            3: "未出场",
            4: "未出场",
            5: "未出场",
            6: "未出场",
            7: "未出场",
            8: "未出场",
        },
        "其他女性反馈": {
            1: "底层女修惊避",
            2: "无人敢帮忙",
            3: "邻屋女修侧目",
            4: "无",
            5: "黑巷妇孺避祸",
            6: "女摊主压价",
            7: "无",
            8: "黑巷女修失神",
        },
        "核心配角成长": {
            1: "孟瘸子未出场",
            2: "杜横山立威",
            3: "孟瘸子暗察",
            4: "摸到灰线入口",
            5: "杜横山爪牙加码",
            6: "孟瘸子试探",
            7: "原身旧识观望",
            8: "杜横山威信受损",
        },
        "场景类型": {
            1: "破屋",
            2: "黑巷门口",
            3: "破屋/巷内",
            4: "破屋密室",
            5: "黑巷追逃",
            6: "灰市小摊",
            7: "废屋布置",
            8: "黑巷死角",
        },
        "章末钩子": {
            1: "今夜不解必死",
            2: "杜横山限时收命",
            3: "找到残功破口",
            4: "再试就会走火",
            5: "孟瘸子愿交易",
            6: "残器竟有古纹",
            7: "今夜设局反杀",
            8: "更大秩序注意到他",
        },
        "本章功能评价": {
            1: "爆点开局",
            2: "压迫",
            3: "铺垫",
            4: "试错/爆点",
            5: "追逃",
            6: "资源过渡",
            7: "名场面前摇",
            8: "爽点/反杀",
        },
    }
}


def col_letter(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def cell_ref(r: int, c: int) -> str:
    return f"{col_letter(c)}{r}"


def inline_cell(r: int, c: int, text: str, style: int = 0) -> str:
    t = escape(str(text))
    return f'<c r="{cell_ref(r,c)}" t="inlineStr" s="{style}"><is><t xml:space="preserve">{t}</t></is></c>'


def row_xml(r: int, cells: list[str], height: int | None = None) -> str:
    attrs = f' r="{r}"'
    if height is not None:
        attrs += f' ht="{height}" customHeight="1"'
    return f'<row{attrs}>{"".join(cells)}</row>'


def xml_header() -> str:
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'


def worksheet_xml(rows: list[str], cols_xml: str, dimension: str, merges=None, freeze: str | None = None) -> str:
    merge_xml = ''
    if merges:
        merge_xml = f'<mergeCells count="{len(merges)}">' + ''.join(f'<mergeCell ref="{m}"/>' for m in merges) + '</mergeCells>'
    if freeze:
        sheet_views = f'<sheetViews><sheetView workbookViewId="0">{freeze}</sheetView></sheetViews>'
    else:
        sheet_views = '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
    return (
        xml_header()
        + '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        + sheet_views
        + '<sheetFormatPr defaultRowHeight="20"/>'
        + cols_xml
        + f'<dimension ref="{dimension}"/>'
        + '<sheetData>' + ''.join(rows) + '</sheetData>'
        + merge_xml
        + '</worksheet>'
    )


styles_xml = xml_header() + '''
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="3">
    <font><sz val="11"/><name val="Microsoft YaHei"/><family val="2"/></font>
    <font><b/><sz val="14"/><color rgb="FFFFFFFF"/><name val="Microsoft YaHei"/><family val="2"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Microsoft YaHei"/><family val="2"/></font>
  </fonts>
  <fills count="11">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF404040"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFDE9D9"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF4CCCC"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFCE5F6"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFD9EAF7"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFD9EAD3"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE7E6E6"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border><left style="thin"><color auto="1"/></left><right style="thin"><color auto="1"/></right><top style="thin"><color auto="1"/></top><bottom style="thin"><color auto="1"/></bottom><diagonal/></border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="13">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="10" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="5" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="6" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="7" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="8" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="9" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="10" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="left" vertical="top" wrapText="1"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>
'''.strip()

worksheets = []

usage_rows = []
usage_rows.append(row_xml(1, [inline_cell(1, 1, '《修真之创世纪》剧情推进总表使用说明', 1)], 24))
usage_rows.append(row_xml(2, [inline_cell(2, 1, '这份工作簿用于“看清楚”章节推进：检查爽点、暧昧、场景变化、资源线、反派线有没有断。Markdown 大纲仍负责“写清楚”。', 3)], 36))
usage_rows.append(row_xml(4, [inline_cell(4, 1, '模块', 2), inline_cell(4, 2, '说明', 2), inline_cell(4, 3, '建议做法', 2)], 24))
usage_items = [
    ('工作表结构', '每卷一个 tab；另外保留“使用说明”“总览”两张表。', '写新卷时复制一个卷模板即可。'),
    ('列设计', 'A=分类，B=线名，C=节奏提示，D 起按章节展开。', '一章一列，按真实章节数填写；不必硬凑满 100 章。'),
    ('行设计', '每一行是一条长期要检查的线。', '主线、女性线、资源线、场景线、章末钩子都要有。'),
    ('单元格填写', '只写关键词，不写长段。', '例：打脸 / 姬清微初次关注 / 黑市交易 / 章末留悬念。'),
    ('颜色理解', '不同颜色对应不同功能区。', '红=主冲突与爽点；粉=女性与暧昧；蓝=世界观；绿=资源势力；黄=体验检查。'),
    ('检查重点', '防止某条线太久不动。', '连续 8-12 章没有爽点、没有情绪反馈、没有场景变化，就要警惕。'),
    ('本表用途', '它是“诊断仪表盘”，不是替代正文。', '先在 00-大纲 和详细卷纲里写逻辑，再在表里做可视化校验。'),
]
for idx, (a, b, c) in enumerate(usage_items, start=5):
    usage_rows.append(row_xml(idx, [inline_cell(idx, 1, a, 4), inline_cell(idx, 2, b, 12), inline_cell(idx, 3, c, 12)], 34))
usage_rows.append(row_xml(14, [inline_cell(14, 1, '推荐标签示例', 2), inline_cell(14, 2, '可直接复用', 2), inline_cell(14, 3, '含义', 2)], 24))
example_tags = [
    ('打脸 / 反杀 / 压场 / 夺势', '爽点类', '用于标记情绪兑现。'),
    ('关注 / 试探 / 嘴硬 / 互救 / 靠近', '暧昧类', '用于标记人物关系发酵。'),
    ('矿场 / 坊市 / 遗迹 / 宗门 / 战场 / 星港 / 学宫', '场景类', '用于防止空间气质单一。'),
    ('资源到账 / 拉拢人手 / 控渠道 / 定标准', '势力类', '用于体现男主“夺势”而不只是升级。'),
]
for idx, (a, b, c) in enumerate(example_tags, start=15):
    usage_rows.append(row_xml(idx, [inline_cell(idx, 1, a, 4), inline_cell(idx, 2, b, 4), inline_cell(idx, 3, c, 12)], 30))
usage_cols = '<cols><col min="1" max="1" width="18" customWidth="1"/><col min="2" max="2" width="42" customWidth="1"/><col min="3" max="3" width="44" customWidth="1"/></cols>'
usage_merges = ['A1:C1', 'A2:C2']
worksheets.append(worksheet_xml(usage_rows, usage_cols, 'A1:C18', usage_merges, '<pane ySplit="3" topLeftCell="A4" activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" activeCell="A4" sqref="A4"/>'))

ov_rows = []
ov_rows.append(row_xml(1, [inline_cell(1, 1, '前八卷总览', 1)], 24))
ov_rows.append(row_xml(2, [inline_cell(2, 1, '本页用于卷与卷之间做横向检查：卖点是否重复、女性推进是否断层、场景是否单一。', 3)], 34))
ov_headers = ['卷名', '卷定位', '核心爽点', '女性/暧昧推进', '场景关键词', '风险提醒']
ov_rows.append(row_xml(4, [inline_cell(4, i + 1, h, 2) for i, h in enumerate(ov_headers)], 24))
for r, item in enumerate(volume_meta, start=5):
    cells = [
        inline_cell(r, 1, item[0], 4),
        inline_cell(r, 2, item[1], 12),
        inline_cell(r, 3, item[2], 12),
        inline_cell(r, 4, item[3], 12),
        inline_cell(r, 5, item[4], 12),
        inline_cell(r, 6, item[5], 12),
    ]
    ov_rows.append(row_xml(r, cells, 38))
ov_cols = '<cols><col min="1" max="1" width="20" customWidth="1"/><col min="2" max="2" width="18" customWidth="1"/><col min="3" max="3" width="28" customWidth="1"/><col min="4" max="4" width="30" customWidth="1"/><col min="5" max="5" width="30" customWidth="1"/><col min="6" max="6" width="28" customWidth="1"/></cols>'
ov_merges = ['A1:F1', 'A2:F2']
worksheets.append(worksheet_xml(ov_rows, ov_cols, 'A1:F12', ov_merges, '<pane ySplit="4" topLeftCell="A5" activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" activeCell="A5" sqref="A5"/>'))

for idx, (sheet_name, positioning, highlights, female_prog, scenes, risk) in enumerate(volume_meta, start=1):
    rows = []
    title = f'{sheet_name}｜章节推进矩阵'
    subtitle = f'填写方式：每格只写关键词。优先记录“推动了什么”，而不是复述剧情。该卷定位：{positioning}。'
    rows.append(row_xml(1, [inline_cell(1, 1, title, 1)], 24))
    rows.append(row_xml(2, [inline_cell(2, 1, subtitle, 3)], 34))
    header_cells = [inline_cell(3, 1, '分类', 2), inline_cell(3, 2, '线名', 2), inline_cell(3, 3, '节奏提示', 2)]
    for c in range(1, 101):
        header_cells.append(inline_cell(3, c + 3, f'第{c}章', 2))
    rows.append(row_xml(3, header_cells, 24))

    sheet_prefill = chapter_prefill.get(sheet_name, {})
    for r_idx, (category, line_name, tip, style_idx) in enumerate(line_rows, start=4):
        cells = [inline_cell(r_idx, 1, category, style_idx), inline_cell(r_idx, 2, line_name, style_idx), inline_cell(r_idx, 3, tip, 12)]
        line_prefill = sheet_prefill.get(line_name, {})
        for chapter in range(1, 101):
            text = line_prefill.get(chapter, '')
            cells.append(inline_cell(r_idx, chapter + 3, text, 11))
        rows.append(row_xml(r_idx, cells, 28))

    memo_row = 21
    rows.append(row_xml(memo_row, [inline_cell(memo_row, 1, '本卷提醒', 2), inline_cell(memo_row, 2, '核心爽点', 2), inline_cell(memo_row, 3, '女性推进', 2), inline_cell(memo_row, 4, '场景关键词', 2), inline_cell(memo_row, 5, '风险提醒', 2)], 24))
    rows.append(row_xml(memo_row + 1, [inline_cell(memo_row + 1, 1, sheet_name, 4), inline_cell(memo_row + 1, 2, highlights, 12), inline_cell(memo_row + 1, 3, female_prog, 12), inline_cell(memo_row + 1, 4, scenes, 12), inline_cell(memo_row + 1, 5, risk, 12)], 42))
    cols = '<cols><col min="1" max="1" width="10" customWidth="1"/><col min="2" max="2" width="20" customWidth="1"/><col min="3" max="3" width="30" customWidth="1"/><col min="4" max="103" width="10" customWidth="1"/></cols>'
    merges = [f'A1:{col_letter(103)}1', f'A2:{col_letter(103)}2']
    freeze = '<pane xSplit="3" ySplit="3" topLeftCell="D4" activePane="bottomRight" state="frozen"/><selection pane="bottomRight" activeCell="D4" sqref="D4"/>'
    worksheets.append(worksheet_xml(rows, cols, f'A1:{col_letter(103)}22', merges, freeze))

sheets_xml = ''.join(f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>' for i, name in enumerate(sheet_names, start=1))
workbook_xml = xml_header() + '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><bookViews><workbookView xWindow="0" yWindow="0" windowWidth="24000" windowHeight="14000" activeTab="1"/></bookViews><sheets>' + sheets_xml + '</sheets></workbook>'
wb_rels = [f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(sheet_names) + 1)]
wb_rels.append(f'<Relationship Id="rId{len(sheet_names) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')
workbook_rels_xml = xml_header() + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(wb_rels) + '</Relationships>'
root_rels_xml = xml_header() + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'
overrides = [
    '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
    '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
]
for i in range(1, len(sheet_names) + 1):
    overrides.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
content_types_xml = xml_header() + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>' + ''.join(overrides) + '</Types>'
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
core_xml = xml_header() + f'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>剧情推进总表</dc:title><dc:creator>Claude Code</dc:creator><cp:lastModifiedBy>Claude Code</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>'
app_titles = ''.join(f'<vt:lpstr>{escape(n)}</vt:lpstr>' for n in sheet_names)
app_xml = xml_header() + f'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Claude Code</Application><HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>{len(sheet_names)}</vt:i4></vt:variant></vt:vector></HeadingPairs><TitlesOfParts><vt:vector size="{len(sheet_names)}" baseType="lpstr">{app_titles}</vt:vector></TitlesOfParts></Properties>'

with ZipFile(out_path, 'w', ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', content_types_xml)
    zf.writestr('_rels/.rels', root_rels_xml)
    zf.writestr('docProps/core.xml', core_xml)
    zf.writestr('docProps/app.xml', app_xml)
    zf.writestr('xl/workbook.xml', workbook_xml)
    zf.writestr('xl/_rels/workbook.xml.rels', workbook_rels_xml)
    zf.writestr('xl/styles.xml', styles_xml)
    for i, ws in enumerate(worksheets, start=1):
        zf.writestr(f'xl/worksheets/sheet{i}.xml', ws)

print(out_path)
print('created')
