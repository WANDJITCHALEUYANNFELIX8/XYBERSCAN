import json
from datetime import datetime

# Couleurs terminal
class Colors:
    RED     = "\033[91m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"

def print_banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗
╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║
 ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗██║     ███████║██╔██╗ ██║
 ██╔██╗   ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██║     ██╔══██║██║╚██╗██║
██╔╝ ██╗   ██║   ██████╔╝███████╗██║  ██║███████║╚██████╗██║  ██║██║ ╚████║
╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Colors.RESET}
{Colors.BLUE}        Votre scanner de vulnérabilités web — by Xyberclan{Colors.RESET}
""")

def print_separator(title=""):
    if title:
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*20} {title} {'='*20}{Colors.RESET}")
    else:
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")

def print_report(headers_result=None, ssl_result=None, sensitive_result=None, ports_result=None, url=""):

    print_banner()
    print_separator("RAPPORT D'ANALYSE")

    print(f"\n{Colors.BOLD}  Cible    :{Colors.RESET} {url}")
    print(f"{Colors.BOLD}  Date     :{Colors.RESET} {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    print_separator()

    # ─── SECTION HEADERS ───
    if headers_result:
        print_separator("HEADERS DE SÉCURITÉ")

        if "error" in headers_result:
            print(f"  {Colors.RED}[ERREUR] {headers_result['error']}{Colors.RESET}")
        else:
            # Headers présents
            if headers_result.get("present"):
                print(f"\n  {Colors.GREEN}{Colors.BOLD}Headers présents :{Colors.RESET}")
                for h in headers_result["present"]:
                    print(f"    {Colors.GREEN}[✓]{Colors.RESET} {h}")

            # Headers manquants
            if headers_result.get("missing"):
                print(f"\n  {Colors.RED}{Colors.BOLD}Headers manquants :{Colors.RESET}")
                for h in headers_result["missing"]:
                    print(f"    {Colors.RED}[✗]{Colors.RESET} {h}")

            # Headers mal configurés
            if headers_result.get("misconfigured"):
                print(f"\n  {Colors.YELLOW}{Colors.BOLD}Mal configurés :{Colors.RESET}")
                for h in headers_result["misconfigured"]:
                    print(f"    {Colors.YELLOW}[!]{Colors.RESET} {h}")

            # HTTP → HTTPS
            if headers_result.get("http_to_https"):
                print(f"\n  {Colors.GREEN}[✓]{Colors.RESET} Redirection HTTP → HTTPS active")
            else:
                print(f"\n  {Colors.RED}[✗]{Colors.RESET} Pas de redirection HTTP → HTTPS")

    # ─── SECTION SSL ───
    if ssl_result:
        print_separator("CERTIFICAT SSL/TLS")

        if "error" in ssl_result:
            print(f"  {Colors.RED}[ERREUR] {ssl_result['error']}{Colors.RESET}")
        else:
            # Validité
            if ssl_result.get("ssl_valid"):
                print(f"  {Colors.GREEN}[✓]{Colors.RESET} Certificat valide")
            else:
                print(f"  {Colors.RED}[✗]{Colors.RESET} Certificat invalide")

            # Version TLS
            tls = ssl_result.get("tls_version", "Inconnu")
            if tls in ["TLSv1.2", "TLSv1.3"]:
                print(f"  {Colors.GREEN}[✓]{Colors.RESET} Version TLS : {tls}")
            else:
                print(f"  {Colors.RED}[✗]{Colors.RESET} Version TLS obsolète : {tls}")

            # Expiration
            days = ssl_result.get("days_remaining")
            if days is not None:
                if days > 30:
                    print(f"  {Colors.GREEN}[✓]{Colors.RESET} Expire dans {days} jours")
                elif days > 0:
                    print(f"  {Colors.YELLOW}[!]{Colors.RESET} Expire dans {days} jours — renouveler bientôt !")
                else:
                    print(f"  {Colors.RED}[✗]{Colors.RESET} Certificat EXPIRÉ !")

            # Émetteur
            issuer = ssl_result.get("issuer", "Inconnu")
            print(f"  {Colors.WHITE}[i]{Colors.RESET} Émetteur : {issuer}")

    # ─── SECTION PAGES SENSIBLES ───
    if sensitive_result:
        print_separator("PAGES SENSIBLES")

        found     = sensitive_result.get("found", [])
        forbidden = sensitive_result.get("forbidden", [])
        total     = sensitive_result.get("total_tested", 0)

        print(f"  {Colors.WHITE}[i]{Colors.RESET} {total} pages testées\n")

        if found:
            print(f"  {Colors.RED}{Colors.BOLD}Pages accessibles — CRITIQUE :{Colors.RESET}")
            for p in found:
                print(f"    {Colors.RED}[!!!]{Colors.RESET} {p['page']}")
        else:
            print(f"  {Colors.GREEN}[✓]{Colors.RESET} Aucune page sensible accessible")

        if forbidden:
            print(f"\n  {Colors.YELLOW}{Colors.BOLD}Pages protégées (403) :{Colors.RESET}")
            for p in forbidden:
                print(f"    {Colors.YELLOW}[!]{Colors.RESET} {p['page']}")

    # ─── SECTION PORTS ───
    if ports_result:
        print_separator("SCAN DE PORTS")

        if ports_result.get("errors"):
            print(f"  {Colors.RED}[ERREUR] {ports_result['errors'][0]}{Colors.RESET}")
        else:
            host          = ports_result.get("host", "")
            open_ports    = ports_result.get("open_ports", [])
            dangerous     = ports_result.get("dangerous_open", [])
            duration      = ports_result.get("scan_duration", "")

            print(f"  {Colors.WHITE}[i]{Colors.RESET} Hôte scanné  : {host}")
            print(f"  {Colors.WHITE}[i]{Colors.RESET} Durée du scan : {duration}\n")

            if open_ports:
                print(f"  {Colors.BOLD}Ports ouverts :{Colors.RESET}")
                for p in sorted(open_ports, key=lambda x: x["port"]):
                    if p["niveau"] == "CRITIQUE":
                        color = Colors.RED
                        tag   = "[!!!]"
                    else:
                        color = Colors.GREEN
                        tag   = "[+]  "
                    print(f"    {color}{tag}{Colors.RESET} Port {p['port']:5d} — {p['service']}")
            else:
                print(f"  {Colors.GREEN}[✓]{Colors.RESET} Aucun port ouvert détecté")

            if dangerous:
                print(f"\n  {Colors.RED}{Colors.BOLD}Ports dangereux ouverts — CRITIQUE :{Colors.RESET}")
                for p in dangerous:
                    print(f"    {Colors.RED}[!!!]{Colors.RESET} Port {p['port']} ({p['service']}) — Fermer immédiatement !")

    # ─── SCORE GLOBAL ───
    print_separator("SCORE DE SÉCURITÉ")
    score = _calculate_score(headers_result, ssl_result, sensitive_result, ports_result)

    if score >= 80:
        color  = Colors.GREEN
        niveau = "BON 🟢"
    elif score >= 50:
        color  = Colors.YELLOW
        niveau = "MOYEN 🟡"
    else:
        color  = Colors.RED
        niveau = "FAIBLE 🔴"

    # Barre de progression
    filled = int(score / 5)
    bar    = "█" * filled + "░" * (20 - filled)

    print(f"\n  {color}{Colors.BOLD}[{bar}] {score}/100 — {niveau}{Colors.RESET}\n")
    print_separator()
    print(f"\n  {Colors.CYAN}Rapport généré par XyberScan — Xyberclan{Colors.RESET}\n")


def _calculate_score(headers_result, ssl_result, sensitive_result, ports_result=None):
    score = 100

    # Pénalités headers
    if headers_result and "missing" in headers_result:
        score -= len(headers_result["missing"]) * 8
    if headers_result and "misconfigured" in headers_result:
        score -= len(headers_result["misconfigured"]) * 5

    # Pénalités SSL
    if ssl_result:
        if not ssl_result.get("ssl_valid"):
            score -= 30
        if ssl_result.get("expired"):
            score -= 20
        tls = ssl_result.get("tls_version", "")
        if tls not in ["TLSv1.2", "TLSv1.3"]:
            score -= 15

    # Pénalités pages sensibles
    if sensitive_result:
        score -= len(sensitive_result.get("found", [])) * 10

    # Pénalités ports
    if ports_result:
        score -= len(ports_result.get("dangerous_open", [])) * 10
        score -= len(ports_result.get("open_ports", [])) * 2

    return max(0, score)


# Exécution directe pour test
if __name__ == "__main__":
    from modules.ssl_check import check_ssl
    from modules.ports import scan_ports
    from modules.sensitive import check_sensitive_pages

    url = input("Entrez l'URL à scanner : ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    ssl     = check_ssl(url)
    ports   = scan_ports(url)
    sensitive = check_sensitive_pages(url)

    print_report(
        ssl_result=ssl,
        ports_result=ports,
        sensitive_result=sensitive,
        url=url
    )