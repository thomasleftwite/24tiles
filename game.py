# game.py
# 24タイルパズルゲーム ゲームロジック

import random
import time
from constants import BOARD_SIZE, BLANK, SHUFFLE_MOVES


class Game:
    """ゲーム状態・ロジックを管理するクラス"""

    # 方向定数：(row_delta, col_delta) で空白が動く方向を表す
    # Aタイプ：矢印キーはタイルが動く方向
    # ↑キー → 空白の下のタイルが上へ → 空白は下から上方向には動かない
    #        → タイルが上へ動く = 空白は下へ移動する？
    # 正確には：↑キー → 空白の下にあるタイルを空白へ移動（タイルが上へ）
    #         タイル移動方向↑ → 空白位置から見ると row+1 のタイルが来る
    DIRECTIONS = {
        "up":    (1, 0),   # 空白の下(row+1)のタイルを上へ
        "down":  (-1, 0),  # 空白の上(row-1)のタイルを下へ
        "left":  (0, 1),   # 空白の右(col+1)のタイルを左へ
        "right": (0, -1),  # 空白の左(col-1)のタイルを右へ
    }

    def __init__(self):
        self.board: list[list[int]] = []
        self.blank_pos: tuple[int, int] = (BOARD_SIZE - 1, BOARD_SIZE - 1)
        self.moves: int = 0
        self.start_time: float | None = None
        self.elapsed_sec: float = 0.0
        self.is_cleared: bool = False
        self.hovered_pos: tuple[int, int] | None = None  # ホバー中タイル位置

        self.reset()
        self.shuffle()

    # ──────────────────────────────────────
    # 初期化・シャッフル
    # ──────────────────────────────────────

    def reset(self) -> None:
        """完成状態（1〜24、右下が空白）にリセット"""
        self.board = []
        num = 1
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                if r == BOARD_SIZE - 1 and c == BOARD_SIZE - 1:
                    row.append(BLANK)
                else:
                    row.append(num)
                    num += 1
            self.board.append(row)
        self.blank_pos = (BOARD_SIZE - 1, BOARD_SIZE - 1)
        self.moves = 0
        self.start_time = None
        self.elapsed_sec = 0.0
        self.is_cleared = False

    def shuffle(self, n: int = SHUFFLE_MOVES) -> None:
        """完成状態から n 手ランダム移動してシャッフル"""
        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
        prev_dir: str | None = None
        count = 0

        while count < n:
            dirs = list(self.DIRECTIONS.keys())
            # 直前の逆方向を除外（すぐ戻らないように）
            if prev_dir is not None:
                dirs = [d for d in dirs if d != opposite[prev_dir]]

            direction = random.choice(dirs)
            if self._do_move(direction):
                prev_dir = direction
                count += 1

        # シャッフル後はタイマー・手数をリセット
        self.moves = 0
        self.start_time = None
        self.elapsed_sec = 0.0
        self.is_cleared = False

    # ──────────────────────────────────────
    # 移動ロジック
    # ──────────────────────────────────────

    def _do_move(self, direction: str) -> bool:
        """
        指定方向にタイルを移動する（内部用）。
        Aタイプ：direction はタイルが動く方向。
        移動できた場合 True、できなかった場合 False を返す。
        """
        dr, dc = self.DIRECTIONS[direction]
        br, bc = self.blank_pos
        # 移動対象タイルの位置（空白から見て反対方向）
        tr, tc = br + dr, bc + dc

        if not (0 <= tr < BOARD_SIZE and 0 <= tc < BOARD_SIZE):
            return False  # ボード外

        # タイルと空白を入れ替え
        self.board[br][bc], self.board[tr][tc] = self.board[tr][tc], self.board[br][bc]
        self.blank_pos = (tr, tc)
        return True

    def move_by_key(self, direction: str) -> bool:
        """
        矢印キー入力によるタイル移動。
        移動できた場合は手数カウント・タイマー開始・クリア判定を行う。
        """
        if self.is_cleared:
            return False
        if self._do_move(direction):
            self._on_moved()
            return True
        return False

    def move_by_click(self, row: int, col: int) -> bool:
        """
        クリックされた位置(row, col)のタイルを空白へ移動する。
        隣接していない場合は False を返す。
        """
        if self.is_cleared:
            return False
        br, bc = self.blank_pos
        # 空白に隣接しているか（上下左右のみ）
        if (abs(row - br) == 1 and col == bc) or (row == br and abs(col - bc) == 1):
            self.board[br][bc], self.board[row][col] = self.board[row][col], self.board[br][bc]
            self.blank_pos = (row, col)
            self._on_moved()
            return True
        return False

    def _on_moved(self) -> None:
        """移動後の共通処理：タイマー開始・手数カウント・クリア判定"""
        if self.start_time is None:
            self.start_time = time.time()
        self.moves += 1
        if self.check_clear():
            self.elapsed_sec = time.time() - self.start_time
            self.is_cleared = True

    # ──────────────────────────────────────
    # クリア判定・タイマー
    # ──────────────────────────────────────

    def check_clear(self) -> bool:
        """ボードが完成状態か判定"""
        num = 1
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if r == BOARD_SIZE - 1 and c == BOARD_SIZE - 1:
                    if self.board[r][c] != BLANK:
                        return False
                else:
                    if self.board[r][c] != num:
                        return False
                    num += 1
        return True

    def get_elapsed(self) -> float:
        """現在の経過時間（秒）を返す"""
        if self.is_cleared:
            return self.elapsed_sec
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time

    @staticmethod
    def format_time(seconds: float) -> str:
        """秒数を MM:SS 形式の文字列に変換"""
        s = int(seconds)
        m = s // 60
        s = s % 60
        return f"{m:02d}:{s:02d}"

    # ──────────────────────────────────────
    # ユーティリティ
    # ──────────────────────────────────────

    def get_tile(self, row: int, col: int) -> int:
        """指定位置のタイル番号を返す（0 = 空白）"""
        return self.board[row][col]

    def is_adjacent_to_blank(self, row: int, col: int) -> bool:
        """指定位置が空白に隣接しているか"""
        br, bc = self.blank_pos
        return (abs(row - br) == 1 and col == bc) or (row == br and abs(col - bc) == 1)

    def restart(self) -> None:
        """ゲームをリスタート（シャッフルし直す）"""
        self.reset()
        self.shuffle()
