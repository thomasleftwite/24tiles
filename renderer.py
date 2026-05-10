# renderer.py
# 24タイルパズルゲーム 描画処理

import pygame
import math
from constants import (
    BOARD_SIZE, TILE_SIZE, TILE_MARGIN, BOARD_OFFSET_X, BOARD_OFFSET_Y,
    WINDOW_WIDTH, WINDOW_HEIGHT, BLANK,
    COLOR_BG, COLOR_SURFACE, COLOR_TILE, COLOR_TILE_HOVER, COLOR_TILE_TEXT,
    COLOR_BLANK, COLOR_BLANK_BORDER, COLOR_BORDER,
    COLOR_TITLE, COLOR_HUD, COLOR_CLEAR_BG, COLOR_CLEAR_TEXT,
    COLOR_RESTART_BTN, COLOR_SHADOW,
    FONT_TITLE, FONT_TILE, FONT_HUD, FONT_CLEAR, FONT_SUB,
)


class Renderer:
    """pygame 描画を担当するクラス"""

    def __init__(self):
        self.font_title:  pygame.font.Font | None = None
        self.font_tile:   pygame.font.Font | None = None
        self.font_hud:    pygame.font.Font | None = None
        self.font_clear:  pygame.font.Font | None = None
        self.font_sub:    pygame.font.Font | None = None
        self._anim_tick: float = 0.0  # クリアアニメーション用

    def init_fonts(self) -> None:
        """フォント初期化（pygame.init() 後に呼ぶこと）"""
        # システムフォントで Bold を使用
        self.font_title = pygame.font.SysFont("segoeuibold,arial", FONT_TITLE, bold=True)
        self.font_tile  = pygame.font.SysFont("segoeuibold,arial", FONT_TILE,  bold=True)
        self.font_hud   = pygame.font.SysFont("segoeui,arial",     FONT_HUD)
        self.font_clear = pygame.font.SysFont("segoeuibold,arial", FONT_CLEAR, bold=True)
        self.font_sub   = pygame.font.SysFont("segoeui,arial",     FONT_SUB)

    # ──────────────────────────────────────
    # 座標変換ヘルパー
    # ──────────────────────────────────────

    @staticmethod
    def board_to_screen(row: int, col: int) -> tuple[int, int]:
        """ボード座標 → スクリーン座標（タイル左上）"""
        x = BOARD_OFFSET_X + col * (TILE_SIZE + TILE_MARGIN)
        y = BOARD_OFFSET_Y + row * (TILE_SIZE + TILE_MARGIN)
        return x, y

    @staticmethod
    def screen_to_board(px: int, py: int) -> tuple[int, int] | None:
        """スクリーン座標 → ボード座標。ボード外なら None"""
        cx = px - BOARD_OFFSET_X
        cy = py - BOARD_OFFSET_Y
        col = cx // (TILE_SIZE + TILE_MARGIN)
        row = cy // (TILE_SIZE + TILE_MARGIN)
        # マージン部分をはじく
        if cx % (TILE_SIZE + TILE_MARGIN) >= TILE_SIZE:
            return None
        if cy % (TILE_SIZE + TILE_MARGIN) >= TILE_SIZE:
            return None
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return None
        return row, col

    # ──────────────────────────────────────
    # メイン描画
    # ──────────────────────────────────────

    def draw(self, surface: pygame.Surface, game, delta: float) -> None:
        """フレームごとの全描画"""
        self._anim_tick += delta
        surface.fill(COLOR_BG)
        self._draw_title(surface)
        self._draw_board(surface, game)
        self._draw_hud(surface, game)
        if game.is_cleared:
            self._draw_clear_overlay(surface, game)

    # ──────────────────────────────────────
    # タイトル
    # ──────────────────────────────────────

    def _draw_title(self, surface: pygame.Surface) -> None:
        title_surf = self.font_title.render("24 Tiles Puzzle", True, COLOR_TITLE)
        x = (WINDOW_WIDTH - title_surf.get_width()) // 2
        y = (BOARD_OFFSET_Y - title_surf.get_height()) // 2
        surface.blit(title_surf, (x, y))

    # ──────────────────────────────────────
    # ボード・タイル
    # ──────────────────────────────────────

    def _draw_board(self, surface: pygame.Surface, game) -> None:
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = game.get_tile(r, c)
                x, y = self.board_to_screen(r, c)
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                if val == BLANK:
                    self._draw_blank(surface, rect)
                else:
                    is_hovered = game.hovered_pos == (r, c) and game.is_adjacent_to_blank(r, c)
                    self._draw_tile(surface, val, rect, is_hovered)

    def _draw_blank(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """空白マスを描画"""
        # 凹み効果：内側に暗い枠
        pygame.draw.rect(surface, COLOR_BLANK, rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_BLANK_BORDER, rect, width=2, border_radius=10)

    def _draw_tile(self, surface: pygame.Surface, number: int,
                   rect: pygame.Rect, hovered: bool) -> None:
        """数字タイルを描画"""
        # 影
        shadow_rect = rect.move(3, 4)
        pygame.draw.rect(surface, COLOR_SHADOW, shadow_rect, border_radius=10)

        # タイル本体
        color = COLOR_TILE_HOVER if hovered else COLOR_TILE
        pygame.draw.rect(surface, color, rect, border_radius=10)

        # 枠線
        pygame.draw.rect(surface, COLOR_BORDER, rect, width=2, border_radius=10)

        # ハイライト（上端に明るい線）
        hl_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width - 8, 6)
        hl_color = (min(color[0] + 60, 255), min(color[1] + 60, 255), min(color[2] + 60, 255))
        pygame.draw.rect(surface, hl_color, hl_rect, border_radius=3)

        # 数字
        text_surf = self.font_tile.render(str(number), True, COLOR_TILE_TEXT)
        tx = rect.x + (TILE_SIZE - text_surf.get_width()) // 2
        ty = rect.y + (TILE_SIZE - text_surf.get_height()) // 2
        surface.blit(text_surf, (tx, ty))

    # ──────────────────────────────────────
    # HUD（タイマー・手数）
    # ──────────────────────────────────────

    def _draw_hud(self, surface: pygame.Surface, game) -> None:
        board_bottom = BOARD_OFFSET_Y + BOARD_SIZE * (TILE_SIZE + TILE_MARGIN) - TILE_MARGIN
        hud_y = board_bottom + 20

        elapsed = game.get_elapsed()
        time_str  = f"⏱  {game.format_time(elapsed)}"
        moves_str = f"🔢  {game.moves} moves"

        time_surf  = self.font_hud.render(time_str,  True, COLOR_HUD)
        moves_surf = self.font_hud.render(moves_str, True, COLOR_HUD)

        # 左右に配置
        surface.blit(time_surf,  (BOARD_OFFSET_X, hud_y))
        mx = WINDOW_WIDTH - BOARD_OFFSET_X - moves_surf.get_width()
        surface.blit(moves_surf, (mx, hud_y))

        # 下線
        line_y = hud_y + max(time_surf.get_height(), moves_surf.get_height()) + 6
        pygame.draw.line(surface, COLOR_SURFACE,
                         (BOARD_OFFSET_X, line_y),
                         (WINDOW_WIDTH - BOARD_OFFSET_X, line_y), 2)

    # ──────────────────────────────────────
    # クリアオーバーレイ
    # ──────────────────────────────────────

    def _draw_clear_overlay(self, surface: pygame.Surface, game) -> None:
        """半透明オーバーレイ＋クリアメッセージを描画"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((17, 17, 27, 200))
        surface.blit(overlay, (0, 0))

        cy = WINDOW_HEIGHT // 2

        # ★ パルスアニメーション
        pulse = 1.0 + 0.04 * math.sin(self._anim_tick * 3.0)

        # "Congratulations!" テキスト
        msg = "Congratulations!"
        msg_surf = self.font_clear.render(msg, True, COLOR_CLEAR_TEXT)
        scaled_w = int(msg_surf.get_width() * pulse)
        scaled_h = int(msg_surf.get_height() * pulse)
        msg_scaled = pygame.transform.smoothscale(msg_surf, (scaled_w, scaled_h))
        mx = (WINDOW_WIDTH - scaled_w) // 2
        surface.blit(msg_scaled, (mx, cy - scaled_h - 30))

        # クリアタイム
        t = game.format_time(game.elapsed_sec)
        time_str = f"Time: {t}   Moves: {game.moves}"
        time_surf = self.font_sub.render(time_str, True, COLOR_HUD)
        tx = (WINDOW_WIDTH - time_surf.get_width()) // 2
        surface.blit(time_surf, (tx, cy + 10))

        # リスタートボタン
        btn_text = "[ R ]  Restart"
        btn_surf = self.font_sub.render(btn_text, True, COLOR_RESTART_BTN)
        bx = (WINDOW_WIDTH - btn_surf.get_width()) // 2
        by = cy + 60
        # ボタン背景
        btn_rect = pygame.Rect(bx - 16, by - 8,
                               btn_surf.get_width() + 32,
                               btn_surf.get_height() + 16)
        pygame.draw.rect(surface, COLOR_SURFACE, btn_rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_RESTART_BTN, btn_rect, width=2, border_radius=8)
        surface.blit(btn_surf, (bx, by))
