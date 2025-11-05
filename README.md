# web-scraping
A collection of Python scripts for web scraping and data extraction. Includes examples using requests, BeautifulSoup, and pandas to collect, clean, and export data from various websites. Ideal for business automation, lead generation, or competitive analysis.


### 🌐 **Sources surveillées**

Le bot collecte des informations pertinentes sur l'actualité crypto via des sources réputées et complémentaires :

- **📊 CoinGecko Research** – Analyses techniques et fondamentales
- **🧠 99Bitcoins** – Résumés éducatifs et actualité vulgarisée
- **🐋 Whalytics** – Suivi des mouvements de gros portefeuilles (whales)
- **📈 MarketWatch** – Tendances macro et impact sur les marchés crypto
- **📰 Business Insider** – Rumeurs, analyses de fonds et innovations
- **🔬 ScienceDirect** – Études universitaires sur le pump & dump
- **🔗 21Shares, ChainRumors, etc.** – Sources de niche pour analyse approfondie

---

### 🧹 **Filtrage intelligent des doublons**

> Le bot ne republie jamais un lien déjà partagé.
> 
> 
> Il utilise un fichier local `posted_articles.json` comme **mémoire persistante**.
> 
- À chaque scan, les liens détectés sont comparés à ceux déjà publiés.
- Si le lien est **nouveau**, il est automatiquement :
    - formaté en message Telegram (Markdown)
    - envoyé dans le canal configuré
    - ajouté au fichier `posted_articles.json`
- Si le lien a déjà été publié, il est ignoré.

---

### ✅ **Avantages de cette approche**

- 🧠 **Optimisation du signal** : le canal Telegram ne reçoit que de l'information fraîche, sans polluer avec du contenu redondant.
- 📁 **Mémoire persistante** : en cas d'arrêt du bot ou de redémarrage, l'historique des articles publiés est conservé.
- 🔍 **Centralisation multi-sources** : les informations issues de différents sites sont harmonisées dans un même format lisible.
