# 🔒 Security Policy

## 📋 Supported Versions

The following versions of Spotube Downloader receive security updates:

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | ✅ Yes             |
| 1.x     | ❌ No (end of life)|

## 🐛 Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

If you discover a security vulnerability in this project, please report it responsibly:

### 📧 How to Report

1. **Email**: Send a detailed report to [jogobonito029@gmail.com](mailto:jogobonito029@gmail.com)
2. **Subject line**: `[SECURITY] Brief description of the vulnerability`
3. **Include in your report**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)

### ⏱️ Response Timeline

- **Acknowledgement**: Within 48 hours
- **Status update**: Within 7 days
- **Fix / patch**: As soon as possible, typically within 30 days

### 🏆 Responsible Disclosure

We appreciate responsible disclosure and will:

- Acknowledge your contribution in the release notes
- Work with you to understand and fix the issue
- Notify you when the fix is released

## 🔐 Security Best Practices for Users

- Always download Spotube Downloader from the [official repository](https://github.com/Alvaro-Manzo/SPOTUBE_DOWNLOADER)
- Keep your Python dependencies up to date (`pip install -r requirements.txt --upgrade`)
- Use a virtual environment to isolate dependencies
- Do not share your Spotify credentials with anyone
- Only download playlists you have the right to download

## 📦 Dependency Security

This project uses the following key dependencies. Please report any known vulnerabilities in them:

- `spotdl` - Spotify downloader library
- `Flask` - Web framework (API mode)
- `yt-dlp` - YouTube downloader (used by spotdl)

---

Thank you for helping keep Spotube Downloader safe! 🙏
