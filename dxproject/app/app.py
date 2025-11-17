from flask import Flask, render_template, request, redirect, url_for
import os

# Flaskオブジェクトの生成
app = Flask(__name__)


# 画面遷移① 左の図: 説明 + 「読み込む」ボタン
@app.route("/")
def home():
    return render_template("index.html")


# カメラでQRコードを読み込む画面（実装は後続。UIのみ）
@app.route("/scan")
def scan():
    return render_template("scan.html")


# （QR読み込み完了後を想定）現在地とプログラム選択ボタン表示
@app.route("/select", methods=["GET", "POST"])
def select():
    if request.method == "POST":
        program = request.form.get("program")
        if not program:
            return render_template("select.html", error="プログラムを選択してください。")
        return redirect(url_for("route_image", program=program))
    return render_template("select.html")


# 道順画像の表示（画像は後で配置予定。プレースホルダ表示のみ）
@app.route("/route")
def route_image():
    program = request.args.get("program", default="未選択")
    image_urls = []

    # 「学科紹介」ボタンのとき、既存の画像を列挙して表示
    if program == "学科紹介":
        routes_dir = os.path.join(app.static_folder, "images", "routes")
        try:
            if os.path.isdir(routes_dir):
                for name in sorted(os.listdir(routes_dir)):
                    lower = name.lower()
                    if lower.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
                        image_urls.append(url_for("static", filename=f"images/routes/{name}"))
        except Exception:
            # 失敗してもアプリは落とさない（テンプレート側でプレースホルダ表示）
            image_urls = []

    return render_template("route.html", program=program, image_urls=image_urls)


if __name__ == "__main__":
    app.run(debug=True)