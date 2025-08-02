import re
from datetime import datetime

def update_readme_timestamp(readme_path="README.md"):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 正規表現で最終更新日を検索し、置換
    # 例: 2025年06月23日 09:24:26 JST
    updated_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S JST")
    new_content = re.sub(r"^最終更新\n(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2} JST)", f"最終更新\n{updated_time}", content, flags=re.MULTILINE)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme_timestamp()


