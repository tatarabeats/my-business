#!/usr/bin/env python3
"""
Kindle Screenshot to PDF Tool
Kindleアプリの全ページをスクリーンショットしてPDFに変換するツール

使い方:
1. Kindleアプリで本を開く
2. このスクリプトを実行
3. 指示に従ってKindleウィンドウをクリック
4. 自動でスクリーンショット→ページめくりを繰り返す
5. 最後にPDFとして保存
"""

import os
import sys
import time
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

try:
    import pyautogui
    from PIL import Image
    import img2pdf
except ImportError as e:
    print(f"必要なライブラリがインストールされていません: {e}")
    print("以下のコマンドでインストールしてください:")
    print("  pip install pyautogui pillow img2pdf")
    sys.exit(1)


class KindleScreenshotToPDF:
    def __init__(
        self,
        output_dir: str = "kindle_screenshots",
        delay: float = 0.5,
        page_turn_key: str = "right",
        max_pages: int = 10000,
    ):
        """
        Args:
            output_dir: スクリーンショット保存ディレクトリ
            delay: ページめくり後の待機時間（秒）
            page_turn_key: ページめくりキー（right/left/space）
            max_pages: 最大ページ数（無限ループ防止）
        """
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.page_turn_key = page_turn_key
        self.max_pages = max_pages
        self.screenshots: list[Path] = []
        self.page_hashes: set[str] = set()

        # pyautoguiの設定
        pyautogui.FAILSAFE = True  # 画面左上にマウスを移動で緊急停止
        pyautogui.PAUSE = 0.1

    def setup_output_dir(self) -> None:
        """出力ディレクトリを作成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = self.output_dir / timestamp
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"スクリーンショット保存先: {self.output_dir}")

    def get_image_hash(self, image: Image.Image) -> str:
        """画像のハッシュを計算（重複検出用）"""
        # 画像を小さくリサイズしてハッシュ計算（高速化）
        small = image.resize((100, 100)).convert("L")
        return hashlib.md5(small.tobytes()).hexdigest()

    def capture_screenshot(self, page_num: int) -> tuple[Path | None, bool]:
        """
        スクリーンショットを撮影

        Returns:
            (保存パス, 重複かどうか)
        """
        # スクリーンショット撮影
        screenshot = pyautogui.screenshot()

        # 重複チェック
        img_hash = self.get_image_hash(screenshot)
        if img_hash in self.page_hashes:
            print(f"  ページ {page_num}: 重複検出 - 最後のページに到達しました")
            return None, True

        self.page_hashes.add(img_hash)

        # 保存
        filepath = self.output_dir / f"page_{page_num:04d}.png"
        screenshot.save(filepath, "PNG")
        self.screenshots.append(filepath)
        print(f"  ページ {page_num}: 保存完了 ({filepath.name})")

        return filepath, False

    def turn_page(self) -> None:
        """ページをめくる"""
        pyautogui.press(self.page_turn_key)
        time.sleep(self.delay)

    def wait_for_user_focus(self) -> None:
        """ユーザーがKindleウィンドウをフォーカスするのを待つ"""
        print("\n" + "=" * 50)
        print("準備手順:")
        print("1. Kindleアプリで本を開いてください")
        print("2. 本の最初のページに移動してください")
        print("3. Kindleウィンドウを最前面にしてください")
        print("4. 準備ができたらEnterキーを押してください")
        print("\n※ 緊急停止: マウスを画面左上隅に移動")
        print("=" * 50)
        input("\nEnterキーを押すと3秒後に開始します...")

        print("\n3秒後に開始します。Kindleウィンドウをクリックしてください！")
        for i in range(3, 0, -1):
            print(f"  {i}...")
            time.sleep(1)
        print("開始！\n")

    def capture_all_pages(self) -> None:
        """全ページをキャプチャ"""
        print("スクリーンショット撮影中...")

        for page_num in range(1, self.max_pages + 1):
            # スクリーンショット撮影
            filepath, is_duplicate = self.capture_screenshot(page_num)

            if is_duplicate:
                break

            # ページめくり
            self.turn_page()

        print(f"\n合計 {len(self.screenshots)} ページをキャプチャしました")

    def create_pdf(self, output_filename: str | None = None) -> Path:
        """スクリーンショットからPDFを作成"""
        if not self.screenshots:
            raise ValueError("スクリーンショットがありません")

        if output_filename is None:
            output_filename = f"kindle_book_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        output_path = self.output_dir.parent / output_filename

        print(f"\nPDF作成中: {output_path}")

        # 画像をPDFに変換
        image_paths = [str(p) for p in sorted(self.screenshots)]

        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))

        print(f"PDF作成完了: {output_path}")
        print(f"ファイルサイズ: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

        return output_path

    def cleanup_screenshots(self, keep: bool = False) -> None:
        """スクリーンショットを削除"""
        if keep:
            print(f"スクリーンショットは {self.output_dir} に保存されています")
            return

        print("スクリーンショットを削除中...")
        for filepath in self.screenshots:
            filepath.unlink()
        self.output_dir.rmdir()
        print("削除完了")

    def run(self, output_filename: str | None = None, keep_screenshots: bool = False) -> Path:
        """メイン処理を実行"""
        self.setup_output_dir()
        self.wait_for_user_focus()
        self.capture_all_pages()
        pdf_path = self.create_pdf(output_filename)
        self.cleanup_screenshots(keep=keep_screenshots)
        return pdf_path


def main():
    parser = argparse.ArgumentParser(
        description="Kindleアプリの全ページをスクリーンショットしてPDFに変換",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python kindle_to_pdf.py
  python kindle_to_pdf.py -o mybook.pdf
  python kindle_to_pdf.py --delay 1.0 --keep-screenshots
  python kindle_to_pdf.py --key left  # 右から左にめくる本の場合

注意事項:
  - 実行中はマウス・キーボードを触らないでください
  - 緊急停止するにはマウスを画面左上隅に移動してください
  - Kindleアプリは全画面表示にするとキレイなPDFが作れます
        """,
    )

    parser.add_argument("-o", "--output", type=str, help="出力PDFファイル名")
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=0.5,
        help="ページめくり後の待機時間（秒）。デフォルト: 0.5",
    )
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        default="right",
        choices=["right", "left", "space"],
        help="ページめくりキー。デフォルト: right",
    )
    parser.add_argument(
        "-m",
        "--max-pages",
        type=int,
        default=10000,
        help="最大ページ数。デフォルト: 10000",
    )
    parser.add_argument(
        "--keep-screenshots",
        action="store_true",
        help="スクリーンショットを削除せず保持",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="kindle_screenshots",
        help="スクリーンショット保存ディレクトリ。デフォルト: kindle_screenshots",
    )

    args = parser.parse_args()

    tool = KindleScreenshotToPDF(
        output_dir=args.output_dir,
        delay=args.delay,
        page_turn_key=args.key,
        max_pages=args.max_pages,
    )

    try:
        pdf_path = tool.run(
            output_filename=args.output,
            keep_screenshots=args.keep_screenshots,
        )
        print(f"\n完了！PDFファイル: {pdf_path}")
    except KeyboardInterrupt:
        print("\n\n中断されました")
        if tool.screenshots:
            print("途中までのスクリーンショットからPDFを作成しますか？ (y/n)")
            if input().lower() == "y":
                pdf_path = tool.create_pdf(args.output)
                print(f"PDFファイル: {pdf_path}")
        sys.exit(1)
    except pyautogui.FailSafeException:
        print("\n\n緊急停止しました（マウスが画面左上隅に移動）")
        if tool.screenshots:
            print("途中までのスクリーンショットからPDFを作成しますか？ (y/n)")
            if input().lower() == "y":
                pdf_path = tool.create_pdf(args.output)
                print(f"PDFファイル: {pdf_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
