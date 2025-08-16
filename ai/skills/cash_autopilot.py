def recommendations_for_event(action: str, payload: dict):
    """
    Retorna uma lista de recomendações (dicts) baseadas no evento.
    Mantém lógica simples por enquanto; expandiremos depois.
    """
    recs = []
    # Exemplo: se evento for de venda/caixa, avaliar fluxo básico
    cash_in  = float(payload.get("cash_in", 0) or 0)
    cash_out = float(payload.get("cash_out", 0) or 0)
    net = cash_in - cash_out

    if net < 0:
        recs.append({
            "kind": "cash",
            "title": "Fluxo de caixa negativo detectado",
            "details": {
                "net": net,
                "tip": "Considere ajustar preços, reduzir custos variáveis e revisar estoque de baixo giro."
            }
        })
    elif action.startswith("finance.sale."):
        recs.append({
            "kind": "engagement",
            "title": "Vendas registradas — reforce recorrência",
            "details": {
                "tip": "Sugira combos de alto giro e ofereça fidelidade simples (cartão carimbado digital)."
            }
        })
    return recs
