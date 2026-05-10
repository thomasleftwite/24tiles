# main.py
# 24タイルパズルゲーム エントリポイント・メインループ

import sys
import pygame
from game import Game
from renderer import Renderer
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


def main() -> None:
    pygame.init()
    pygame.display.set_caption("24 Tiles Puzzle")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock  = pygame.time.Clock()

    game     = Game()
    renderer = Renderer()
    renderer.init_fonts()

    prev_time = pygame.time.get_ticks()

    running = True
    while running:
        # ── デルタ時間計算 ──────────────────────────
        now = pygame.time.get_ticks()
        delta = (now - prev_time) / 1000.0
        prev_time = now

        # ── イベント処理 ────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                _handle_key(event, game)

            elif event.type == pygame.MOUSEMOTION:
                # ボード内ならホバー位置を更新、ボード外なら None
                game.hovered_pos = renderer.screen_to_board(event.pos[0], event.pos[1])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左クリック
                    pos = renderer.screen_to_board(event.pos[0], event.pos[1])
                    if pos is not None:
                        game.move_by_click(pos[0], pos[1])

        # ── 描画 ────────────────────────────────────
        renderer.draw(screen, game, delta)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def _handle_key(event: pygame.event.Event, game: Game) -> None:
    """キーボードイベントを処理する"""
    key = event.key

    # リスタート
    if key == pygame.K_r:
        game.restart()
        return

    # 終了
    if key == pygame.K_ESCAPE:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        return

    # 矢印キー → タイル移動（Aタイプ：キーの方向にタイルが動く）
    direction_map = {
        pygame.K_UP:    "up",
        pygame.K_DOWN:  "down",
        pygame.K_LEFT:  "left",
        pygame.K_RIGHT: "right",
        # WASD も対応
        pygame.K_w: "up",
        pygame.K_s: "down",
        pygame.K_a: "left",
        pygame.K_d: "right",
    }
    if key in direction_map:
        game.move_by_key(direction_map[key])


if __name__ == "__main__":
    main()
