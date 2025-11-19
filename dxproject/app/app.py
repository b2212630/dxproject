from flask import Flask, render_template, request, redirect, url_for, session
import os

# Flaskオブジェクトの生成
app = Flask(__name__)
app.secret_key = os.urandom(24)  # セッション用の秘密鍵


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
            return render_template("select.html", error="プログラムを選択してください。", qr_code=session.get("qr_code", ""))
        print(f"DEBUG select POST: qr_code={session.get('qr_code', '')}, program={program}")
        return redirect(url_for("route_image", program=program))
    qr_code = request.args.get("qr_code", session.get("qr_code", ""))
    if qr_code:
        session["qr_code"] = qr_code
        print(f"DEBUG select GET: qr_code saved to session: {qr_code}")
    print(f"DEBUG select GET: session qr_code={session.get('qr_code', '')}")
    return render_template("select.html", qr_code=qr_code)


# 道順画像の表示（画像は後で配置予定。プレースホルダ表示のみ）
@app.route("/route")
def route_image():
    program = request.args.get("program", default="未選択")
    qr_code = session.get("qr_code", "")
    image_urls = []

    # デバッグ用: セッションとプログラムの値を確認
    print(f"DEBUG: qr_code={qr_code}, program={program}")
    
    # static_folderのパスを確認（デフォルトは'app/static'）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    routes_dir = os.path.join(base_dir, "static", "images", "routes")
    print(f"DEBUG: routes_dir={routes_dir}")
    print(f"DEBUG: routes_dir exists={os.path.isdir(routes_dir)}")
    
    # QRコードとプログラムの組み合わせに応じて特定の画像を表示
    image_filename = None
    
    if qr_code == "学生ホール":
        if program == "学科紹介":
            image_filename = "学生ホール-B101.png"
        elif program == "模擬講義":
            image_filename = "学生ホール-B201.png"
        elif program == "研究室見学":
            image_filename = "学生ホール-E304.png"
        elif program == "バス停":
            image_filename = "学生ホール-バス停.png"
    elif qr_code == "体育館":
        if program == "学科紹介":
            image_filename = "体育館-B101.png"
        elif program == "模擬講義":
            image_filename = "体育館-B201.png"
        elif program == "研究室見学":
            image_filename = "体育館-E304.png"
        elif program == "バス停":
            image_filename = "体育館-バス停.png"
    
    print(f"DEBUG: image_filename={image_filename}")
    
    if image_filename:
        image_path = os.path.join(routes_dir, image_filename)
        print(f"DEBUG: image_path={image_path}")
        print(f"DEBUG: image_path exists={os.path.isfile(image_path)}")
        
        if os.path.isfile(image_path):
            image_url = url_for("static", filename=f"images/routes/{image_filename}")
            image_urls.append(image_url)
            print(f"DEBUG: image_url={image_url}")
        else:
            print(f"DEBUG: 画像ファイルが見つかりません: {image_path}")
    
    # フォールバック: QRコードが設定されていない場合の既存の動作
    if not image_urls and program == "学科紹介":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        routes_dir = os.path.join(base_dir, "static", "images", "routes")
        try:
            if os.path.isdir(routes_dir):
                for name in sorted(os.listdir(routes_dir)):
                    lower = name.lower()
                    if lower.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
                        image_urls.append(url_for("static", filename=f"images/routes/{name}"))
        except Exception as e:
            # 失敗してもアプリは落とさない（テンプレート側でプレースホルダ表示）
            print(f"DEBUG: エラー発生: {e}")
            image_urls = []

    print(f"DEBUG: image_urls={image_urls}")
    return render_template("route.html", program=program, image_urls=image_urls)


if __name__ == "__main__":
    app.run(debug=True)