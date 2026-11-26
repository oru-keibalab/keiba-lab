# -*- coding: utf-8 -*-
"""ジャパンカップ2026 特集ページ生成（mile-cs-2026.html のCSSを流用）"""
import io, re, sys

SRC = 'mile-cs-2026.html'
OUT = 'japan-cup-2026.html'

src = io.open(SRC, encoding='utf-8').read()
style = src[src.index('<style>'):src.index('</style>') + len('</style>')]

TITLE = '【ジャパンカップ2026】確定枠順18頭・過去10年データ分析＆東京芝2400m攻略 | おるの重賞予想ラボ'
DESC = '2026年ジャパンカップ（G1・11/29 東京芝2400m）の確定枠順18頭を公開！枠番・馬番・騎手を1頭ずつ掲載し、外国馬6頭の枠位置、トニービンを持つ6頭、過去10年の傾向、東京芝2400mのコース攻略までまとめました。'

# (枠, 馬番, 馬名, 性齢, 斤量, 騎手, 厩舎, 外国, 短評, トニービン)
HORSES = [
    (1, 1, 'ヘデントール', '牡5', '58.0', 'T.マーカンド', '美浦・木村哲也', False,
     '父ルーラーシップ。前走京都大賞典5着、天皇賞（春）5着。長距離G1で通用したスタミナ型', True),
    (1, 2, 'コスモキュランダ', '牡5', '58.0', '丹内祐次', '美浦・加藤士津八', False,
     'ブリンカー着用。前走天皇賞（秋）9着、宝塚記念4着。自分の形に持ち込めるか', False),
    (2, 3, 'メイショウタバル', '牡5', '58.0', '武豊', '栗東・石橋守', False,
     '宝塚記念連覇。前走は凱旋門賞14着。ハナを切ってどこまで粘れるか', False),
    (2, 4, 'クロワデュノール', '牡4', '58.0', 'C.デムーロ', '栗東・斉藤崇史', False,
     '天皇賞（春）・大阪杯とG1を連勝。前走天皇賞（秋）は1番人気5着。内2枠4番から巻き返し', False),
    (3, 5, 'シェイクユアハート', '牡6', '58.0', '古川吉洋', '栗東・宮徹', False,
     '札幌記念・金鯱賞勝ち。前走天皇賞（秋）6着。父ハーツクライで東京2400mは血統的に合う', True),
    (3, 6, 'マスカレードボール', '牡4', '58.0', 'C.ルメール', '美浦・手塚貴久', False,
     '昨年2着馬。前走天皇賞（秋）は2番人気11着。今年は香港・英国と海外2戦を消化している', True),
    (4, 7, 'ファイアンクランツ', '牡4', '58.0', 'J.モレイラ', '美浦・堀宣行', False,
     '目黒記念勝ち。前走アルゼンチン共和国杯8着。父ドゥラメンテ×母父ハーツクライ', True),
    (4, 8, 'オンブズマン', '牡5', '58.0', 'W.ビュイック', '海外・J&Tゴスデン', True,
     '英チャンピオンSなどG1・5勝。初の2400mが焦点で、この一戦が引退レース', False),
    (5, 9, 'カランダガン', 'セ5', '58.0', 'M.バルザローナ', '海外・F.グラファール', True,
     '昨年の勝ち馬。前走英チャンピオンS2着。外国馬初の連覇がかかる', False),
    (5, 10, 'ミニーホーク', '牝4', '56.0', 'R.ムーア', '海外・A.オブライエン', True,
     '英チャンピオンS（F&M）1着、凱旋門賞10着。12月香港国際競走にも選出', False),
    (6, 11, 'ヴェルテンベルク', '牡6', '58.0', '横山典弘', '栗東・宮本博', False,
     '天皇賞（春）2着。前走京都大賞典7着。東京2400mは昨年12月の有馬記念以来', False),
    (6, 12, 'テアオ', '牡4', '58.0', 'L.トーレス', '海外・J.サドラー', True,
     '南米G1勝ち馬。前走は米国。米国のスピード血統で初来日', False),
    (7, 13, 'アーバンシック', '牡5', '58.0', 'A.プーシャン', '美浦・武井亮', False,
     '前走新潟記念5着。昨年天皇賞（秋）5着。父スワーヴリチャードで東京2400mに実績', True),
    (7, 14, 'タガノデュード', '牡5', '58.0', 'M.デムーロ', '栗東・宮徹', False,
     '前走天皇賞（秋）4着（14番人気）。母父ハーツクライで上がり33秒3を使った', True),
    (7, 15, 'エキサイトバイオ', '牡4', '58.0', '荻野極', '栗東・今野貞一', False,
     '菊花賞3着。前走は昨年12月の有馬記念8着で、約1年ぶりの実戦。初の2400m', False),
    (8, 16, 'ダノンデサイル', '牡5', '58.0', '戸崎圭太', '栗東・安田翔伍', False,
     '天皇賞（秋）1着。大阪杯3着・宝塚記念3着・有馬記念3着とG1で安定。8枠16番から', False),
    (8, 17, 'ゴリアット', 'セ6', '58.0', 'C.スミヨン', '海外・F.グラファール', True,
     '独オイロパ賞1着。キングジョージ5着。有馬記念を最大目標に1か月日本に滞在', False),
    (8, 18, 'エシカルダイヤモンド', 'セ6', '58.0', '坂井瑠星', '海外・W.マリンズ', True,
     '米G2 2着、BCターフ9着。ドイツ血統のスタミナ型で、高速決着は割り引き', False),
]

