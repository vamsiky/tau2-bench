"""Deterministic unit check for the A3 (closure-eligibility) and A4 (PIN-reset
procedure) tool guards added to banking_knowledge/tools.py.

These assert the guard logic directly, independent of any stochastic LLM episode.
Run: uv run python claudedocs/a1a4_fixes/guard_unit_check.py
"""
from tau2.domains.banking_knowledge.environment import get_db
from tau2.domains.banking_knowledge.tools import KnowledgeTools


def main() -> None:
    results = []

    # ---- A3: retention writes require the two eligibility reads first ----
    t = KnowledgeTools(get_db())
    r1 = t.apply_credit_card_account_flag_6147(
        "cc_x", "u", "annual_fee_waived", "11/14/2026", "loyalty_benefit"
    )
    results.append(("A3 flag blocked before reads",
                    "Closure-eligibility checks incomplete" in r1))

    # after the two reads are recorded, the guard must NOT block (it will fail
    # later on account-not-found, which proves it passed the eligibility guard)
    t._discoverable_calls_made.update(
        {"get_user_dispute_history_7291", "get_pending_replacement_orders_5765"}
    )
    r2 = t.apply_credit_card_account_flag_6147(
        "cc_x", "u", "annual_fee_waived", "11/14/2026", "loyalty_benefit"
    )
    results.append(("A3 flag passes guard after reads",
                    "Closure-eligibility checks incomplete" not in r2))

    # statement credit with retention_offer is likewise gated
    t2 = KnowledgeTools(get_db())
    r3 = t2.apply_statement_credit_8472("u", "cc_x", 20.0, "retention_offer")
    results.append(("A3 statement-credit blocked before reads",
                    "Closure-eligibility checks incomplete" in r3))
    # a non-retention statement credit is NOT gated (must not block)
    r4 = t2.apply_statement_credit_8472("u", "cc_x", 20.0, "goodwill_adjustment")
    results.append(("A3 non-retention credit not gated",
                    "Closure-eligibility checks incomplete" not in r4))

    # ---- A4: PIN reset routed by stored security signals ----
    t3 = KnowledgeTools(get_db())
    t3.db.debit_cards.data["dbc_fraud"] = {
        "card_id": "dbc_fraud", "last_4_digits": "1111", "status": "ACTIVE",
        "fraud_alert_active": True, "pin_lock_reason": "failed_attempts",
    }
    t3.db.debit_cards.data["dbc_hold"] = {
        "card_id": "dbc_hold", "last_4_digits": "2222", "status": "ACTIVE",
        "fraud_alert_active": False, "pin_lock_reason": "security_hold",
    }
    t3.db.debit_cards.data["dbc_ok"] = {
        "card_id": "dbc_ok", "last_4_digits": "3333", "status": "ACTIVE",
        "fraud_alert_active": False, "pin_lock_reason": "failed_attempts",
    }
    rf = t3.reset_debit_card_pin_6284("dbc_fraud", "1111", "8127")
    results.append(("A4 fraud-alert card blocks PIN reset",
                    "active fraud alert" in rf))
    rh = t3.reset_debit_card_pin_6284("dbc_hold", "2222", "8127")
    results.append(("A4 security-hold card blocks PIN reset",
                    "security hold" in rh))
    rok = t3.reset_debit_card_pin_6284("dbc_ok", "3333", "8127")
    results.append(("A4 normal card allows PIN reset",
                    "active fraud alert" not in rok and "security hold" not in rok
                    and "reset" in rok.lower()))

    print("\n== A3/A4 guard unit checks ==")
    ok = True
    for name, passed in results:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    print(f"\n{'ALL PASS' if ok else 'SOME FAILED'} ({sum(p for _,p in results)}/{len(results)})")


if __name__ == "__main__":
    main()
