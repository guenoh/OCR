# 📱 ADB Screenshot OCR with Visualization

ADB를 통해 안드로이드 기기의 스크린샷을 캡처하고, EasyOCR로 한글/영문 텍스트를 추출한 후, 결과를 시각화하는 프로젝트입니다.

## ✨ 주요 기능

- 📱 **ADB 스크린샷 캡처**: 안드로이드 기기에서 자동으로 스크린샷 캡처
- 🖼️ **이미지 전처리**: 왼쪽 크롭 및 스케일링
- 🔍 **OCR 텍스트 추출**: 한글/영문 텍스트 인식 (EasyOCR)
- 🎨 **결과 시각화**:
  - 텍스트 영역에 사각형 그리기
  - 신뢰도 기반 색상 표시 (초록/주황/빨강)
  - 한글/영문 텍스트 레이블 표시
  - 신뢰도 점수 표시

## 📁 프로젝트 구조

```
ocr/
├── src/                          # 소스 코드 모듈
│   ├── __init__.py
│   ├── adb_capture.py           # ADB 스크린샷 캡처
│   ├── image_processor.py       # 이미지 전처리
│   ├── ocr_extractor.py         # OCR 텍스트 추출
│   └── visualizer.py            # 결과 시각화
├── main.py                       # 메인 실행 파일
├── fonts/                        # 한글 폰트 (Hyundai Sans UI)
├── setup.sh                      # 설치 스크립트
├── screenshot.png                # 원본 스크린샷
├── screenshot_processed.png      # 전처리된 이미지
├── screenshot_with_ocr.png       # 시각화 결과 이미지
└── ocr_results.txt               # 텍스트 추출 결과
```

## 🚀 설치 및 실행

### 1. 환경 설정

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows

# 패키지 설치
pip install easyocr pillow
```

### 2. ADB 연결 확인

```bash
# 안드로이드 기기가 연결되어 있는지 확인
adb devices
```

### 3. 실행

```bash
# 가상환경 활성화 후 실행
source venv/bin/activate
python main.py
```

## 📊 출력 결과

프로그램 실행 시 다음 파일들이 생성됩니다:

1. **screenshot.png** - ADB로 캡처한 원본 스크린샷
2. **screenshot_processed.png** - 크롭 및 스케일링된 이미지
3. **screenshot_with_ocr.png** - OCR 결과가 시각화된 이미지
   - 초록색 사각형: 신뢰도 > 80%
   - 주황색 사각형: 신뢰도 60-80%
   - 빨간색 사각형: 신뢰도 < 60%
4. **ocr_results.txt** - 추출된 텍스트 상세 정보

## 🎨 시각화 예시

OCR 결과 이미지에는 다음 정보가 표시됩니다:
- 각 텍스트 영역을 감싸는 컬러 사각형
- 사각형 위에 표시되는 한글/영문 텍스트
- 텍스트 상단에 표시되는 신뢰도 점수 (0.00 ~ 1.00)

## ⚙️ 설정 변경

`main.py`의 설정 섹션에서 파라미터를 수정할 수 있습니다:

```python
# Configuration
CROP_LEFT = 850         # 왼쪽 크롭 픽셀 수
SCALE_FACTOR = 0.5      # 스케일 배율 (0.5 = 50%)
LANGUAGES = ['ko', 'en'] # OCR 언어 (한글, 영문)
```

## 📦 의존성

- **Python 3.9+**
- **EasyOCR** - 다국어 OCR 엔진
- **Pillow** - 이미지 처리
- **OpenCV** - 컴퓨터 비전 (EasyOCR 내부 사용)
- **PyTorch** - 딥러닝 프레임워크 (EasyOCR 내부 사용)

## 🔧 문제 해결

### ADB 연결 오류
```bash
# ADB 서버 재시작
adb kill-server
adb start-server

# 기기 재연결 확인
adb devices
```

### 폰트 오류
프로젝트는 `fonts/` 디렉토리의 Hyundai Sans UI 폰트를 사용합니다. 폰트가 없는 경우 시스템 기본 폰트를 사용합니다.

## 📝 라이선스

MIT License

## 🙋 개발자

이 프로젝트는 안드로이드 기기의 UI 텍스트를 자동으로 추출하고 분석하기 위해 개발되었습니다.
