"""JAXA Earth Python API (jaxa.earth.je) 用 MCP サーバー。"""

import json
from typing import List, Optional

try:
    from fastmcp import FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

from jaxa_earth_mcp.docs_reference import JAXA_EARTH_DOCS_V0_1_6
from jaxa_earth_mcp.docs_reference import get_reference_doc

# FastMCP サーバーの初期化
mcp = FastMCP("jaxa-earth-mcp")


@mcp.tool()
def get_api_documentation(class_name: str = "all") -> str:
    """JAXA Earth Python API (jaxa.earth.je v0.1.6) の公式ドキュメントおよびコード例を取得します。

    Args:
        class_name: ドキュメントを取得するクラス名 ('FeatureCollection', 'ImageCollectionList', 'ImageCollection', 'ImageProcess', または 'all')。
    """
    return get_reference_doc(class_name)


@mcp.tool()
def list_collections(keywords: Optional[List[str]] = None) -> str:
    """JAXA Earth プラットフォームで利用可能な衛星データセットの一覧取得およびフィルタリングを行います。

    Args:
        keywords: コレクションをフィルタリングするためのキーワードリスト（例: ['ALOS', 'LST', 'PRISM']）。
    """
    try:
        from jaxa.earth import je
        col_list, band_list = je.ImageCollectionList(ssl_verify=False).filter_name(keywords=keywords or [])  # noqa
        res = {
            "source": "JAXA STAC Live API",
            "collections_found": len(col_list),
            "data": [{"collection": c, "band": b} for c, b in zip(col_list, band_list)]  # noqa
        }
        return json.dumps(res, indent=2, ensure_ascii=False)
    except Exception as e:
        # ライブAPI呼出失敗または jaxa.earth 未インストール時のフォールバック処理
        popular = JAXA_EARTH_DOCS_V0_1_6["popular_collections"]
        if keywords:
            filtered = [
                c for c in popular
                if any(kw.lower() in c["id"].lower() or kw.lower() in c["name"].lower() for kwstr in keywords for kw in [kwstr])  # noqa
            ]
        else:
            filtered = popular

        res = {
            "source": "Curated JAXA Earth Registry (Live API offline or fallback)",  # noqa
            "note": str(e),
            "collections": filtered
        }
        return json.dumps(res, indent=2, ensure_ascii=False)


@mcp.tool()
def generate_jaxa_python_script(
    collection: str = "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
    start_date: str = "2021-01-01T00:00:00",
    end_date: str = "2022-01-01T00:00:00",
    resolution: float = 20.0,
    geojson_path: str = "gadm36_JPN_0.geojson",
    select_band: str = "DSM",
    calc_stats: bool = True
) -> str:
    """jaxa.earth.je APIを使用して衛星データを取得・処理する実行可能なPythonスクリプトを自動生成します。

    Args:
        collection: JAXA Earth コレクションID。
        start_date: ISO 8601 形式の開始日時 (YYYY-MM-DDTHH:MM:SS)。
        end_date: ISO 8601 形式の終了日時 (YYYY-MM-DDTHH:MM:SS)。
        resolution: 空間解像度フィルタ（メートル単位）。
        geojson_path: 領域指定用 GeoJSON ファイルパス。
        select_band: 対象バンド名（例: 'DSM', 'LST', 'HH'）。
        calc_stats: 空間統計量を計算するコードを含めるかどうか。
    """
    script = f'''# 自動生成された JAXA Earth Python API スクリプト (jaxa.earth.je v0.1.6)
from jaxa.earth import je

# 1. GeoJSON から領域境界の読み込み
geoj_path = "{geojson_path}"
geoj = je.FeatureCollection().read(geoj_path).select([])

# 2. 衛星ラスタ画像コレクションの検索・取得
# メソッド呼び出し順序の規約: filter_date -> filter_resolution -> filter_bounds -> select -> get_images
data_out = (
    je.ImageCollection("{collection}")
    .filter_date(["{start_date}", "{end_date}"])
    .filter_resolution({resolution})
    .filter_bounds(geoj[0])
    .select("{select_band}")
    .get_images()
)

# 3. ラスタ画像の表示と処理
img_proc = je.ImageProcess(data_out).show_images()
'''
    if calc_stats:
        script += '''
# 4. 空間統計量（平均、標準偏差、最小値、最大値など）の計算
img_proc = img_proc.calc_spatial_stats().show_spatial_stats()
'''
    return script


@mcp.resource("jaxa://docs/api")
def api_docs_resource() -> str:
    """JAXA Earth Python API v0.1.6 完全リファレンスを提供するリソース。"""
    return get_reference_doc("all")


@mcp.resource("jaxa://collections/popular")
def popular_collections_resource() -> str:
    """主要な JAXA 衛星データセット一覧を提供するリソース。"""
    return json.dumps(JAXA_EARTH_DOCS_V0_1_6["popular_collections"], indent=2, ensure_ascii=False)  # noqa


@mcp.prompt()
def satellite_data_analysis(query: str) -> str:
    """JAXA 衛星データ解析用プロンプトテンプレートを作成します。"""
    return f"""あなたは JAXA Earth Python API (`jaxa.earth.je`) を習熟したデータサイエンティストです。
ユーザーのリクエスト: "{query}"

JAXA Earth API (v0.1.6) の規約に従った完全な Python ソリューションを提供してください:
1. `jaxa.earth.je` モジュールを使用する。
2. ImageCollection の厳密なメソッド呼び出し順序を守る:
   `ImageCollection(col).filter_date(...).filter_resolution(...).filter_bounds(...).select(...).get_images()`
3. 出力されたラスタデータを `ImageProcess` で可視化・処理する。
"""


def run_server():
    """FastMCP サーバーを実行します。"""
    mcp.run()


if __name__ == "__main__":
    run_server()
