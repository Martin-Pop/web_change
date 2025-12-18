## Funkce

- **Sledování změn**: Uživatel zadá URL a časový interval (sekundy).
- **Porovnávání**:
    1. Aplikace stáhne obsah stránky.
    2. Vybere textový obsah viditelný na obrazovce.
    3. Vytvoří **hash** tohoto textu.
    4. Porovná nový hash s předchozím uloženým stavem.
- **Statistiky**: Veškeré změny jsou okamžitě odesílány do prohlížeče pomocí **WebSocketů**.
- **Log**: Info o monitorování je ukládáno do [MonoLogger](https://github.com/Grimhandy321/MonoLogger)

---

## Spuštění

1. Naklonuj repo `git clone ...`
2. Změň direcotory `cd ..` 
2.5 Pokud chcete vytvořte venv a aktivujte ho
3. Stáhni závislosti `pip install -r requirements.txt`
4. Do `.env` napiš token který získáš upravením a spuštěním `create_user.py`
```bash
WS_TOKEN="vas token"
WS_CONNECT_ENDPOINT="wss://adresa pro monologger/ws/connect"
````
5. zapni `app.py`

---