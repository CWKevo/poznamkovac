# i18n (preklady/lokalizácia) - návod

V prvom rade musíš extrahovať prekladateľný text zo zdrojového kódu pomocou `generovat_messages_pot.sh`.

Potom, `novy_jazyk.sh <ISO kód>` vytvorí nový priečinok pre daný jazyk.
Tam môžeš upraviť `messages.pot` pre daný jazyk, napr.: `./preklady/<id>/LC_MESSAGES/messages.pot`.

Keď budeš hotový, zkompiluj súbor prekladu do `.mo` formátu ktorému Flask rozumie pomocou `zkompilovat_preklady.sh`.

Ak pridáš nové texty do zdrojového kódu, budeš musieť aktualizovať súbor `messages.pot` (`aktualizovat_preklady.sh`). S trochou šťastia to nerozhádže existujúce prekladové súbory (budeš musieť byť opatrný).
Pamätaj, že prekladateľné texty musia byť v zdrojovom kóde ohraničené pomocou syntaxu `_(...)` (alebo `{% trans %}...{% endtrans %}` v Jinja šablónach).

Flask-Babel dokumentácia (v angličtine): [https://flask-babel.tkte.ch](https://flask-babel.tkte.ch/)
