# Makefile for Mirror Monitor Project

.PHONY: setup run clean schedule

# نصب نیازمندی‌ها در یک محیط مجازی
setup:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	@echo "Setup complete. Virtual environment created."

# اجرای برنامه
run:
	./venv/bin/python monitor.py

# پاک کردن فایل‌های تولید شده
clean:
	rm -rf venv
	rm -f report.json
	@echo "Cleaned up project files."

# راهنمای اجرای ادواری (کرون جاب)
schedule:
	@echo "To run this script every hour, add the following line to your crontab (crontab -e):"
	@echo "0 * * * * cd $(shell pwd) && make run >> monitor.log 2>&1"
