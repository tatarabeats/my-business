# PromptVault - AIプロンプト集サブスク

月額課金型のプロンプト集サービスのMVPです。

## ファイル構成

```
my-business/
├── index.html    # LP（ランディングページ）
├── members.html  # 会員専用ページ
├── style.css     # スタイル
└── README.md     # このファイル
```

---

## 動かし方（スマホでもOK）

### 方法1: GitHub Pages（推奨・無料）

1. このリポジトリをGitHubにpush
2. GitHubの **Settings** → **Pages** を開く
3. **Source** で `main` ブランチを選択 → **Save**
4. 数分後、`https://{ユーザー名}.github.io/{リポジトリ名}/` でアクセス可能

### 方法2: ローカルで確認（PC）

```bash
# Python 3の場合
python -m http.server 8000

# ブラウザで http://localhost:8000 を開く
```

### 方法3: Netlify Drop（最速）

1. https://app.netlify.com/drop を開く
2. このフォルダをドラッグ＆ドロップ
3. 即座に公開URL取得

---

## 決済の設定（Stripe Payment Links）

### 手順

1. [Stripe](https://stripe.com/jp) でアカウント作成
2. **Products** → **Add Product** で商品作成
   - 名前: `PromptVault 月額プラン`
   - 価格: `¥980` / 月（recurring）
3. **Payment Links** → **Create payment link**
4. 作成したリンクを `index.html` の `#payment-link` 部分に貼り付け

```html
<!-- 変更前 -->
<a href="#payment-link" class="cta-button">

<!-- 変更後 -->
<a href="https://buy.stripe.com/xxxxx" class="cta-button">
```

---

## 会員限定ページの保護（本番用）

### 方法A: Stripe Customer Portal + リダイレクト

1. 決済完了後、会員ページURLをメールで送信（Stripe自動メール機能）
2. 会員ページURLを推測困難なものに変更（例: `members-a1b2c3d4.html`）

### 方法B: 認証サービス連携（より堅牢）

- [Memberstack](https://www.memberstack.com/) - Stripe連携あり
- [Outseta](https://www.outseta.com/) - 認証+決済+CRM

### 方法C: Netlify + Stripe連携

- Netlifyの Identity 機能 + Stripe Webhooks

---

## 今後の拡張アイデア

### 自動でコンテンツを増やす

1. **ChatGPT API でプロンプト自動生成**
   - 新しいカテゴリのプロンプトを定期生成
   - GitHub Actions で週1回自動コミット

2. **ユーザー投稿プロンプト**
   - Google Forms で募集 → 審査後追加

3. **トレンド連動**
   - 話題のAIツール用プロンプトを追加

---

## 収益シミュレーション

| 会員数 | 月額 | 月収 | 年収 |
|-------|------|------|------|
| 10人 | ¥980 | ¥9,800 | ¥117,600 |
| 50人 | ¥980 | ¥49,000 | ¥588,000 |
| 100人 | ¥980 | ¥98,000 | ¥1,176,000 |

※ Stripe手数料（3.6%）は別途

---

## ライセンス

MIT
