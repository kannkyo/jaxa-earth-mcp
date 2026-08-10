"""JAXA Earth Python API v0.1.6 リファレンスドキュメントデータベース。"""

JAXA_EARTH_DOCS_V0_1_6 = {
    "version": "0.1.6",
    "overview": (
        "このPython APIパッケージは、JAXAが保有する様々な地球観測データを活用するために開発されました。"
        "本APIを使用することで、各衛星データの仕様、センサー、解像度等を詳細に意識することなく、"
        "簡単にデータを取得し処理することができます。\n"
        "je モジュールには主に 4 つのクラスが含まれます: FeatureCollection, ImageCollectionList, "
        "ImageCollection, ImageProcess。"
    ),
    "classes": {
        "FeatureCollection": {
            "description": "ローカルコンピュータからGeoJSONデータのフィーチャコレクションを読み込み、特定フィーチャを選択します。",  # noqa
            "attributes": {
                "feature_collection": "dict: read メソッド実行後に更新されるプロパティ。デフォルトは None。"  # noqa
            },
            "methods": {
                "__init__": "FeatureCollection インスタンスの初期化。",
                "read(path: str)": "指定されたパスの GeoJSON データをフィーチャコレクションとして読み込みます。",  # noqa
                "select(keywords: list = [])": "キーワードリストに基づいてフィーチャコレクションのプロパティをフィルタリングします。"  # noqa
            },
            "example": """from jaxa.earth import je
geoj_path = "gadm36_JPN_0.geojson"
geoj = je.FeatureCollection().read(geoj_path).select([])"""
        },
        "ImageCollectionList": {
            "description": "キーワードに基づいてJAXAのコレクションカタログJSONを取得およびフィルタリングします。",
            "attributes": {
                "stac_collections": "dict: JAXA STAC APIから取得したSTACコレクション一覧。"
            },
            "methods": {
                "__init__(ssl_verify: bool = True)": "SSL検証フラグを指定して初期化。",
                "filter_name(keywords: list = [])": "キーワードでコレクションカタログをフィルタリングし、(collections, bands) を返します。"  # noqa
            },
            "example": """from jaxa.earth import je
keywords = ["LST", "_half-month"]
collections, bands = je.ImageCollectionList(ssl_verify=False).filter_name(keywords=keywords)"""
        },
        "ImageCollection": {
            "description": "日付、解像度、領域、バンドなどのクエリ条件に基づいて、JAXAの選択されたコレクションカタログJSONおよびラスタ画像を取得します。",  # noqa
            "attributes": {
                "stac_date": "filter_date 実行後の Stac クラスオブジェクト",
                "stac_ppu": "filter_resolution 実行後の Stac クラスオブジェクト",
                "stac_bounds": "filter_bounds 実行後の Stac クラスオブジェクト",
                "stac_band": "select 実行後の Stac クラスオブジェクト"
            },
            "methods": {
                "__init__(collection: str = 'JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global', stac_cog_url: str = None, ssl_verify: bool = True)": "対象コレクションIDを指定してImageCollectionを初期化。",  # noqa
                "filter_date(date: list)": "日付リスト（例: ['2021-01-01T00:00:00', '2022-01-01T00:00:00']）でフィルタリング。",  # noqa
                "filter_resolution(resolution: float)": "空間解像度（メートル単位）でフィルタリング。※最初に filter_date を呼ぶ必要があります。",  # noqa
                "filter_bounds(geojson_feature: dict)": "GeoJSONの領域でフィルタリング。※最初に filter_resolution を呼ぶ必要があります。",  # noqa
                "select(band: str = None)": "バンド名でフィルタリング。※最初に filter_bounds を呼ぶ必要があります。",  # noqa
                "get_images()": "設定されたフィルタ条件に基づいてラスタ画像データを取得。"
            },
            "example": """from jaxa.earth import je
data_out = je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global")\\
             .filter_date(["2021-01-01T00:00:00","2022-01-01T00:00:00"])\\
             .filter_resolution(20)\\
             .filter_bounds(geoj[0])\\
             .select("DSM")\\
             .get_images()"""
        },
        "ImageProcess": {
            "description": "取得したImageCollectionのデータに対して処理、可視化、空間統計量の計算を行います。",
            "attributes": {
                "raster": "画像ラスタデータオブジェクト",
                "spatial_stats": "計算された空間統計量辞書"
            },
            "methods": {
                "__init__(data_out)": "ImageCollection.get_images() の出力データで ImageProcess を初期化。",  # noqa
                "show_images()": "ラスタ画像を表示/描画します。",
                "calc_spatial_stats()": "空間統計量（平均、標準偏差、最小値、最大値など）を計算。",
                "show_spatial_stats()": "計算された空間統計量を表示します。",
                "diff_images(ref)": "参照用 ImageCollection データとの差分を計算します。",
                "mask_images(mask, method_query: str = 'values_equal', values: float = [0, 1])": "マスクデータを用いてラスタ画素をマスキングします。"  # noqa
            },
            "example": """from jaxa.earth import je
img = je.ImageProcess(data_out)\\
        .show_images()\\
        .calc_spatial_stats()\\
        .show_spatial_stats()"""
        }
    },
    "popular_collections": [
        {
            "id": "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
            "name": "ALOS World 3D - 30m (AW3D30)",
            "bands": ["DSM"],
            "description": "全世界 30m 解像度 標高データ (DSM)"
        },
        {
            "id": "JAXA.EORC_ALOS-2.PALSAR-2.v2.1.0_global",
            "name": "ALOS-2 PALSAR-2 グローバルモザイク",
            "bands": ["HH", "HV"],
            "description": "Lバンド合成開口レーダ (SAR) モザイクデータ"
        },
        {
            "id": "JAXA.EORC_GCOM-C.SGLI_LST_half-month",
            "name": "GCOM-C SGLI 地表面温度",
            "bands": ["LST"],
            "description": "半月（15日）合成 地表面温度データ"
        },
        {
            "id": "JAXA.EORC_GSMaP.v8_global",
            "name": "世界の雨分布リアルタイム (GSMaP)",
            "bands": ["hourlyGPM"],
            "description": "全球降水量推定データ"
        }
    ]
}

