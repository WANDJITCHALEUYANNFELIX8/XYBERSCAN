import requests

# Liste des pages sensibles à tester
SENSITIVE_PAGES = [
    "/.env",
    "/.git",
    "/.git/config",
    "/admin",
    "/admin/login",
    "/administrator",
    "/backup",
    "/backup.zip",
    "/backup.sql",
    "/config.php",
    "/config.yml",
    "/config.json",
    "/wp-admin",
    "/wp-config.php",
    "/phpmyadmin",
    "/database.sql",
    "/db.sql",
    "/passwd",
    "/etc/passwd",
    "/robots.txt",
    "/sitemap.xml",
    "/.htaccess",
    "/server-status",
    "/server-info",
    "/api/v1/users",
    "/api/users",
    "/swagger",
    "/swagger-ui.html",
    "/actuator",
    "/console",
    "/debug",
]

def check_sensitive_pages(url):

    # Nettoyer l'URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    url = url.rstrip("/")

    results = {
        "url": url,
        "found": [],        # pages trouvées (200)
        "redirected": [],   # pages qui redirigent (301/302)
        "forbidden": [],    # pages protégées (403)
        "total_tested": len(SENSITIVE_PAGES),
        "errors": []
    }

    headers = {
        "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 Chrome/120.0.0.0"
    }

    print(f"\n[*] Test de {len(SENSITIVE_PAGES)} pages sensibles sur {url}...\n")

    for page in SENSITIVE_PAGES:
        full_url = url + page
        try:
            response = requests.get(
                full_url,
                timeout=5,
                allow_redirects=False,
                headers=headers
            )

            if response.status_code == 200:
                results["found"].append({
                    "page": page,
                    "status": 200,
                    "niveau": "CRITIQUE"
                })
                print(f"  [!!!] TROUVE    {page} -> 200 OK")

            elif response.status_code in [301, 302, 307, 308]:
                results["redirected"].append({
                    "page": page,
                    "status": response.status_code,
                    "niveau": "INFO"
                })
                print(f"  [->]  REDIRECT  {page} -> {response.status_code}")

            elif response.status_code == 403:
                results["forbidden"].append({
                    "page": page,
                    "status": 403,
                    "niveau": "AVERTISSEMENT"
                })
                print(f"  [!]   INTERDIT  {page} -> 403")

        except requests.exceptions.Timeout:
            results["errors"].append(f"Timeout sur {page}")

        except requests.exceptions.ConnectionError:
            results["errors"].append(f"Connexion impossible sur {page}")

        except Exception as e:
            results["errors"].append(f"Erreur sur {page} : {str(e)}")

    print(f"\n[*] Scan terminé !")
    print(f"    Pages trouvées   : {len(results['found'])}")
    print(f"    Redirections     : {len(results['redirected'])}")
    print(f"    Interdites (403) : {len(results['forbidden'])}")

    return results