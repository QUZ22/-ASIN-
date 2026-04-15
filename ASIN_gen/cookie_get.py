import os
import json
from playwright.sync_api import sync_playwright

# ==========================================
# 功能说明：
# 1. 本脚本用于获取并保存亚马逊全球站点的登录状态 (Cookie & LocalStorage)。
# 2. 采用 Playwright 隐身模式，注入防爬避让参数，降低验证码出现概率。
# 3. 支持全球 22 个正式站点，保存的文件可供自动化爬虫长期复用。
# ==========================================

# 亚马逊全球 22 个正式站点映射表
AMAZON_SITES = {
    "us": "https://www.amazon.com",
    "ca": "https://www.amazon.ca",
    "mx": "https://www.amazon.com.mx",
    "uk": "https://www.amazon.co.uk",
    "de": "https://www.amazon.de",
    "fr": "https://www.amazon.fr",
    "it": "https://www.amazon.it",
    "es": "https://www.amazon.es",
    "nl": "https://www.amazon.nl",
    "se": "https://www.amazon.se",
    "pl": "https://www.amazon.pl",
    "be": "https://www.amazon.com.be",
    "jp": "https://www.amazon.co.jp",
    "au": "https://www.amazon.com.au",
    "in": "https://www.amazon.in",
    "sg": "https://www.amazon.sg",
    "ae": "https://www.amazon.ae",
    "sa": "https://www.amazon.sa",
    "eg": "https://www.amazon.eg",
    "tr": "https://www.amazon.com.tr",
    "br": "https://www.amazon.com.br"
}


def run():
    print("=" * 50)
    print("🚀 Amazon Global Auth Center | 跨国登录授权中心")
    print("=" * 50)

    # 1. 用户交互：选择站点
    raw_input = input("👉 请输入要授权的国家简称 (例如 us, uk, jp): ")
    site = raw_input.lower().strip()

    if site not in AMAZON_SITES:
        print(f"❌ 错误: 暂时不支持站点 '{raw_input}'。")
        return

    base_url = AMAZON_SITES[site]
    save_path = f"auth_{site}.json"

    print(f"\n[系统信息]: 准备开启 {site.upper()} 站授权流程...")
    print(f"[目标网址]: {base_url}")

    with sync_playwright() as p:
        # 2. 浏览器初始化：注入抗检测参数
        browser = p.chromium.launch(
            headless=False,  # 必须开启有头模式以便手动登录
            args=['--disable-blink-features=AutomationControlled']
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        page = context.new_page()
        # 抹除 window.navigator.webdriver 特征
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # 3. 访问登录入口
        try:
            # 采用标准 OpenID 登录跳转逻辑
            login_url = f"{base_url}/ap/signin?openid.pape.max_auth_age=0&openid.return_to={base_url}&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
            page.goto(login_url, timeout=30000)

            # 自动兜底：如果跳转失败（404 或拦截），则回退至主页
            if "404" in page.title() or "Robot Check" in page.title():
                print("💡 快捷登录口受限，已跳转至首页，请手动点击 'Sign In'。")
                page.goto(base_url)
        except Exception as e:
            print(f"⚠️ 连接超时，正在跳转首页: {base_url}")
            page.goto(base_url)

        # 4. 操作指引面板
        print("\n" + "*" * 50)
        print(f"📡 【正在等待 {site.upper()} 站登录】")
        print("   1. 请在弹出的浏览器窗口中输入账号密码。")
        print("   2. 如遇人机验证，请手动完成。")
        print("   3. 登录成功（看到个人姓名）后，切勿关闭浏览器。")
        print("   4. 回到此命令行按【回车】键完成授权抓取。")
        print("*" * 50 + "\n")

        input(f"✅ 确认登录成功后，按回车保存 {site.upper()} 站权限 >>> ")

        # 5. 核心：保存存储状态 (Storage State)
        # 这包含了该站点下所有的 Cookie、Session 和 LocalStorage
        context.storage_state(path=save_path)

        if os.path.exists(save_path) and os.path.getsize(save_path) > 100:
            print(f"\n🎉 授权成功！文件已保存至: {os.path.abspath(save_path)}")
            print(f"🔗 后续程序只需载入该 JSON 即可跳过登录。")
        else:
            print("\n❌ 授权失败: 未能生成有效文件，请确保已正常进入首页。")

        browser.close()


if __name__ == "__main__":
    run()