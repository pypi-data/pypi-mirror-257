from selenium import webdriver

# 启动 Chrome 浏览器
driver = webdriver.Chrome()

# 打开网页
driver.get("https://www.qq.com")

# 设置浏览器窗口大小以确保整个页面都能显示在屏幕上
driver.maximize_window()

# 截取整个页面的屏幕并保存为图片
driver.save_screenshot("screenshot.png")

# 关闭浏览器
driver.quit()
