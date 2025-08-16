def recommendations_for_event(action: str, payload: dict):
    if action == "auth.login.success":
        return [{
            "kind": "engagement",
            "title": "Bem-vindo de volta! 2 ações para hoje",
            "details": {"checklist": [
                "Cobrar recebíveis vencidos via WhatsApp.",
                "Criar um combo de alto giro."
            ]}
        }]
    if action == "auth.password.reset.confirmed":
        return [{
            "kind": "onboarding",
            "title": "Senha redefinida — configure alertas",
            "details": {"tip": "Ative alertas de estoque mínimo e cobrança automática."}
        }]
    return []
