# drilling_data_processor
### ** پکیج پردازش داده‌های حفاری**

#### **ساختار اصلی پکیج**:

drilling_data_processor/
├── setup.py
├── requirements.txt
└── drilling_processor/
    ├── __init__.py
    ├── core.py
    ├── preprocessors/
    │   ├── __init__.py
    │   ├── cleaners.py
    │   ├── outliers.py
    │   ├── feature_engine.py
    │   └── quality.py
    ├── pipelines/
    │   ├── __init__.py
    │   └── ml_pipeline.py
    └── utils/
        ├── __init__.py
        ├── validators.py
        └── loggers.py


---

### **توضیحات فایل‌ها**:

#### **1. فایل‌های سطح ریشه**:
| فایل | توضیحات |
|------|---------|
| `setup.py` | تنظیمات اصلی پکیج شامل نام، نسخه و وابستگی‌ها |
| `requirements.txt` | لیست کتابخانه‌های مورد نیاز |

#### **2. پوشه اصلی (drilling_processor)**:
| فایل/پوشه | توضیحات |
|-----------|---------|
| `__init__.py` | فایل اولیه برای معرفی ماژول |
| `core.py` | کلاس اصلی `DrillingDataProcessor` برای مدیریت کلی پردازش |

#### **3. پوشه preprocessors**:
| فایل | توضیحات |
|------|---------|
| `cleaners.py` | کلاس `DataCleaner` برای مدیریت مقادیر گم‌شده و داده‌های نامعتبر |
| `outliers.py` | کلاس `OutlierDetector` برای شناسایی داده‌های پرت |
| `feature_engine.py` | کلاس `FeatureEngineer` برای ساخت ویژگی‌های جدید |
| `quality.py` | کلاس `QualityChecker` برای تولید گزارش کیفیت داده |

#### **4. پوشه pipelines**:
| فایل | توضیحات |
|------|---------|
| `ml_pipeline.py` | شامل تابع `build_ml_pipeline()` برای ساخت پایپ‌لاین یادگیری ماشین |

#### **5. پوشه utils**:
| فایل | توضیحات |
|------|---------|
| `validators.py` | توابع اعتبارسنجی داده‌های ورودی |
| `loggers.py` | سیستم ثبت رویدادها و خطاها |

---

### **نمونه کد تست‌ها**:
ساختار پوشه تست:

tests/
├── unit/
│   ├── test_cleaners.py
│   ├── test_outliers.py
│   └── ...
└── integration/
    ├── test_pipeline.py
    └── ...




مثال از تست cleaners:

```python
# tests/unit/test_cleaners.py
def test_missing_value_imputation():
    """تست عملکرد جایگزینی مقادیر خالی"""
    test_data = pd.DataFrame({
        'Pressure': [1500, np.nan, 3000],
        'Temperature': [80, 120, np.nan]
    })
    
    cleaner = DataCleaner()
    result = cleaner.handle_missing_values(test_data)
    assert result.isnull().sum().sum() == 0
```




### **نحوه اجرای تست‌ها**:
```bash
# اجرای تمام تست‌ها
python -m pytest tests/

# اجرای تست‌های واحد
python -m pytest tests/unit/

# اجرای تست‌های یکپارچه‌سازی
python -m pytest tests/integration/
```

---


### **نکات فنی**:
1. هر ماژول به صورت مستقل قابل توسعه است
2. تست‌ها تمام سناریوهای ممکن را پوشش می‌دهند
3. مستندات هر تابع در خود فایل‌ها موجود است
4. از آخرین استانداردهای کدنویسی پایتون پیروی می‌کند


---
✍️ Developed by **Parnian Mahdian** | [GitHub Profile](https://github.com/Pmahdian)
