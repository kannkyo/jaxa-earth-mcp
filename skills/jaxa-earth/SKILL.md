---
name: jaxa-earth
description: JAXA Earth Python API (jaxa.earth.je v0.1.6) を使用した衛星観測データ（AW3D30, GSMaP, GCOM-C LST, ALOS-2 PALSAR-2等）の検索、取得、解析、並びに MCP サーバー連携・コード生成スキル。
---

# JAXA Earth Python API (jaxa.earth.je) 指導スキル

このスキルは、JAXA (宇宙航空研究開発機構) が提供する地球観測データプラットフォーム用の Python API (`jaxa.earth.je` v0.1.6) および MCP サーバー (`jaxa-earth-mcp`) を活用して、衛星データを取得・処理・解析するための標準知識と実装手順を提供します。

---

## 1. 概要とコアモジュール

`jaxa.earth.je` モジュールは主に以下の4つのクラスで構成されます：

1. **`FeatureCollection`**: GeoJSON 形式の領域データの読み込みとフィーチャ選択
2. **`ImageCollectionList`**: 衛星データコレクションおよびバンドの検索・フィルタリング
3. **`ImageCollection`**: 指定された期間、解像度、領域、バンドに基づいて衛星ラスタ画像を検索・ダウンロード
4. **`ImageProcess`**: 取得したラスタ画像の表示、空間統計量計算、差分計算、マスキング処理

---

## 2. 厳密なメソッド呼び出し順序 (Method Chaining Rule)

`ImageCollection` を使用する際は、以下の順番を守ってメソッドをチェイン接続する必要があります。順序が異なるとエラーになる場合があります。

```
ImageCollection(collection_id)
  -> filter_date([start_date, end_date])
  -> filter_resolution(resolution_meters)
  -> filter_bounds(geojson_feature)
  -> select(band_name)
  -> get_images()
```

---

## 3. 実装パターンと標準コード例

### A. 衛星画像の取得と空間統計計算
```python
from jaxa.earth import je

# 1. 領域の読み込み (GeoJSON)
geoj_path = "area.geojson"
geoj = je.FeatureCollection().read(geoj_path).select([])

# 2. 衛星ラスタ画像の検索と取得
data_out = (
    je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global")
    .filter_date(["2021-01-01T00:00:00", "2022-01-01T00:00:00"])
    .filter_resolution(20)
    .filter_bounds(geoj[0])
    .select("DSM")
    .get_images()
)

# 3. 画像表示と統計量算出
img = (
    je.ImageProcess(data_out)
    .show_images()
    .calc_spatial_stats()
    .show_spatial_stats()
)
```

### B. コレクション一覧の検索
```python
from jaxa.earth import je

# キーワードによるデータセット検索
keywords = ["LST", "_half-month"]
collections, bands = je.ImageCollectionList(ssl_verify=False).filter_name(keywords=keywords)
for c, b in zip(collections, bands):
    print(f"Collection: {c}, Band: {b}")
```

### C. 画像の差分計算とマスキング
```python
from jaxa.earth import je

# 差分計算 (refデータとの比較)
diff_proc = img_proc1.diff_images(data_out2)

# マスキング処理 (土地被覆や特定のビット値による抽出)
masked_proc = img_proc.mask_images(mask_data, method_query="values_equal", values=[1, 2])
```

---

## 4. MCP サーバー (jaxa-earth-mcp) との連携

`jaxa-earth-mcp` が有効化されている環境では、以下の MCP ツールを利用できます：

- `list_collections`: 利用可能な JAXA データセットの検索
- `get_api_documentation`: API 仕様書 (`docs.md` v0.1.6) の参照
- `generate_jaxa_python_script`: 正しいチェーン順序を持つ Python スクリプトの自動生成

---

## 5. 主要データセット一覧

| コレクション ID | データ名 | 主なバンド | 用途 |
|---|---|---|---|
| `JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global` | AW3D30 標高データ | `DSM` | 標高・地形解析 |
| `JAXA.EORC_ALOS-2.PALSAR-2.v2.1.0_global` | ALOS-2 PALSAR-2 モザイク | `HH`, `HV` | 森林・浸水・SAR解析 |
| `JAXA.EORC_GCOM-C.SGLI_LST_half-month` | GCOM-C SGLI 地表面温度 | `LST` | 地表面温度・熱島現象 |
| `JAXA.EORC_GSMaP.v8_global` | GSMaP 降水量 | `hourlyGPM` | 降水・豪雨解析 |
