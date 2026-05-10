# constants.py
# 24タイルパズルゲーム 定数定義

# ボード設定
BOARD_SIZE = 5          # 5×5
TILE_COUNT = 24         # タイル枚数（1〜24）
BLANK = 0               # 空白マスの値

# タイルサイズ・マージン
TILE_SIZE = 100         # ピクセル
TILE_MARGIN = 6         # タイル間スペース
BOARD_OFFSET_X = 20     # ボード左端オフセット
BOARD_OFFSET_Y = 70     # ボード上端オフセット（タイトル分）

# ウィンドウサイズ
WINDOW_WIDTH  = BOARD_SIZE * (TILE_SIZE + TILE_MARGIN) + BOARD_OFFSET_X * 2 - TILE_MARGIN
WINDOW_HEIGHT = BOARD_OFFSET_Y + BOARD_SIZE * (TILE_SIZE + TILE_MARGIN) - TILE_MARGIN + 160

# FPS
FPS = 60

# シャッフル手数
SHUFFLE_MOVES = 150

# ────────────────────────────────────────
# カラーパレット（Catppuccin Mocha ベース）
# ────────────────────────────────────────
COLOR_BG          = (30, 30, 46)     # 背景（Crust）
COLOR_SURFACE     = (49, 50, 68)     # 表面（Surface0）
COLOR_TILE        = (137, 180, 250)  # タイル（Blue）
COLOR_TILE_HOVER  = (116, 199, 236)  # ホバー（Sapphire）
COLOR_TILE_TEXT   = (30, 30, 46)     # タイル上テキスト
COLOR_BLANK       = (49, 50, 68)     # 空白マス
COLOR_BLANK_BORDER= (88, 91, 112)    # 空白枠線
COLOR_BORDER      = (203, 166, 247)  # タイル枠線（Mauve）
COLOR_TITLE       = (205, 214, 244)  # タイトルテキスト
COLOR_HUD         = (166, 173, 200)  # HUD テキスト（Subtext1）
COLOR_CLEAR_BG    = (40, 42, 54)     # クリアオーバーレイ
COLOR_CLEAR_TEXT  = (166, 227, 161)  # クリアメッセージ（Green）
COLOR_RESTART_BTN = (203, 166, 247)  # リスタートボタン（Mauve）
COLOR_SHADOW      = (17, 17, 27)     # タイル影

# ────────────────────────────────────────
# フォントサイズ
# ────────────────────────────────────────
FONT_TITLE   = 28
FONT_TILE    = 36
FONT_HUD     = 22
FONT_CLEAR   = 48
FONT_SUB     = 24
