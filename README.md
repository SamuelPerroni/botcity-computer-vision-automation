# botcity computer vision automation
> Bot registers invoices in the Contoso Application using data provided in a spreadsheet. <br>
> The entire interaction process was carried out using botstudio computer vision.


## 💻 Prerequisites

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- You have installed  `Python >= 3.11`
- You have a `<Windows>` machine .

## 🚀 Cloning botcity computer vision automation

To clone botcity computer vision automation, follow these steps:

Windows:

```
git clone https://github.com/SamuelPerroni/botcity-computer-vision-automation.git
```

## ☕ Using botcity computer vision automation

To use botcity computer vision automation, follow these steps:

```
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

in the contoso-invoices Folder

type: python bot.py

```

## Project Tree
```
contoso-invoices
├─ .gitignore
├─ config
│  ├─ __init__.py
│  └─ const.py
├─ data
│  ├─ input
│  │  └─ Contoso Coffee Shop Invoices.xlsx
│  └─ temp
├─ resources
│  ├─ dependencies
│  │  ├─ ContosoInvoicingStup.msi
│  │  └─ tesseract-ocr-w64-setup-5.4.0.20240606.exe
├─ workflows
│  ├─ __init__.py
│  └─ invoices_record.py
├─ bot.py
├─ build.bat
├─ build.ps1
├─ build.sh
├─ contosoFaturas.botproj
├─ README.md
└─ requirements.txt
```
