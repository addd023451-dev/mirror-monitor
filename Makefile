# متغیرها
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: all install run clean

# دستور پیش‌فرض وقتی کاربر فقط مینویسد make
all: install

# ایجاد محیط مجازی و نصب وابستگی‌ها
install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	@echo "🔄 Creating Virtual Environment..."
	python3 -m venv $(VENV)
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	@touch $(VENV)/bin/activate
	@echo "✓ Setup complete. Type 'make run' to execute."

# اجرای برنامه با پایتونِ داخل محیط مجازی
run: install
	$(PYTHON) src/main.py --manager pip

# پاک‌سازی فایل‌های اضافی
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "🧹 Cleaned up workspace."
