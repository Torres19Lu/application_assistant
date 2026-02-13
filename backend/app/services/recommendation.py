"""
AI 智能推荐服务
基于相似案例分析，为用户推荐合适的院校和专业
使用多维度相似度计算 + 录取概率统计
"""
import math
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func
from app.models.case import Case
from app.models.university import University
from app.models.major import Major
from app.schemas.case import RecommendationRequest, RecommendationResult


# ============================
# 分数归一化工具
# ============================

def normalize_gpa(gpa: Optional[float], scale: float = 4.0) -> Optional[float]:
    """将 GPA 归一化到 0-1 范围"""
    if gpa is None:
        return None
    if scale == 100:
        return min(gpa / 100.0, 1.0)
    elif scale == 5.0:
        return min(gpa / 5.0, 1.0)
    else:
        return min(gpa / 4.0, 1.0)


def normalize_ielts(score: Optional[float]) -> Optional[float]:
    if score is None:
        return None
    return min(score / 9.0, 1.0)


def normalize_toefl(score: Optional[int]) -> Optional[float]:
    if score is None:
        return None
    return min(score / 120.0, 1.0)


def normalize_gre(score: Optional[int]) -> Optional[float]:
    if score is None:
        return None
    return min(score / 340.0, 1.0)


def normalize_gmat(score: Optional[int]) -> Optional[float]:
    if score is None:
        return None
    return min(score / 800.0, 1.0)


STRENGTH_MAP = {"weak": 0.3, "medium": 0.6, "strong": 1.0}


def soft_background_score(
    internship: int = 0,
    research: int = 0,
    publication: int = 0,
    work_years: float = 0.0,
    recommendation_strength: str = "medium"
) -> float:
    """软背景综合评分 0-1"""
    s = 0.0
    s += min(internship / 5.0, 1.0) * 0.25
    s += min(research / 3.0, 1.0) * 0.25
    s += min(publication / 3.0, 1.0) * 0.20
    s += min(work_years / 5.0, 1.0) * 0.15
    s += STRENGTH_MAP.get(recommendation_strength, 0.6) * 0.15
    return s


# ============================
# 相似度计算
# ============================

def compute_similarity(user_profile: dict, case: Case) -> float:
    """
    计算用户画像与历史案例之间的加权相似度 (0~1)
    维度:
      - GPA 权重 0.30
      - 语言成绩 权重 0.25
      - 研究生考试 权重 0.15
      - 软背景 权重 0.20
      - 本科背景 权重 0.10
    """
    scores: List[float] = []
    weights: List[float] = []

    # --- GPA ---
    u_gpa = normalize_gpa(user_profile.get("gpa"), user_profile.get("gpa_scale", 4.0))
    c_gpa = normalize_gpa(case.gpa, case.gpa_scale or 4.0)
    if u_gpa is not None and c_gpa is not None:
        scores.append(1.0 - abs(u_gpa - c_gpa))
        weights.append(0.30)

    # --- 语言成绩 (取较好的：IELTS or TOEFL) ---
    u_lang = normalize_ielts(user_profile.get("ielts_overall")) or normalize_toefl(user_profile.get("toefl_total"))
    c_lang = normalize_ielts(case.ielts_overall) or normalize_toefl(case.toefl_total)
    if u_lang is not None and c_lang is not None:
        scores.append(1.0 - abs(u_lang - c_lang))
        weights.append(0.25)

    # --- GRE / GMAT ---
    u_test = normalize_gre(user_profile.get("gre_total")) or normalize_gmat(user_profile.get("gmat_total"))
    c_test = normalize_gre(case.gre_total) or normalize_gmat(case.gmat_total)
    if u_test is not None and c_test is not None:
        scores.append(1.0 - abs(u_test - c_test))
        weights.append(0.15)

    # --- 软背景 ---
    u_soft = soft_background_score(
        user_profile.get("internship_count", 0),
        user_profile.get("research_count", 0),
        user_profile.get("publication_count", 0),
        user_profile.get("work_years", 0.0),
        user_profile.get("recommendation_strength", "medium"),
    )
    c_soft = soft_background_score(
        case.internship_count or 0,
        case.research_count or 0,
        case.publication_count or 0,
        case.work_years or 0.0,
        case.recommendation_strength or "medium",
    )
    scores.append(1.0 - abs(u_soft - c_soft))
    weights.append(0.20)

    # --- 本科院校匹配 ---
    u_uni = (user_profile.get("undergraduate_university_name") or "").lower().strip()
    c_uni = (case.undergraduate_university_name or "").lower().strip()
    if u_uni and c_uni:
        if u_uni == c_uni:
            scores.append(1.0)
        elif u_uni in c_uni or c_uni in u_uni:
            scores.append(0.7)
        else:
            scores.append(0.3)
    else:
        scores.append(0.5)  # 缺失则中性
    weights.append(0.10)

    if not weights:
        return 0.5

    total_weight = sum(weights)
    similarity = sum(s * w for s, w in zip(scores, weights)) / total_weight
    return similarity