rows = []
for waku, num, name, seirei, kg, jockey, stable, foreign, comment, tonibin in HORSES:
    badge = '<span class="waku-badge waku-%d">%d</span>' % (waku, waku)
    fbadge = ' <span style="display:inline-block;font-size:9.5px;font-weight:800;color:#1d4ed8;background:#dbeafe;border:1px solid #bfdbfe;border-radius:4px;padding:0 4px;vertical-align:middle;">外国</span>' if foreign else ''
    tbadge = ' <span style="display:inline-block;font-size:9.5px;font-weight:800;color:#b45309;background:#fef3c7;border:1px solid #fcd34d;border-radius:4px;padding:0 4px;vertical-align:middle;">トニービン</span>' if tonibin else ''
    rows.append('''        <div class="wl-row">
          <div class="wl-head">
            <span class="waku-badge waku-{waku}">{waku}</span>
            <span class="wl-num">{num}</span>
            <span class="wl-name">{name}</span>{fbadge}{tbadge}
          </div>
          <div class="wl-sub">{seirei} {kg}kg ／ {jockey} ／ {stable}</div>
          <div class="wl-cm">{comment}</div>
        </div>'''.format(waku=waku, num=num, name=name, fbadge=fbadge, tbadge=tbadge,
                           seirei=seirei, kg=kg, jockey=jockey, stable=stable, comment=comment))

waku_list = '\n'.join(rows)

BODY = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="ジャパンカップ2026,ジャパンC予想,確定枠順,東京芝2400m,過去10年傾向,おるの重賞予想ラボ">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://oru-keibalab.github.io/keiba-lab/japan-cup-2026.html">

  <!-- Open Graph / OGP -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://oru-keibalab.github.io/keiba-lab/japan-cup-2026.html">
  <meta property="og:site_name" content="おるの重賞予想ラボ">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://oru-keibalab.github.io/keiba-lab/profile.png">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:site" content="@keiba114ne">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://oru-keibalab.github.io/keiba-lab/profile.png">

  <!-- 構造化データ (JSON-LD) -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "image": "https://oru-keibalab.github.io/keiba-lab/profile.png",
    "datePublished": "2026-11-26T15:00:00+09:00",
    "dateModified": "2026-11-26T15:00:00+09:00",
    "author": {{
      "@type": "Person",
      "name": "おる",
      "url": "https://x.com/keiba114ne"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "おるの重賞予想ラボ",
      "url": "https://oru-keibalab.github.io/keiba-lab/"
    }},
    "description": "{desc}"
  }}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
  {style}
