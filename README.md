# 📚 CourseTime Analyzer

**CourseTime Analyzer** is a Python-based YouTube course playlist analyzer.  
It searches YouTube for playlists matching your query, extracts all video durations, and calculates the **total study time**.

The project uses:
- **Selenium** → for YouTube automation  
- **Tkinter** → for a clean, interactive GUI  
- **webdriver-manager** → for automatic ChromeDriver handling  

---

## 🚀 Features
- Search YouTube for a course playlist by query  
- Fetch playlist title and creator  
- Display total video count  
- Calculate total duration in hours  
- Clickable playlist link inside GUI  
- Show video durations (first 15 displayed, rest summarized)  
- Clean GUI with background image  

---

## 📦 Requirements
- Python **3.9+**  
- Google Chrome (latest version)  

---

## 🔧 Installation

Clone this repository:
```bash
git clone https://github.com/SaamiAbbasKhan/CourseTime-Analyzer.git
cd CourseTime-Analyzer
```

Install dependencies:
```bash
pip install -r requirements.txt
```
Run the GUI:
```bash
python graphics.py
```

Or run in CLI mode:
```bash
python main.py
```
---

## 📂 Project Structure
```pgsql
├── main.py         # Core logic: scraping and analyzing YouTube playlists
├── graphics.py     # Tkinter GUI wrapper
├── images/         # Image assets (e.g., background, icons)
│   └── books.png
├── requirements.txt
├── README.md
├── .gitignore      # Ignored files and folders
└── LICENSE         # Open-source license

```
---
## 🎮 Usage
- Open the app (graphics.py).
- Enter your course query (e.g., "Python full course").
- Hit Run and let Selenium do the work.
- Results will appear in the GUI with clickable links.
- Or just directly run (main.py) for CLI (command line interface) approach. 

---

## ⚠️ Notes & Limitations

- YouTube changes it's structure someetimes → sometimes scraping may fail.
- If you see an unexpected error, just rerun the program.
- Requires a stable internet connection.
- Only top playlist from search results is analyzed.

---

## 🛠️ Future Enhancements
This is an open project, feel free to improve! Possible upgrades:
- Support for multiple playlists
- Export results to CSV/Excel
- Show exact course progress tracker
- Add support for other platforms (Coursera, Udemy, etc.)

---

## 🙌 Acknowledgements
Built with ❤️ using Python, Selenium, and Tkinter.

---

## 🔖 Disclaimer
This was just a fun side project, so sometimes unexpected errors may occur.
In such cases, simply rerun the program.
Contributions and feature enhancements are welcome — feel free to fork and improve! 🚀