# ============================
# 推荐引擎
# ============================

def generate_recommendations(
    request: RecommendationRequest,
    db: Session,
    top_k: int = 10,
    similarity_threshold: float = 0.3
) -> List[RecommendationResult]:
    """
    根据用户画像从历史案例数据库中生成院校/专业推荐
    
    算法流程:
    1. 加载所有已验证（或全部）案例
    2. 对每条案例计算与用户画像的相似度
    3. 按 (录取院校, 录取专业) 分组
    4. 对每组计算录取概率 = admitted / total（相似案例中）
    5. 按录取概率加权排序，返回 top_k
    """
    user_dict = request.model_dump()

    # 获取所有案例
    all_cases = db.query(Case).all()
    if not all_cases:
        return []

    # 计算每条案例的相似度
    case_sims: List[tuple] = []
    for case in all_cases:
        sim = compute_similarity(user_dict, case)
        if sim >= similarity_threshold:
            case_sims.append((case, sim))

    if not case_sims:
        return []

    # 按 (university_id, major_id) 分组统计
    groups: Dict[tuple, dict] = {}
    for case, sim in case_sims:
        key = (case.admitted_university_id, case.admitted_major_id)
        if key not in groups:
            groups[key] = {
                "university_id": case.admitted_university_id,
                "major_id": case.admitted_major_id,
                "total": 0,
                "admitted": 0,
                "total_sim": 0.0,
                "gpa_sum": 0.0,
                "gpa_count": 0,
                "ielts_sum": 0.0,
                "ielts_count": 0,
                "toefl_sum": 0.0,
                "toefl_count": 0,
                "gre_sum": 0.0,
                "gre_count": 0,
                "scholarship_count": 0,
            }
        g = groups[key]
        g["total"] += 1
        g["total_sim"] += sim
        if case.result == "录取":
            g["admitted"] += 1
        if case.gpa:
            g["gpa_sum"] += case.gpa
            g["gpa_count"] += 1
        if case.ielts_overall:
            g["ielts_sum"] += case.ielts_overall
            g["ielts_count"] += 1
        if case.toefl_total:
            g["toefl_sum"] += case.toefl_total
            g["toefl_count"] += 1
        if case.gre_total:
            g["gre_sum"] += case.gre_total
            g["gre_count"] += 1
        if case.scholarship and case.scholarship.strip():
            g["scholarship_count"] += 1

    # 生成推荐结果
    results: List[dict] = []
    for key, g in groups.items():
        university = db.query(University).filter(University.id == g["university_id"]).first()
        major = db.query(Major).filter(Major.id == g["major_id"]).first()
        if not university or not major:
            continue

        # 录取概率: 基于相似案例的录取比例 + 相似度加权公式
        if g["total"] > 0:
            # 基础录取率（统计）
            base_rate = g["admitted"] / g["total"]
            # 平均相似度
            avg_sim = g["total_sim"] / g["total"]
            # 综合录取概率 = 基础录取率 * 相似度修正
            # 相似度越高，概率越可信，但也稍微加成
            probability = base_rate * (0.6 + 0.4 * avg_sim)
            # 数据量越少，置信度越低 → 向50%回归
            confidence = 1 - math.exp(-g["total"] / 3.0)
            probability = probability * confidence + 0.5 * (1 - confidence)
            probability = round(probability * 100, 1)
            probability = min(probability, 99.0)
        else:
            probability = 50.0

        results.append({
            "university_id": university.id,
            "university_name": university.name,
            "major_id": major.id,
            "major_name": major.name,
            "country": university.country or "",
            "admission_probability": probability,
            "similar_cases_count": g["total"],
            "admitted_count": g["admitted"],
            "avg_gpa": round(g["gpa_sum"] / g["gpa_count"], 2) if g["gpa_count"] else None,
            "avg_ielts": round(g["ielts_sum"] / g["ielts_count"], 1) if g["ielts_count"] else None,
            "avg_toefl": round(g["toefl_sum"] / g["toefl_count"], 1) if g["toefl_count"] else None,
            "avg_gre": round(g["gre_sum"] / g["gre_count"], 1) if g["gre_count"] else None,
            "scholarship_rate": round(g["scholarship_count"] / g["total"] * 100, 1) if g["total"] else 0.0,
        })

    # 按录取概率降序排列
    results.sort(key=lambda x: x["admission_probability"], reverse=True)
    return [RecommendationResult(**r) for r in results[:top_k]]