</head>
<body>

  <!-- Header -->
  <header>
    <div class="container header-content">
      <a href="index.html" class="brand">
        <div class="brand-icon">🏇</div>
        <div>
          <span class="brand-title">おるの重賞予想ラボ</span>
          <span class="brand-sub">HYBRID KEIBA LAB</span>
        </div>
      </a>
      <a href="index.html" class="back-btn">← TOPへ戻る</a>
    </div>
  </header>

  <main class="container">

    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
      <a href="index.html">TOP</a>
      <span>&gt;</span>
      <span>ジャパンカップ2026 特集</span>
    </div>

    <!-- Hero -->
    <section class="article-hero">
      <div class="hero-tags">
        <span class="tag-g1">G1</span>
        <span class="tag-date">2026.11.29 (日) 15:40発走</span>
        <span class="tag-course">東京12R 芝2400m(左) 定量</span>
      </div>
      <h1 class="article-title">【ジャパンカップ2026】確定枠順18頭・過去10年データ分析＆東京芝2400m攻略</h1>
      <p class="article-lead">
        第46回ジャパンカップ。開催は11月29日（日）東京12R・芝2400m（左回り・Cコース2週目）、3歳以上オープン（国際）の定量戦、1着賞金5億円です。
        日本馬12頭・外国馬6頭の18頭が顔を揃え、<b>11月26日（木）14時すぎに枠番・馬番が確定</b>しました。
        このページでは確定枠順を1頭ずつ掲載し、外国馬6頭の枠位置、トニービンの血を持つ6頭、過去10年の傾向と東京芝2400mの攻略ポイントまでをまとめています。
        管理人の本命◎と勝負買い目は、最終追い切りと枠順を見たうえで追って更新します。
      </p>
    </section>

    <!-- 広告枠①: ヘッダー下 バナー枠（A8.net 320x50） -->
    <div class="ad-container">
      <span class="ad-label">SPONSORED / おすすめポイ活で馬券代GET</span>
      <div style="display:flex; justify-content:center; align-items:center; margin-top:4px;">
        <a href="https://px.a8.net/svt/ejp?a8mat=4BGGBK+2S0UEQ+3ZZC+HXSGH" rel="nofollow" style="display:inline-block; max-width:100%; overflow:hidden; border-radius:8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          <img border="0" width="320" height="50" alt="ポイ活" src="https://www22.a8.net/svt/bgt?aid=261108128168&wid=001&eno=01&mid=s00000018660003013000&mc=1" style="max-width:100%; height:auto; display:block;">
        </a>
        <img border="0" width="1" height="1" src="https://www16.a8.net/0.gif?a8mat=4BGGBK+2S0UEQ+3ZZC+HXSGH" alt="">
      </div>
    </div>

    <!-- 開催概要 -->
    <h2 class="section-title">📋 開催概要</h2>
    <article class="data-card">
      <div class="tbl-wrap">
        <table class="data-table" style="width: 100%;">
          <tbody>
            <tr><th style="width:34%;">レース名</th><td><strong>第46回 ジャパンカップ（G1）</strong></td></tr>
            <tr><th>開催日</th><td>2026年11月29日（日） 5回東京8日</td></tr>
            <tr><th>発走時刻</th><td>15時40分（東京12R）</td></tr>
            <tr><th>競馬場・コース</th><td>東京競馬場 芝2,400m（左回り・Cコース2週目）</td></tr>
            <tr><th>条件</th><td>3歳以上オープン（国際）（指定） 定量</td></tr>
            <tr><th>斤量</th><td>4歳以上 牡馬・せん馬58kg／牝馬56kg</td></tr>
            <tr><th>出走頭数</th><td><strong>18頭</strong>（日本馬12頭／外国馬6頭）</td></tr>
            <tr><th>1着本賞金</th><td>5億円（2着2億円・3着1億3,000万円）</td></tr>
            <tr><th>枠順確定</th><td>11月26日（木）14時すぎ <b style="color:#e11d48;">発表済み（枠番・馬番確定）</b></td></tr>
            <tr><th>本命◎</th><td><b style="color:#e11d48;">おるさんの本命◎待ち（枠順確定後更新）</b></td></tr>
          </tbody>
        </table>
      </div>
      <p class="note">
        ※枠順・馬番・性齢・負担重量・騎手は、11月26日（木）に確定した出馬表のとおりに1頭ずつ掲載しています。
        外国馬6頭はカクガイ（初来日）で、馬体重など当日の発表がある情報は確認でき次第追記します。
      </p>
      <p class="note-src">出典：11月26日発表の確定出馬表（東京12R 第46回ジャパンカップ）</p>
    </article>

    <!-- 確定枠順 -->
    <h2 class="section-title">🏁 確定枠順18頭（11月26日 14時すぎ発表）</h2>
    <article class="data-card">
      <p class="note" style="margin-top:0;">
        枠番・馬番順に並べています。性齢・斤量・騎手・厩舎もあわせて掲載。<b>外国</b>は海外調教馬、<b>トニービン</b>は5代血統表にトニービンの血を持つ馬です。
        印（◎○▲△☆）は管理人の本命◎が決まり次第この下の「渾身予想」に反映します。
      </p>
      <div class="waku-list">
{waku_list}
      </div>
      <p class="note-src">※枠色は1枠白・2枠黒・3枠赤・4枠青・5枠黄・6枠緑・7枠橙・8枠桃。</p>
    </article>

    <!-- 枠の並び -->
    <h2 class="section-title">🎯 枠順から見る注目ポイント</h2>

    <article class="data-card">
      <h3 class="data-card-title">① 外国馬6頭の枠位置：オンブズマンとカランダガンが隣り合う</h3>
      <ul class="point-list">
        <li><strong>オンブズマン4枠8番・カランダガン5枠9番・ミニーホーク5枠10番。</strong>欧州の上位3頭が8〜10番に固まりました。互いの動きを見ながら運べる一方、この3頭で同じ位置に集まる形になれば、折り合いと進路取りが勝負を分けます。</li>
        <li><strong>テアオは6枠12番。</strong>南米出身の4歳牡馬で、単騎で前に行けるタイプ。日本の速い流れについてこられるかが焦点です。</li>
        <li><strong>ゴリアット8枠17番・エシカルダイヤモンド8枠18番。</strong>スタミナ型の2頭がそろって外枠。道中に外々を回らされると最後の直線で甘くなる可能性があります。</li>
      </ul>
    </article>

    <article class="data-card">
      <h3 class="data-card-title">② トニービンの血を持つ6頭</h3>
      <p class="note" style="margin-top:0;">
        今年の18頭のうち、5代血統表にトニービンの血が入るのは次の6頭です（馬番順）。
      </p>
      <div class="stat-grid">
        <div class="stat-box"><div class="stat-label">1枠1番</div><div class="stat-val">ヘデントール<small>父ルーラーシップ</small></div></div>
        <div class="stat-box"><div class="stat-label">3枠5番</div><div class="stat-val">シェイクユアハート<small>父ハーツクライ</small></div></div>
        <div class="stat-box"><div class="stat-label">3枠6番</div><div class="stat-val">マスカレードボール<small>父ドゥラメンテ</small></div></div>
        <div class="stat-box"><div class="stat-label">4枠7番</div><div class="stat-val">ファイアンクランツ<small>父ドゥラメンテ×母父ハーツクライ</small></div></div>
        <div class="stat-box"><div class="stat-label">7枠13番</div><div class="stat-val">アーバンシック<small>父スワーヴリチャード</small></div></div>
        <div class="stat-box"><div class="stat-label">7枠14番</div><div class="stat-val">タガノデュード<small>母父ハーツクライ</small></div></div>
      </div>
      <p class="note">
        近年のジャパンカップはトニービンの血を持つ馬が上位を占めてきました。2023年は1〜6着を独占、2024年は1・2着、2025年は2着。
        今年は6頭が該当し、そのうち4頭（5・6・7・14番）が3〜7枠の中ほど、2頭（1・13番）が内めの枠に入っています。
      </p>
    </article>

    <article class="data-card">
      <h3 class="data-card-title">③ メイチで来る馬と、次を残す馬</h3>
      <ul class="point-list">
        <li><strong>完全メイチ：オンブズマン（4枠8番）。</strong>この一戦を最後に引退して種牡馬入りする予定。欧州年度代表馬が有終の美を狙います。</li>
        <li><strong>完全メイチ：カランダガン（5枠9番）。</strong>外国馬として史上初の連覇が最大目標。前走の英チャンピオンSは2着でした。</li>
        <li><strong>次を残す：ゴリアット（8枠17番）。</strong>陣営は最大の目標を12月27日の有馬記念と明言し、1か月日本に滞在します。</li>
        <li><strong>次を残す：ミニーホーク（5枠10番）。</strong>登録馬で唯一、12月の香港国際競走に選出されており、結果次第で香港へ向かいます。</li>
        <li><strong>日本勢は国内専念。</strong>11月25日に発表された香港国際競走の選出馬に、日本馬は1頭も入りませんでした。秋の大目標をここに据えて出し切るローテです。</li>
      </ul>
    </article>

    <article class="data-card">
      <h3 class="data-card-title">④ 日本勢の並び：内にクロワデュノール、外にダノンデサイル</h3>
      <ul class="point-list">
        <li><strong>2枠4番 クロワデュノール（C.デムーロ）。</strong>天皇賞（春）と大阪杯を制した4歳。前走の天皇賞（秋）は1番人気で5着。内目の枠からロスなく運べるか。</li>
        <li><strong>8枠16番 ダノンデサイル（戸崎圭太）。</strong>天皇賞（秋）を勝った5歳。大阪杯・宝塚記念・有馬記念とG1で3着を重ねており、外枠からどう立ち回るか。</li>
        <li><strong>3枠6番 マスカレードボール（C.ルメール）。</strong>昨年2着。今年は香港・英国と海外2戦を経ての参戦で、疲労とリズムが鍵になります。</li>
        <li><strong>2枠3番 メイショウタバル（武豊）。</strong>宝塚記念連覇の先行馬。前走は凱旋門賞14着で、ハナを切ってどこまで粘れるか。</li>
        <li><strong>7枠14番 タガノデュード（M.デムーロ）。</strong>前走の天皇賞（秋）で14番人気ながら4着。上がり33秒3を使っており、展開が向けば上位に割って入る余地があります。</li>
      </ul>
    </article>

    <!-- 過去10年 -->
    <h2 class="section-title">📊 過去10年のデータ傾向（2016〜2025年）</h2>
    <article class="data-card">
      <h3 class="data-card-title">① 1番人気の信頼が厚く、人気薄の逆襲がほとんどない</h3>
      <div class="tbl-wrap">
        <table class="data-table" style="min-width: 340px;">
          <thead>
            <tr><th>項目</th><th>数値</th></tr>
          </thead>
          <tbody>
            <tr><td>1番人気の複勝率</td><td><strong>90%</strong></td></tr>
            <tr><td>勝ち馬の最低人気</td><td>すべて5番人気以内</td></tr>
            <tr><td>10番人気以下</td><td>0-0-0-73</td></tr>
            <tr><td>最多の前走</td><td>天皇賞（秋）組 5勝</td></tr>
          </tbody>
        </table>
      </div>
      <p class="note">
        1番人気が10回中9回は3着以内。勝ち馬はすべて5番人気以内で、10番人気以下は1頭も3着に入っていません。
        相手探しは「実績上位を素直に取る」のが基本で、穴を探すなら人気の中位までが現実的です。
      </p>
    </article>

    <article class="data-card">
      <h3 class="data-card-title">② 東京芝2400m（Cコース2週目）の攻略</h3>
      <ul class="point-list">
        <li><strong>スタートは向正面の直線入口。</strong>1コーナーまでの距離が長く、テンはそれほど速くなりません。ただし2週目で内が傷み始める開催終盤で、先行馬は外めを回されるロスを見込む必要があります。</li>
        <li><strong>直線は525.9m（Aコース）で、Cコースはやや短い。</strong>上がり32〜33秒台が必須の決着で、瞬発力と持続力の両方が問われます。</li>
        <li><strong>キャリアを通じて東京2400mを使えるか。</strong>初距離のオンブズマンとエキサイトバイオは、最後の1ハロンで脚が持つかが焦点になります。</li>
        <li><strong>今年は良馬場想定。</strong>過去5年（2021〜2025）はすべて良馬場で、勝ちタイムは2分20秒3〜2分25秒5。上がり32〜33秒台を使える馬が上位に来ています。</li>
      </ul>
    </article>

    <!-- おるの渾身予想 -->
    <h2 class="section-title">👑 おるの渾身予想</h2>

    <section class="prediction-slot" id="oru-prediction" style="border:2px solid #e11d48; border-radius:16px; background:#fff; padding:18px 16px;">
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
        <span class="prediction-badge" style="background:#e11d48; color:#fff; font-size:11px; font-weight:800; padding:4px 12px; border-radius:20px;">🔥 FINAL PREDICTION</span>
        <span style="font-size:11.5px; font-weight:800; color:#b45309; background:#fef3c7; padding:3px 10px; border-radius:12px;">本命◎待ち・枠順確定版</span>
      </div>
      <div class="prediction-heading" style="font-size:17px; font-weight:900; color:#0f172a; margin-bottom:8px;">◎ おるさんの本命◎待ち（枠順確定後更新）</div>
      <p class="prediction-desc" style="font-size:12.5px; color:#475569; line-height:1.7; margin-bottom:14px;">
        枠順が確定したので、ここから最終追い切りと当日の馬場を見て本命を決めます。
        過去10年は1番人気の複勝率90%・勝ち馬はすべて5番人気以内と、上位評価の馬が素直に走るレース。
        一方で今年は外国馬6頭のレベルが高く、オンブズマン（4枠8番）とカランダガン（5枠9番）が8〜10番に並びました。
        日本勢はダノンデサイル（8枠16番）・クロワデュノール（2枠4番）・マスカレードボール（3枠6番）が軸候補で、
        トニービンの血を持つ6頭（1・5・6・7・13・14番）の取捨も今年のポイントになります。本命と買い目は追って公開します。
      </p>
      <div style="background:#f8fafc; border:1px dashed #cbd5e1; border-radius:12px; padding:13px 14px;">
        <div style="font-size:12.5px; font-weight:800; color:#0f172a; margin-bottom:6px;">🎫 勝負買い目</div>
        <div style="font-size:13px; font-weight:700; color:#64748b; line-height:1.7;">本命◎の発表と同時に公開します。</div>
      </div>
    </section>

    <!-- スケジュール -->
    <h2 class="section-title">🗓️ ジャパンカップ 今週の予定</h2>
    <div class="timeline">
      <div class="timeline-row">
        <span class="timeline-date">11/26 (木)</span>
        <span class="timeline-desc">✅14時すぎ 枠順確定（18頭・馬番確定）→ 特集ページ公開</span>
      </div>
      <div class="timeline-row">
        <span class="timeline-date">11/27 (金)</span>
        <span class="timeline-desc">最終追い切り・外国馬の調教後馬体重発表</span>
      </div>
      <div class="timeline-row">
        <span class="timeline-date">11/28 (土)</span>
        <span class="timeline-desc">前日オッズ・馬場状態の確認 → 本命◎と買い目を更新</span>
      </div>
      <div class="timeline-row">
        <span class="timeline-date">11/29 (日)</span>
        <span class="timeline-desc">15時40分 発走（東京12R）</span>
      </div>
    </div>

    <!-- 全レースナビ CTA -->
    <a href="jra.html" class="cta-box">
      <span class="cta-label">⚡ 土日72レース網羅</span>
      <div class="cta-title">中央競馬 全レースAI予想ナビを見る（無料）→</div>
      <div class="cta-desc">東京・京都の全レースで印（◎○▲△☆）・短評・3連複F＆馬連買い目を公開中。</div>
    </a>

    <!-- 他重賞リンク -->
    <h2 class="section-title">📚 過去の重賞特集</h2>
    <div class="next-cards">
      <a href="mile-cs-2026.html" class="next-card" style="border-left-color:#e11d48;">
        <div class="nc-date" style="color:#be123c;">11/22（日）京都11R</div>
        <div class="nc-name">マイルチャンピオンシップ（G1）2026 特集</div>
        <div class="nc-desc">確定枠順18頭・京都マイルの過去10年データ分析。</div>
      </a>
      <a href="elizabeth-2026.html" class="next-card" style="border-left-color:#f59e0b;">
        <div class="nc-date" style="color:#b45309;">11/15（日）京都11R</div>
        <div class="nc-name">エリザベス女王杯（G1）2026 特集</div>
        <div class="nc-desc">確定枠順・全18頭の陣営コメント・適性マトリクス・コース攻略。</div>
      </a>
      <a href="musashino-2026.html" class="next-card" style="border-left-color:#0284c7;">
        <div class="nc-date" style="color:#0369a1;">11/14（土）東京11R</div>
        <div class="nc-name">武蔵野ステークス（G3）2026 特集</div>
        <div class="nc-desc">ダート1600mの過去10年データ分析。</div>
      </a>
    </div>

    <!-- 広告枠: 楽天競馬 300x250 -->
    <div class="ad-container" style="margin: 22px auto 14px;">
      <span class="ad-label">SPONSORED / 地方競馬公式ネット投票</span>
      <div style="display:flex; justify-content:center; align-items:center; margin-top:6px;">
        <a href="https://ad2.trafficgate.net/t/r/73/1958/319727_399705" target="_blank" rel="nofollow" style="display:inline-block; max-width:100%; border-radius:12px; overflow:hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
          <img src="https://srv2.trafficgate.net/t/b/73/1958/319727_399705" alt="楽天競馬 会員登録で1000円もらえる！" style="max-width:100%; height:auto; display:block;" />
        </a>
      </div>
    </div>

    <!-- 忍者AdMax インプレッション広告枠 -->
    <div class="ad-container" style="margin: 32px 0;">
      <span class="ad-label">SPONSORED / インプレッション広告</span>
      <div style="display:flex; justify-content:center; align-items:center; margin-top:8px; min-height:100px;">
        <!-- admax -->
        <script src="https://adm.shinobi.jp/s/e95b06bd6b69ee0b778825791b1acd78"></script>
        <!-- admax -->
      </div>
    </div>

    <!-- プロフィール -->
    <div class="profile-card">
      <img src="profile.png" alt="おる" class="profile-avatar" style="width:48px; height:48px; border-radius:50%; object-fit:cover; background:#fff; border:2px solid #e2e8f0;">
      <div class="profile-info">
        <div class="profile-name">おる（おるの重賞予想ラボ）</div>
        <p class="profile-bio">競馬歴9年目・オルフェーヴルをこよなく愛する競馬ファン。独自のデータ分析とラップ指数を融合した重賞予想を発信中！</p>
        <a href="https://x.com/keiba114ne" target="_blank" rel="noopener noreferrer" class="x-follow-btn">
          𝕏 @keiba114ne をフォロー
        </a>
      </div>
    </div>

    <!-- TOPへ戻る -->
    <div class="bottom-back">
      <a href="index.html" class="btn-return">← 予想ラボ トップページへ戻る</a>
    </div>

    <!-- PR: ロケットナウ（Rocket Now）配達員登録 -->
    <div style="margin: 18px 0 20px;">
      <a href="https://rocketnowdriver.app.link/lSBps4zLl8b" target="_blank" rel="noopener noreferrer" style="display:block; text-decoration:none; background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:14px 16px; box-shadow:0 2px 8px rgba(15,23,42,0.06);">
        <span style="display:inline-block; font-size:10px; font-weight:800; letter-spacing:0.08em; color:#64748b; border:1px solid #cbd5e1; border-radius:4px; padding:1px 6px; margin-bottom:8px;">PR</span>
        <span style="display:block; font-size:13.5px; font-weight:900; line-height:1.5; color:#0f172a;">🚀 スキマ時間で軍資金づくり｜ロケットナウ（Rocket Now）配達員登録はこちら</span>
        <span style="display:block; font-size:11px; line-height:1.7; color:#475569; margin-top:6px;">配達員アプリから登録して、空いた時間に配達パートナーとして働けるフードデリバリーです。報酬・登録条件の詳細は公式サイトでご確認ください。</span>
        <span style="display:inline-block; margin-top:10px; font-size:12px; font-weight:800; color:#2563eb;">配達員登録の詳細を見る →</span>
      </a>
    </div>

    <footer>
      &copy; 2026 おるの重賞予想ラボ All Rights Reserved.
    </footer>

  </main>

</body>
</html>
'''

html = BODY.format(title=TITLE, desc=DESC, style=style, waku_list=waku_list)
io.open(OUT, 'w', encoding='utf-8').write(html)
print('wrote', OUT, len(html))
