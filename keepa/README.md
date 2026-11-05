# Keepa on Amazon（スマホ用）

スマホのブラウザでAmazonの商品ページを開いたとき、商品タイトルの下にKeepaの価格推移グラフとサクラチェッカーへのボタンを表示します。Keepaの専用アプリは不要です。

- `keepa-amazon.user.js` … ユーザースクリプト本体
- `index.html` … 導入ページ（インストールボタンとブックマークレットのコピー）

## 表示内容

- Keepaの価格推移グラフ（Amazon本体・新品・中古・ランキング）
- 期間切替：1ヶ月 / 3ヶ月 / 1年 / 全期間
- 「Keepaで詳しく見る」リンク（keepa.comの商品ページをブラウザで開く）
- 「サクラチェッカーで見る」ボタン（sakura-checker.jp の商品ページを開く。amazon.co.jp のみ）

## 導入

GitHub Pagesで公開した場合、`https://{ユーザー名}.github.io/my-business/keepa/` を開いて手順に従ってください。

- 方法A（自動表示）：iPhoneはSafari＋「Userscripts」アプリ、AndroidはFirefox＋Tampermonkey
- 方法B（ブックマークレット）：アプリ追加なし。商品ページでブックマークを押すと表示、もう一度押すと非表示

## 対応サイト

amazon.co.jp / .com / .co.uk / .de / .fr / .ca / .it / .es / .in / .com.mx