def get_reference_doc(class_name: str = None) -> str:
    """指定されたクラスまたは全体の公式リファレンスドキュメントを取得します。"""
    if not class_name or class_name.lower() == "all":
        output = [f"# JAXA Earth Python API ドキュメント (v{JAXA_EARTH_DOCS_V0_1_6['version']})\n"]  # noqa
        output.append(JAXA_EARTH_DOCS_V0_1_6["overview"])
        output.append("\n## 利用可能なクラス:\n")
        for cls_name, info in JAXA_EARTH_DOCS_V0_1_6["classes"].items():
            output.append(f"### `jaxa.earth.je.{cls_name}`")
            output.append(f"{info['description']}\n")
            output.append("メソッド:")
            for m, m_desc in info["methods"].items():
                output.append(f"- `{m}`: {m_desc}")
            output.append("\n使用例:")
            output.append(f"```python\n{info['example']}\n```\n")
        return "\n".join(output)
    
    cls_dict = {k.lower(): k for k in JAXA_EARTH_DOCS_V0_1_6["classes"].keys()}
    target_cls = cls_dict.get(class_name.lower())
    if target_cls:
        info = JAXA_EARTH_DOCS_V0_1_6["classes"][target_cls]
        res = [f"# クラス: `jaxa.earth.je.{target_cls}`\n", info["description"], "\n### 属性 (Attributes):"]  # noqa
        for attr, desc in info["attributes"].items():
            res.append(f"- `{attr}`: {desc}")
        res.append("\n### メソッド (Methods):")
        for m, m_desc in info["methods"].items():
            res.append(f"- `{m}`: {m_desc}")
        res.append("\n### 使用例:")
        res.append(f"```python\n{info['example']}\n```")
        return "\n".join(res)
    else:
        return f"不明なクラス名 '{class_name}' です。利用可能なクラス: {list(JAXA_EARTH_DOCS_V0_1_6['classes'].keys())}"  # noqa
