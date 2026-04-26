"""
Демонстрационный скрипт для проверки функций калькулятора.
Запуск: python demo.py
"""

from app.calculator import (
    erlang_b,
    erlang_c,
    reservation_erlang_b,
    reservation_find_v_r,
    erlang_b_overload
)

def main():
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ФУНКЦИЙ КАЛЬКУЛЯТОРА ТЕЛЕТРАФИКА")
    print("=" * 60)

    # 1. Прямая задача Эрланг B
    v, a = 10, 5
    p = erlang_b(v, a)
    m = a * (1 - p)
    print(f"\n1. Эрланг B (прямая задача):")
    print(f"   v = {v}, a = {a}")
    print(f"   p = {p:.6f} ({p*100:.2f}%)")
    print(f"   m = {m:.4f}")

    # 2. Прямая задача Эрланг C
    p_wait = erlang_c(v, a)
    print(f"\n2. Эрланг C (прямая задача):")
    print(f"   v = {v}, a = {a}")
    print(f"   p_wait = {p_wait:.6f} ({p_wait*100:.2f}%)")

    # 3. Прямая задача с резервированием
    v, r, a = 12, 2, 7
    p_res, m_res = reservation_erlang_b(v, r, a)
    print(f"\n3. Резервирование (прямая задача):")
    print(f"   v = {v}, r = {r}, эффективных каналов = {v - r}")
    print(f"   a = {a}")
    print(f"   p = {p_res:.6f}")
    print(f"   m = {m_res:.4f}")

    # 4. Обратная задача 1 – подбор v и r для резервирования
    a_target = 7
    p_target = 0.01
    v_opt, r_opt = reservation_find_v_r(a_target, p_target)
    print(f"\n4. Резервирование (обратная задача 1):")
    print(f"   a = {a_target}, p_target = {p_target}")
    print(f"   Найдено: v = {v_opt}, r = {r_opt}")
    print(f"   Эффективных каналов: {v_opt - r_opt}")

    # 5. Перегрузка есть (p* > p)
    v, p_star, p_norm = 10, 0.05, 0.01
    reduction = erlang_b_overload(v, p_star, p_norm)
    print(f"\n5. Перегрузка (есть):")
    print(f"   v = {v}, p* = {p_star}, p = {p_norm}")
    if reduction < 0:
        reduction = 0.0
    print(f"   Доля выгрузки = {reduction:.2f}%")

    # 6. Перегрузка отсутствует (p* <= p)
    p_star_low = 0.008
    reduction_zero = erlang_b_overload(v, p_star_low, p_norm)
    if reduction_zero < 0 or p_star_low <= p_norm:
        reduction_zero = 0.0
    print(f"\n6. Перегрузка (отсутствует):")
    print(f"   v = {v}, p* = {p_star_low}, p = {p_norm}")
    print(f"   Доля выгрузки = {reduction_zero:.2f}%")
    print("   → Перегрузка отсутствует, выгрузка не требуется.\n")

    print("=" * 60)
    print("Демонстрация завершена.")
    print("=" * 60)

if __name__ == "__main__":
    main()