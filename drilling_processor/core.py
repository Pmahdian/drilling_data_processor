import pandas as pd
from typing import Optional, Dict, Any
from pathlib import Path
from .preprocessors.cleaners import DataCleaner
from .preprocessors.outliers import OutlierDetector
from .preprocessors.feature_engine import FeatureEngineer
from .preprocessors.quality import QualityChecker
from .utils.validators import DataValidator
from .utils.loggers import ProcessingLogger


class DrillingDataProcessor:
    def __init__(
        self,
        file_path: str,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        هسته اصلی پردازش داده‌های حفاری با قابلیت‌های:
        - بارگذاری خودکار داده‌ها
        - پیکربندی پیشرفته
        - سیستم لاگینگ یکپارچه
        
        پارامترها:
            file_path: مسیر فایل داده
            config: دیکشنری پیکربندی (اختیاری)
        """
        self.file_path = Path(file_path)
        self.config = config or {}
        self.logger = ProcessingLogger()
        self.cleaner = DataCleaner()
        self.outlier_detector = OutlierDetector()
        self.feature_engineer = FeatureEngineer()
        self.quality_checker = QualityChecker()
        self.validator = DataValidator()
        self._data = None

    @property
    def data(self) -> pd.DataFrame:
        """دسترسی به داده‌ها با property"""
        if self._data is None:
            self.load_data()
        return self._data

    def load_data(self) -> pd.DataFrame:
        """بارگذاری و اعتبارسنجی داده‌ها"""
        try:
            self.logger.log_processing_step(
                f"Loading data from {self.file_path}", "info"
            )
            self._data = pd.read_parquet(self.file_path)
            
            # بررسی مقدار `None` برای داده‌های اولیه
            if self._data is None or self._data.empty:
                raise ValueError("❌ داده اولیه برای پردازش نامعتبر است!")

            # اعتبارسنجی ساختار داده
            is_valid, msg = self.validator.validate_input_data(self._data)
            if not is_valid:
                raise ValueError(f"Data validation failed: {msg}")
                
            self.logger.log_processing_step(
                f"Successfully loaded {len(self._data)} records", "info"
            )
            return self._data
            
        except Exception as e:
            self.logger.log_processing_step(
                f"Data loading error: {str(e)}", "error"
            )
            raise

    def run_pipeline(self) -> pd.DataFrame:
        """اجرای کامل پایتلاین پردازش داده"""
        if self._data is None or self._data.empty:
            raise ValueError("❌ خطا: داده‌ای برای پردازش موجود نیست!")

        steps = [
            ('Data Cleaning', self._clean_data),
            ('Outlier Handling', self._handle_outliers),
            ('Feature Engineering', self._engineer_features),
            ('Quality Check', self._check_quality)
        ]
        
        for step_name, step_func in steps:
            try:
                self.logger.log_processing_step(
                    f"Starting {step_name}", "info"
                )
                step_func()
            except Exception as e:
                self.logger.log_processing_step(
                    f"Error in {step_name}: {str(e)}", "error"
                )
                raise
                
        return self._data

    def _clean_data(self):
        """مرحله پاک‌سازی داده‌ها"""
        if self._data is None or self._data.empty:
            raise ValueError("❌ خطا: نمی‌توان داده‌های `None` را پاک‌سازی کرد!")

        self._data = self.cleaner.handle_missing_values(
            self._data,
            strategy=self.config.get('imputation_strategy', 'median')
        )
        self._data = self.cleaner.remove_duplicates(self._data)

    def _handle_outliers(self):
        """مدیریت داده‌های پرت"""
        if self._data is None or self._data.empty:
            raise ValueError("❌ خطا: نمی‌توان داده‌های `None` را بررسی کرد!")

        if self.config.get('remove_outliers', True):
            outlier_mask = self.outlier_detector.detect(
                self._data,
                method=self.config.get('outlier_method', 'isolation_forest')
            )
            self._data = self._data[~outlier_mask]

    def _engineer_features(self):
        """مهندسی ویژگی‌های جدید"""
        if self._data is None or self._data.empty:
            raise ValueError("❌ خطا: داده‌ای برای مهندسی ویژگی‌ها موجود نیست!")

        self._data = self.feature_engineer.add_pt_ratio(self._data)
        self._data = self.feature_engineer.add_flow_efficiency(self._data)
        if self.config.get('add_formation_features', True):
            self._data = self.feature_engineer.add_formation_metrics(self._data)

    def _check_quality(self):
        """کنترل نهایی کیفیت داده‌ها"""
        if self._data is None or self._data.empty:
            raise ValueError("❌ خطا: داده‌ای برای بررسی کیفیت موجود نیست!")

        self.quality_report = self.quality_checker.generate_report(self._data)
        self.logger.log_processing_step(
            "Quality check completed", "info"
        )