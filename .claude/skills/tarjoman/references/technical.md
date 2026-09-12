# Technical & Engineering Translation Reference Guide (راهنمای ترجمه فنی، مهندسی و نرم‌افزار)

## Overview
The Technical domain profile is optimized for software engineering documentation, API references, architecture decision records (ADRs), developer guides, deployment manuals, and cloud infrastructure tutorials. Technical Persian translation demands concise imperative verbs, uncorrupted code blocks, exact command-line arguments, and clear developer ergonomics.

---

## 1. Code Fences & Inline Code Protection

Code blocks and terminal commands must remain 100% verbatim:
- **Code Fences**: All ` ```bash `, ` ```python `, ` ```json ` blocks must pass through translation without a single character or indentation change.
- **Inline Code**: Inline tokens like `` `npm install` ``, `` `--config` ``, `` `const user_id = 42;` ``, and environment variables like `` `DATABASE_URL` `` must be preserved within backticks.
- **Do not translate code identifiers**: Variable names, function names (`getUserById`), class names, or JSON keys (`"timeout_ms"`) must never be localized.

---

## 2. Concise Imperative Instructions (افعال امری و گام‌های اجرایی)

Technical documentation is procedural. English steps typically begin with imperatives (*Click*, *Configure*, *Run*, *Verify*).
In Persian technical writing, express procedural steps using clear, direct imperatives:

| English Step | Strong Technical Persian | Avoid (Verbose/Passive) |
|---|---|---|
| Run the migration script | اسکریپت مایگریشن را اجرا کنید. | عملیات اجرای اسکریپت باید صورت پذیرد. |
| Set the environment variable | متغیر محیطی را مقداردهی کنید. | اقدام به تنظیم متغیر محیطی نمایید. |
| Restart the daemon | سرویس پس‌زمینه (Daemon) را بازراه‌اندازی کنید. | دیمون باید مجدداً استارت شود. |
| Verify the endpoint response | پاسخ نقطه پایانی (Endpoint) را بررسی نمایید. | درستی پاسخ مورد سنجش قرار گیرد. |

---

## 3. Developer Terminology & Loanwords vs Persian Equivalents

In software documentation, striking the right balance between standard Academy-approved Persian terms and industry loanwords is critical for clarity:

| Technical Concept | Recommended Persian | Acceptable Industry Variant | Never Use (Confusing/Obsolete) |
|---|---|---|---|
| Framework | فریم‌ورک / چارچوب کاری | چارچوب | استخوان‌بندی |
| Repository | مخزن / ریپازیتوری | ریپو | انبارگاه داده |
| Deploy | دیپلوی کردن / مستقر ساختن | استقرار | گسیل داشتن |
| Pipeline | خط لوله | پایپ‌لاین | لوله‌کشی |
| Endpoint | نقطه پایانی | اندپوینت | تهِ خط |
| Latency | تأخیر زمان پاسخ‌دهی | لتنسی | درنگ |
| Cache | حافظه موقت / کَش | کَشینگ | انبار پنهان |
| Branch | شاخه | برنچ | انشعاب |
| Commit | ثبت تغییرات / کامیت | کامیت | متعهد شدن |

---

## 4. UI Strings & System Messages
- For UI actions: Button labels and menu actions should be enclosed in Persian quotation marks:
  - *Example*: روی دکمه «تأیید و ارسال» (Submit) کلیک کنید.
- Retain Western Latin digits (`0123456789`) in error codes (`HTTP 404`, `500 Internal Server Error`), IP addresses (`127.0.0.1`), and port numbers (`:8080`).
- Directional safety: When writing file paths (`/etc/nginx/nginx.conf`) inside Persian text, ensure they are placed within backticks or isolated so slashes do not transpose.
