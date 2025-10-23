#!/usr/bin/env python3
"""Text Correction Module - OCR 오타 보정"""

from difflib import get_close_matches
import re


# 도메인 특화 사전 (차량 UI 용어)
VEHICLE_DICTIONARY = {
    # 일반 UI 용어
    "내비게이선": "내비게이션",
    "내비게이쎤": "내비게이션",
    "내비게이이선": "내비게이션",
    "블루림크": "블루링크",
    "불루림크": "블루링크",
    "끌루림크": "블루링크",
    "붙무림크": "블루링크",
    "중림": "중립",
    "끊어칭": "끊어져",
    "끊어적": "끊어져",
    "비닐번호": "비밀번호",
    "비닐번호름": "비밀번호를",
    "비닐번호지": "비밀번호를",

    # 차량 관련
    "공조": "공조",
    "라이트": "라이트",
    "라미트": "라이트",
    "시트": "시트",
    "도어": "도어",
    "창문": "창문",
    "잠금": "잠금",
    "주차": "주차",
    "운전자": "운전자",
    "보조": "보조",

    # 설정 관련
    "일반": "일반",
    "설정": "설정",
    "선정": "설정",
    "화면": "화면",
    "사운드": "사운드",
    "사운트": "사운드",
    "밝기": "밝기",
    "연결": "연결",
    "편의": "편의",
    "정보": "정보",

    # 영문
    "업": "앱",
    "Profile": "Profile",
    "OFF": "OFF",
    "ON": "ON",
}

# 추가 일반 한글 교정 사전
COMMON_CORRECTIONS = {
    "잠킴": "잠김",
    "해재": "해제",
    "해체": "해제",
    "초기와": "초기화",
    "확인한": "확인한",
}


def correct_text(text, confidence=1.0, threshold=0.8):
    """
    텍스트 오타 보정

    Args:
        text (str): 원본 텍스트
        confidence (float): OCR 신뢰도
        threshold (float): 보정을 적용할 신뢰도 임계값

    Returns:
        tuple: (보정된 텍스트, 보정 여부)
    """
    if not text or len(text.strip()) == 0:
        return text, False

    # 신뢰도가 높으면 보정 안 함
    if confidence >= threshold:
        return text, False

    original_text = text
    corrected = False

    # 1. 도메인 사전으로 정확히 매칭
    if text in VEHICLE_DICTIONARY:
        text = VEHICLE_DICTIONARY[text]
        corrected = True
    elif text in COMMON_CORRECTIONS:
        text = COMMON_CORRECTIONS[text]
        corrected = True
    else:
        # 2. 유사도 기반 매칭 (부분 문자열 포함)
        all_dict = {**VEHICLE_DICTIONARY, **COMMON_CORRECTIONS}

        # 정확도 검사: 80% 이상 유사한 단어 찾기
        matches = get_close_matches(text, all_dict.keys(), n=1, cutoff=0.8)
        if matches:
            text = all_dict[matches[0]]
            corrected = True

    return text, corrected


def correct_ocr_results(ocr_results, confidence_threshold=0.8):
    """
    OCR 결과 전체에 대해 오타 보정 수행

    Args:
        ocr_results (list): OCR 결과 [(bbox, text, confidence), ...]
        confidence_threshold (float): 보정 적용 신뢰도 임계값

    Returns:
        list: 보정된 OCR 결과와 통계
    """
    corrected_results = []
    correction_count = 0

    for bbox, text, confidence in ocr_results:
        corrected_text, was_corrected = correct_text(text, confidence, confidence_threshold)

        if was_corrected:
            correction_count += 1
            print(f"   ✓ 보정: '{text}' → '{corrected_text}' (신뢰도: {confidence:.2%})")

        corrected_results.append((bbox, corrected_text, confidence))

    return corrected_results, correction_count


def add_custom_word(original, corrected):
    """
    사용자 정의 사전에 단어 추가

    Args:
        original (str): 원본 (오타)
        corrected (str): 보정된 단어
    """
    VEHICLE_DICTIONARY[original] = corrected


def get_dictionary_stats():
    """
    사전 통계 반환

    Returns:
        dict: 사전 통계
    """
    return {
        "vehicle_terms": len(VEHICLE_DICTIONARY),
        "common_corrections": len(COMMON_CORRECTIONS),
        "total": len(VEHICLE_DICTIONARY) + len(COMMON_CORRECTIONS)
    }
