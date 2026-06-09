"""

OPIS:
    Ten przykład pokazuje, jak rozpoznawać dane osobowe (PII) w zbiorze dokumentów.
    Endpoint recognize_pii_entities jest dostępny tylko dla wersji API v3.1 i nowszych.

UŻYCIE:

    Przed uruchomieniem przykładu:
    1) Edytuj poniższą zmienną `endpoint` i wpisz endpoint swojego zasobu Azure Language
       (znajdziesz go w portalu Azure: zasób Language → Keys and Endpoint).
       Format: https://NAZWA-ZASOBU.cognitiveservices.azure.com/
    2) Uwierzytelnij się do zasobu poprzez "az login" - jeśli polecenie nie działa,
       zainstaluj Azure CLI, zrestartuj terminal i spróbuj ponownie.

    python recognizepiientities_pl_clean.py albo ikonką "uruchom" po wejściu w plik
    
Więcej info: 

https://aka.ms/azsdk/language/pii
https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/how-to/redact-text-pii
https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories
https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories-list
"""


def sample_recognize_pii_entities() -> None:
    # [START recognize_pii_entities]
    import os
    from azure.identity import DefaultAzureCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    endpoint = "https://YOUR-RESOURCE-NAME.cognitiveservices.azure.com/"  # zastąp nazwą swojego zasobu z portalu Azure

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=DefaultAzureCredential(),
        language = "pl"
    )
    
    
    documents = [
        """Jestem Anna Nowak.
        Mój numer telefonu to 31256032344 a PESEL 86042146381. 
        Można się ze mną skontaktować też pisząc na: anowak@microsoft.com."""
    ]


    result = text_analytics_client.recognize_pii_entities(documents)
    docs = [doc for doc in result if not doc.is_error]

    for idx, doc in enumerate(docs):
        print(f"Oryginalny tekst: {documents[idx]}")

        # Ręczna redakcja — zastępujemy gwiazdkami tylko encje z pewnością >= 60%
        text = documents[idx]
        high_confidence = sorted(
            [e for e in doc.entities if e.confidence_score >= 0.6],
            key=lambda e: e.offset,
            reverse=True
        )
        for entity in high_confidence:
            text = text[:entity.offset] + '*' * entity.length + text[entity.offset + entity.length:]
        print(f"Zredagowany tekst: {text}")

    # [END recognize_pii_entities]

    print(
        "Powyżej zanonimizowane zostały dane wrażliwe zidentyfikowane z >= 60% pewności"
    )
    low_confidence_entities = []
    for doc in docs:
        for entity in doc.entities:
            if entity.confidence_score < 0.6:
                low_confidence_entities.append(
                    f"{entity.text} ({entity.category}, pewność: {entity.confidence_score:.0%})"
                )

    if low_confidence_entities:
        print("Poza tym, zidentyfikowano następujące dane z pewnością < 60%: '{}'".format(
            "', '".join(low_confidence_entities)
        ))
    else:
        print("Nie zidentyfikowano dodatkowych danych z pewnością < 60%.")


if __name__ == '__main__':
    sample_recognize_pii_entities()


"""
Przykładowy output:

Oryginalny tekst: Jestem Anna Nowak.
        Mój numer telefonu to 31256032344 a PESEL 86042146381. 
        Można się ze mną skontaktować też pisząc na: anowak@microsoft.com.
Zredagowany tekst: Jestem **********.
        Mój numer telefonu to *********** a PESEL ***********. 
        Można się ze mną skontaktować też pisząc na: ********************.
Powyżej zanonimizowane zostały dane wrażliwe zidentyfikowane z >= 60% pewności
Nie zidentyfikowano dodatkowych danych z pewnością < 60%.
"""
